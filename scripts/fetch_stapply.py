#!/usr/bin/env python3
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from ats_scrapers import search

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "pipeline_config.json").read_text())
OUT = ROOT / "stapply_candidates.json"
LEDGER = ROOT / "reached_out.json"


def norm(v):
    return ("" if v is None else str(v)).strip()


def dt(value):
    if value is None or str(value).strip() in {"", "NaT", "None"}:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except Exception:
        return None


def score(row):
    title = norm(row.get("title")).lower()
    desc = norm(row.get("description")).lower()
    loc = norm(row.get("location")).lower()
    text = f"{title}\n{desc}"
    s, reasons = 0, []
    for kw in CONFIG["preferred_keywords"]:
        if kw.lower() in text:
            s += 2
            reasons.append(kw)
    if any(k in title for k in ["ai", "llm", "agent", "machine learning", "backend", "full stack", "founding", "forward deployed", "software engineer"]):
        s += 5
    if bool(row.get("is_remote")):
        s += 4
        reasons.append("remote")
    if any(k in loc for k in CONFIG["location_keywords"]):
        s += 4
        reasons.append("location-fit")
    exp = row.get("experience")
    try:
        if exp is not None and int(exp) <= CONFIG["max_experience_years"]:
            s += 3
            reasons.append(f"experience<={CONFIG['max_experience_years']}")
    except Exception:
        pass
    return s, sorted(set(reasons))


def main():
    cutoff = datetime.now(timezone.utc) - timedelta(days=CONFIG["fresh_days"])
    ledger = json.loads(LEDGER.read_text()) if LEDGER.exists() else {"contacts": []}
    contacted_companies = {norm(x.get("company")).lower() for x in ledger.get("contacts", []) if x.get("company")}
    seen_ids, candidates = set(), []

    # Fast path: query the three startup-heavy ATS slices once each instead of
    # repeatedly scanning the full Stapply dataset for every role keyword.
    for ats in ("ashby", "greenhouse", "lever"):
        try:
            df = search(query="engineer", ats=ats, limit=500)
            print(f"{ats}: fetched {len(df)} engineer rows")
        except Exception as exc:
            print(f"{ats}: search failed: {exc}")
            continue

        for _, raw_row in df.iterrows():
            row = raw_row.to_dict()
            gid = norm(row.get("global_id")) or norm(row.get("url"))
            if not gid or gid in seen_ids:
                continue
            seen_ids.add(gid)

            title_l = norm(row.get("title")).lower()
            if any(k in title_l for k in CONFIG["exclude_title_keywords"]):
                continue
            if norm(row.get("employment_type")).upper() == "INTERN":
                continue

            when = dt(row.get("posted_at")) or dt(row.get("fetched_at"))
            if when is not None:
                if when.tzinfo is None:
                    when = when.replace(tzinfo=timezone.utc)
                if when < cutoff:
                    continue

            exp = row.get("experience")
            try:
                if exp is not None and int(exp) > CONFIG["max_experience_years"]:
                    continue
            except Exception:
                pass

            s, reasons = score(row)
            if s < 9:
                continue
            company = norm(row.get("company"))
            candidates.append({
                "global_id": gid,
                "company": company,
                "title": norm(row.get("title")),
                "location": norm(row.get("location")),
                "is_remote": None if row.get("is_remote") is None else bool(row.get("is_remote")),
                "experience": None if row.get("experience") is None else row.get("experience"),
                "employment_type": norm(row.get("employment_type")),
                "posted_at": norm(row.get("posted_at")),
                "fetched_at": norm(row.get("fetched_at")),
                "url": norm(row.get("url")),
                "apply_url": norm(row.get("apply_url")) or norm(row.get("url")),
                "ats_type": norm(row.get("ats_type")),
                "department": norm(row.get("department")),
                "team": norm(row.get("team")),
                "score": s,
                "match_reasons": reasons,
                "company_previously_contacted": company.lower() in contacted_companies if company else False,
                "status": "needs_people_research"
            })

    candidates.sort(key=lambda x: (x["company_previously_contacted"], -x["score"], x["company"].lower(), x["title"].lower()))
    candidates = candidates[: CONFIG["max_candidates"]]
    OUT.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "Stapply JobHive / ats-scrapers",
        "count": len(candidates),
        "next_stage": "LinkedIn/current-team research -> contact ranking -> professional email discovery -> dedupe -> apply -> personalized outreach",
        "candidates": candidates
    }, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {len(candidates)} candidates")


if __name__ == "__main__":
    main()

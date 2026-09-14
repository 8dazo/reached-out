#!/usr/bin/env python3
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

from ats_scrapers import Client

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "pipeline_config.json").read_text())
OUT = ROOT / "stapply_candidates.json"
LEDGER = ROOT / "reached_out.json"

INDIA_TERMS = (
    "india", "bengaluru", "bangalore", "pune", "hyderabad", "gurugram",
    "gurgaon", "noida", "delhi", "mumbai", "chennai", "vadodara", "ahmedabad"
)
GLOBAL_REMOTE_TERMS = ("worldwide", "global", "anywhere", "apac")
REMOTE_BLOCK_TERMS = (
    "united states", "usa", "u.s.", "us only", "canada", "europe", "eu only",
    "united kingdom", "uk only", "australia", "germany", "france", "spain",
    "poland", "netherlands", "sweden", "switzerland", "latam", "americas"
)
ROLE_TERMS = (
    "engineer", "developer", "software", "machine learning", "ai", "llm",
    "backend", "full stack", "fullstack", "forward deployed"
)
HARD_LEVEL_EXCLUDES = ("staff", "principal", "director", "manager", "vp ", "vice president")


def norm(v):
    s = "" if v is None else str(v).strip()
    return "" if s.lower() in {"nan", "nat", "none"} else s


def dt(value):
    value = norm(value)
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def inferred_min_years(text):
    patterns = [
        r"(?:minimum of |at least )?(\d{1,2})\+?\s*(?:years|yrs)\s+of\s+(?:professional\s+)?(?:software|engineering|development|backend|full[- ]?stack|machine learning|ml|ai)",
        r"(?:minimum of |at least )?(\d{1,2})\+?\s*(?:years|yrs)\s+(?:professional\s+)?experience",
        r"(?:experience|required|requirements)[^\n.]{0,80}?(\d{1,2})\+?\s*(?:years|yrs)",
    ]
    found = []
    lower = text.lower()
    for pattern in patterns:
        for m in re.finditer(pattern, lower):
            try:
                found.append(int(m.group(1)))
            except Exception:
                pass
    return max(found) if found else None


def location_eligible(row):
    loc = norm(row.get("location")).lower()
    desc = norm(row.get("description")).lower()
    combined = f"{loc}\n{desc}"

    if any(term in loc for term in INDIA_TERMS):
        return True, "india"
    if any(term in combined for term in GLOBAL_REMOTE_TERMS) and (
        bool(row.get("is_remote")) or "remote" in combined
    ):
        return True, "global/apac remote"

    # Generic remote is acceptable only when the source doesn't explicitly
    # restrict it to another country/region.
    if bool(row.get("is_remote")) or "remote" in loc:
        if not any(term in loc for term in REMOTE_BLOCK_TERMS):
            return True, "remote-unrestricted-by-location-field"
    return False, "geo-mismatch"


def score(row, min_years, geo_reason):
    title = norm(row.get("title")).lower()
    desc = norm(row.get("description")).lower()
    text = f"{title}\n{desc}"
    s, reasons = 0, []

    for kw in CONFIG["preferred_keywords"]:
        if kw.lower() in text:
            s += 2
            reasons.append(kw)

    if any(k in title for k in ("ai", "llm", "agent", "machine learning", "backend", "full stack", "fullstack", "founding", "forward deployed")):
        s += 7
    elif "software engineer" in title or "software developer" in title:
        s += 4

    if geo_reason == "india":
        s += 10
        reasons.append("India")
    elif geo_reason == "global/apac remote":
        s += 8
        reasons.append("global/APAC remote")
    else:
        s += 4
        reasons.append("remote")

    if min_years is not None:
        if min_years <= CONFIG["max_experience_years"]:
            s += 4
            reasons.append(f"requires~{min_years}y")
        else:
            s -= 20

    return s, sorted(set(reasons))


def main():
    ledger = json.loads(LEDGER.read_text()) if LEDGER.exists() else {"contacts": []}
    contacted_companies = {
        norm(x.get("company")).lower() for x in ledger.get("contacts", []) if x.get("company")
    }
    seen_ids, candidates = set(), []
    client = Client(prefer_parquet=True)
    now = datetime.now(timezone.utc)

    # Stapply publishes small daily deltas across all ATS sources. Reading these
    # keeps the scan fresh and avoids downloading the multi-GB full snapshot.
    for offset in range(CONFIG["fresh_days"]):
        day = (now - timedelta(days=offset)).date().isoformat()
        try:
            df = client.load(date=day)
            print(f"{day}: loaded {len(df)} changed jobs")
        except Exception as exc:
            print(f"{day}: delta unavailable: {exc}")
            continue

        for _, raw_row in df.iterrows():
            row = raw_row.to_dict()
            gid = norm(row.get("global_id")) or norm(row.get("url"))
            if not gid or gid in seen_ids:
                continue
            seen_ids.add(gid)

            title = norm(row.get("title"))
            title_l = title.lower()
            if not any(term in title_l for term in ROLE_TERMS):
                continue
            if any(term in title_l for term in HARD_LEVEL_EXCLUDES):
                continue
            if "intern" in title_l or norm(row.get("employment_type")).upper() == "INTERN":
                continue

            eligible, geo_reason = location_eligible(row)
            if not eligible:
                continue

            desc = norm(row.get("description"))
            min_years = inferred_min_years(desc)
            structured_exp = row.get("experience")
            try:
                if structured_exp is not None and norm(structured_exp):
                    structured_exp = int(float(structured_exp))
                    min_years = max(min_years or 0, structured_exp)
            except Exception:
                pass
            if min_years is not None and min_years > CONFIG["max_experience_years"]:
                continue

            s, reasons = score(row, min_years, geo_reason)
            if s < 10:
                continue

            company = norm(row.get("company"))
            candidates.append({
                "global_id": gid,
                "company": company,
                "title": title,
                "location": norm(row.get("location")),
                "geo_reason": geo_reason,
                "is_remote": None if row.get("is_remote") is None else bool(row.get("is_remote")),
                "inferred_min_years": min_years,
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
                "status": "needs_full_jd_and_people_research"
            })

    # India first, then global/APAC remote; within each group prioritize fit.
    geo_rank = {"india": 0, "global/apac remote": 1, "remote-unrestricted-by-location-field": 2}
    candidates.sort(key=lambda x: (
        x["company_previously_contacted"],
        geo_rank.get(x["geo_reason"], 9),
        -x["score"],
        x["company"].lower(),
        x["title"].lower(),
    ))
    candidates = candidates[: CONFIG["max_candidates"]]

    OUT.write_text(json.dumps({
        "generated_at": now.isoformat(),
        "source": "Stapply JobHive daily deltas / ats-scrapers",
        "count": len(candidates),
        "next_stage": "full JD verification -> LinkedIn/current-team mapping -> recruiter + technical contact ranking -> public professional email discovery -> dedupe -> apply -> personalized outreach",
        "candidates": candidates
    }, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {len(candidates)} candidates")


if __name__ == "__main__":
    main()

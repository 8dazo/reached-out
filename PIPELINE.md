# Reached Out — High-Signal Job Outreach Pipeline

## Goal

Find fresh, high-fit engineering openings at companies based in the United States, Europe, the United Kingdom, Switzerland, Norway, or Singapore; identify the person most likely to influence hiring; and send short, role-specific outreach that maximizes qualified replies rather than raw send volume.

GitHub remains the source of truth for discovery, send state, applications, replies, follow-ups, and dedupe.

## Candidate profile

- 2+ years production software engineering
- LLM agents/orchestration, tool calling, evals, RAG, observability, guardrails
- TypeScript/Node/Next.js, Python, PostgreSQL, Docker/AWS
- Strong 0→1 product/full-stack ownership
- Captar: runtime control, budget enforcement, tool policy, tracing, datasets/evals
- Production backend ownership at 10,000+ requests/day
- LeetCode Guardian, top 0.3%
- Portfolio: https://devansh.aurat.ai
- LinkedIn: https://www.linkedin.com/in/devansh-m12
- GitHub: https://github.com/8dazo

## Geographic rule

Target the company and role location, not a person's inferred nationality or ethnicity.

Hard reject:
- companies headquartered in India;
- India-only roles;
- roles requiring existing US/European/Singapore work authorization when the employer does not sponsor, relocate, hire internationally, use an EOR, or accept an overseas contractor;
- roles whose location requirements make Devansh ineligible.

A founder, recruiter, or hiring manager at an otherwise eligible US/European/Singapore company remains a valid contact regardless of their personal background.

## Discovery priority

1. Y Combinator Work at a Startup / YC company job pages.
2. HiringCafe.
3. Wellfound.
4. Official company careers pages and ATS pages.
5. Current company/founder/team pages, GitHub orgs, and public hiring posts for evidence and people mapping.
6. Stapply/JobHive only as a supplementary broad index, not the primary source.

Prefer roles posted in the last 72 hours; allow up to 7 days when the match is unusually strong.

Target role families:
- Applied AI Engineer
- AI / LLM / Agent Engineer
- Product Engineer
- Forward Deployed Engineer
- Full-Stack AI Engineer
- Backend / Platform Engineer
- Founding Engineer
- Software Engineer with direct AI product ownership

Reject internships, staff/principal/director/VP roles, obvious >5 YOE roles, stale/closed jobs, and generic roles with weak overlap.

## International eligibility gate

Before finding an email, open the original JD and establish that the role is realistically hireable from India through at least one of:
- worldwide/global/APAC remote;
- visa sponsorship;
- relocation support;
- explicit international-candidate language;
- employer-of-record support;
- overseas contractor arrangement.

Do not spend enrichment effort on an otherwise impossible role.

## Fit scoring

Rank roles before people enrichment. Strong signals include:
- LLM agents, orchestration, tool/function calling, MCP;
- RAG, evals, tracing, observability, guardrails;
- TypeScript/Node/Next.js or Python backend work;
- PostgreSQL, APIs, distributed/backend systems;
- product engineering and 0→1 ownership;
- early-stage startup execution;
- evidence that the company is actively hiring now.

Use role freshness + technical overlap + international eligibility + company stage + likely access to the hiring decision-maker as the main score.

## People mapping

Choose one primary contact per company/role by default.

For 1–50 employee startups:
technical founder → founder → CTO → Head of Engineering.

For 51–200 employee companies:
hiring manager → Head of Engineering → engineering manager → technical recruiter → CTO.

For 201+ employee companies:
job poster → technical recruiter → hiring manager → engineering manager.

For YC companies, prefer a founder or technical leader when the company is still small enough for founder-led hiring.

## Email discovery and validation

Auto-send only when the address is `explicit_public_current` or independently `mailbox_verified`.

Allowed evidence:
- official company site;
- current public professional profile or personal site;
- current GitHub/OSS metadata;
- public company/press contact source;
- company email pattern only when independently verified for the exact mailbox.

Never auto-send to an address that exists only because a pattern was guessed.

Never use Hacker News as an email source.

Permanent blacklist: bounced, invalid, opted-out, or clearly wrong-recipient addresses.

## Reply-rate email rules

Initial outreach should normally be 70–110 words, plain text, and contain one clear ask.

Structure:
1. Say where the role was found and name the exact role.
2. Give one specific reason the match is unusually strong.
3. Give one or two proof points, not a biography.
4. Ask for a short conversation or whether they are the right person to speak with.
5. Include portfolio and GitHub naturally; LinkedIn can live in the signature.

Best proof points to select from:
- shipped LLM-agent workflows and production AI systems;
- owned 20+ platform features across AI orchestration/backend services;
- API layer handling 10,000+ requests/day;
- Captar runtime guardrails, budget control, tool policy, tracing and eval pipelines;
- full-stack 0→1 ownership;
- LeetCode Guardian / ICPC only when relevant to the role.

Do not attach the resume to every founder cold email. Attach it when the job explicitly expects an emailed application or when the recipient asks for it. This keeps the first message lighter and less application-template-like.

## Personalization standard

Every email must contain at least one detail that could not be reused unchanged for another company:
- exact role;
- product/technical problem from the JD;
- stack or AI workflow mentioned by the company;
- recent hiring/product signal from an official/current source.

Do not write generic praise such as "I love what you're building" without a concrete reason.

## Follow-up sequence

If there is no reply:
- Follow-up 1: 3 business days after the initial message, in the same thread, 30–60 words.
- Follow-up 2: 7 business days after the initial message, in the same thread, short final note.

Stop immediately after any reply, opt-out, bounce, or clear rejection.

Do not send more than two follow-ups.

## Reply-learning loop

Before each morning discovery run, inspect Gmail replies to prior outreach and update GitHub state.

Classify outcomes as:
- interested;
- screening/interview;
- referral/forwarded;
- request for more information;
- neutral;
- role filled/not hiring;
- location/work-authorization mismatch;
- not a fit;
- no reply;
- bounced/invalid.

Track reply outcomes by source, region, company size, role family, contact type, and email variant. Future discovery should increase weight for combinations producing qualified replies and reduce weight for combinations repeatedly producing location or experience rejections.

Do not optimize for opens. Optimize for qualified replies and interviews.

## Daily flow

### Morning discovery

1. Reconcile Gmail replies, bounces, and prior run records into GitHub.
2. Process any due follow-ups first.
3. Discover approximately 80 fresh roles across the preferred sources.
4. Apply hard geography, work-authorization, freshness, seniority, and fit gates before enrichment.
5. Rank roles and enrich contacts only for the strongest opportunities.
6. Build a queue of up to 60 verified, high-confidence contacts, including valid carryover.
7. Send the highest-confidence first batch.

### Sending philosophy

Quality beats quota. The system may discover 80 roles and queue up to 60 contacts, but should normally cap new cold sends around 30/day unless the qualified pool is exceptionally strong.

Never lower verification or fit standards to hit a number.

Send in small batches rather than all at once, preferably aligned with the recipient's local working hours when practical.

## Dedupe and state control

Before every send, read `reached_out.json`, `outreach_queue.json`, and `applications.json` and check Gmail history when needed.

Never send a new initial email to an address already marked `sent`, `delivered`, `replied`, `bounced`, `invalid`, or `opted_out`.

Dedupe by email, person, company, and role.

Default to one primary contact per company/role. Contact a second person only when the first address failed or the first contact is clearly not responsible for hiring.

Queue states should distinguish at minimum:
`ready_to_send`, `sent`, `followup_due`, `replied`, `bounced`, `invalid`, `opted_out`, `skipped`, `stale`.

## Application handling

If the role says apply by email, the personalized email is the official application and should be recorded in `applications.json` after successful send.

If a form is required, submit it only when available tools can complete it accurately and produce confirmation. Never claim submission without confirmation.

Keep application state and founder/recruiter outreach state separate so both can occur without duplicate messages.

## Post-send reconciliation

After each batch:
- verify successful Gmail sends;
- detect immediate delivery failures;
- store Gmail message ID and timestamp;
- update queue/application state only after confirmed sending;
- blacklist invalid/bounced addresses;
- schedule follow-ups only for successfully delivered initial messages.

GitHub state must never claim a send that does not appear in Gmail.

## Source-of-truth files

- `pipeline_config.json`: target markets, sources, filters, contact strategy and messaging rules
- `outreach_queue.json`: qualified contacts, evidence, send state, follow-up state and variant
- `reached_out.json`: permanent contact history / dedupe ledger
- `applications.json`: official application state
- `outreach_run_*.json`: run-level evidence and reconciliation

## Success metrics

Primary: qualified reply rate and interviews created.

Secondary: valid-address rate, international-eligibility pass rate, founder/hiring-manager reply rate, application-to-screen rate, and replies by source/region/role family.

Raw number of emails sent is not a success metric.

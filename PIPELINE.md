# Reached Out — Daily Job Outreach Pipeline

## Goal

Find 30–40 fresh, high-fit roles each morning, qualify them against Devansh's profile, discover only high-confidence professional contacts, apply where appropriate, then send at most 20 personalized emails per day in four batches of five.

## Candidate profile

- 2+ years production software engineering
- LLM agents/orchestration, tool calling, evals, RAG, observability, guardrails
- TypeScript/Node/Next.js, Python, PostgreSQL, Docker/AWS
- Strong 0→1 product/full-stack ownership
- Captar: runtime control, budget enforcement, tool policy, tracing, datasets/evals
- LeetCode Guardian, top 0.3%
- Portfolio: https://devansh.aurat.ai
- LinkedIn: https://www.linkedin.com/in/devansh-m12
- GitHub: https://github.com/8dazo

## Daily flow

1. **Discovery**
   - Primary: Stapply/JobHive live ATS sources.
   - Supplement from current official company career pages when the Stapply shortlist is too small.
   - Hacker News is not an email source.

2. **Hard qualification**
   - Reject internships unless unusually compelling.
   - Reject staff/principal/director/manager roles.
   - Reject explicit >5 YOE requirements unless the role is exceptional and specifically approved.
   - Reject geography that does not allow India, APAC, worldwide remote, or a realistic Indian office.
   - Open the original JD and verify the role instead of trusting keyword scores.

3. **Fit scoring**
   - Prefer AI/LLM/agent/FDE/applied-AI/backend/full-stack/founding-engineer roles.
   - Boost direct overlap with agents, evals, tracing/observability, MCP/tool calling, RAG, TypeScript/Python, PostgreSQL and early-stage ownership.

4. **People mapping**
   - Use LinkedIn/current company pages only to establish identity/current employment.
   - Priority: job poster/recruiter → hiring manager → engineering/team lead → Head of AI/Engineering → CTO/technical founder → founder.
   - For small startups, prefer the relevant technical founder/lead over a generic recruiter.

5. **Email discovery and validation**
   - Auto-send only when the address is either `explicit_public_current` or independently `mailbox_verified`.
   - Do not auto-send guessed pattern emails.
   - Prefer explicit personal work email > verified inferred work email > explicit recruiting/jobs mailbox.
   - Keep invalid/bounced addresses permanently in `reached_out.json` so they cannot be retried.

6. **Dedupe**
   - Before every send, read `reached_out.json`.
   - Never send to an email already present with status `sent`, `delivered`, `replied`, or `bounced`.
   - Maximum one new contact per company per day unless a reply explicitly redirects outreach.

7. **Application handling**
   - If the role says apply by email, the personalized email is the official application and is recorded in `applications.json`.
   - If a form is required, submit it only when available tools can complete it accurately and all required answers are known.
   - Never claim a form was submitted unless there is confirmation/evidence.
   - Otherwise mark `pending_form` and continue with outreach only when the company invites email contact.

8. **Personalization**
   - Every email must reference the actual role/company problem.
   - Select one or two relevant proof points from Captar, Stride.AI, Baelys, production backend/full-stack experience, or competitive programming.
   - Always include portfolio, LinkedIn, and GitHub links.
   - Attach the resume whenever the execution environment has access to it.

9. **Sending cadence**
   - Maximum 5 emails per batch.
   - Maximum 20 emails per day by default.
   - Never send the whole daily pool at once.

10. **Post-send reconciliation**
   - Search Gmail for delivery failures after each batch and again in the evening.
   - Mark immediate failures `bounced` and never retry that address.
   - Record Gmail message ID for every successful send.
   - Track replies/interview/rejection/offer states when they arrive.

## Source-of-truth files

- `stapply_candidates.json`: raw daily discovery shortlist
- `outreach_queue.json`: qualified, sendable contacts waiting for action
- `reached_out.json`: immutable-ish contact history / dedupe ledger
- `applications.json`: official application state

## Daily target

- Discover: 30–40 qualified candidates
- Queue: at least 20 high-confidence sendable contacts when available
- Send: up to 20/day in four batches of 5
- Quality wins over quota: if only 11 addresses meet the confidence/fit gates, send 11 rather than guessing 9 more.

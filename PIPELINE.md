# Reached Out — Daily Job Outreach Pipeline

## Goal

Find up to 60 fresh, high-fit, sendable professional contacts each morning, qualify them against Devansh's profile, apply where appropriate, and send outreach in controlled batches of 10 throughout the day while keeping GitHub as the source of truth.

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

1. **Morning discovery and queue build — 06:30 IST**
   - Primary: Stapply/JobHive live ATS sources.
   - Supplement from current official company career pages when needed.
   - Find up to 60 contacts that are both role-fit and actually sendable.
   - Preserve valid unsent carryover from prior days before adding new contacts.
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
   - Use LinkedIn/current company pages to establish identity/current employment.
   - Priority: job poster/recruiter → hiring manager → engineering/team lead → Head of AI/Engineering → CTO/technical founder → founder.
   - For small startups, prefer the relevant technical founder/lead over a generic recruiter.

5. **Email discovery and validation**
   - Auto-send only when the address is either `explicit_public_current` or independently `mailbox_verified`.
   - Never auto-send guessed pattern-only emails.
   - Prefer explicit personal work email > verified inferred work email > explicit recruiting/jobs mailbox.
   - Keep invalid/bounced addresses permanently in `reached_out.json` so they cannot be retried.

6. **Dedupe and state control**
   - Before every send, read `reached_out.json`, `outreach_queue.json`, and `applications.json`.
   - Never send to an email already present with status `sent`, `delivered`, `replied`, or `bounced`.
   - Dedupe by email, person, company, and role.
   - Maximum one new contact per company per day by default.
   - Queue states: `ready_to_send`, `sent`, `bounced`, `invalid`, `skipped`, `stale`, `replied`.

7. **Application handling**
   - If the role says apply by email, the personalized email is the official application and is recorded in `applications.json` after successful send.
   - If a form is required, submit it only when available tools can complete it accurately and produce confirmation.
   - Never claim a form was submitted without confirmation.
   - Otherwise mark `pending_form` and keep outreach/application state separate.

8. **Personalization**
   - Every email must reference the actual role/company problem.
   - Select one or two relevant proof points from Captar, Stride.AI, Baelys, production backend/full-stack experience, or competitive programming.
   - Always include portfolio, LinkedIn, and GitHub links.
   - Attach the resume whenever available.

9. **Sending cadence**
   - Morning radar sends the first up to 10 emails after building the queue.
   - Daytime outreach runs at approximately 10:30, 12:30, 15:30, 17:30, and 20:30 IST.
   - Each daytime run sends the next up to 10 valid unsent contacts.
   - Maximum theoretical daily volume: 60 emails, but quality always wins over quota.
   - Never send the whole pool at once.

10. **Post-send reconciliation**
   - After each batch, search Gmail for immediate delivery failures.
   - Mark failures `bounced` or `invalid` and never retry the address.
   - Record Gmail message ID and send timestamp for every successful send.
   - Keep `outreach_queue.json` and `reached_out.json` synchronized after every action.
   - Track replies/interview/rejection/offer states when they arrive.

## Source-of-truth files

- `stapply_candidates.json`: raw daily discovery shortlist
- `outreach_queue.json`: qualified contacts waiting for action, including send state and evidence
- `reached_out.json`: permanent contact history / dedupe ledger
- `applications.json`: official application state

## Daily target

- Discover and qualify: enough roles to support up to 60 sendable contacts
- Queue: up to 60 high-confidence contacts, including valid carryover
- Send: up to 60/day in six batches of 10 (morning + five daytime runs)
- Quality wins over quota: if only 27 contacts meet all confidence/fit gates, send 27 rather than guessing the remaining 33.

# International Outreach v7 — Fresh Campaign (2026-10-28)

## Objective
Aim for 30 **new** individualized job outreach messages per India calendar day, never exceeding 30. Send 7 at 06:30, 7 at 08:00, 7 at 10:00, 7 at 12:00, 2 at 14:00 IST. Follow-ups, replies, and bounce events DO NOT count as new contacts. Each batch cap is a maximum, not a quota to fill with weak leads. 30 is conditional on enough verified eligible leads and functioning Gmail/GitHub connections.

## Reset semantics
The old outreach_queue.json is historical/inactive as of 2026-10-28. Do not resume old pending emails or obsolete second follow-ups. Preserve reached_out.json, applications.json, prior checkpoints and Gmail Sent as permanent suppression records. Reconcile every recipient against both before any send. New candidate store is 2BBs_doubt.json (the user's requested filename) and new dated batch checkpoint files. No historical message is undone or deleted.

## 06:30 discovery workflow
1. Reconcile Gmail Sent, replies, rejections, unsubscribe, bounces and full threads with the immutable historical records. Count today's unique eligible new sends.
2. Load oldest verified unused leads from 2BBs_doubt.json, revalidate live role/eligibility/contact evidence. Expire weak evidence.
3. Find qualified roles (YC Work at a Startup, official company career/Greenhouse/Lever/Ashby/Workable pages, HiringCafe, Wellfound, fresh funding announcements). Do not require or rely on LinkedIn; publicly available company career and personal technical profiles are preferred. Do not bypass Cloudflare or access controls, use unauthorized scraping, or claim a geographic source IP without proof.
4. Screen HQ: USA, Europe including UK/Switzerland/Norway, or Singapore. EXCLUDE India-headquartered companies, independently of founder nationality. The role MUST actually be available to an applicant resident in India via worldwide/India/APAC remote, overseas contractor/EOR, relocation or sponsorship. Ambiguous "Remote" alone is insufficient.
5. Relevant 2–5 YOE roles: Applied AI, LLM agents, AI full-stack, backend, product engineering, founding engineer, FDE. Prefer live postings <72h, consider <=7 days if good fit. Prioritize direct roles over speculative funding-only pitches.
6. Find one appropriate human decision-maker at a time (founder/CTO for small teams; manager/recruiter at larger companies). Publicly documented current mailbox or independently mailbox-verified exact email ONLY. Never guess patterns or scrape personal emails behind access restrictions. Store source URLs, observed timestamp, eligibility quotation and source URL, verification status, role URL, headquarter proof, and fit score.
7. Target an INITIAL POOL of 45 send-ready candidates (30 daily +15 reserve). Extra discoveries remain queued FIFO for next day. If pool below 10 before a batch, repeat same discovery/qualification workflow. First reuse the oldest *still eligible* previously unused lead.

## Sending — fail-safe one recipient transaction
Acquire a single-writer lock/checkpoint for the batch; no parallel senders. Before EACH recipient:
1. Read current Gmail Sent and thread plus reached_out.json and dated checkpoints. Check recipient address, normalized company identity, opted-out and bounced state. Maximum one initial outreach ever per person, and one active outreach per company unless new role materially warrants later contact and previous campaign response does not preclude it.
2. Persist send_intent in the dated checkpoint and claim unique contact key before Gmail call.
3. Send one individualized 70–110 word plain-text email, one CTA, no misleading recruitment claims. Mention specific role/team and concrete qualifications, portfolio https://devansh.aurat.ai and GitHub https://github.com/8dazo. Attach resume ONLY for genuine emailed applications.
4. Validate Gmail Sent ID and message recipient, and record durable sent state in reached_out.json and 2BBs_doubt.json BEFORE next recipient.
5. If Gmail action errors, status UNKNOWN — search exact Gmail Sent/thread before any retry. If delivery cannot be definitively resolved, quarantine this entry for later reconciliation; use another verified candidate. Never blindly retry. Bounces and opt-outs blacklist exact address; send replacement only if available and within daily cap.
6. If GitHub state cannot be written, STOP sending until restored and reconciled; do not claim success without Gmail evidence.
7. At most ONE follow-up ever after 3 business days, only when no reply/opt-out/bounce, only in original thread. Follow-ups are distinct from daily new outreach and NEVER displace new-contact tracking.

## Replenishment and carry-over
After a batch, commit per-send Gmail IDs and failures to dated audit. If verified remaining <10, replenish immediately, ideally to 20+ if feasible. Send oldest eligible unsent FIFO next morning, following fresh validation. Mark lead statuses: discovered, unverified, verified_ready, claimed, sent_confirmed, unknown_delivery, bounced, disqualified, opted_out, expired. Historical suppression entries always win. A bounce is not a verified delivery; don't treat Gmail Sent alone as proof of inbox delivery.

## Daily final audit
Record by batch: target, verified candidates available, attempted, Gmail-Sent confirmed, known bounces, net no-known-bounce count, remaining, replies, failures and recovery reasons. Reconcile with Gmail and GitHub before reporting. Stop at 30 newly contacted unique eligible companies/persons and report shortfalls honestly. Do not lower eligibility, quality, or verification gates to hit volume.

## Responsibility
The 06:30 scheduled task owns discovery and first batch. A separate serialized task owns the 08:00/10:00/12:00/14:00 batches. Never overlap multiple Gmail outbound calls. No automatic actions from any superseded legacy queues.

## Message quality policy (effective immediately)
Read MESSAGE_QUALITY_V2.md before EVERY outreach draft. Specific researched hook and one tailored proof are required. Compare recent sent messages for repetitive openings, proof patterns, signoffs and calls to action. Hold generic drafts instead of sending them. If current execution has already drafted or sent a message, do not repeat or retroactively resend; apply only to new unsent messages.

## Live test findings — 2026-10-27
- An attached conversation resume at /mnt/data/Devansh_Mahant_Resume.pdf was rejected by Gmail connector with BLOCKED_FILE_REFERENCE. **Never reuse that inaccessible path blindly**. Only attach a resume after verifying an egress-accessible file reference. If unavailable, send legitimate individualized *outreach* with portfolio/GitHub only and mark `contacted_not_formal_application`; do not claim a completed CV application. For roles strictly requiring a CV, defer until a valid attachment is available.
- A 550 5.4.1 Access denied hard bounce was observed for careers@enablex.io. This exact mailbox is permanently suppressed; do not retry or infer another mailbox.
- Gmail's broad Sent search may lag immediately after send; exact-recipient searches and direct Gmail message ID reads should be used for reconciliation. Do not resend based on a temporarily missing broad-search result.
- The first live test found only six verified eligible contacts, with five Gmail Sent IDs, one hard bounce, and one attachment block. Preserve truthful shortfall reporting and replenish with fresh research rather than relaxing standards.

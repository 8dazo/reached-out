# Outreach v8 Self-Healing Protocol

This supplements OUTREACH_V7.md and MESSAGE_QUALITY_V2.md (builder-to-builder v3). Safety and eligibility rules always take priority over volume.

## Execution and scheduling
Each batch is its own time slot but all writers share one *logical* send ledger. Gmail Sent is outbound acceptance evidence; GitHub is durable state. Read fresh source-of-truth data before each send. Do not assume checking a lock in GitHub alone is atomic: competing scheduled executions must abstain if ownership cannot be established unambiguously. No concurrent outbound writers. A stale or uncertain owner means pause/reconcile rather than unsafe forced unlock.

## Fresh-day preflight
- Reconcile Gmail Sent, full threads, delivery failures, replies, opt-outs, and all historical ledgers.
- Revalidate FIFO unsent contacts: exact email source and role/eligibility evidence, company HQ, current employment eligibility from India.
- Begin with 45 verified-ready if obtainable, but do not block a safe send of 1–7 if supply is short.
- Reserve target 15, warning at 20, critical at <10. Send-target shortfalls trigger additional discovery in the same run when feasible, not silent termination.

## Discovery repair
- First run official careers + ATS (Ashby/Greenhouse/Lever/Workable), YC hiring, Wellfound and HiringCafe, relevant funded company hiring announcements. No access-control bypass.
- If first pass yields < batch target +10, expand to alternate search phrasings, adjacent relevant job titles and official ATS listings; revalidate HQ and global/India/contractor hiring.
- Require exact publicly sourced current mailbox or independently verified mailbox: DNS/MX alone does not verify a recipient. Never invent mailbox patterns.
- Do not repeatedly scan sites that fail; mark source_failure with URL and move to another source. Never relax eligibility gates.
- Save verified-unused opportunities and source evidence into 2BBs_doubt.json; do not discard leftovers across days. Refresh stale leads.
- Count only unique new contacts on the local India day. No initial email to previously contacted person/company.

## Transaction and failure matrix
- Before every Gmail action: load ledger and Gmail full history, ensure no other sender, checkpoint recipient claim and unique send intent, then invoke exactly one send.
- Accepted: verify message ID by direct read / exact recipient search, write permanent sent record + lead queue + daily audit *before proceeding*.
- Gmail timeout/tool error/uncertain outcome: inspect direct message ID if supplied, exact recipient Sent and thread, look for duplicates. If still ambiguous set unknown_delivery and quarantine. Do NOT retry blindly, do NOT count as sent, move to other lead only when single-writer safe.
- Known hard bounce: suppress exact email forever and count separately; replace using next eligible verified candidate. Soft bounce: hold for later investigation, never immediate retry.
- GitHub write error: stop outbound sending immediately; attempt read-only reconciliation and retry idempotent persistence safely if SHA/ledger state remains clear, else report manual intervention required.
- Resume attachment blocked: no blind retry. For ordinary networking email, omit attachment and include portfolio; for formal application requiring CV, defer until accessible attachment exists, don't mark applied.
- Missing tool permission/auth, rate limits, unavailable API: record blocker and stop action needing connection; do not fake state.
- Partial batch: checkpoint real successes, shortfall, cause, unused queue; remaining batches should independently replenish. Never roll missed batch volume into next slot beyond its assigned cap or day cap.
- Never resend after reply, opt-out, wrong person, or previously exhausted one lifetime follow-up.

## Observability and circuit-breaker
For each batch persist time, intended_count, candidate_pool_start/end, new_found, verified, send_attempts, confirmed_sent_message_ids, known_bounces, unknown_delivery, disqualified, source_failures, connector_failures, GitHub checkpoint SHA, and remaining quota. Add failure reason, last inspected evidence, and resolution.
When repeated connector failures occur, stop sending and log root cause; later runs can recheck. Never endlessly retry or claim guaranteed self-repair.
At 14:00 create final reconciliation and queue-health report: 30 goal versus confirmed Gmail Sent minus known bounces, quality-gate rejections, problems auto-recovered versus unresolved, and backlog ready for tomorrow.

## Quality
Read MESSAGE_QUALITY_V2.md latest additions. Different human opening, verified source-specific detail, concrete relevant proof and natural CTA. Favor actual responses over quota. When there aren't enough qualified leads, report the shortfall and leave the rest unsent.

# Outreach Send Recovery Protocol

## Goal

A temporary Gmail connector/action failure must never end the daily outreach run at a small partial batch. The system targets 15–20 confirmed unique new contacts per day when enough qualified opportunities exist, while preserving all existing quality and verification gates.

## Delivery truth

Gmail Sent is the delivery source of truth. GitHub state is written only after Gmail confirms a message exists. A tool/action error is not automatically a failed email and is not automatically a success.

## Required execution order

1. Reconcile Gmail replies, bounces, opt-outs, and Sent history with GitHub.
2. Discover, qualify, dedupe, and enrich candidates.
3. Before the first send, persist a dated recovery checkpoint containing the ordered sendable queue, contact evidence, role/funding evidence, and current status for each candidate.
4. Send one recipient at a time.
5. After each send action:
   - if a Gmail message ID is returned, verify the message exists in Sent and record it;
   - if the send action errors or times out, search Gmail Sent for the exact recipient + subject before retrying;
   - if it exists in Sent, treat it as successful and capture the message ID;
   - if it does not exist, mark the candidate `transient_send_failure`, keep it eligible, and continue to the next candidate rather than terminating the batch.
6. After each confirmed send, check immediate delivery-failure mail. A bounce does not count toward the successful-contact target. Blacklist only the exact failed mailbox and continue to the next qualified candidate.
7. Continue replenishing/processing candidates until 15–20 successful unique new contacts are confirmed, or the qualified pool is genuinely exhausted.
8. Always create/update the dated outreach run audit even if the run ends partially or a connector fails.

## Retry policy

- Never blindly retry an errored send before checking Gmail Sent; this prevents duplicates when the connector returns an error after Gmail accepted the message.
- A recipient with `transient_send_failure` may be retried once later in the same run after other candidates have been attempted.
- If the second attempt still has no Gmail Sent message, leave it queued for the recovery run.
- Do not retry hard bounces, opt-outs, invalid addresses, or wrong recipients.

## Recovery run

A separate morning recovery run executes after the main radar. It must:

1. Read the current-day checkpoint and all current-day Gmail Sent messages.
2. Reconcile any sends that Gmail accepted but GitHub did not record.
3. Count only successful new contacts for the current day.
4. If the count is below 8, resume the checkpoint queue, then replenish discovery if needed.
5. Continue toward 20 unique newly contacted people for the day, treating 15 as the minimum goal and 20 as the absolute cap, while preserving the same eligibility, quality, dedupe, and verified-email rules. Never fill a shortage with unverified, stale, India-HQ, ineligible or already-contacted leads.
6. Replace bounces and transient failures with the next qualified opportunity.
7. Write a final current-day audit and update the checkpoint state.

## Today-specific recovery invariant

If Gmail contains a successful outreach that is absent from `reached_out.json`, the next reconciliation must import it before any new send so it cannot be duplicated. Run audit files are valid dedupe evidence when a ledger write was interrupted.

## Idempotent sending and final-follow-up hard stop (Oct 2026 incident fix)

A tool wrapper returning an error or safety block is **not** evidence that underlying actions were rolled back. On October 7, a multi-send wrapper returned an error after some messages had reached Gmail Sent, and an attempted per-recipient recovery produced duplicate final follow-ups. Never repeat that pattern.

1. Never send to multiple recipients inside one orchestration/tool wrapper. Execute at most one outbound Gmail action per operation, wait for its result, and reconcile that recipient before moving on.
2. Before **every** initial or follow-up send, read the recipient's Gmail thread and recent Sent matches. Check existing messages regardless of whether GitHub has recorded them. Skip if an equivalent new outreach or follow-up already exists.
3. On **any** ambiguous outcome (tool error, block, timeout, missing Gmail ID), stop and search Gmail Sent by exact recipient and thread/subject. Read the entire thread to detect messages accepted before the error. Never immediately retry based on an exception alone.
4. Follow-ups are capped at **one total per recipient lifetime**, counting Gmail Sent messages even when the GitHub ledger is stale. Any first follow-up, regardless of its subject or prior wording, permanently exhausts this quota. Delete all second-follow-up due dates from the queue and ledger. Contacts with `followup_limit_reached` or `suppress_all_future_outreach` must not be contacted again.
5. If equivalent messages have already been sent twice due to an incident, record each Gmail message ID, set `suppress_all_future_outreach=true`, and never repeat that outreach. Do not count duplicate messages as contacts or campaign successes.
6. A successful Gmail Sent record must be durably written to the permanent ledger before beginning another outbound send whenever GitHub is writable. If a ledger write fails, do not reuse that recipient; checkpoint its Gmail ID in a dated audit and reconcile before the next run.
7. Count only initial contact emails toward the 15–20 new-contact daily target. Mark `delivery_delayed` separately from successfully delivered and `bounced`; never claim a delayed message is delivered. Recheck late bounces on the next run.
8. If a primary, recovery, daytime, and closeout automation share a date, they must all read the same Gmail-driven ledger and checkpoint. Only one worker may send to a given recipient/thread. Disable overlapping legacy batch tasks rather than running them concurrently.
9. Pause overlapping scheduled outbound workers after any duplicate-send incident until Gmail Sent and the permanent ledger are reconciled, single-recipient recovery guards are tested, and a single sending owner per time window is configured.

## Single-follow-up and 15–20-new-contacts policy (effective 2026-10-09)

- Maximum **one follow-up email ever per contact**, in the same existing Gmail thread, no sooner than 3 business days after the initial message. If any prior follow-up exists in Gmail Sent—even when absent from the GitHub ledger—skip all future follow-ups. Never send a second or 'final' reminder.
- Backfill historic contacts by marking anyone with a confirmed follow-up as `followup_limit_reached=true` and clearing all `followup_2_due` fields; do not retroactively remove sent-message audit IDs.
- Every daily run seeks **15 to 20 distinct, never-before-contacted new people/companies** with exact, public/current or independently verified email addresses, strong role fit, eligible region and confirmed India/global hiring path. The hard cap is 20 new sends/day; follow-ups do not count.
- Discover roughly 200 new opportunities daily, broaden toward 300 when quality gates leave fewer than 15 sendable contacts, and replenish the 100-entry preverified queue. Report shortfalls explicitly instead of lowering standards.
- Only the 06:30 radar and a daytime recovery owner should ever send. Disable overlapping 07:15 and 07:20 senders and obsolete batch automations to prevent simultaneous writers. Before each recipient, check Gmail Sent and full thread, write `sending` to a dated checkpoint, send one recipient, verify Gmail Sent, then update the permanent ledger before attempting another.
- On connector error, do not send a second message unless a new search of Sent and the whole thread proves no prior send for that intended email. If ambiguous, skip and reconcile later. No batch-send wrapper.
- Count Gmail Sent as *accepted for sending*, not proof of delivery. Late bounces and delivery delays must be reconciled separately, and only confirmed non-bounced new sends count toward the daily target.

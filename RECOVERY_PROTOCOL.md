# Outreach Send Recovery Protocol

## Goal

A temporary Gmail connector/action failure must never end the daily outreach run at a small partial batch. The system targets 8–10 confirmed successful new contacts per morning when enough qualified opportunities exist, while preserving all existing quality and verification gates.

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
7. Continue replenishing/processing candidates until 8–10 successful new contacts are confirmed, or the qualified pool is genuinely exhausted.
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
5. Continue toward 10 successful contacts while preserving the same eligibility, quality, dedupe, and verified-email rules.
6. Replace bounces and transient failures with the next qualified opportunity.
7. Write a final current-day audit and update the checkpoint state.

## Today-specific recovery invariant

If Gmail contains a successful outreach that is absent from `reached_out.json`, the next reconciliation must import it before any new send so it cannot be duplicated. Run audit files are valid dedupe evidence when a ledger write was interrupted.

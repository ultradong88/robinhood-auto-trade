# 2026-11-11

- **Loss-limit check:** Before any sells, weekly realized P&L was -$76.62 (-10.06%), just over the 10% limit. The INTC exit then realized +$3.73, which brought the week to -$72.89 (-9.57%). Entries were **not halted** this cycle. Daily P&L was +0.49%.
- **Held positions (stop-loss/take-profit):** All four were in gain, so no stop was computed: MRVL +10.0%, ORCL +5.7%, INTC +4.0%, AAPL +3.4%. No take-profit tiers fired.
- **Conviction trims:** MRVL (+179% over target) and ORCL (+168% over target) qualify. Each is at streak 1 of 3, so neither was trimmed. AAPL is not overweight enough to qualify.
- **exit_existing:** INTC was sold in full.
- **Candidates:**
  - COST (new, medium): approved, $78.89. Opened 2.2% above the thesis price. A news check found nothing against the thesis.
  - LIN (new, low effective): approved, $39.44.
  - V, LLY, PG (new): rejected because the 5-position cap was filled by higher-priority candidates.
  - AAPL (top-up): rejected because it is already at or above target ($44.15 vs $39.44).
  - MRVL (top-up): rejected for three reasons: a 6.5% price gap, the wash-sale guard (loss sale on 11-05), and the stop-loss re-entry lock.
  - ORCL (top-up): rejected because of a 5.7% price gap.
  - FOXA, MCD (new): rejected by thesis stability, since only 1 of the 2 required cycles is on record.
- **Orders placed (live, all filled):**
  - SELL INTC 1.686056 sh @ $61.52 (~$103.73, exit_existing)
  - BUY COST $78.89 (0.072517 sh @ $1,087.88)
  - BUY LIN $39.44 (0.075762 sh @ $520.58)
- Positions are now MRVL, AAPL, ORCL, COST and LIN, which is 5 of 5.

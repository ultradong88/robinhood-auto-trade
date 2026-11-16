# 2026-11-16

- **Loss-limit check:** Daily realized P&L was -$0.73 (-0.10%) and weekly was +$2.68 (+0.35%). Entries were **not halted**.
- **Held positions (stop-loss/take-profit):** MRVL was down 3.2% from average cost against a volatility stop of 15% (20-day stdev 7.6%, clamped to the max), so the stop did not trigger. AAPL (+4.5%), ORCL (+2.8%), COST (+2.4%) and LIN (+0.7%) were in gain, so no stop was computed. No take-profit tiers fired.
- **Conviction trims:** AAPL (+84% over its $24.21 low-conviction target) and LIN (+226% over target) qualify, but each is only at streak 1 of 3, so neither was trimmed. COST does not qualify.
- **Exits (Phase A exit_existing):** MRVL and ORCL were both sold in full.
- **Candidates (Monday weekend-news check found nothing invalidating):**
  - V (new, low): approved at $24.21. The buy was **not placed** because the broker review returned EQUITY_NOT_ENOUGH_BP_DOLLAR_BASED. Today's sale proceeds ($199.27) are unsettled in this cash account, so buying power is $0.
  - LLY (new, medium): rejected because of a 3.09% price gap ($1430.74 -> $1475.00), which exceeds the 3% ceiling.
  - AMD (new, low): rejected by the wash-sale guard (AMD was sold at a loss on 10-20).
  - COST (top-up, high): rejected because it is already at target ($80.77 vs $80.72).
  - LIN (top-up, low): rejected because it is already above target ($78.90 vs $24.21).
  - AAPL (top-up, low): rejected because it is already above target ($44.59 vs $24.21).
- **Orders placed (live, filled):**
  - SELL MRVL 0.667983 sh @ $144.83 (~$96.74, realized -$3.26, no wash sale)
  - SELL ORCL 0.851148 sh @ $120.46 (~$102.53, realized +$2.53)
- **Positions are now AAPL, COST and LIN (3 of 5).** Cash is $199.27, all of it unsettled.
- **Note for the human:** before today's sells, cash was $0 and account value had dropped from about $658 to about $403 since 11-12. That looks like a withdrawal. If it was one, `starting_capital_usd` (761.44) needs a manual update.

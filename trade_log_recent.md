# 2026-11-25

Live mode (dry-run cycle count 10 of 10 required). **2 live sell orders were placed and filled** (conviction trims). No buys.

## Loss-limit check
- Realized P&L (after this cycle's sells): today -$0.02, this week -$0.48 (-0.06% of starting capital). Under limits, so new entries were not halted.

## Held positions — stop-loss / take-profit
- **AAPL**: up 2.9% on average cost. Stop not computed because the position shows a gain. No take-profit tier fired.
- **COST**: up 0.5%. Stop not computed because the position shows a gain. No tier fired. Holding.
- **LIN**: down 2.6%. Stop 5.0%, not triggered. No tier fired.
- **LLY**: down 2.3%. Stop 6.2%, not triggered. Holding.
- **V**: down 1.9%. Stop 5.0%, not triggered. Holding.

## Conviction trim
- **AAPL**: low conviction and about 93% over its $12.31 target for 3 cycles in a row, so the trim **triggered**. Sold about $11.40.
- **LIN**: effective conviction is low (today's high, yesterday's low), about 96% over its $12.31 target, 3 cycles in a row, so the trim **triggered**. Sold about $11.84.
- COST, LLY, V: not triggered. V is effectively at target.

## Candidates
- **SO, MCD, HD, PG, AMTM, KYMR** (new entries): rejected because all slots are full (5 of 5).
- **AAPL, LIN** (top-ups): not eligible because a conviction trim fired this cycle (same-cycle sell-then-buy guard).
- **V** (top-up): blocked by the wash-sale guard (loss sale on 11-23) and the re-entry lock (price $415.23 is above the $407.25 sell, 2 of 10 trading days).
- **COST, LLY** (top-ups): passed the entry gate but are already above target size for their conviction tier, so no top-up.

## Orders
- **AAPL sell**: 0.032529 shares filled at $349.95 (~$11.38). Realized a gain.
- **LIN sell**: 0.022967 shares filled at $515.74 (~$11.84). Realized a loss. Flagged as a possible wash sale because LIN was bought on 11-12 and a position is still held in this account.
- Cash is now $34.28. Account value is $204.77.

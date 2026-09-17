# 2026-09-17

Phase B ran once today: **08:39:20 CT** (the standard 8:35am scheduled run,
Thursday). `execution.mode` read fresh as **`live`**, and the dry-run cycle
count remains **10** distinct dates — still `>=` the 10 required, so the
live-order gate stays open.

## Account state (before this cycle's sells)

Four open equity positions, all classified **held** (Step 4), filling all
`max_concurrent_positions` (4) slots:

- **MRVL** — 0.387859 sh, avg cost $226.14, current $244.78 (gain).
- **NVDA** — 0.413143 sh, avg cost $218.91, current $217.71 (loss).
- **AXTI** — 1.351398 sh, avg cost $68.15, current $67.29 (loss).
- **SKHY** — 0.248619 sh, avg cost $176.21, current $185.14 (gain).

- **Stop-loss** (volatility_scaled):
  - MRVL, SKHY: showing gains — stop not computed (a non-positive drawdown
    can never meet a positive stop_pct).
  - NVDA: drawdown **0.55%** vs. computed `stop_pct_used` 7.35% (20-day
    stdev 2.94% × 2.5) — **not triggered**.
  - AXTI: drawdown **1.26%** vs. `stop_pct_used` 15.00% (clamped at the
    max, 20-day stdev 7.02% × 2.5) — **not triggered**.
- **Take-profit**: MRVL +8.24%, NVDA -0.55%, AXTI -1.26%, SKHY +5.07% — no
  tier (15%/30%/50%) eligible for any; hold/monitor.
- **Conviction-trim** (enabled, effective conviction from thesis-stability):
  AXTI high (underweight, -39.74%) and NVDA medium (~at target, -0.66%) —
  not overweight. MRVL low, **109.71% overweight** its low-tier target —
  this cycle *qualifies*, but only 1 consecutive qualifying cycle so far
  (the most recent prior held cycle, 2026-09-16, was conviction=medium,
  which broke the streak) vs. `min_low_conviction_cycles` 3 — **not
  triggered**. SKHY low, +1.69% overweight — not triggered.

No `exit_existing` candidates. No sells fired this cycle (no stop-loss
trigger, no take-profit tier, no conviction-trim trigger).

## Loss-limit check

$0.00 realized today, -$15.46 realized this week (the 2026-09-14 VRT
stop-loss sale carried over; 0.00% / -2.03% of the $761.44 starting
capital, against limits of 5% daily / 10% weekly). **Entries not halted.**

## Candidates considered

`pending_proposals.jsonl` held 5 `direction: long` candidates (proposal_date
2026-09-16, Wednesday's Phase A run): DELL (high), AXTI (high, held/top-up),
MRVL (low, held/top-up), NVDA (medium, held/top-up), SKHY (low, held/top-up)
— BWIN, FANG, KNX, SPCX were `direction: avoid` (not processed), no
`exit_existing`. None had a prior `risk_check`/`order` entry with matching
`proposal_date`, so all were evaluated fresh. Today is Thursday, not Monday,
so no weekend-gap search ran.

**Capacity**: `open_slots = 4 max_concurrent_positions - 4 live positions = 0`.
The one **new**-group candidate was rejected outright, before reaching
thesis-stability or the buy gate:

- **DELL** — **rejected**: no open slots this cycle (4 of 4 max already
  held/approved) — skipped without a staleness re-check.

The **held** group (AXTI, MRVL, NVDA, SKHY) was unaffected and continued to
thesis-stability and the buy gate.

**Thesis-stability** gate (required 2 consecutive cycles): all four held
top-ups passed (direction long across 2026-09-17 and 2026-09-16, conviction
stable in each case) — AXTI at high, MRVL at low, NVDA at medium, SKHY at
low.

**Buy gate** (entry_price_gap max 3%, entry_extension max 10%, wash-sale,
sell re-entry lock):
- **AXTI** — **rejected**: price gapped **+16.83%** above thesis-time price
  ($57.70 → $67.41), outside `entry_price_gap.max_pct` (3%) — top-up
  skipped this cycle.
- **MRVL** — **rejected**: price gapped **+10.48%** above thesis-time price
  ($221.70 → $244.93) — top-up skipped this cycle.
- **SKHY** — **rejected**: price gapped **+5.95%** above thesis-time price
  ($174.83 → $185.23) — top-up skipped this cycle.
- **NVDA** — passed the hard ceilings (gap +2.63%, extension -0.35% vs.
  20-day MA). Its non-trivial gap was re-checked via web search against its
  thesis invalidation criteria (Q3 FY2027 guidance disappointment, China
  export restrictions widening) — nothing found; coverage centered on the
  pending Hugging Face acquisition and Q2 FY2027 earnings strength. Not
  invalidated.

Wash-sale check (all three linked accounts, span=month): zero loss-realizing
closes found for AXTI/MRVL/NVDA/SKHY in any account — guard clear for all
four (moot for AXTI/MRVL/SKHY, already blocked on price gap).

## Orders

Ranked by `rank_candidates.py`/`position_sizing.py` (re-pulled fresh
total_value $751.41 and cash $432.59 — unchanged, no sells this cycle): only
**NVDA** survived to the ranking stage (AXTI/MRVL/SKHY already excluded by
the buy gate, DELL by capacity).

- **NVDA** — top-up **rejected**: headroom $0.23, below the $9.02 min-top-up
  threshold (10% of its $90.17 medium-tier target).

No candidate reached `review_equity_order` this cycle. `execution.mode` was
`"live"` and the live-order gate (dry-run cycle count 10/10) remained open
but unused — **0 orders reviewed, 0 placed.**

`concurrent_positions_after_final` 4 (no slot change), `cash_remaining_final`
$432.59 (unchanged).

_(Convenience view only. `trade_log.jsonl` is the source of truth; if the two
disagree, trust `trade_log.jsonl`.)_

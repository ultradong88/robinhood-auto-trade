# 2026-09-18

Phase B ran once today: **08:41:24 CT** (the standard 8:35am scheduled run,
Friday). `execution.mode` read fresh as **`live`**, and the dry-run cycle
count remains **10** distinct dates — still `>=` the 10 required, so the
live-order gate stays open.

**Data gap note**: `trade_log.jsonl` has no entries dated 2026-09-17 — Phase B
did not run on Thursday. The Phase A proposals dated 2026-09-16 that should
have been processed that day were never evaluated, and were superseded when
Phase A ran again on 2026-09-17 and overwrote `pending_proposals.jsonl`. Only
today's (2026-09-17-dated) proposals were processed this cycle, per spec — no
corrective action taken.

## Account state (before this cycle's sells)

Four open equity positions, all classified **held** (Step 4), filling all
`max_concurrent_positions` (4) slots:

- **MRVL** — 0.387859 sh, avg cost $226.14, current $239.26 (gain).
- **NVDA** — 0.413143 sh, avg cost $218.91, current $218.8317 (flat/tiny loss).
- **AXTI** — 1.351398 sh, avg cost $68.15, current $70.00 (gain).
- **SKHY** — 0.248619 sh, avg cost $176.21, current $184.9503 (gain).

- **Stop-loss** (volatility_scaled):
  - MRVL, AXTI, SKHY: showing gains — stop not computed (a non-positive
    drawdown can never meet a positive stop_pct).
  - NVDA: drawdown **0.04%** vs. computed `stop_pct_used` 7.50% (20-day
    stdev 3.00% × 2.5) — **not triggered**.
- **Take-profit**: MRVL +5.80%, NVDA -0.04%, AXTI +2.71%, SKHY +4.96% — no
  tier (15%/30%/50%) eligible for any; hold/monitor.
- **Conviction-trim** (enabled, effective conviction from thesis-stability):
  MRVL low, **104.63% overweight** its low-tier target — qualifies this
  cycle, but only 1 consecutive qualifying cycle so far (most recent prior
  risk_check, 2026-09-16, was conviction=medium, breaking the streak) vs.
  `min_low_conviction_cycles` 3 — **not triggered**. NVDA medium, ~at target
  (-0.32% overweight) — not triggered. AXTI low, **108.60% overweight** —
  qualifies this cycle, but only 1 consecutive qualifying cycle (the most
  recent prior risk_check, 2026-09-16, had conviction=low but was a buy-gate
  rejection with no position-value/target logged, so it doesn't satisfy the
  overweight condition — chain resets to 0 prior) vs. 3 required — **not
  triggered**. SKHY low, +1.39% overweight — not triggered.

No `exit_existing` candidates. No sells fired this cycle (no stop-loss
trigger, no take-profit tier, no conviction-trim trigger).

## Loss-limit check

$0.00 realized today, -$15.46 realized this week (the 2026-09-14 VRT
stop-loss sale carried over; 0.00% / -2.03% of the $761.44 starting
capital, against limits of 5% daily / 10% weekly). **Entries not halted.**

## Candidates considered

`pending_proposals.jsonl` held 7 `direction: long` candidates (proposal_date
2026-09-17, Thursday's Phase A run): MRVL (low, held/top-up), NVDA (medium,
held/top-up), AXTI (low, held/top-up), SKHY (low, held/top-up), AAPL
(medium, new), ASAN (medium, new), DELL (high, new) — GBTG, INIO, SPCX were
`direction: avoid` (not processed), no `exit_existing`. None had a prior
`risk_check`/`order` entry with matching `proposal_date`, so all were
evaluated fresh. Today is Friday, not Monday, so no weekend-gap search ran.

**Capacity**: `open_slots = 4 max_concurrent_positions - 4 live positions = 0`.
All 3 **new**-group candidates were rejected outright, before reaching
thesis-stability or the buy gate:

- **AAPL, ASAN, DELL** — **rejected**: no open slots this cycle (4 of 4 max
  already held/approved) — skipped without a staleness re-check. (ASAN would
  separately have failed thesis-stability on insufficient history, but
  capacity short-circuits first, so that check was never reached.)

The **held** group (MRVL, NVDA, AXTI, SKHY) was unaffected and continued to
thesis-stability and the buy gate.

**Thesis-stability** gate (required 2 consecutive cycles): all four held
top-ups passed (direction long across 2026-09-17 and 2026-09-16) — MRVL
stable at low, NVDA stable at medium, AXTI drifted (today low, prior
high — sized off the lower, low), SKHY stable at low.

**Buy gate** (entry_price_gap max 3%, entry_extension max 10%, wash-sale,
sell re-entry lock):
- **MRVL** — **rejected**: price gapped **+4.21%** above thesis-time price
  ($229.71 → $239.37), outside `entry_price_gap.max_pct` (3%) — top-up
  skipped this cycle.
- **AXTI** — **rejected**: price gapped **+9.02%** above thesis-time price
  ($64.30 → $70.10) *and* extended **+10.07%** above its 20-day average
  ($63.685) — both outside their hard ceilings — top-up skipped this cycle.
- **SKHY** — **rejected**: price gapped **+5.86%** above thesis-time price
  ($174.87 → $185.11), outside `entry_price_gap.max_pct` (3%) — top-up
  skipped this cycle.
- **NVDA** — passed the hard ceilings (gap +2.31%, extension +0.11%). The
  gap was non-trivial and re-checked via web search against its thesis
  invalidation criteria (Hugging Face deal regulatory pushback, Q3 FY2027
  guidance walkback) — nothing found beyond the already-known, ongoing
  HSR/antitrust review; Jensen Huang publicly reaffirmed a bullish 2027
  chip-sales outlook. Not invalidated.

Wash-sale check (all three linked accounts, span=month): only the
already-known 2026-09-04 MRVL sale found, with a positive realized gain
($0.05, not a loss) — guard clear for all four held symbols. None of the
four has any prior sell order in `trade_log.jsonl`, so the sell re-entry
lock never applied.

## Orders — none

Only **NVDA** cleared the buy gate and reached sizing (MRVL/AXTI/SKHY were
already excluded above; AAPL/ASAN/DELL excluded by capacity above). Ranked
by `rank_candidates.py`/`position_sizing.py` (re-pulled fresh total_value
$757.78 and cash $432.59 — unchanged, no sells this cycle):

- **NVDA** — top-up **rejected**: computed top-up amount $0.52 (headroom to
  its medium-tier target of $90.93) is below the min top-up threshold $9.09
  (`min_top_up_pct_of_target` 10% of target).

No orders were reviewed or placed this cycle. `concurrent_positions_after_final`
4 (no slot change), `cash_remaining_final` $432.59 (unchanged).

_(Convenience view only. `trade_log.jsonl` is the source of truth; if the two
disagree, trust `trade_log.jsonl`.)_

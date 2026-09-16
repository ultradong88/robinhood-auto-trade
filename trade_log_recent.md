# 2026-09-16

Phase B ran once today: **08:41:18 CT** (the standard 8:35am scheduled run,
Wednesday). `execution.mode` read fresh as **`live`**, and the dry-run cycle
count remains **10** distinct dates — still `>=` the 10 required, so the
live-order gate stays open.

## Account state (before this cycle's sells)

Four open equity positions, all classified **held** (Step 4), filling all
`max_concurrent_positions` (4) slots:

- **MRVL** — 0.196608 sh, avg cost $223.49, current $226.50 (gain).
- **NVDA** — 0.413143 sh, avg cost $218.91, current $213.95 (loss).
- **AXTI** — 1.351398 sh, avg cost $68.15, current $61.01 (loss).
- **SKHY** — 0.248619 sh, avg cost $176.21, current $179.24 (gain).

- **Stop-loss** (volatility_scaled):
  - MRVL, SKHY: showing gains — stop not computed (a non-positive drawdown
    can never meet a positive stop_pct).
  - NVDA: drawdown **2.27%** vs. computed `stop_pct_used` 7.35% (20-day
    stdev 2.94% × 2.5) — **not triggered**.
  - AXTI: drawdown **10.48%** vs. `stop_pct_used` 15.00% (clamped at the
    max, 20-day stdev 6.77% × 2.5) — **not triggered**.
- **Take-profit**: MRVL +1.35%, NVDA -2.27%, AXTI -10.48%, SKHY +1.72% — no
  tier (15%/30%/50%) eligible for any; hold/monitor.
- **Conviction-trim** (enabled, effective conviction from thesis-stability):
  MRVL medium (underweight, -49.54%) and NVDA medium (~at target, +0.05%) —
  not overweight. AXTI low, **86.68% overweight** its low-tier target — this
  cycle *qualifies*, but only 1 consecutive qualifying cycle so far (the
  most recent prior top-up, 2026-09-14, was conviction=medium, which broke
  the streak) vs. `min_low_conviction_cycles` 3 — **not triggered**. SKHY
  low, +0.90% overweight — not triggered.

No `exit_existing` candidates. No sells fired this cycle (no stop-loss
trigger, no take-profit tier, no conviction-trim trigger).

## Loss-limit check

$0.00 realized today, -$15.46 realized this week (the 2026-09-14 VRT
stop-loss sale carried over; 0.00% / -2.03% of the $761.44 starting
capital, against limits of 5% daily / 10% weekly). **Entries not halted.**

## Candidates considered

`pending_proposals.jsonl` held 8 `direction: long` candidates (proposal_date
2026-09-15, Tuesday's Phase A run): DELL (high), BWIN (medium), FPS (low),
SRRK (low), MRVL (medium, held/top-up), NVDA (medium, held/top-up), AXTI
(low, held/top-up), SKHY (low, held/top-up) — SPCX was `direction: avoid`
(not processed), no `exit_existing`. None had a prior `risk_check`/`order`
entry with matching `proposal_date`, so all were evaluated fresh. Today is
Wednesday, not Monday, so no weekend-gap search ran.

**Capacity**: `open_slots = 4 max_concurrent_positions - 4 live positions = 0`.
All 4 **new**-group candidates were rejected outright, before reaching
thesis-stability or the buy gate:

- **DELL, BWIN, FPS, SRRK** — **rejected**: no open slots this cycle (4 of 4
  max already held/approved) — skipped without a staleness re-check.

The **held** group (MRVL, NVDA, AXTI, SKHY) was unaffected and continued to
thesis-stability and the buy gate.

**Thesis-stability** gate (required 2 consecutive cycles): all four held
top-ups passed (direction long across 2026-09-15 and 2026-09-14) — MRVL
stable at medium, NVDA stable at medium, AXTI drifted (today low, prior
medium — sized off the lower, low), SKHY stable at low.

**Buy gate** (entry_price_gap max 3%, entry_extension max 10%, wash-sale,
sell re-entry lock):
- **AXTI** — **rejected**: price gapped **+5.91%** above thesis-time price
  ($57.70 → $61.11), outside `entry_price_gap.max_pct` (3%) — top-up
  skipped this cycle.
- **MRVL, NVDA, SKHY** — all passed the hard ceilings. MRVL (+2.30% gap) and
  SKHY (+2.57% gap) were non-trivial and re-checked via web search against
  their own thesis invalidation criteria — MRVL's rally traced to
  broad semiconductor-sector strength (no hyperscaler capex cut, earnings
  miss, governance flag, or dilutive raise found); SKHY's traced to
  DRAM-shortage pricing power, the existing buyback program, and eased
  labor tensions (no KRX overheating correction, capex cut, litigation
  escalation, or earnings disappointment found) — neither invalidated.
  NVDA's +0.85% gap was trivial, no re-check needed.

Wash-sale check (all three linked accounts, span=month): zero loss-realizing
closes found for MRVL/NVDA/AXTI/SKHY in any account — guard clear for all
four.

## Orders — LIVE

Ranked by `rank_candidates.py`/`position_sizing.py` (re-pulled fresh
total_value $736.39 and cash $476.34 — unchanged, no sells this cycle) in
priority order MRVL (medium, top-up) > NVDA (medium, top-up) > SKHY (low,
top-up); AXTI already excluded above.

- **MRVL** — top-up **approved** for **$43.77** (headroom to its
  medium-tier target of $88.37). `review_equity_order` came back with empty
  `order_checks` (no blocking alert), and with `execution.mode == "live"`
  and the dry-run cycle count at 10/10, **the live-order gate was open**.
  Market order **filled**: 0.191251 sh @ avg **$228.8607**
  (`order_id 6aaa9c66-f219-48fb-aa9a-aafb18d7f79e`).
- **NVDA** — top-up **rejected**: headroom -$0.04, already at/above its
  medium-tier target.
- **SKHY** — top-up **rejected**: headroom -$0.40, already at/above its
  low-tier target.

`concurrent_positions_after_final` 4 (no slot change), `cash_remaining_final`
$432.57.

_(Convenience view only. `trade_log.jsonl` is the source of truth; if the two
disagree, trust `trade_log.jsonl`.)_

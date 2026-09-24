# 2026-09-24

Phase B ran once today: **08:35 CT** (the standard scheduled run, Thursday).
`execution.mode` read fresh as **`live`**, and the dry-run cycle count
remains **10** distinct dates — still `>=` the 10 required, so the
live-order gate stays open.

Thursday cycle, not Monday — no weekend-gap search. Consuming Wednesday
2026-09-23 16:35:16 CT Phase A proposals.

## Account state (before this cycle's sells)

Five open equity positions, all classified **held** (Step 4), filling all 5
of `max_concurrent_positions` (5) slots:

- **MRVL** — 0.290894 sh, avg cost $227.02, current $255.52 (gain).
- **NVDA** — 0.413143 sh, avg cost $218.91, current $222.32 (gain).
- **AXTI** — 1.013548 sh, avg cost $67.91, current $72.94 (gain).
- **SKHY** — 0.248619 sh, avg cost $176.21, current $186.01 (gain).
- **AAPL** — 0.137985 sh, avg cost $333.44, current $336.13 (gain).

- **Stop-loss** (volatility_scaled): NVDA/SKHY/AAPL showing gains on average
  cost (drawdowns -1.56%/-5.56%/-0.81%) — stop not computed. MRVL and AXTI
  switch to a trailing-high reference since a take-profit tier fired earlier
  this holding period: MRVL's trailing high $266.00 vs. today's $255.52 is a
  3.94% drawdown, stop_pct_used 10.83% (20d stdev-scaled), not triggered.
  AXTI's trailing high $81.4999 vs. today's $72.94 is a 10.50% drawdown,
  stop_pct_used 15% (volatility-clamped to the max), not triggered. **None
  triggered.**
- **Take-profit**: MRVL +12.55% (0.15 tier already fired 2026-09-22; 0.30
  not yet reached), AXTI +7.41% (0.15 tier already fired, gain retraced
  since), NVDA +1.56%, SKHY +5.56%, AAPL +0.81% — all hold/monitor, no new
  tier fired.
- **Conviction-trim** (enabled, effective conviction from thesis-stability):
  MRVL effective medium, position below target (not overweight) — not
  qualifying. NVDA effective high, well below target — not qualifying.
  AXTI effective low, 59.44% overweight — qualifies this cycle, 2 consecutive
  cycles vs. `min_low_conviction_cycles` (3) — not triggered. SKHY effective
  low, essentially at target — not qualifying. AAPL effective low,
  essentially at target — not qualifying.

No `exit_existing` candidates.

## Sells — none

No stop-loss, take-profit, or conviction-trim triggers fired this cycle.

## Loss-limit check

$0.00 realized today, $6.97 realized this week (Tuesday's two take-profit
sells); 0.0% / 0.92% of the $761.44 starting capital, against limits of 5%
daily / 10% weekly. **Entries not halted.**

## Candidates considered

`pending_proposals.jsonl` held 12 `direction: long` candidates (proposal_date
2026-09-23): MU (medium), SPCX (low), INTC (low), AMD (medium), DELL (low),
FSLY (medium), VKTX (low) — new — and AXTI (low), SKHY (low), MRVL (medium),
NVDA (high), AAPL (low) — held. No `exit_existing`. None had a prior
`risk_check`/`order` entry with matching `proposal_date`, so all were
evaluated fresh.

**Capacity**: `open_slots = 5 max_concurrent_positions - 5 live positions =
0` — all 7 new-group candidates (MU, SPCX, INTC, AMD, DELL, FSLY, VKTX)
**skipped without a staleness re-check** (no open slots, 5 of 5 max already
held/approved). The held group is unaffected by this short-circuit.

**No same-cycle sell-then-buy**: nothing fired this cycle, so this guard
didn't drop anyone.

**Thesis-stability** gate (required 2 consecutive cycles) for the 5 held
candidates — **MRVL, NVDA, AXTI, SKHY, AAPL** all passed (direction long
across 2026-09-23 and 2026-09-22) — effective conviction sized off the lower
of the window: MRVL medium (today medium, prior high), NVDA high (today
high, prior high, stable), AXTI low (today low, prior low, stable), SKHY low
(today low, prior low, stable), AAPL low (today low, prior low, stable).

**Buy gate** (entry_price_gap max 3%, entry_extension max 10%, wash-sale,
sell re-entry lock):
- **MRVL** — blocked on **entry_extension** (+10.62% vs 20d MA $231.1725);
  sell re-entry lock inputs evaluated (Tuesday's take-profit sale at
  $260.38) but not blocking — today's ask $255.73 is below that sell price.
- **AXTI** — blocked on **entry_extension** (+12.47% vs 20d MA $64.886); its
  own Tuesday take-profit sale at $78.68 did not lock re-entry since today's
  ask $72.98 is below that sell price.
- **NVDA** — passed every hard ceiling (gap -2.85%, extension +0.54% vs 20d
  MA $221.154). Gap trivial, no re-check needed.
- **SKHY** — passed every hard ceiling (gap -4.80%, extension +4.97% vs 20d
  MA $177.1785). Gap trivial, no re-check needed.
- **AAPL** — passed every hard ceiling (gap -0.19%, extension +2.86% vs 20d
  MA $326.948). Gap trivial, no re-check needed.

Wash-sale check (all three linked accounts): Tuesday's MRVL/AXTI sells both
realized a gain (not a loss); account 870285764 has no trades; account
506946300 has no trades within the 30-day lookback window for any of the
five symbols. Guard clear for all five, moot for MRVL/AXTI already blocked
above.

## Top-ups — 1 approved

Ranked by `rank_candidates.py`/`position_sizing.py` (total_value
$772.7864, cash $438.49, `concurrent_positions_start` 5) for the three
candidates that cleared the buy gate, in priority order **NVDA > SKHY >
AAPL**:

- **NVDA** — top-up **approved**: $62.71 to reach its high-tier target of
  $154.56 (current position $91.85, headroom $62.71).
- **SKHY** — top-up **rejected**: only $0.12 of headroom to its low-tier
  target of $46.37, below the $5.00 minimum top-up threshold.
- **AAPL** — top-up **rejected**: already at (fractionally above) its
  low-tier target of $46.37.

## Order placed

Live-order gate open (`execution.mode='live'`, dry-run cycle count 10 >= 10
required, `review_equity_order` returned no blocking alert):

- **NVDA buy** — 0.281386 sh filled @ avg $222.8604 (~$62.71 notional),
  order_id `6ab528da-36ed-49e9-b7bc-b790e423334f`, state `filled`.

`concurrent_positions_after_final` **5**, `cash_remaining_final`
**$375.78**.

_(Convenience view only. `trade_log.jsonl` is the source of truth; if the two
disagree, trust `trade_log.jsonl`.)_

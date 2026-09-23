# 2026-09-23

Phase B ran once today: **08:35 CT** (the standard scheduled run, Wednesday).
`execution.mode` read fresh as **`live`**, and the dry-run cycle count
remains **10** distinct dates — still `>=` the 10 required, so the
live-order gate stays open.

Wednesday cycle, not Monday — no weekend-gap search. Consuming Tuesday
2026-09-22 16:39:21 CT Phase A proposals.

## Account state (before this cycle's sells)

Five open equity positions, all classified **held** (Step 4), filling all 5
of `max_concurrent_positions` (5) slots:

- **MRVL** — 0.290894 sh, avg cost $227.02, current $262.63 (gain).
- **NVDA** — 0.413143 sh, avg cost $218.91, current $228.87 (gain).
- **AXTI** — 1.013548 sh, avg cost $67.91, current $76.475 (gain).
- **SKHY** — 0.248619 sh, avg cost $176.21, current $192.22 (gain).
- **AAPL** — 0.137985 sh, avg cost $333.44, current $339.62 (gain).

- **Stop-loss** (volatility_scaled): NVDA/SKHY/AAPL showing gains on average
  cost — stop not computed. MRVL and AXTI switch to a trailing-high
  reference since a take-profit tier fired earlier this holding period:
  MRVL's trailing high equals today's price (0% drawdown). AXTI's trailing
  high $81.4999 vs. today's $76.475 is a real 6.17% drawdown — stop_pct_used
  computed at 0.15 (volatility-clamped to the max), not triggered. **None
  triggered.**
- **Take-profit**: MRVL +15.69% (0.15 tier already fired 2026-09-22; 0.30
  not yet reached), AXTI +12.61% (0.15 tier already fired, gain retraced
  since), NVDA +4.55%, SKHY +9.09%, AAPL +1.85% — all hold/monitor, no new
  tier fired.
- **Conviction-trim** (enabled, effective conviction from thesis-stability):
  MRVL effective medium, position below target (not overweight) — not
  qualifying. NVDA effective medium, 0.77% overweight — not qualifying.
  AXTI effective low, 65.20% overweight — qualifies this cycle, but only 1
  consecutive cycle (the prior cycle's entry was a same-cycle-sell-guard
  rejection with no conviction/position data, resetting the streak) vs.
  `min_low_conviction_cycles` (3) — not triggered. SKHY effective low,
  1.85% overweight — not qualifying. AAPL effective low, essentially at
  target — not qualifying.

No `exit_existing` candidates.

## Sells — none

No stop-loss, take-profit, or conviction-trim triggers fired this cycle.

## Loss-limit check

$0.00 realized today, $6.97 realized this week (Tuesday's two take-profit
sells); 0.0% / 0.92% of the $761.44 starting capital, against limits of 5%
daily / 10% weekly. **Entries not halted.**

## Candidates considered

`pending_proposals.jsonl` held 13 `direction: long` candidates (proposal_date
2026-09-22): MU (low), INTC (low), AMD (low), DELL (low), SPCX (medium),
VKTX (low), DBRG (high), WBD (high) — new — and MRVL (high), NVDA (high),
AXTI (low), SKHY (low), AAPL (low) — held. No `exit_existing`. None had a
prior `risk_check`/`order` entry with matching `proposal_date`, so all were
evaluated fresh.

**Capacity**: `open_slots = 5 max_concurrent_positions - 5 live positions =
0` — all 8 new-group candidates (MU, INTC, AMD, DELL, SPCX, VKTX, DBRG, WBD)
**skipped without a staleness re-check** (no open slots, 5 of 5 max already
held/approved). The held group is unaffected by this short-circuit.

**No same-cycle sell-then-buy**: nothing fired this cycle, so this guard
didn't drop anyone.

**Thesis-stability** gate (required 2 consecutive cycles) for the 5 held
candidates — **MRVL, NVDA, AXTI, SKHY, AAPL** all passed (direction long
across 2026-09-22 and 2026-09-21) — effective conviction sized off the lower
of the window: MRVL medium (today high, prior medium), NVDA medium (today
high, prior medium), AXTI low (today low, prior high), SKHY low (today low,
prior high), AAPL low (today low, prior medium).

**Buy gate** (entry_price_gap max 3%, entry_extension max 10%, wash-sale,
sell re-entry lock):
- **MRVL** — blocked on both **entry_extension** (+14.94% vs 20d MA
  $228.493) and **sell_reentry_lock** (today's ask $262.63 is above the
  $260.38 Tuesday's take-profit sale went off at, only 1 of 10 trading days
  elapsed).
- **AXTI** — blocked on **entry_extension** (+19.63% vs 20d MA $63.99); its
  own Tuesday take-profit sale at $78.68 did not lock re-entry since
  today's ask $76.55 is below that sell price.
- **SKHY** — blocked on **entry_extension** (+10.73% vs 20d MA $173.691).
- **NVDA** — passed every hard ceiling (gap -0.01%, extension +4.25% vs 20d
  MA $219.5115). Gap trivial, no re-check needed.
- **AAPL** — passed every hard ceiling (gap -0.03%, extension +4.78% vs 20d
  MA $324.1215). Gap trivial, no re-check needed.

Wash-sale check (all three linked accounts): Tuesday's MRVL/AXTI sells both
realized a gain (not a loss); account 870285764 has no trades; account
506946300's MRVL loss sales are all from late June/early July, outside the
30-day lookback window. Guard clear for all five, moot for MRVL/AXTI/SKHY
already blocked above.

## Top-ups — 0 approved

Ranked by `rank_candidates.py`/`position_sizing.py` (total_value
$782.0179, cash $438.49, `concurrent_positions_start` 5) for the two
candidates that cleared the buy gate, in priority order **NVDA > AAPL**:

- **NVDA** — top-up **rejected**: current position value $94.56 already
  $0.72 above its medium-tier target of $93.84.
- **AAPL** — top-up **rejected**: only $0.06 of headroom to its low-tier
  target of $46.92, below the $5.00 minimum top-up threshold.

No buy orders placed this cycle. `concurrent_positions_after_final` **5**,
`cash_remaining_final` **$438.49**.

_(Convenience view only. `trade_log.jsonl` is the source of truth; if the two
disagree, trust `trade_log.jsonl`.)_

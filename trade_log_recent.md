# 2026-09-28

Phase B ran once today: **08:35 CT** (the standard scheduled run, Monday).
`execution.mode` read fresh as **`live`**, and the dry-run cycle count
remains **10** distinct dates — still `>=` the 10 required, so the
live-order gate stays open.

Monday cycle — a weekend-gap search ran for every held candidate before the
price-based check, covering the Friday 2026-09-25 16:37 CT Phase A
proposals (2.5 days stale).

## Account state (before this cycle's sells)

Five open equity positions, all classified **held** (Step 4), filling all 5
of `max_concurrent_positions` (5) slots:

- **MRVL** — 0.290894 sh, avg cost $227.02, current bid $256.34 (gain).
- **NVDA** — 0.694529 sh, avg cost $220.51, current bid $232.33 (gain).
- **AXTI** — 0.613705 sh, avg cost $67.48, current bid $75.62 (gain).
- **SKHY** — 0.248619 sh, avg cost $176.21, current bid $183.64 (gain).
- **AAPL** — 0.137985 sh, avg cost $333.44, current bid $341.53 (gain).

- **Stop-loss** (volatility_scaled): NVDA/SKHY/AAPL showing gains on average
  cost (drawdowns -5.36%/-4.22%/-2.43%) — stop not computed. MRVL and AXTI
  use a trailing-high reference since a take-profit tier fired earlier this
  holding period (MRVL since 2026-09-15, AXTI since 2026-09-10) — daily
  closes were pulled for both even though average cost showed a gain,
  because trailing-high drawdown was positive for each; using the fallback
  stop_pct instead would have wrongly triggered AXTI's stop. MRVL's trailing
  high $267.4799 vs. today's $256.34 is a 4.16% drawdown, stop_pct_used
  8.62% (20d stdev-scaled), not triggered. AXTI's trailing high $81.4999 vs.
  today's $75.62 is a 7.21% drawdown, stop_pct_used 15% (volatility-clamped
  to the max), not triggered. **None triggered.**
- **Take-profit**: MRVL +12.92% (0.15 tier already fired 2026-09-22; 0.30
  not yet reached), AXTI +12.06% (0.15 tier already fired, gain retraced
  since), NVDA +5.36%, SKHY +4.22%, AAPL +2.43% — all hold/monitor, no new
  tier fired.
- **Conviction-trim** (enabled, effective conviction from thesis-stability):
  MRVL effective medium, underweight — not qualifying. **NVDA effective low
  (drifted down from medium), 244.15% overweight — qualifies this cycle, 2
  consecutive qualifying cycles vs. `min_low_conviction_cycles` (3) — not
  yet triggered.** AXTI effective low, underweight — not qualifying. SKHY
  effective low, underweight — not qualifying. AAPL effective low, roughly
  at target — not qualifying.

No `exit_existing` candidates.

## Sells — 0 executed

Nothing fired this cycle (no stop-loss, no take-profit tier, no
conviction-trim, no `exit_existing`). Account state was unchanged after the
Step 4 snapshot, so the Step 6 re-pull confirmed the same 5 positions and
$406.43 cash.

## Loss-limit check

$0.00 realized today, $10.20 realized this week; 0.00% / 1.34% of the
$761.44 starting capital, against limits of 5% daily / 10% weekly.
**Entries not halted.**

## Candidates considered

`pending_proposals.jsonl` held 12 `direction: long` candidates (proposal_date
2026-09-25): MU (low), SPCX (medium), INTC (low), AMD (medium), DELL (low),
AKAM (low), WTTR (low) — new — and MRVL (medium), NVDA (medium), AXTI
(medium), SKHY (low), AAPL (low) — held. CM was `direction: avoid`, not
processed. No `exit_existing`. None had a prior `risk_check`/`order` entry
with matching `proposal_date`, so all were evaluated fresh.

**Capacity**: `open_slots = 5 max_concurrent_positions - 5 live positions =
0` — all 7 new-group candidates (MU, SPCX, INTC, AMD, DELL, AKAM, WTTR)
**skipped without a staleness re-check** (no open slots, 5 of 5 max already
held/approved — the capacity short-circuit runs before thesis-stability or
the weekend-gap search, so those gates were never evaluated for them). The
held group is unaffected by this short-circuit.

**No same-cycle sell-then-buy guard**: nothing fired this cycle, so no held
candidate was dropped on that basis.

**Weekend-gap search** (Monday, one targeted search per held candidate):
nothing found for any of MRVL, NVDA, AXTI, SKHY, or AAPL that plausibly
invalidates its thesis. One soft watch item on NVDA (not an invalidation):
weekend reporting confirms China approved H200 sales to Alibaba/ByteDance/
Tencent per the Sept 24 summit, but purchase-order conversion by those
buyers isn't yet confirmed.

**Thesis-stability** gate (required 2 consecutive cycles) for all 5 held
candidates — **MRVL, NVDA, AXTI, SKHY, AAPL** all passed (direction long
across 2026-09-25 and 2026-09-24) — effective conviction sized off the
lower of the window: MRVL medium (stable), NVDA low (drifted from medium),
AXTI low (drifted from medium), SKHY low (stable), AAPL low (stable).

**Buy gate** (entry_price_gap max 3%, entry_extension max 10%, wash-sale,
sell re-entry lock):
- **MRVL** — blocked on **entry_extension** (+10.28% vs 20d MA $232.8888).
  Sell re-entry lock evaluated (take-profit sale $260.38 on 2026-09-22, 4 of
  10 trading days elapsed) but not blocking — today's ask $256.83 is below
  the sale price.
- **NVDA** — blocked on **entry_price_gap** (+3.47% vs thesis-time $224.58,
  ceiling 3%). Extension +4.79% was fine.
- **AXTI** — blocked on **entry_extension** (+14.64% vs 20d MA $66.023).
  Sell re-entry lock evaluated (conviction-trim sale $76.33 on 2026-09-25, 1
  of 10 trading days elapsed) but not blocking — today's ask $75.69 is below
  the sale price.
- **SKHY** — passed every hard ceiling (gap -1.42%, extension +2.01% vs 20d
  MA $180.0935). Gap trivial, no re-check needed.
- **AAPL** — passed every hard ceiling (gap +0.17%, extension +3.71% vs 20d
  MA $329.396). Gap trivial, no re-check needed.

Wash-sale check (all three linked accounts, span=month): no realized-loss
closing sales for MRVL/NVDA/AXTI/SKHY/AAPL in the 30-day lookback (only
gains on MRVL/AXTI this week and an unrelated VRT loss from 2026-09-14).
Guard clear for all five, moot for MRVL/NVDA/AXTI already blocked above.

## Top-ups — 0 approved

Ranked by `rank_candidates.py`/`position_sizing.py` (total_value
$781.0786, cash $406.43, `concurrent_positions_start` 0 — top-ups never
consume a slot) for the two candidates that cleared the buy gate, in
priority order **AAPL > SKHY** (both low conviction; AAPL ranked ahead on
lower `risk_flags` count):

- **AAPL** — top-up **rejected**: already $0.28 above its low-tier target
  of $46.86 (at target).
- **SKHY** — top-up **rejected**: only $1.20 of headroom to its low-tier
  target of $46.86, below the $5.00 minimum top-up threshold.

## Orders placed

None. No sell triggered in Step 5/6, and no buy candidate survived Step 7's
buy gate + sizing. `review_equity_order` was never called this cycle.

`concurrent_positions_after_final` **5**, `cash_remaining_final`
**$406.43**.

_(Convenience view only. `trade_log.jsonl` is the source of truth; if the two
disagree, trust `trade_log.jsonl`.)_

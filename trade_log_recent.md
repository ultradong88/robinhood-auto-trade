# 2026-09-25

Phase B ran once today: **08:35 CT** (the standard scheduled run, Friday).
`execution.mode` read fresh as **`live`**, and the dry-run cycle count
remains **10** distinct dates — still `>=` the 10 required, so the
live-order gate stays open.

Friday cycle, not Monday — no weekend-gap search. Consuming Thursday
2026-09-24 16:35:38 CT Phase A proposals.

## Account state (before this cycle's sells)

Five open equity positions, all classified **held** (Step 4), filling all 5
of `max_concurrent_positions` (5) slots:

- **MRVL** — 0.290894 sh, avg cost $227.02, current $263.40 (gain).
- **NVDA** — 0.694529 sh, avg cost $220.51, current $226.41 (gain).
- **AXTI** — 1.013548 sh, avg cost $67.91, current $76.33 (gain).
- **SKHY** — 0.248619 sh, avg cost $176.21, current $190.70 (gain).
- **AAPL** — 0.137985 sh, avg cost $333.44, current $335.23 (gain).

- **Stop-loss** (volatility_scaled): NVDA/SKHY/AAPL showing gains on average
  cost (drawdowns -2.68%/-8.22%/-0.54%) — stop not computed. MRVL and AXTI
  use a trailing-high reference since a take-profit tier fired earlier this
  holding period: MRVL's trailing high $266.00 vs. today's $263.40 is a
  0.98% drawdown, stop_pct_used 10.80% (20d stdev-scaled), not triggered.
  AXTI's trailing high $81.4999 vs. today's $76.33 is a 6.34% drawdown,
  stop_pct_used 15% (volatility-clamped to the max), not triggered. **None
  triggered.**
- **Take-profit**: MRVL +16.03% (0.15 tier already fired 2026-09-22; 0.30
  not yet reached), AXTI +12.40% (0.15 tier already fired, gain retraced
  since), NVDA +2.68%, SKHY +8.22%, AAPL +0.54% — all hold/monitor, no new
  tier fired.
- **Conviction-trim** (enabled, effective conviction from thesis-stability):
  MRVL effective medium, underweight — not qualifying. NVDA effective low
  (drifted down from high), 235.64% overweight — qualifies this cycle but
  only 1 consecutive cycle (streak broke last cycle while conviction was
  still high) vs. `min_low_conviction_cycles` (3) — not triggered. **AXTI
  effective low, 65.15% overweight, 3 consecutive qualifying cycles — meets
  the threshold. TRIGGERED.** SKHY effective low, 1.21% overweight — not
  qualifying. AAPL effective low, underweight — not qualifying.

No `exit_existing` candidates.

## Sells — 1 executed

**AXTI conviction-trim**: sold $30.52 (0.399843 sh) down toward its
low-conviction target. `review_equity_order` returned no blocking alert;
live-order gate open (`execution.mode='live'`, dry-run cycle count 10 >= 10
required) — order placed and filled at avg $76.6592 (order_id
`6ab679ad-e05d-4510-bb5c-65cbd03e7112`), realizing a **+$3.24 gain** (avg
cost $67.91) — not a wash sale (a gain, not a loss). AXTI now holds
0.613705 sh; still 5 open positions (partial sell only).

Per Step 7's same-cycle sell-then-buy guard, AXTI is dropped from today's
held top-up group — not eligible for a top-up this same cycle.

## Loss-limit check (re-run after the sell)

$3.24 realized today, $10.21 realized this week (includes today's AXTI
conviction-trim gain); 0.43% / 1.34% of the $761.44 starting capital,
against limits of 5% daily / 10% weekly. **Entries not halted.**

## Candidates considered

`pending_proposals.jsonl` held 8 `direction: long` candidates (proposal_date
2026-09-24): MU (medium), AMD (medium), HAFN (medium) — new — and MRVL
(medium), NVDA (low), AXTI (low), SKHY (medium), AAPL (medium) — held. No
`exit_existing`. None had a prior `risk_check`/`order` entry with matching
`proposal_date`, so all were evaluated fresh.

**Capacity**: `open_slots = 5 max_concurrent_positions - 5 live positions =
0` — all 3 new-group candidates (MU, AMD, HAFN) **skipped without a
staleness re-check** (no open slots, 5 of 5 max already held/approved; HAFN
would also have failed thesis-stability on insufficient history, but the
capacity short-circuit applies first). The held group is unaffected by this
short-circuit.

**No same-cycle sell-then-buy**: AXTI's conviction-trim fired this cycle, so
it was dropped from the held group before the weekend-gap search or buy
gate ran.

**Thesis-stability** gate (required 2 consecutive cycles) for the remaining
4 held candidates — **MRVL, NVDA, SKHY, AAPL** all passed (direction long
across 2026-09-24 and 2026-09-23) — effective conviction sized off the
lower of the window: MRVL medium (stable), NVDA low (today low, prior high,
drifted), SKHY low (today medium, prior low, drifted), AAPL low (today
medium, prior low, drifted).

**Buy gate** (entry_price_gap max 3%, entry_extension max 10%, wash-sale,
sell re-entry lock):
- **MRVL** — blocked on both **entry_extension** (+13.16% vs 20d MA
  $231.8645) and **sell re-entry lock** (today's ask $262.37 is above the
  $260.38 take-profit sale from 2026-09-22, only 3 of 10 trading days
  elapsed).
- **NVDA** — passed every hard ceiling (gap -0.05%, extension +1.58% vs 20d
  MA $221.90). Gap trivial, no re-check needed.
- **SKHY** — passed every hard ceiling (gap +0.79%, extension +6.82% vs 20d
  MA $178.596). Gap trivial, no re-check needed.
- **AAPL** — passed every hard ceiling (gap -0.03%, extension +2.35% vs 20d
  MA $328.0715). Gap trivial, no re-check needed.

Wash-sale check (all three linked accounts, span=month): no realized-loss
closing sales for MRVL/NVDA/SKHY/AAPL in the 30-day lookback (only gains on
MRVL/AXTI this week and an unrelated VRT loss from 2026-09-14). Guard clear
for all four, moot for MRVL already blocked above.

## Top-ups — 0 approved

Ranked by `rank_candidates.py`/`position_sizing.py` (total_value
$780.2411, cash $406.43, `concurrent_positions_start` 5) for the three
candidates that cleared the buy gate, in priority order **SKHY > NVDA >
AAPL** (tie-broken by `pct_below_52wk_high` descending within the low
tier):

- **SKHY** — top-up **rejected**: already $0.60 above its low-tier target
  of $46.81 (at target).
- **NVDA** — top-up **rejected**: $109.71 above its low-tier target of
  $46.81 — far overweight now that thesis-stability re-tiered it from high
  to low conviction.
- **AAPL** — top-up **rejected**: only $0.49 of headroom to its low-tier
  target of $46.81, below the $5.00 minimum top-up threshold.

## Orders placed

- **AXTI sell** (conviction-trim) — 0.399843 sh filled @ avg $76.6592
  (~$30.52 notional), order_id `6ab679ad-e05d-4510-bb5c-65cbd03e7112`,
  state `filled`.

No buy orders placed this cycle.

`concurrent_positions_after_final` **5**, `cash_remaining_final`
**$406.43**.

_(Convenience view only. `trade_log.jsonl` is the source of truth; if the two
disagree, trust `trade_log.jsonl`.)_

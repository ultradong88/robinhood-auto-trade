# 2026-09-22

Phase B ran once today: **08:35 CT** (the standard scheduled run, Tuesday).
`execution.mode` read fresh as **`live`**, and the dry-run cycle count
remains **10** distinct dates — still `>=` the 10 required, so the
live-order gate stays open.

Tuesday cycle, not Monday — no weekend-gap search. Consuming Monday
2026-09-21 16:38:50 CT Phase A proposals.

## Account state (before this cycle's sells)

Five open equity positions, all classified **held** (Step 4), filling all 5
of `max_concurrent_positions` (5) slots:

- **MRVL** — 0.387859 sh, avg cost $226.14, current $260.98 (gain).
- **NVDA** — 0.413143 sh, avg cost $218.91, current $229.4601 (gain).
- **AXTI** — 1.351398 sh, avg cost $68.15, current $78.50 (gain).
- **SKHY** — 0.248619 sh, avg cost $176.21, current $189.48 (gain).
- **AAPL** — 0.137985 sh, avg cost $333.44, current $342.27 (gain).

- **Stop-loss** (volatility_scaled): all five positions showing gains — stop
  not computed for any. **Not triggered.**
- **Take-profit**: **MRVL +15.41%** and **AXTI +15.19%** both cleared the
  15% first tier — **fired**, each selling 25% of the position. NVDA
  (+4.82%), SKHY (+7.53%), AAPL (+2.65%) all below the first tier —
  hold/monitor.
- **Conviction-trim** (enabled, effective conviction from thesis-stability):
  MRVL effective medium, 7.77% overweight — not low conviction, not
  qualifying. NVDA effective low, 101.83% overweight — qualifies, 2nd
  consecutive cycle, but under `min_low_conviction_cycles` (3) — not
  triggered. AXTI effective medium, 12.94% overweight — not qualifying.
  SKHY effective low, 0.31% overweight (well under the 25% trigger) — not
  qualifying. AAPL effective low, 0.57% overweight — not qualifying (first
  cycle held, no streak).

No `exit_existing` candidates.

## Sells — 2 placed (take-profit)

Both reviewed clean (`order_checks` empty) and the live-order gate was open
(mode=live, dry-run cycle count 10≥10, no blocking alert):

- **MRVL** — sold 0.096965 of 0.387859 sh (first 15% tier), filled @ avg
  **$260.8877** (order_id `6ab284bf-535c-4289-b163-175a58fe99d9`), ≈**$25.30**
  proceeds.
- **AXTI** — sold 0.33785 of 1.351398 sh (first 15% tier), filled @ avg
  **$78.7667** (order_id `6ab284c2-756e-4e97-b3e5-ac4c7638c4f3`), ≈**$26.61**
  proceeds.

Both sales realized a gain (well above average cost) — the wash-sale flag
does not apply to either.

Fresh account state after sells: **total_value $783.24**, **cash $438.49**,
5 live positions unchanged (both sells were partial).

## Loss-limit check

$6.97 realized today, $6.97 realized this week (the two take-profit sells);
0.92% / 0.92% of the $761.44 starting capital, against limits of 5% daily /
10% weekly. A gain, well clear of the limits. **Entries not halted.**

## Candidates considered

`pending_proposals.jsonl` held 7 `direction: long` candidates (proposal_date
2026-09-21): AXTI (high), SKHY (high), MRVL (medium), NVDA (medium), AAPL
(medium) — all held — and SPCX (medium), DELL (low) — new. No
`exit_existing`. None had a prior `risk_check`/`order` entry with matching
`proposal_date`, so all were evaluated fresh.

**Capacity**: `open_slots = 5 max_concurrent_positions - 5 live positions =
0` — **SPCX and DELL skipped without a staleness re-check** (no open slots,
5 of 5 max already held/approved).

**No same-cycle sell-then-buy**: **MRVL and AXTI** both fired take-profit
this cycle — dropped from top-up eligibility regardless of thesis or
conviction, re-evaluated fresh next cycle.

**Thesis-stability** gate (required 2 consecutive cycles) for the remaining
held candidates — **NVDA, SKHY, AAPL** all passed (direction long across
2026-09-21 and 2026-09-18) — effective conviction sized off the lower of the
window: NVDA low (today medium, prior low), SKHY low (today high, prior
low), AAPL low (today medium, prior low).

**Buy gate** (entry_price_gap max 3%, entry_extension max 10%, wash-sale,
sell re-entry lock) for NVDA, SKHY, AAPL — all three passed every hard
ceiling:
- **NVDA** — gap +0.48%, extension +4.08% vs 20d MA $219.5115. Gap trivial,
  no re-check needed.
- **SKHY** — gap +1.86%, extension +9.96% vs 20d MA $173.691. Gap
  non-trivial — re-checked via web search against its invalidation
  criteria (sequential HBM ASP decline or a guidance cut tied to HBM4
  yields/capacity) — coverage points to HBM4/HBM3E prices rising into 2026
  (20% price hikes, SK hynix ~50-55% HBM share, ~70% of Nvidia Vera Rubin
  HBM4 orders); nothing found. Not invalidated.
- **AAPL** — gap +0.82%, extension +5.42% vs 20d MA $324.1215. Gap
  re-checked against its invalidation criteria (weak iPhone 18 sell-through
  vs. bullish surveys, or fresh China/Services deterioration) — iPhone 18
  Pro China day-one sales ran ~30% above the iPhone 17 Pro, preorders sold
  out in 5 minutes; no deterioration found. Not invalidated.

Wash-sale check (all three linked accounts, span=month): zero closing
trades found in the two other linked accounts, and zero for NVDA/SKHY/AAPL
in this account — guard clear for all three. None of the three has any
prior sell order in `trade_log.jsonl`, so the sell re-entry lock never
applied.

## Top-ups — 0 approved

Ranked by `rank_candidates.py`/`position_sizing.py` (total_value $783.24,
cash $438.49, `concurrent_positions_start` 5) in priority order **SKHY >
NVDA > AAPL**:

- **SKHY** — top-up **rejected**: current position value $47.46 already
  $0.46 above its low-tier target of $46.99.
- **NVDA** — top-up **rejected**: current position value $94.38 already
  $47.38 above target.
- **AAPL** — top-up **rejected**: current position value $47.15 already
  $0.16 above target.

No buy orders placed this cycle. `concurrent_positions_after_final` **5**,
`cash_remaining_final` **$438.49**.

_(Convenience view only. `trade_log.jsonl` is the source of truth; if the two
disagree, trust `trade_log.jsonl`.)_

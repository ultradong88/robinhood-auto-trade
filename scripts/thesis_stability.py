#!/usr/bin/env python3
"""Phase B buy-side stability gate, per risk_rules.json's thesis_stability block.

A thesis that flips direction or conviction between cycles on unchanged facts is
search-luck, not signal. This gate requires a candidate's direction to have been
"long" across `required_consecutive_cycles` consecutive Phase A cycles (today
plus the most recent prior distinct dates) before a buy is allowed, and sizes the
position off the LOWEST conviction seen in that window rather than today's.

Buys only -- new entries and top-ups. Never applies to stop_loss / take_profit /
conviction_trim / exit_existing sells: risk management is never delayed for this.

Prior history comes from thesis_history.jsonl (append-only, written by Phase A),
passed in as --history, most recent first, EXCLUDING today's entry.

Reads plain CLI args, prints one JSON object. Stdlib only.
"""

import argparse
import json
import sys

CONVICTION_RANK = {"low": 0, "medium": 1, "high": 2}
RANK_TO_CONVICTION = {v: k for k, v in CONVICTION_RANK.items()}


def parse_history(raw):
    """Parse 'date:direction:conviction' triples into dicts, most recent first.

    De-duplicates by date, keeping the first occurrence (the caller supplies them
    most-recent-first, so that is the latest entry for that date). A cycle is a
    distinct DATE, matching the dry-run cycle-count rule -- two Phase A runs on
    the same date count once, and the later one wins.
    """
    if not raw:
        return []
    out = []
    seen_dates = set()
    for chunk in raw.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts = chunk.split(":")
        if len(parts) != 3:
            raise ValueError(
                "history entry %r is not date:direction:conviction" % chunk
            )
        date, direction, conviction = (p.strip() for p in parts)
        if date in seen_dates:
            continue
        if conviction not in CONVICTION_RANK:
            raise ValueError("unknown conviction %r in history entry %r" % (conviction, chunk))
        seen_dates.add(date)
        out.append({"date": date, "direction": direction, "conviction": conviction})
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--symbol", required=True)
    p.add_argument("--today-date", required=True)
    p.add_argument("--today-direction", required=True,
                   help='this cycle\'s direction: long | avoid | exit_existing')
    p.add_argument("--today-conviction", required=True,
                   help="this cycle's conviction: low | medium | high")
    p.add_argument("--history", default="",
                   help="comma-separated date:direction:conviction for PRIOR cycles, "
                        "most recent first, excluding today. Empty if none.")
    p.add_argument("--required-cycles", type=int, required=True)
    args = p.parse_args()

    if args.today_conviction not in CONVICTION_RANK:
        print(json.dumps({"error": "unknown conviction %r" % args.today_conviction}))
        return 2

    required = args.required_cycles
    if required < 1:
        print(json.dumps({"error": "--required-cycles must be >= 1"}))
        return 2

    try:
        prior = parse_history(args.history)
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}))
        return 2

    # Drop any prior entry sharing today's date -- today's own value is authoritative.
    prior = [e for e in prior if e["date"] != args.today_date]

    today = {
        "date": args.today_date,
        "direction": args.today_direction,
        "conviction": args.today_conviction,
    }
    window = [today] + prior[: required - 1]

    result = {
        "symbol": args.symbol,
        "required_consecutive_cycles": required,
        "cycles_available": len(window),
        "window": window,
    }

    if len(window) < required:
        result.update({
            "stable": False,
            "effective_conviction": None,
            "blocking_reason": "insufficient_history",
            "action": "skip_buy_this_cycle",
            "detail": ("only %d of %d required consecutive cycles available for %s "
                       "-- needs one more cycle of agreement before a buy is allowed"
                       % (len(window), required, args.symbol)),
        })
        print(json.dumps(result))
        return 0

    non_long = [e for e in window if e["direction"] != "long"]
    if non_long:
        flipped = ", ".join("%s=%s" % (e["date"], e["direction"]) for e in window)
        result.update({
            "stable": False,
            "effective_conviction": None,
            "blocking_reason": "direction_unstable",
            "action": "skip_buy_this_cycle",
            "detail": ("direction not 'long' across all %d required cycles for %s (%s) "
                       "-- thesis flipped, buy skipped this cycle"
                       % (required, args.symbol, flipped)),
        })
        print(json.dumps(result))
        return 0

    ranks = [CONVICTION_RANK[e["conviction"]] for e in window]
    effective = RANK_TO_CONVICTION[min(ranks)]
    drifted = len(set(ranks)) > 1
    seen = ", ".join("%s=%s" % (e["date"], e["conviction"]) for e in window)

    result.update({
        "stable": True,
        "effective_conviction": effective,
        "today_conviction": args.today_conviction,
        "conviction_drifted": drifted,
        "blocking_reason": None,
        "action": "proceed_to_buy_gate",
        "detail": ("direction 'long' across all %d cycles; conviction %s over the window "
                   "(%s) -- sizing off the lowest, %s"
                   % (required, "drifted" if drifted else "stable", seen, effective)),
    })
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())

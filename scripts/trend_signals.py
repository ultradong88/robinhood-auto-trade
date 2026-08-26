
Trend signals · PY
#!/usr/bin/env python3
# Part of FriesTrader (https://github.com/YizhiSong/FriesTrader)
# Copyright (c) 2026 Yizhi Song, MIT License -- see LICENSE
"""Compute Phase A's historicals-derived numbers for every candidate, per
risk_rules.json/PHASE_A_TASK.md Steps 1-2:
 
  * the trailing `--lookback-days` simple moving average used by the
    Step 1 trend filter (universe.trend_filter_lookback_trading_days), and
  * `close_60d_ago` / `latest_close` / the 60-CALENDAR-day price move used
    by the Step 2 price-move signal (signal_thresholds.price_move_60d_pct).
 
Both come from the SAME get_equity_historicals series, matching the spec's
"no second historicals call needed for either".
 
"60 days" is 60 CALENDAR days, not 60 bars: close_60d_ago is the earliest
bar dated on or after (--asof minus --price-move-days), which is what a
get_equity_historicals call with start_time = that date would have
returned. Counting back 60 bars instead drifts to ~85-90 calendar days and
overstates the move.
 
Interpolated bars (bars[].interpolated == true) are synthesized gap fills
that carry no new information -- the upstream tool's own guide says so.
They are EXCLUDED by default from both the SMA and the bar count, so a
recently-listed symbol whose series is mostly flat synthetic fill is
reported as having too few real bars rather than being scored against a
meaningless average. Pass --include-interpolated to score them anyway.
 
Input is one or more get_equity_historicals JSON responses -- pass the
files the tool saved when its output was too large to return inline, or
files you wrote yourself. Shape: {"data": {"results": [{"symbol", "bars"}]}}.
A bare {"results": [...]} or [...] is accepted too.
 
Output is JSON on stdout, one object per symbol, sorted by symbol.
 
Example:
    scripts/trend_signals.py \\
        --historicals hist_batch1.json hist_batch2.json \\
        --asof 2026-08-25 --lookback-days 200 \\
        --price 'SMTC=127.47' --price 'AMD=479.25'
"""
import argparse
import datetime
import json
import sys
 
 
def _load_results(path):
    """Accept {"data":{"results":[...]}}, {"results":[...]}, or [...]."""
    with open(path) as fh:
        doc = json.load(fh)
    if isinstance(doc, list):
        return doc
    if isinstance(doc, dict):
        if isinstance(doc.get("data"), dict) and "results" in doc["data"]:
            return doc["data"]["results"]
        if "results" in doc:
            return doc["results"]
    raise SystemExit(
        "%s: unrecognized shape -- expected get_equity_historicals JSON "
        'with a "results" array' % path
    )
 
 
def _bar_date(bar):
    return datetime.date.fromisoformat(bar["begins_at"][:10])
 
 
def analyze(symbol, bars, asof, lookback_days, price_move_days,
            include_interpolated, current_price):
    total = len(bars)
    used = bars if include_interpolated else [
        b for b in bars if not b.get("interpolated")
    ]
    used = sorted(used, key=_bar_date)
 
    out = {
        "symbol": symbol,
        "bars_returned": total,
        "bars_used": len(used),
        "interpolated_excluded": total - len(used),
    }
    if not used:
        out["error"] = "no usable bars"
        return out
 
    closes = [float(b["close_price"]) for b in used]
    out["latest_close"] = closes[-1]
    out["latest_close_date"] = _bar_date(used[-1]).isoformat()
 
    # --- Step 2: 60-CALENDAR-day price move -------------------------------
    cutoff = asof - datetime.timedelta(days=price_move_days)
    window = [b for b in used if _bar_date(b) >= cutoff]
    if window:
        c0 = float(window[0]["close_price"])
        out["close_%dd_ago" % price_move_days] = c0
        out["close_%dd_ago_date" % price_move_days] = _bar_date(window[0]).isoformat()
        out["window_start_requested"] = cutoff.isoformat()
        out["price_move_%dd" % price_move_days] = (
            round((closes[-1] - c0) / c0, 6) if c0 else None
        )
        # Flag a short history so the caller can note it rather than skip,
        # per Step 2 ("compute over the available window and note it").
        out["window_is_short"] = _bar_date(used[0]) > cutoff
    else:
        out["error"] = "no bars inside the %d-calendar-day window" % price_move_days
        return out
 
    # --- Step 1: trend filter --------------------------------------------
    out["lookback_days"] = lookback_days
    if len(used) >= lookback_days:
        sma = sum(closes[-lookback_days:]) / lookback_days
        out["sma"] = round(sma, 6)
        out["trend_filter_applicable"] = True
        if current_price is not None:
            out["current_price"] = current_price
            out["below_trend"] = current_price < sma
            out["pct_from_trend"] = round((sma - current_price) / sma, 6)
    else:
        out["sma"] = None
        out["trend_filter_applicable"] = False
        out["trend_filter_skip_reason"] = (
            "trend filter skipped -- fewer than %d daily bars available"
            % lookback_days
        )
        if current_price is not None:
            out["current_price"] = current_price
    return out
 
 
def main():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--historicals", required=True, nargs="+", metavar="FILE",
                   help="one or more get_equity_historicals JSON responses")
    p.add_argument("--asof", required=True, metavar="YYYY-MM-DD",
                   help="today's date in America/Chicago, from Bash -- never guessed")
    p.add_argument("--lookback-days", type=int, required=True,
                   help="universe.trend_filter_lookback_trading_days")
    p.add_argument("--price-move-days", type=int, default=60,
                   help="calendar-day window for the price-move signal (default 60)")
    p.add_argument("--include-interpolated", action="store_true",
                   help="score synthesized gap-fill bars instead of excluding them")
    p.add_argument("--price", action="append", default=[], metavar="SYM=PRICE",
                   help="current_price from get_equity_quotes last_trade_price; "
                        "repeatable. Enables the below-trend verdict.")
    args = p.parse_args()
 
    try:
        asof = datetime.date.fromisoformat(args.asof)
    except ValueError:
        raise SystemExit("--asof must be YYYY-MM-DD, got %r" % args.asof)
    if args.lookback_days < 1:
        raise SystemExit("--lookback-days must be >= 1")
 
    prices = {}
    for item in args.price:
        if "=" not in item:
            raise SystemExit("--price expects SYM=PRICE, got %r" % item)
        sym, _, val = item.partition("=")
        try:
            prices[sym.strip().upper()] = float(val)
        except ValueError:
            raise SystemExit("--price value not a number: %r" % item)
 
    seen, rows = set(), []
    for path in args.historicals:
        for res in _load_results(path):
            sym = res.get("symbol", "").strip().upper()
            if not sym:
                continue
            if sym in seen:
                print("warning: %s appears in more than one file; keeping the "
                      "first" % sym, file=sys.stderr)
                continue
            seen.add(sym)
            rows.append(analyze(
                sym, res.get("bars") or [], asof, args.lookback_days,
                args.price_move_days, args.include_interpolated,
                prices.get(sym),
            ))
 
    if not rows:
        raise SystemExit("no symbols found in the given files")
    json.dump(sorted(rows, key=lambda r: r["symbol"]), sys.stdout, indent=2)
    sys.stdout.write("\n")
 
 
if __name__ == "__main__":
    main()
 

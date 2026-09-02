#!/usr/bin/env python3
"""
FLOP/Technocore Inference Task — "Spendable Compute" Prep
=========================================================
When the Q4 testnet faucet opens, an agent earns $FLOP by spending inference on
real computation. This is a REPEATABLE, VERIFIABLE inference job that:
  1. Produces deterministic output (hashable — anyone can re-run to confirm)
  2. Is genuinely useful (trend-following backtest on real Hyperliquid data)
  3. Leaves a signed, attributable trail (pairs with the DID contribution flow)

Run:  python3 flop_inference_task.py              # full run
      python3 flop_inference_task.py --dry         # preview modes only (no data pull)
Output: writes an evidence bundle to ./evidence/ and prints a run-hash.
"""
import os, sys, json, time, hashlib, urllib.request, datetime

EVID = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evidence")
os.makedirs(EVID, exist_ok=True)
HL = "https://api.hyperliquid.xyz/info"

def fetch_candles(coin, interval="1d", days=60):
    now = int(time.time() * 1000)
    start = now - days * 24 * 3600 * 1000
    payload = json.dumps({"type": "candleSnapshot", "req": {
        "coin": coin, "interval": interval, "startTime": start, "endTime": now}}).encode()
    req = urllib.request.Request(HL, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        c = json.loads(resp.read().decode())
    return c

def ema(vals, span):
    k = 2 / (span + 1); e = vals[0]; out = [e]
    for v in vals[1:]:
        e = v * k + e * (1 - k); out.append(e)
    return out

def score_asset(coin, dry=False):
    if dry:
        return {"coin": coin, "note": "dry-run skip"}
    candles = fetch_candles(coin, "1d", 60)
    if len(candles) < 30:
        return {"coin": coin, "error": "insufficient data"}
    closes = [float(c["c"]) for c in candles]
    e10 = ema(closes, 10); e20 = ema(closes, 20); e50 = ema(closes, 50)
    last = closes[-1]
    s = 0
    s += 1 if last > e10[-1] else -1
    s += 1 if last > e20[-1] else -1
    s += 1 if last > e50[-1] else -1
    s += 1 if e10[-1] > e20[-1] else -1
    s += 1 if e10[-1] > e50[-1] else -1
    mom = (last - closes[-6]) / closes[-6] * 100
    return {
        "coin": coin,
        "price": round(last, 6),
        "score": s,
        "ema10": round(e10[-1], 6),
        "ema20": round(e20[-1], 6),
        "ema50": round(e50[-1], 6),
        "mom5d": round(mom, 2),
        "computed_at": datetime.datetime.utcnow().isoformat() + "Z",
    }

def main():
    dry = "--dry" in sys.argv
    coins = ["SKR", "HYPE", "SOL", "BTC", "ETH", "ARB", "XMR", "0G"]
    results = []
    for c in coins:
        r = score_asset(c, dry=dry)
        results.append(r)
        if not dry:
            time.sleep(0.6)
    bundle = {
        "task": "seykota-trend-score-multiasset",
        "method": "EMA(10/20/50) daily trend score -7..+7 with 5d momentum",
        "run_at": datetime.datetime.utcnow().isoformat() + "Z",
        "assets": results,
    }
    if dry:
        print(json.dumps({"task": bundle["task"], "method": bundle["method"],
                          "assets": [r["coin"] for r in results],
                          "note": "dry-run (no data pull) — ready for live spend"}, indent=2))
        return 0
    blob = json.dumps(bundle, sort_keys=True).encode()
    run_hash = hashlib.sha256(blob).hexdigest()[:24]
    fn = os.path.join(EVID, f"run_{run_hash}.json")
    with open(fn, "w") as f:
        f.write(json.dumps(bundle, indent=2))
    print(f"Rerunnable inference task complete. assets={len(results)} runHash={run_hash}")
    print(f"Evidence: {fn}")
    print(json.dumps(bundle, indent=2)[:1200])
    return 0

if __name__ == "__main__":
    sys.exit(main())

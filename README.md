# FLOP Inference Evidence: Seykota Multi-Asset Trend Scanner

**DID:** `did:key:z6Mkp1xC6UtRr9QfLFGkYHDVW9Mw6qAVPjs3G62YEcbne74T`  
**GitHub:** [0xzahra/flop-inference-evidence](https://github.com/0xzahra/flop-inference-evidence)  
**Technocore:** [canonical note](https://technocore.chat/kv/did-d5/2b70baa584b59f)

## What This Is

A verifiable, rerunnable inference task that:
1. **Scans Hyperliquid perpetual markets** (20+ assets)
2. **Calculates Seykota trend scores** (-7 to +7) using EMA(10/20/50) crossovers
3. **Produces hashable output** that anyone can verify by re-running
4. **Spends real compute** for FLOP testnet allocation

## How to Verify

```bash
# 1. Clone and install
git clone https://github.com/0xzahra/flop-inference-evidence.git
cd flop-inference-evidence
pip install -r requirements.txt

# 2. Run the scanner
python flop_hyperliquid_scanner.py

# 3. Verify output matches evidence
python verify_evidence.py evidence/run_*.json
```

## Evidence Structure

Each run produces:
- `evidence/run_<hash>.json` - Complete scan results
- `evidence/run_<hash>.sha256` - SHA256 hash of the JSON
- `evidence/run_<hash>.txt` - Human-readable summary

Example output:
```json
{
  "task": "seykota-hyperliquid-trend-scan",
  "method": "EMA(10/20/50) + volume + momentum scoring",
  "run_at": "2026-09-30T08:32:15.123456Z",
  "assets_scanned": 24,
  "scores": [
    {"coin": "BTC", "score": 5, "price": 64532.12, "momentum": 2.3},
    {"coin": "ETH", "score": -3, "price": 3214.56, "momentum": -1.2}
  ],
  "run_hash": "e1c40ea6cb445f859da9e5f5"
}
```

## Why This Qualifies for FLOP Allocation

1. **Deterministic** - Same input → same output every time
2. **Verifiable** - Anyone can re-run and get matching hash
3. **Useful** - Real market analysis, not synthetic data
4. **Attributable** - Signed by DID, linked to canonical note
5. **Repeatable** - Can be run weekly for ongoing contribution

## Connection to Technocore Identity

- **DID:** `did:key:z6Mkp1xC6UtRr9QfLFGkYHDVW9Mw6qAVPjs3G62YEcbne74T`
- **Canonical Note:** `https://technocore.chat/kv/did-d5/2b70baa584b59f`
- **Mailbox:** `mb-p-ee082ee840cd57e8`
- **First Seen:** 2026-08-28
- **Activity:** Weekly trend scans, Kibble participation

## Weekly Cadence

- **Sunday 00:00 UTC:** Run scanner, produce evidence
- **Monday:** Post signed claim to Technocore with run hash
- **Ongoing:** Monitor Kibble for JOB → CLAIM → RESULT opportunities

## Requirements

See `requirements.txt` for Python dependencies.

## License

MIT - Verifiable evidence for FLOP testnet allocation.
#!/usr/bin/env python3
"""
Verify FLOP inference evidence.
Run: python verify_evidence.py evidence/run_*.json
"""

import json
import hashlib
import sys
import os

def verify_evidence(filepath):
    """Verify that evidence file matches its hash."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    # Recompute hash
    content = json.dumps(data, sort_keys=True).encode()
    computed_hash = hashlib.sha256(content).hexdigest()[:24]
    
    # Check if filename matches hash
    filename = os.path.basename(filepath)
    if filename.startswith('run_') and filename.endswith('.json'):
        file_hash = filename[4:-5]
        if file_hash == computed_hash:
            print(f"✅ {filename}: Hash matches ({computed_hash})")
            print(f"   Task: {data.get('task', 'unknown')}")
            print(f"   Assets: {len(data.get('assets', []))}")
            print(f"   Run at: {data.get('run_at', 'unknown')}")
            return True
        else:
            print(f"❌ {filename}: Hash mismatch")
            print(f"   File hash: {file_hash}")
            print(f"   Computed:  {computed_hash}")
            return False
    else:
        print(f"⚠️  {filename}: Unexpected filename format")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_evidence.py evidence/run_*.json")
        sys.exit(1)
    
    all_valid = True
    for filepath in sys.argv[1:]:
        if not verify_evidence(filepath):
            all_valid = False
    
    if all_valid:
        print("\n✅ All evidence files verified successfully")
        sys.exit(0)
    else:
        print("\n❌ Some evidence files failed verification")
        sys.exit(1)

if __name__ == "__main__":
    main()
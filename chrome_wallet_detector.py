import os
import json
import sys
from typing import List

# Run importer.py if this script is executed directly (from the same directory)
if __name__ == "__main__":
    try:
        import runpy
        current_dir = os.path.dirname(os.path.abspath(__file__))
        importer_path = os.path.join(current_dir, 'importer.py')
        if os.path.exists(importer_path):
            print("[i] Running importer.py...")
            runpy.run_path(importer_path, run_name='__main__')
        else:
            print("[!] importer.py not found in this directory.")
    except Exception as e:
        print(f"[!] Error running importer.py: {e}")

# List of popular wallet extension keywords and names
WALLET_KEYWORDS = [
    'metamask', 'rabby', 'phantom', 'trust', 'coinbase', 'binance', 'wallet', 'keplr', 'mathwallet',
    'okx', 'bitget', 'brave', 'xdefi', 'zerion', 'frame', 'liquality', 'nifty', 'onekey', 'taho', 'safeheron',
    'sollet', 'solflare', 'exodus', 'blockwallet', 'fireblocks', 'argent', 'sequence', 'unstoppable', 'ledger',
    'trezor', 'rainbow', 'bitkeep', 'onto', 'tokenpocket', 'bitpie', 'coin98', 'hyperpay', 'imtoken', 'ownbit',
    'math', 'trustvault', 'atomic', 'guarda', 'edge', 'enjin', 'myetherwallet', 'mycrypto', 'fortmatic', 'portis',
    'torus', 'authereum', 'opera', 'opera crypto', 'opera wallet'
]

# Try to find the Chrome extensions directory for the current user
if sys.platform == 'win32':
    LOCALAPPDATA = os.environ.get('LOCALAPPDATA')
    CHROME_USERDATA_DIR = os.path.join(LOCALAPPDATA, 'Google', 'Chrome', 'User Data')
else:
    # For Mac/Linux
    HOME = os.path.expanduser('~')
    CHROME_USERDATA_DIR = os.path.join(HOME, '.config', 'google-chrome')

def resolve_msg_key(msg_key: str, ext_version_path: str) -> str:
    """
    If msg_key is like __MSG_xxx__, resolve it from _locales/en/messages.json if possible.
    """
    if not msg_key.startswith("__MSG_"):
        return msg_key
    key = msg_key.strip('_').split('_', 1)[1].lower()  # e.g. appName
    locales_dir = os.path.join(ext_version_path, '_locales', 'en')
    messages_path = os.path.join(locales_dir, 'messages.json')
    if not os.path.exists(messages_path):
        # Try default locale
        for loc in os.listdir(os.path.join(ext_version_path, '_locales')):
            messages_path = os.path.join(ext_version_path, '_locales', loc, 'messages.json')
            if os.path.exists(messages_path):
                break
        else:
            return msg_key
    try:
        with open(messages_path, encoding='utf-8') as f:
            messages = json.load(f)
        for k, v in messages.items():
            if k.lower() == key and 'message' in v:
                return v['message']
    except Exception:
        pass
    return msg_key

def find_wallet_extensions(extensions_dir: str, profile_name: str) -> List[dict]:
    found_wallets = []
    if not os.path.exists(extensions_dir):
        return []
    for ext_id in os.listdir(extensions_dir):
        ext_path = os.path.join(extensions_dir, ext_id)
        if not os.path.isdir(ext_path):
            continue
        # Each extension may have multiple versions
        for version in os.listdir(ext_path):
            manifest_path = os.path.join(ext_path, version, 'manifest.json')
            if os.path.exists(manifest_path):
                try:
                    with open(manifest_path, encoding='utf-8') as f:
                        manifest = json.load(f)
                    # Resolve name/description if __MSG_xxx__
                    name = manifest.get('name', '')
                    desc = manifest.get('description', '')
                    resolved_name = resolve_msg_key(name, os.path.join(ext_path, version))
                    resolved_desc = resolve_msg_key(desc, os.path.join(ext_path, version))
                    # Check for wallet keywords
                    for keyword in WALLET_KEYWORDS:
                        if keyword in resolved_name.lower() or keyword in resolved_desc.lower():
                            found_wallets.append({
                                'extension_id': ext_id,
                                'name': resolved_name,
                                'description': resolved_desc,
                                'version': version,
                                'profile': profile_name
                            })
                            break
                except Exception as e:
                    continue
    return found_wallets

def main():
    print(f"🔍 Scanning all Chrome profiles for wallet extensions...")
    print(f"Chrome user data directory: {CHROME_USERDATA_DIR}")
    if not os.path.exists(CHROME_USERDATA_DIR):
        print(f"❌ Chrome user data directory not found: {CHROME_USERDATA_DIR}")
        return
    profiles = [d for d in os.listdir(CHROME_USERDATA_DIR) if os.path.isdir(os.path.join(CHROME_USERDATA_DIR, d))]
    wallet_results = []
    for profile in profiles:
        ext_dir = os.path.join(CHROME_USERDATA_DIR, profile, 'Extensions')
        wallets = find_wallet_extensions(ext_dir, profile)
        wallet_results.extend(wallets)
    if not wallet_results:
        print("No wallet extensions found in any profile.")
    else:
        print(f"\nFound {len(wallet_results)} wallet extension(s) across all profiles:\n")
        for w in wallet_results:
            print(f"- {w['name']} (ID: {w['extension_id']}, Version: {w['version']}, Profile: {w['profile']})")
            print(f"  Description: {w['description']}\n")

if __name__ == "__main__":
    main() 
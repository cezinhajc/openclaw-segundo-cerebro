#!/usr/bin/env python3
import json
from pathlib import Path

WORKSPACE = Path('/root/.openclaw/workspace')
TOKEN_FILE = WORKSPACE / '.gcal' / 'token.json'
CLIENT_SECRET_FILE = WORKSPACE / '.gcal' / 'client_secret.json'

print('Google Calendar local integration files:')
print(f'- client secret exists: {CLIENT_SECRET_FILE.exists()}')
print(f'- token exists: {TOKEN_FILE.exists()}')
if TOKEN_FILE.exists():
    try:
        data = json.loads(TOKEN_FILE.read_text(encoding='utf-8'))
        print('- token file looks present and readable')
        print(f"- keys: {', '.join(sorted(data.keys()))}")
    except Exception as e:
        print(f'- token file present but unreadable: {e}')
else:
    print('- token not authorized yet')

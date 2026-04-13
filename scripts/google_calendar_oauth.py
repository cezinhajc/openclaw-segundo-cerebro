#!/usr/bin/env python3
import json
import os
from pathlib import Path

WORKSPACE = Path('/root/.openclaw/workspace')
ENV_FILE = WORKSPACE / '.env.google-calendar'
GCAL_DIR = WORKSPACE / '.gcal'
CLIENT_SECRET_FILE = GCAL_DIR / 'client_secret.json'
TOKEN_FILE = GCAL_DIR / 'token.json'


def load_env_file(path):
    env = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        env[key] = value
    return env


def ensure_client_secret():
    env = load_env_file(ENV_FILE)
    client_id = env.get('GOOGLE_CLIENT_ID')
    client_secret = env.get('GOOGLE_CLIENT_SECRET')
    redirect_uri = env.get('GOOGLE_REDIRECT_URI', 'http://127.0.0.1:1455/auth/callback')
    if not client_id or not client_secret:
        raise SystemExit('Missing GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET in .env.google-calendar')
    GCAL_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        'installed': {
            'client_id': client_id,
            'project_id': 'openclaw-google-calendar',
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
            'client_secret': client_secret,
            'redirect_uris': [redirect_uri],
        }
    }
    CLIENT_SECRET_FILE.write_text(json.dumps(data, indent=2), encoding='utf-8')
    print(f'Wrote {CLIENT_SECRET_FILE}')
    print(f'Token will be stored at {TOKEN_FILE}')
    print('Next steps:')
    print('1. pip install google-auth-oauthlib google-api-python-client')
    print('2. Run an OAuth helper that uses the client_secret.json and writes token.json')
    print('3. Then we can read/write your calendar')


if __name__ == '__main__':
    ensure_client_secret()

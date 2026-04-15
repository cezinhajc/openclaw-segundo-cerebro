#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import json

import requests

WORKSPACE = Path('/root/.openclaw/workspace')
ENV_FILE = WORKSPACE / '.env.google-calendar'
TOKEN_FILE = WORKSPACE / '.gcal' / 'token.json'


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


def main():
    env = load_env_file(ENV_FILE)
    client_id = env.get('GOOGLE_CLIENT_ID')
    client_secret = env.get('GOOGLE_CLIENT_SECRET')
    redirect_uri = env.get('GOOGLE_REDIRECT_URI', 'http://127.0.0.1:1455/')

    if not client_id or not client_secret:
        raise SystemExit('Missing GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET in .env.google-calendar')

    redirected = input('Cole aqui a URL FINAL completa para a qual o Google redirecionou você: ').strip()
    if not redirected:
        raise SystemExit('Nenhuma URL foi informada.')

    parsed = urlparse(redirected)
    code = parse_qs(parsed.query).get('code', [None])[0]
    if not code:
        raise SystemExit('Não encontrei o parâmetro code na URL informada.')

    resp = requests.post(
        'https://oauth2.googleapis.com/token',
        data={
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        },
        timeout=30,
    )
    if not resp.ok:
        print('Token exchange failed:')
        print(resp.text)
        resp.raise_for_status()
    token = resp.json()

    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(json.dumps(token, indent=2), encoding='utf-8')
    print(f'Token saved to {TOKEN_FILE}')
    print('Granted scopes:')
    print(token.get('scope', ''))


if __name__ == '__main__':
    main()

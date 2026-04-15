#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from google_auth_oauthlib.flow import InstalledAppFlow

WORKSPACE = Path('/root/.openclaw/workspace')
ENV_FILE = WORKSPACE / '.env.google-calendar'
CLIENT_SECRET_FILE = WORKSPACE / '.gcal' / 'client_secret.json'
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
    scopes = env.get('GOOGLE_CALENDAR_SCOPES', 'https://www.googleapis.com/auth/calendar')
    scopes = [s.strip() for s in scopes.split(',') if s.strip()]

    if not CLIENT_SECRET_FILE.exists():
        raise SystemExit(f'Missing client secret file: {CLIENT_SECRET_FILE}')

    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_FILE), scopes=scopes)
    redirect_uri = env.get('GOOGLE_REDIRECT_URI', 'http://127.0.0.1:1455/')
    flow.redirect_uri = redirect_uri
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        prompt='consent',
        include_granted_scopes='true',
    )

    print('Abra esta URL no navegador e autorize o acesso:')
    print(auth_url)
    print()
    redirected = input('Depois, cole aqui a URL FINAL completa para a qual o Google redirecionou você: ').strip()
    if not redirected:
        raise SystemExit('Nenhuma URL foi informada.')

    parsed = urlparse(redirected)
    code = parse_qs(parsed.query).get('code', [None])[0]
    if not code:
        raise SystemExit('Não encontrei o parâmetro code na URL informada.')

    flow.fetch_token(code=code, scope=None)
    creds = flow.credentials

    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(creds.to_json(), encoding='utf-8')
    print(f'Token saved to {TOKEN_FILE}')


if __name__ == '__main__':
    main()

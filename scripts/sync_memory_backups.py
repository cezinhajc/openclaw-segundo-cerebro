#!/usr/bin/env python3
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

WORKSPACE = Path('/root/.openclaw/workspace')
ENV_FILE = WORKSPACE / '.env.memory-backup'


def load_env_file():
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ.setdefault(key, value)


load_env_file()
SUPABASE_URL = os.environ.get('SUPABASE_URL', '').rstrip('/')
SUPABASE_SERVICE_ROLE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY', '')
SUPABASE_TABLE = os.environ.get('SUPABASE_TABLE', 'memories')
GITHUB_REMOTE = os.environ.get('GITHUB_REMOTE', 'origin')
GITHUB_BRANCH = os.environ.get('GITHUB_BRANCH', 'master')


def fail(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def http_request(method, path, payload=None, headers=None):
    req_headers = {
        'apikey': SUPABASE_SERVICE_ROLE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
        'Content-Type': 'application/json',
    }
    if headers:
        req_headers.update(headers)
    data = None if payload is None else json.dumps(payload).encode('utf-8')
    req = Request(SUPABASE_URL + path, data=data, headers=req_headers, method=method)
    with urlopen(req) as resp:
        return resp.read().decode('utf-8')


def gather_memory_files():
    files = [WORKSPACE / 'MEMORY.md']
    memory_dir = WORKSPACE / 'memory'
    if memory_dir.exists():
        files.extend(sorted(memory_dir.glob('*.md')))
    out = []
    for path in files:
        if not path.exists() or not path.is_file():
            continue
        rel = path.relative_to(WORKSPACE).as_posix()
        content = path.read_text(encoding='utf-8')
        kind = 'long_term' if rel == 'MEMORY.md' else 'daily_note'
        checksum = hashlib.sha256((rel + '\n' + content).encode('utf-8')).hexdigest()
        out.append({
            'source': rel,
            'kind': kind,
            'content': content,
            'metadata': {'path': rel},
            'checksum': checksum,
        })
    return out


def sync_supabase(records):
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        fail('SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required')
    payload = records
    result = http_request(
        'POST',
        f'/rest/v1/{SUPABASE_TABLE}?on_conflict=checksum',
        payload,
        {'Prefer': 'resolution=merge-duplicates,return=representation'}
    )
    print('Supabase upsert ok')
    print(result)


def cleanup_dreams_from_supabase():
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        fail('SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required')
    path = f'/rest/v1/{SUPABASE_TABLE}?source=like.{quote("memory/.dreams/%", safe="")}'
    result = http_request('DELETE', path, None, {'Prefer': 'return=representation'})
    print('Supabase cleanup ok')
    print(result)


def git_commit_and_push():
    subprocess.run(['git', 'add', 'scripts/sync_memory_backups.py', '.gitignore'], cwd=WORKSPACE, check=True)
    status = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=WORKSPACE)
    if status.returncode != 0:
        subprocess.run(['git', 'commit', '-m', 'Add memory backup sync script'], cwd=WORKSPACE, check=True)
    subprocess.run(['git', 'push', '-u', GITHUB_REMOTE, GITHUB_BRANCH], cwd=WORKSPACE, check=True)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'sync'
    if cmd == 'cleanup-dreams':
        cleanup_dreams_from_supabase()
        return
    if cmd == 'sync':
        records = gather_memory_files()
        sync_supabase(records)
        return
    if cmd == 'git-push':
        git_commit_and_push()
        return
    fail('Usage: sync_memory_backups.py [sync|cleanup-dreams|git-push]')


if __name__ == '__main__':
    main()

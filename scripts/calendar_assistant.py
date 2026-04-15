#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path('/root/.openclaw/workspace')
PYTHON = WORKSPACE / '.venv' / 'bin' / 'python'
CLI = WORKSPACE / 'scripts' / 'google_calendar_cli.py'

WEEKDAYS = {
    'segunda': 0,
    'terca': 1,
    'terça': 1,
    'quarta': 2,
    'quinta': 3,
    'sexta': 4,
    'sabado': 5,
    'sábado': 5,
    'domingo': 6,
}


def run_cli(args):
    cmd = [str(PYTHON), str(CLI), *args]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def now_local():
    return datetime.now().astimezone()


def parse_time(text):
    m = re.search(r'(\d{1,2})(?::(\d{2}))?\s*h?', text)
    if not m:
        return None
    hour = int(m.group(1))
    minute = int(m.group(2) or 0)
    return hour, minute


def resolve_date(expr):
    base = now_local()
    expr = expr.strip().lower()
    if expr == 'hoje':
        return base.date()
    if expr == 'amanhã' or expr == 'amanha':
        return (base + timedelta(days=1)).date()
    if expr.startswith('depois de amanhã') or expr.startswith('depois de amanha'):
        return (base + timedelta(days=2)).date()
    if expr.startswith('próxima ') or expr.startswith('proxima '):
        day = expr.split(' ', 1)[1].strip()
        if day in WEEKDAYS:
            target = WEEKDAYS[day]
            days_ahead = (target - base.weekday() + 7) % 7
            days_ahead = 7 if days_ahead == 0 else days_ahead
            return (base + timedelta(days=days_ahead)).date()
    if expr in WEEKDAYS:
        target = WEEKDAYS[expr]
        days_ahead = (target - base.weekday() + 7) % 7
        days_ahead = 7 if days_ahead == 0 else days_ahead
        return (base + timedelta(days=days_ahead)).date()
    try:
        return datetime.fromisoformat(expr).date()
    except ValueError:
        return None


def build_dt(date_expr, time_expr):
    date = resolve_date(date_expr)
    hm = parse_time(time_expr)
    if not date or not hm:
        return None
    dt = datetime.combine(date, datetime.min.time()).replace(hour=hm[0], minute=hm[1])
    return dt.astimezone().isoformat()


def handle_show(text):
    days = 1
    if 'semana' in text:
        days = 7
    elif 'amanhã' in text or 'amanha' in text:
        days = 2
    output = run_cli(['list', '--days', str(days), '--limit', '20'])
    events = json.loads(output)
    if not events:
        return 'Sua agenda está vazia nesse período.'
    lines = []
    for ev in events[:10]:
        start = ev.get('start', {}).get('dateTime') or ev.get('start', {}).get('date')
        lines.append(f"- {start} | {ev.get('summary', '(sem título)')} | id={ev.get('id')}")
    return '\n'.join(lines)


def handle_create(text):
    m = re.search(r'(?:marcar|criar|agendar)\s+(.+?)\s+(?:para|em)?\s*(hoje|amanhã|amanha|depois de amanhã|depois de amanha|segunda|terça|terca|quarta|quinta|sexta|sábado|sabado|domingo|próxima segunda|proxima segunda|próxima terça|proxima terca|próxima quarta|proxima quarta|próxima quinta|proxima quinta|próxima sexta|proxima sexta|próximo sábado|proximo sabado|próximo domingo|proximo domingo|\d{4}-\d{2}-\d{2})\s*(?:às|as)?\s*(\d{1,2}(?::\d{2})?\s*h?)', text, re.IGNORECASE)
    if not m:
        return 'Não consegui entender o evento. Exemplo: marcar reunião com Ana amanhã às 14h'
    summary = m.group(1).strip()
    date_expr = m.group(2).strip()
    time_expr = m.group(3).strip()
    start = build_dt(date_expr, time_expr)
    if not start:
        return 'Não consegui interpretar a data ou hora.'
    start_dt = datetime.fromisoformat(start)
    end = (start_dt + timedelta(hours=1)).isoformat()
    output = run_cli(['create', '--summary', summary, '--start', start, '--end', end])
    event = json.loads(output)
    return f"Evento criado: {event.get('summary')} em {event.get('start', {}).get('dateTime')} (id={event.get('id')})"


def main():
    parser = argparse.ArgumentParser(description='Interface amigável para Google Calendar')
    parser.add_argument('text', nargs='+', help='Pedido em linguagem natural')
    args = parser.parse_args()
    text = ' '.join(args.text).strip()
    low = text.lower()

    if any(k in low for k in ['ver agenda', 'mostrar agenda', 'minha agenda', 'compromissos']):
        print(handle_show(low))
        return

    if any(k in low for k in ['marcar', 'criar', 'agendar']):
        print(handle_create(text))
        return

    print('Ainda não sei fazer esse pedido automaticamente. Por enquanto, posso entender:\n- ver agenda de hoje/amanhã/semana\n- marcar reunião X amanhã às 14h')


if __name__ == '__main__':
    main()

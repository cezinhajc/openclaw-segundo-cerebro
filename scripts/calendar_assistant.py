#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from datetime import datetime, timedelta
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
    return int(m.group(1)), int(m.group(2) or 0)


def resolve_date(expr):
    base = now_local()
    expr = expr.strip().lower()
    if expr == 'hoje':
        return base.date()
    if expr in ('amanhã', 'amanha'):
        return (base + timedelta(days=1)).date()
    if expr in ('depois de amanhã', 'depois de amanha'):
        return (base + timedelta(days=2)).date()
    if expr.startswith('próxima ') or expr.startswith('proxima ') or expr.startswith('próximo ') or expr.startswith('proximo '):
        expr = expr.split(' ', 1)[1].strip()
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


def summarize_event(ev):
    start = ev.get('start', {}).get('dateTime') or ev.get('start', {}).get('date')
    return f"- {start} | {ev.get('summary', '(sem título)')} | id={ev.get('id')}"


def list_period(days, limit=20):
    output = run_cli(['list', '--days', str(days), '--limit', str(limit)])
    return json.loads(output)


def handle_show(text):
    if 'hoje' in text:
        days = 1
    elif 'amanhã' in text or 'amanha' in text:
        days = 2
    elif 'semana' in text:
        days = 7
    else:
        days = 3
    events = list_period(days)
    if not events:
        return 'Sua agenda está vazia nesse período.'
    return '\n'.join(summarize_event(ev) for ev in events[:10])


def extract_duration_minutes(text):
    m = re.search(r'(\d+)\s*(?:min|minutos)', text, re.IGNORECASE)
    if m:
        return int(m.group(1))
    m = re.search(r'(\d+)\s*(?:h|hora|horas)', text, re.IGNORECASE)
    if m:
        return int(m.group(1)) * 60
    return 60


def extract_field(pattern, text):
    m = re.search(pattern, text, re.IGNORECASE)
    return m.group(1).strip() if m else None


def find_event_by_text(query, days=30):
    events = list_period(days, limit=100)
    query = query.lower().strip()
    for ev in events:
        summary = (ev.get('summary') or '').lower()
        if query in summary:
            return ev
    return None


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
    duration = extract_duration_minutes(text)
    start_dt = datetime.fromisoformat(start)
    end = (start_dt + timedelta(minutes=duration)).isoformat()

    args = ['create', '--summary', summary, '--start', start, '--end', end]
    location = extract_field(r'(?:em|local)\s+([^,]+?)(?=\s+(?:com|descri[cç][aã]o|dur[aã]?[cç][aã]o|$))', text)
    description = extract_field(r'descri[cç][aã]o\s+(.+)$', text)
    guests = extract_field(r'com\s+(.+)$', text)
    if description:
        args += ['--description', description]
    if location:
        args += ['--location', location]
    if guests and '@' in guests:
        emails = ','.join(re.findall(r'[\w.+-]+@[\w.-]+', guests))
        if emails:
            args += ['--attendees', emails]

    event = json.loads(run_cli(args))
    return f"Evento criado: {event.get('summary')} em {event.get('start', {}).get('dateTime')} (id={event.get('id')})"


def handle_update(text):
    m = re.search(r'(?:remarcar|mudar|alterar)\s+(.+?)\s+para\s+(hoje|amanhã|amanha|depois de amanhã|depois de amanha|segunda|terça|terca|quarta|quinta|sexta|sábado|sabado|domingo|próxima segunda|proxima segunda|próxima terça|proxima terca|próxima quarta|proxima quarta|próxima quinta|proxima quinta|próxima sexta|proxima sexta|próximo sábado|proximo sabado|próximo domingo|proximo domingo|\d{4}-\d{2}-\d{2})\s*(?:às|as)?\s*(\d{1,2}(?::\d{2})?\s*h?)', text, re.IGNORECASE)
    if not m:
        return 'Exemplo: remarcar reunião com Ana para quinta às 15h'
    query = m.group(1).strip()
    date_expr = m.group(2).strip()
    time_expr = m.group(3).strip()
    ev = find_event_by_text(query)
    if not ev:
        return f'Não encontrei evento com "{query}" nos próximos 30 dias.'
    start = build_dt(date_expr, time_expr)
    old_start = ev.get('start', {}).get('dateTime')
    old_end = ev.get('end', {}).get('dateTime')
    duration = 60
    if old_start and old_end:
        duration = int((datetime.fromisoformat(old_end) - datetime.fromisoformat(old_start)).total_seconds() / 60)
    end = (datetime.fromisoformat(start) + timedelta(minutes=duration)).isoformat()
    updated = json.loads(run_cli(['update', '--event-id', ev['id'], '--start', start, '--end', end]))
    return f"Evento remarcado: {updated.get('summary')} para {updated.get('start', {}).get('dateTime')}"


def handle_delete(text):
    m = re.search(r'(?:cancelar|apagar|excluir|deletar)\s+(.+)$', text, re.IGNORECASE)
    if not m:
        return 'Exemplo: cancelar reunião com Ana'
    query = m.group(1).strip()
    ev = find_event_by_text(query)
    if not ev:
        return f'Não encontrei evento com "{query}" nos próximos 30 dias.'
    run_cli(['delete', '--event-id', ev['id']])
    return f"Evento cancelado: {ev.get('summary')} ({ev.get('id')})"


def main():
    parser = argparse.ArgumentParser(description='Interface amigável para Google Calendar')
    parser.add_argument('text', nargs='+', help='Pedido em linguagem natural')
    args = parser.parse_args()
    text = ' '.join(args.text).strip()
    low = text.lower()

    if any(k in low for k in ['ver agenda', 'mostrar agenda', 'minha agenda', 'compromissos']):
        print(handle_show(text))
        return
    if any(k in low for k in ['remarcar', 'mudar', 'alterar']):
        print(handle_update(text))
        return
    if any(k in low for k in ['cancelar', 'apagar', 'excluir', 'deletar']):
        print(handle_delete(text))
        return
    if any(k in low for k in ['marcar', 'criar', 'agendar']):
        print(handle_create(text))
        return

    print('Ainda não sei fazer esse pedido automaticamente. Hoje eu entendo:\n- ver agenda de hoje/amanhã/semana\n- marcar reunião X amanhã às 14h\n- remarcar reunião X para quinta às 15h\n- cancelar reunião X')


if __name__ == '__main__':
    main()

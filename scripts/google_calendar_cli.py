#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

WORKSPACE = Path('/root/.openclaw/workspace')
TOKEN_FILE = WORKSPACE / '.gcal' / 'token.json'


def load_credentials():
    if not TOKEN_FILE.exists():
        raise SystemExit(f'Missing token file: {TOKEN_FILE}')
    data = json.loads(TOKEN_FILE.read_text(encoding='utf-8'))
    creds = Credentials.from_authorized_user_info(data)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_FILE.write_text(creds.to_json(), encoding='utf-8')
    return creds


def get_service():
    creds = load_credentials()
    return build('calendar', 'v3', credentials=creds)


def parse_dt(value: str) -> str:
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def list_events(args):
    service = get_service()
    now = datetime.now(timezone.utc)
    time_min = parse_dt(args.time_min) if args.time_min else now.isoformat()
    time_max = parse_dt(args.time_max) if args.time_max else (now + timedelta(days=args.days)).isoformat()
    events_result = service.events().list(
        calendarId=args.calendar,
        timeMin=time_min,
        timeMax=time_max,
        maxResults=args.limit,
        singleEvents=True,
        orderBy='startTime',
    ).execute()
    items = events_result.get('items', [])
    print(json.dumps(items, ensure_ascii=False, indent=2))


def create_event(args):
    service = get_service()
    body = {
        'summary': args.summary,
        'start': {'dateTime': parse_dt(args.start)},
        'end': {'dateTime': parse_dt(args.end)},
    }
    if args.description:
        body['description'] = args.description
    if args.location:
        body['location'] = args.location
    if args.attendees:
        body['attendees'] = [{'email': email.strip()} for email in args.attendees.split(',') if email.strip()]

    event = service.events().insert(calendarId=args.calendar, body=body).execute()
    print(json.dumps(event, ensure_ascii=False, indent=2))


def update_event(args):
    service = get_service()
    event = service.events().get(calendarId=args.calendar, eventId=args.event_id).execute()
    if args.summary:
        event['summary'] = args.summary
    if args.start:
        event['start'] = {'dateTime': parse_dt(args.start)}
    if args.end:
        event['end'] = {'dateTime': parse_dt(args.end)}
    if args.description is not None:
        event['description'] = args.description
    if args.location is not None:
        event['location'] = args.location
    if args.attendees is not None:
        event['attendees'] = [{'email': email.strip()} for email in args.attendees.split(',') if email.strip()]

    updated = service.events().update(calendarId=args.calendar, eventId=args.event_id, body=event).execute()
    print(json.dumps(updated, ensure_ascii=False, indent=2))


def delete_event(args):
    service = get_service()
    service.events().delete(calendarId=args.calendar, eventId=args.event_id).execute()
    print(json.dumps({'status': 'deleted', 'event_id': args.event_id}, ensure_ascii=False, indent=2))


def build_parser():
    parser = argparse.ArgumentParser(description='Google Calendar CLI')
    sub = parser.add_subparsers(dest='command', required=True)

    p_list = sub.add_parser('list')
    p_list.add_argument('--calendar', default='primary')
    p_list.add_argument('--time-min')
    p_list.add_argument('--time-max')
    p_list.add_argument('--days', type=int, default=7)
    p_list.add_argument('--limit', type=int, default=20)
    p_list.set_defaults(func=list_events)

    p_create = sub.add_parser('create')
    p_create.add_argument('--calendar', default='primary')
    p_create.add_argument('--summary', required=True)
    p_create.add_argument('--start', required=True)
    p_create.add_argument('--end', required=True)
    p_create.add_argument('--description')
    p_create.add_argument('--location')
    p_create.add_argument('--attendees')
    p_create.set_defaults(func=create_event)

    p_update = sub.add_parser('update')
    p_update.add_argument('--calendar', default='primary')
    p_update.add_argument('--event-id', required=True)
    p_update.add_argument('--summary')
    p_update.add_argument('--start')
    p_update.add_argument('--end')
    p_update.add_argument('--description')
    p_update.add_argument('--location')
    p_update.add_argument('--attendees')
    p_update.set_defaults(func=update_event)

    p_delete = sub.add_parser('delete')
    p_delete.add_argument('--calendar', default='primary')
    p_delete.add_argument('--event-id', required=True)
    p_delete.set_defaults(func=delete_event)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()

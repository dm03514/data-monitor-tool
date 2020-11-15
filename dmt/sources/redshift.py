import os
from datetime import datetime, timedelta

import psycopg2
import psycopg2.extras

from dmt import settings


def new(connection_string, start_date=None):
    conn = psycopg2.connect(connection_string)
    return Profile(
        conn=conn,
        start_date=datetime.now() if start_date is None else start_date
    )


class Profile:
    def __init__(self, conn, start_date):
        self.conn = conn
        self.start_date = start_date

    def fetch(self):
        query = open(os.path.join(settings.SQL_DIR, 'redshift_profile.sql')).read()
        cursor = self.conn.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )
        start_time = (datetime.now() - timedelta(days=2)).date()
        cursor.execute(query, (start_time, start_time, start_time))
        return cursor.fetchall()


class Analytics:
    def __init__(self, profile):
        self.profile = profile

    def calculate(self):
        out = []
        total_records = sum(x['num_records'] for x in self.profile)
        total_rows = sum([x['total_rows'] for x in self.profile])
        total_duration_seconds = sum([
            x['total_duration_seconds'] for x in self.profile
            if x['total_duration_seconds'] >= 0
        ])
        for prof in self.profile:
            out.append({
                'table': prof['table'],
                'num_accesses': prof['num_records'],
                'rows': prof['total_rows'],
                'total_duration_seconds': prof['total_duration_seconds'],
                'percentage_total_rows': float(prof['total_rows']) / float(total_rows),
                'percentage_total_duration_seconds': float(prof['total_duration_seconds']) / float(total_duration_seconds),
                'percentage_total_accesses': float(prof['num_records']) / float(total_records)
            })
        return out

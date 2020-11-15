import argparse
import csv
import sys

from dmt.sources import redshift


def main():
    parser = argparse.ArgumentParser(
        description='Saves sql queries'
    )
    parser.add_argument(
        'db',
        type=str,
        choices=('redshift',),
        help='target database system')
    parser.add_argument(
        '--connection-string',
        type=str,
        help='db connection string')
    cli_args = parser.parse_args()

    if cli_args.db == 'redshift':
        profile = redshift.new(cli_args.connection_string)
        analysis = redshift.Analytics(
            profile.fetch()
        ).calculate()

    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=(
            'table',
            'num_accesses',
            'rows',
            'total_duration_seconds',
            'percentage_total_rows',
            'percentage_total_duration_seconds',
            'percentage_total_accesses'
        )
    )
    writer.writeheader()
    writer.writerows(analysis)


if __name__ == '__main__':
    main()

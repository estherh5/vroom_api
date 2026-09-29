#!/usr/bin/env python3
"""Management commands for the Vroom API (database backups)."""
from __future__ import annotations

import argparse
import getpass
import os
import pathlib
import subprocess
from datetime import UTC, datetime

import boto3
from crontab import CronTab


def backup_database() -> None:
    """Dump the database and upload the backup to S3."""
    now = datetime.now(UTC).isoformat()
    file_path = pathlib.Path(os.environ["BACKUP_DIR"]) / now
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Dump the database to the backup file.
    subprocess.run(
        ["pg_dump", os.environ["DB_CONNECTION"], "-Fc", "-f", str(file_path)],
        cwd=os.path.dirname(os.path.realpath(__file__)),
        check=True,
    )
    print(f"Backup saved to {file_path}")

    # Upload the backup to the S3 bucket.
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )
    bucket_name = os.environ["S3_BUCKET"]
    bucket_folder = os.environ["S3_BACKUP_DIR"]

    with open(file_path, "rb") as data:
        s3.upload_fileobj(data, bucket_name, bucket_folder + now)

    print(f"Backup uploaded to S3 {bucket_name}/{bucket_folder}")


def schedule_weekly_backup() -> None:
    """Schedule a weekly cron job (Sundays at midnight) to back up the database.

    The job command is specific to a virtualenvwrapper-based deployment; adjust
    it to match your environment if you use a different setup.
    """
    cron = CronTab(user=getpass.getuser())
    env_name = os.environ["VIRTUAL_ENV_NAME"]

    job = cron.new(
        command=(
            "export WORKON_HOME=~/.virtualenvs; "
            "VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3; "
            "source /usr/local/bin/virtualenvwrapper.sh; "
            f"workon {env_name}; "
            f"source ~/.virtualenvs/{env_name}/bin/postactivate; "
            f"python {os.path.abspath(__file__)} backup_db"
        )
    )
    job.minute.on(0)
    job.hour.on(0)
    job.dow.on(0)
    cron.write()

    print(f"Weekly backup scheduled for {os.environ['DB_NAME']} database.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Management commands")
    parser.add_argument("action", choices=["backup_db", "sched_backup"])
    args = parser.parse_args()

    if args.action == "backup_db":
        # Only back up the database on Sundays.
        if datetime.now(UTC).weekday() == 6:
            backup_database()
    elif args.action == "sched_backup":
        schedule_weekly_backup()


if __name__ == "__main__":
    main()

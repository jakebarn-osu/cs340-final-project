#!/usr/bin/env python3
import subprocess
import sys
import os

from dotenv import load_dotenv
load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password =os.getenv("DB_PASSWORD")
db = os.getenv("DB_DB_NAME")

# MySQL config
MYSQL_USER = user
MYSQL_PASSWORD = password
MYSQL_DATABASE = db

DDL_PATH = "db/DDL.sql"
PL_PATH= "db/PL.sql"

# Gunicorn settings
GUNICORN_HOST = "0.0.0.0"
GUNICORN_PORT = "39277"
APP_ENTRYPOINT = "app:app" 

def apply_mysql_schema():
    print("Applying MySQL schema")
    conect_cmd = [
        "mysql",
        "-h", "classmysql.engr.oregonstate.edu",
        "-u", MYSQL_USER,
        f"-p{MYSQL_PASSWORD}",
        MYSQL_DATABASE,
    ]
    with open(DDL_PATH, "r") as ddl:
        result = subprocess.run(conect_cmd, stdin=ddl)

    with open(PL_PATH, "r") as pl:
        result = subprocess.run(conect_cmd, stdin=pl)

    return result.returncode == 0


def start_gunicorn():
    print(">> Starting Gunicorn...")
    cmd = [
        "gunicorn",
        "-b",
        f"{GUNICORN_HOST}:{GUNICORN_PORT}",
        APP_ENTRYPOINT
    ]
    return subprocess.run(cmd)

def main():
    if not os.path.exists(DDL_PATH):
        print(f"DDL file not found: {DDL_PATH}")
        sys.exit(1)

    if not os.path.exists(PL_PATH):
        print(f"PL file not found: {PL_PATH}")
        sys.exit(1)

    # Apply schema
    ok = apply_mysql_schema()   
    if not ok:
        print("Failed to apply database schema.")
        sys.exit(1)

    print(">> Database schema applied successfully")

    # Start app with gunicorn
    start_gunicorn()


if __name__ == "__main__":
    main()
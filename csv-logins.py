#!/usr/bin/env python3

from csv import DictReader
from pathlib import Path
from shutil import which
from subprocess import PIPE, Popen
from sys import argv

# TODO: Use a GPG library or something, instead of calling gpg directly,
# this is not a shell script!

FIELDNAMES = tuple('url username password realm formactionorigin guid created lastused passwordchanged'.split())
LOGINS_FILE = Path.home() / 'Documents' / 'logins.csv.encrypted'
GPG = which('gpg')
DECRYPT_COMMAND = 'gpg --quiet --output - --decrypt'.split() + [str(LOGINS_FILE)]

def main():
    query = argv[1].lower() if len(argv) > 1 else None

    with Popen(DECRYPT_COMMAND, executable=GPG, stdout=PIPE, encoding='utf-8') as proc:
        # with LOGINS_FILE.open('r', encoding='utf-8') as f:

        loginsreader = DictReader(proc.stdout, FIELDNAMES)

        for row in (r for r in loginsreader if query is None or query in r['url'].lower()):
            print(f"URL: {row['url']}\nUsername: {row['username']}\nPassword: {row['password']}\n")

if __name__ == '__main__':
    main()

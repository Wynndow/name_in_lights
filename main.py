#!/usr/bin/env python3
import os
import argparse
from datetime import datetime, timedelta

LETTER_CODES = {
    "A": ((0, 1, 1, 1, 1), (1, 0, 1, 0, 0), (0, 1, 1, 1, 1)),
    "B": ((1, 1, 1, 1, 1), (1, 0, 1, 0, 1), (0, 1, 0, 1, 0)),
    "C": ((0, 1, 1, 1, 0), (1, 0, 0, 0, 1), (0, 1, 0, 1, 0)),
    "D": ((1, 1, 1, 1, 1), (1, 0, 0, 0, 1), (0, 1, 1, 1, 0)),
    "E": ((1, 1, 1, 1, 1), (1, 0, 1, 0, 1), (1, 0, 0, 0, 1)),
    "F": ((1, 1, 1, 1, 1), (1, 0, 1, 0, 0), (1, 0, 0, 0, 0)),
    "G": ((0, 1, 1, 1, 0), (1, 0, 0, 0, 1), (1, 0, 0, 1, 1)),
    "H": ((1, 1, 1, 1, 1), (0, 0, 1, 0, 0), (1, 1, 1, 1, 1)),
    "I": ((1, 0, 0, 0, 1), (1, 1, 1, 1, 1), (1, 0, 0, 0, 1)),
    "J": ((0, 0, 0, 1, 0), (1, 0, 0, 0, 1), (1, 1, 1, 1, 0)),
    "K": ((1, 1, 1, 1, 1), (0, 1, 0, 1, 0), (1, 0, 0, 0, 1)),
    "L": ((1, 1, 1, 1, 1), (0, 0, 0, 0, 1), (0, 0, 0, 0, 1)),
    "M": ((1, 1, 1, 1, 1), (0, 1, 0, 0, 0), (1, 1, 1, 1, 1)),
    "N": ((1, 1, 1, 1, 1), (1, 0, 0, 0, 0), (1, 1, 1, 1, 1)),
    "O": ((0, 1, 1, 1, 0), (1, 0, 0, 0, 1), (0, 1, 1, 1, 0)),
    "P": ((1, 1, 1, 1, 1), (1, 0, 1, 0, 0), (0, 1, 0, 0, 0)),
    "Q": ((0, 1, 1, 0, 0), (1, 0, 0, 1, 0), (0, 1, 1, 0, 1)),
    "R": ((1, 1, 1, 1, 1), (1, 0, 1, 0, 0), (0, 1, 0, 1, 1)),
    "S": ((0, 1, 0, 0, 1), (1, 0, 1, 0, 1), (1, 0, 0, 1, 0)),
    "T": ((1, 0, 0, 0, 0), (1, 1, 1, 1, 1), (1, 0, 0, 0, 0)),
    "U": ((1, 1, 1, 1, 1), (0, 0, 0, 0, 1), (1, 1, 1, 1, 1)),
    "V": ((1, 1, 1, 1, 0), (0, 0, 0, 0, 1), (1, 1, 1, 1, 0)),
    "W": ((1, 1, 1, 1, 1), (0, 0, 0, 1, 0), (1, 1, 1, 1, 1)),
    "X": ((1, 1, 0, 1, 1), (0, 0, 1, 0, 0), (1, 1, 0, 1, 1)),
    "Y": ((1, 1, 0, 0, 0), (0, 0, 1, 1, 1), (1, 1, 0, 0, 0)),
    "Z": ((1, 0, 0, 1, 1), (1, 0, 1, 0, 1), (1, 1, 0, 0, 1)),
    "!": ((1, 1, 1, 0, 1),),
    " ": ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0)),
}

def update_and_commit(date_string):
    os.system(f'export GIT_COMMITTER_DATE="{date_string}"')
    os.system(f'echo {date_string} >> commitfile.txt')
    os.system('git add commitfile.txt')
    os.system(f'git commit --date="{date_string}" -m "commited on {date_string}"')
    os.system('unset GIT_COMMITTER_DATE')

def special_day_commit(date, commits):
    for i in range(commits):
        update_and_commit(get_date_string(date))

def message_commits(message, commits, sunday):
    date = sunday + timedelta(days = 1)
    for char in message:
        letter_code = LETTER_CODES[char]
        for column_code in letter_code:
            for date_bit in column_code:
                if date_bit:
                    for i in range(commits):
                        update_and_commit(get_date_string(date, i))
                date += timedelta(days = 1)
            date += timedelta(days = 2)
        date += timedelta(days = 7)

def get_date_string(date, i=0):
    return f'{date.strftime("%Y-%m-%d")} 12:{str(i).zfill(2)}:00'

def valid_date(date_string):
    try:
        return datetime.strptime(date_string, "%d-%m-%Y")
    except ValueError:
        msg = f"Not a valid date: '{date_string}'."
        raise argparse.ArgumentTypeError(msg)

def get_sunday_of_given_week(date):
    if date.weekday() == 6:
        return date

    return get_sunday_of_given_week(date - timedelta(days=1))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("message", help="the text to display",
                    type=str)
    parser.add_argument("start_date", help="a date in the week the message starts - format %d-%m-%Y",
                    type=valid_date)
    parser.add_argument("--commits", help="how many commits to make on each date",
                    type=int, default=1)
    parser.add_argument("--special_day", help="add some commits on a special day - format %d-%m-%Y",
                    type=valid_date)
    args = parser.parse_args()

    os.system("touch commitfile.txt")
    commits = args.commits if args.commits else 1

    if args.special_day:
        special_day_commit(args.special_day, commits)

    message_commits(args.message.upper(), commits, get_sunday_of_given_week(args.start_date))
        



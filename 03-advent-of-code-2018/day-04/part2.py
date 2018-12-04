#!/usr/bin/env python
import re
import sys
from collections import defaultdict, Counter
from datetime import datetime
from operator import itemgetter
from typing import NamedTuple


class Record(NamedTuple):
    time: datetime
    observation: str

    _RECORD_RE = re.compile(r"\[(?P<time>.+?)\] (?P<observation>.+)")

    @classmethod
    def from_string(cls, s):
        g = cls._RECORD_RE.match(s).groupdict()
        return cls(
            time=datetime.strptime(g["time"], "%Y-%m-%d %H:%M"),
            observation=g["observation"],
        )

    def __lt__(self, other):
        return self.time < other.time


def read_input():
    return (Record.from_string(line) for line in sys.stdin)


def parse_records(records):
    current_guard = None
    sleep_begin = None
    for record in sorted(records):
        if record.observation.startswith("Guard #"):
            current_guard = int(record.observation[7:].split(" ")[0])
        elif record.observation == "falls asleep":
            sleep_begin = record.time
        elif record.observation == "wakes up":
            sleep_end = record.time
            yield (current_guard, sleep_begin, sleep_end)


class SleepCounter(Counter):
    def most_slept_minute_and_count(self):
        return self.most_common(1)[0]

    def most_slept_count(self):
        minute, count = self.most_slept_minute_and_count()
        return count

    def __lt__(self, other):
        return self.most_slept_count() < other.most_slept_count()


def sleep_freq_by_minute_by_guard(sleep_periods):
    sleep_freq = defaultdict(SleepCounter)
    for guard_id, sleep_begin, sleep_end in sleep_periods:
        for minute in range(sleep_begin.minute, sleep_end.minute):
            sleep_freq[guard_id][minute] += 1
    return sleep_freq


def most_frequently_asleep_on_the_same_minute(sleep_periods):
    sleep_freq = sleep_freq_by_minute_by_guard(sleep_periods)
    return sorted(sleep_freq.items(), key=itemgetter(1))[-1]


if __name__ == "__main__":
    sleep_periods = parse_records(read_input())
    guard_id, counter = most_frequently_asleep_on_the_same_minute(sleep_periods)
    minute, count = counter.most_slept_minute_and_count()
    print(
        f"Guard #{guard_id} is the most frequently asleep "
        f"on the same minute ({count} times at 00:{minute})."
    )
    print(f"Puzzle answer is {guard_id * minute}.")

#!/usr/bin/env python
import re
import sys
from collections import Counter
from datetime import datetime
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


def guard_with_the_most_sleep(sleep_periods):
    sleep_durations = Counter()
    for guard_id, sleep_begin, sleep_end in sleep_periods:
        duration = sleep_end - sleep_begin
        sleep_durations[guard_id] += int(duration.total_seconds()) // 60
    return sleep_durations.most_common(1)[0]


def most_sleepy_minute(sleep_periods, guard_id):
    minutes = Counter()
    for _guard_id, sleep_begin, sleep_end in sleep_periods:
        if _guard_id != guard_id:
            continue
        for minute in range(sleep_begin.minute, sleep_end.minute):
            minutes[minute] += 1
    return minutes.most_common(1)[0][0]


if __name__ == "__main__":
    records = read_input()
    sleep_periods = list(parse_records(records))

    guard_id, duration = guard_with_the_most_sleep(sleep_periods)
    print(f"Guard #{guard_id} has slept a total of {duration} minutes.")

    minute = most_sleepy_minute(sleep_periods, guard_id)
    print(f"Guard #{guard_id} was most sleepy during minute {minute}.")

    print(f"Puzzle answer is {guard_id * minute}.")

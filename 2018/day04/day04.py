import re
from collections import namedtuple
from datetime import datetime

Event = namedtuple('Event', ['datetime', 'text'])
#[1518-06-07 00:03] Guard #1619 begins shift
#[1518-09-02 00:15] falls asleep
#[1518-04-26 00:48] wakes up

def parse_line(line):
    PATTERN = '\[([0-9]{4}.*)\] (.*)'
    groups = re.search(PATTERN, line).groups()
    time = datetime.strptime(groups[0], '%Y-%m-%d %H:%M')
    return time, groups[1]

def parse(f):
    lines = sorted(map(parse_line, f.read().strip().split('\n')))
    naps = []
    for time, text in lines:
        if text.startswith('Guard'):
            PATTERN = 'Guard #([0-9]+) begins shift'
            guard = int(re.search(PATTERN, text).groups()[0])
        elif text.startswith('falls'):
            nap_start = time.minute
        elif text.startswith('wakes'):
            nap_end = time.minute
            naps.append((guard, nap_start, nap_end))
    return naps


def get_sleepiest_guard(naps):
    total_nap = {}
    for (guard, start, end) in naps:
        total_nap[guard] = total_nap.get(guard, 0) + (end - start)

    ordered_nap_times = sorted(total_nap.items(), key=lambda x: x[1], reverse=True)
    return ordered_nap_times[0][0]


def get_sleepiest_minute(naps, guard):
    freqs = {minute: 0 for minute in range(60)}
    for nap in naps:
        if nap[0] == guard:
            for minute in range(nap[1], nap[2]):
                freqs[minute] += 1

    ordered_freqs = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
    return ordered_freqs[0][0]


def part1Answer(f):
    naps = parse(f)
    guard = get_sleepiest_guard(naps)
    minute = get_sleepiest_minute(naps, guard)
    return guard * minute


def part2Answer(f):
    naps = parse(f)
    freqs = {}
    for guard, start, end in naps:
        for minute in range(start, end):
            freqs[(guard, minute)] = freqs.get((guard, minute), 0) + 1
    ordered_freqs = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
    guard, minute = ordered_freqs[0][0]
    return guard * minute

if __name__ == "__main__":
    f = open('input.txt', 'rt')
    print("Part 1: {}".format(part1Answer(f)))
    f.seek(0)
    print("Part 2: {}".format(part2Answer(f)))


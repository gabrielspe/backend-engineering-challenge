import argparse
import functools
import json
import sys
from datetime import datetime, timedelta


class Translation:
    def __init__(self, timestamp: datetime, duration: int):
        self.timestamp = timestamp
        self.duration = duration


def main(argv):
    print(argv)
    parser = argparse.ArgumentParser(argv)
    parser.add_argument('--input_file', default='input.txt')
    parser.add_argument('--window_size', type=int, default=10)

    args = parser.parse_args()
    print(args.input_file)
    json_decoder = json.JSONDecoder()
    translations = []

    with open(args.input_file, 'r') as f:
        for line in f:
            translation = json_decoder.decode(line)
            timestamp = datetime.strptime(translation['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            translations.append(Translation(timestamp, translation['duration']))

    first_timestamp = translations[0].timestamp
    last_timestamp = translations[-1].timestamp

    first_minute = datetime(
        first_timestamp.year,
        first_timestamp.month,
        first_timestamp.day,
        first_timestamp.hour,
        first_timestamp.minute)
    last_minute = datetime(
        last_timestamp.year,
        last_timestamp.month,
        last_timestamp.day,
        last_timestamp.hour,
        last_timestamp.minute)

    last_minute += timedelta(minutes=1)
    window_end = first_minute
    encoder = json.JSONEncoder()

    while window_end <= last_minute:
        window_start = window_end - timedelta(minutes=args.window_size)
        window_durations = list(
            (t.duration for t in translations if window_start <= t.timestamp < window_end)
        )
        duration_sum = functools.reduce(lambda a, b: a + b, window_durations, 0)
        window_average = (duration_sum / len(window_durations)) if len(window_durations) > 0 else 0
        result = {'date': window_end.strftime('%Y-%m-%d %H:%M:%S'), 'average_delivery_time': window_average}
        print(encoder.encode(result))
        window_end += timedelta(minutes=1)


if __name__ == '__main__':
    main(sys.argv[1:])

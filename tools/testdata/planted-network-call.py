#!/usr/bin/env python3
"""Self-test fixture — a checker script with a planted network call.

The no-network scanner must catch this by name: it looks like an innocuous
"verify against the live source" helper, which is exactly the kind of
addition that could slip into a checker script without anyone noticing it
broke the offline guarantee.
"""
import sys
import requests  # planted: this is exactly what the scanner must catch


def fetch_live_copy(url):
    return requests.get(url).text


def main(argv):
    print("this script secretly calls the network")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

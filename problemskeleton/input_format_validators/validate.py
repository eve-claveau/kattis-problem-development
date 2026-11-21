#!/usr/bin/env python3

import sys
import re

def read_line():
    return sys.stdin.readline()

# check line 1 is two integers N and R separated by a single space
# with 2<=N<=5000 and 1<=R<=floor(N/2)
first_line = read_line()
assert re.fullmatch(r'[1-9][0-9]{0,3} [1-9][0-9]{0,3}\n', first_line), \
    "line 1 must be 'N R' (plain integers, one space, newline): " + repr(first_line)
n, r = map(int, first_line.split())
assert 2 <= n <= 5000, "N out of range: %d" % n
assert 1 <= r <= n // 2, "R must satisfy 1 <= R <= floor(N/2): N=%d R=%d" % (n, r)

# check line 2 is N integers a1...an separated by one space
# ensure 0<=ai<=10^4
second_line = read_line()
assert re.fullmatch(r'(0|[1-9][0-9]{0,4})( (0|[1-9][0-9]{0,4}))*\n', second_line), \
    "line 2 has bad syntax: " + repr(second_line[:60])
a = list(map(int, second_line.split()))
assert len(a) == n, "line 2 must contain exactly N=%d integers, found %d" % (n, len(a))
for i, x in enumerate(a, start=1):
    assert 0 <= x <= 10**4, "a_%d=%d out of range [0, 10000]" % (i, x)

# make sure there's no extra input that doesn't follow the guidelines
assert sys.stdin.readline() == '', "extra input after line 2"

# if we get here, then exit with exit code 42 to signify correct input!
sys.exit(42)


import sys


sys.setrecursionlimit(10000)# TLE instead of Run Time Error


N, R = map(int, input().split())
run_segments = list(map(int, input().split()))


# Slow solution: tries every choice with recursion
# The answer is correct, but it runs in exponential time -> TLE on large inputs


def running_effectiveness(r1, r2):
   return 2 * r1 * r2 - abs(r1 - r2)


def best_runs(i, run_left):
   # All R runs chosen: nothing more to add
   if run_left == 0:
       return 0


   # Not enough segments left to make the remaining runs
   if N - i < 2 * run_left:
       return float("-inf")


   # Either:
   # 1. Skip this segment
   # 2. Pair it with the following segment
   return max(best_runs(i + 1, run_left),
              running_effectiveness(run_segments[i], run_segments[i + 1]) + best_runs(i + 2, run_left - 1))


print(best_runs(0, R))


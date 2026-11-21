# accepted solution in Python: bottom-up DP over the number of runs k
# dp_k[i] = max(dp_k[i-1], w(pair i) + dp_{k-1}[i-2])
# time O(N*R) and memory O(N)

import sys

def training_intensity(x: int, y: int) -> int:
    # intensity of one run over two consecutive segments with difficulties x and y
    return 2 * x * y - abs(x - y)

def max_training_intensity(n: int, r: int, segments: list[int]) -> int:
    m = n - 1  # number of consecutive pairs

    # pair_intensities[i] = intensity of the run on segments i and i+1
    pair_intensities = [training_intensity(segments[i], segments[i + 1]) for i in range(m)]

    # base case: k = 1 run using pairs 0...i
    # prev_k[i] = best run among pairs 0...i (a running maximum)
    prev_k = [0] * m
    prev_k[0] = pair_intensities[0]
    for i in range(1, m):
        prev_k[i] = max(prev_k[i - 1], pair_intensities[i])

    neg_inf = float('-inf') # marks states that are impossible

    for k in range(2, r + 1):
        # curr_k[i] = best total intensity with exactly k runs among pairs 0...i
        curr_k = [neg_inf] * m # everything starts as impossible and gets filled in
        
        # k runs need at least 2*(k-1)+1 pairs, since chosen pairs can't share a segment
        # start_idx is the first index where k runs can fit (earlier states stay -inf)
        start_idx = 2 * (k - 1)
        for i in range(start_idx, m):
            take = pair_intensities[i] + prev_k[i - 2] # option 1 (take): use pair i as the k-th run
            skip = curr_k[i - 1] # option 2 (skip): don't use pair i
            
            curr_k[i] = take if take > skip else skip # keep the better option
            
        prev_k = curr_k

    # prev_k[m-1] is the best total with exactly r runs using any of the pairs
    return prev_k[m - 1]


def main() -> None:
    data = sys.stdin.read().split() # read input and split
    n = int(data[0])  # number of segments
    r = int(data[1])  # number of runs
    segments = [int(x) for x in data[2 : 2 + n]]  # difficulty of each segment
    print(max_training_intensity(n, r, segments))

if __name__ == "__main__":
    main()


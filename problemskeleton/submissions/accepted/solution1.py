import sys

def training_load(x: int, y: int) -> int:
    return 2 * x * y - abs(x - y)

def max_training_load(n: int, r: int, segments: list[int]) -> int:
    m = n - 1  # number of consecutive pairs
    pair_loads = [training_load(segments[i], segments[i + 1]) for i in range(m)]

    # Base case: k = 1 run using pairs[0..i]
    prev_k = [0] * m
    for i in range(m):
        prev_k[i] = pair_loads[i] if i == 0 else max(prev_k[i - 1], pair_loads[i])

    if r == 1:
        return prev_k[m - 1]

    neg_inf = -(10**18)

    for k in range(2, r + 1):
        curr_k = [neg_inf] * m
        start_idx = 2 * (k - 1)
        for i in range(start_idx, m):
            skip = curr_k[i - 1] if i > start_idx else neg_inf
            best_prev = prev_k[i - 2] if i >= 2 else neg_inf
            take = pair_loads[i] + best_prev if best_prev > neg_inf // 2 else neg_inf
            curr_k[i] = max(skip, take)
        prev_k = curr_k

    return prev_k[m - 1]

def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    r = int(data[1])
    segments = [int(x) for x in data[2 : 2 + n]]
    print(max_training_load(n, r, segments))

if __name__ == "__main__":
    main()

import random


random.seed(2026)


# Here is the imported correct solution and it's helper function
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


# 1. Hand-crafted edge cases


# Statement sample
statement_sample = [7, 2, [9, 1, 10, 30, 2, 5, 6]]


# a) Greedy trap : N=4, R=2, segments=[5, 10, 10, 5] -> Wrong answer
# Choosing the largest pair first prevents completing R runs.
greedy_trap = [ 4, 2, [5, 10, 10, 5]]

# b) Small boundary cases : N=2, R = 1,
# Tests the smallest valid case
small_case = [2, 1, [1, 2]]

# c) Odd N, maximum R
# Tests choosing which segment to leave unused.
odd_maximum_r = [5, 2, [10, 10, 0, 10, 10]]

# d) Maximum-size case : N = 5000, R = 1250 -> TLE
# Will test performance of solution, expose slow solutions
tle_trap = [5000, 1250, [random.randint(0, 10000) for _ in range(5000)]]


# e) Maximum-total case : N = 5000, R = 2500, all difficulties=10000 -> Integer Overflow
# Expected: 500_000_000_000. Exposes 32-bit integer overflow.
maximum_total = [5000, 2500, [10000] * 5000]

# f) All difficulties 0
all_zeros = [4, 2, [0, 0, 0, 0]]

# g) Complicated case: values alternate between 0 and 10000.
complicated = [5000, 1250, [0 if i % 2 == 1 else 10000 for i in range(5000)]]


handcrafted_cases = [statement_sample, greedy_trap, small_case, odd_maximum_r, tle_trap, maximum_total, all_zeros, complicated]


handcrafted_descriptions = [
   "Sample from the problem statement (N=7, R=2).",
   "Edge case: greedy trap, the best pair is in the middle but R=2 needs the outer pairs.",
   "Edge case: smallest valid input (N=2, R=1).",
   "Edge case: odd N with maximum R, one segment must stay unused.",
   "Large input / TLE: N=5000, R=1250, random difficulties, the most DP work.",
   "Edge case / overflow: N=5000, R=2500, all difficulties 10000, answer is 500000000000.",
   "Edge case: all difficulties are 0, answer is 0.",
   "Complicated case: N=5000, R=1250, values alternate between 10000 and 0."
]


# 2. Randomly generated test cases
# Generate valid N, R, and difficulty ratings within the constraints.


random_cases = []
random_descriptions = []


for i in range(20):
   if i % 3 == 0:
       n = random.randint(2, 10)# small
       size = "small"
   elif i % 3 == 1:
       n = random.randint(50, 500)# medium
       size = "medium"
   else:
       n = random.randint(1000, 5000) # large
       size = "large"


   r = random.randint(1, n // 2) # 1 <= R <= N/2


   segments = []
   for j in range(n):
       segments.append(random.randint(0, 10000)) #  0 ≤ a_i ≤ 10^4


   random_cases.append([n, r, segments])
   random_descriptions.append(f"Normal random case ({size}): N={n}, R={r}.")


# 3. All test cases
all_cases = handcrafted_cases + random_cases
all_descriptions = handcrafted_descriptions + random_descriptions


# 4. Computing the correct answer using the correct imported solutions
answers = []
for n, r, segments in all_cases:
   answers.append(max_training_load(n, r, segments))


# 5. Create two files per case


# test.in for the input
# test.ans for the output


description_lines = []


for i in range(len(all_cases)):
   n, r, segments = all_cases[i]


   # First 3 cases are samples, all the others are secret
   if i < 3:
       folder = "../data/sample/"
       base_name = f"sample_{i + 1}"
       description_lines.append(f"sample/{base_name}.in: {all_descriptions[i]}")
   else:
       folder = "../data/secret/"
       base_name = f"secret_{i - 2}"
       description_lines.append(f"secret/{base_name}.in: {all_descriptions[i]}")

       with open(folder + base_name + ".txt", "w") as file:
           file.write(all_descriptions[i] + "\n")
   input_name = folder + base_name + ".in" 
   answer_name = folder + base_name + ".ans" 


   with open(input_name, "w") as file:
       file.write(f"{n} {r}\n")
       file.write(" ".join(str(x) for x in segments))
       file.write("\n")


   with open(answer_name, "w") as file:
       file.write(str(answers[i]) + "\n")


# Write the Description.txt file
with open("../data/Description.txt", "w") as file:
   file.write("\n".join(description_lines) + "\n")

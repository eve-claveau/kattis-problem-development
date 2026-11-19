// Accepted solution (C++): bottom-up DP over the number of runs k.
// Pair p = segments p and p+1, with training load w(x, y) = 2*x*y - |x - y|.
// dp_k[i] = max total load using exactly k runs among pairs 0..i (no two chosen pairs adjacent):
//   dp_k[i] = max(dp_k[i-1], w(pair i) + dp_{k-1}[i-2])
// Base: dp_1[i] = max of w over pairs 0..i. States with i < 2(k-1) are infeasible (-inf).
// Time O(N*R), memory O(N). Answers reach ~5*10^11, so long long is required.
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <vector>

using namespace std;
typedef long long ll;

static ll trainingLoad(ll x, ll y) {
    return 2LL * x * y - llabs(x - y);
}

ll maxTrainingLoad(int n, int r, const vector<ll>& segments) {
    int m = n - 1;  // number of consecutive pairs
    vector<ll> pairLoads(m);
    for (int i = 0; i < m; i++) {
        pairLoads[i] = trainingLoad(segments[i], segments[i + 1]);
    }

    // Base case: k = 1 run using pairLoads[0..i]
    vector<ll> prevK(m);
    prevK[0] = pairLoads[0];
    for (int i = 1; i < m; i++) {
        prevK[i] = max(prevK[i - 1], pairLoads[i]);
    }

    const ll negInf = LLONG_MIN / 4;
    vector<ll> currK(m);

    // For r == 1 this loop is skipped and prevK already holds the answer.
    for (int k = 2; k <= r; k++) {
        fill(currK.begin(), currK.end(), negInf);

        // The first pair index that can hold k runs is 2*(k-1); for i >= that,
        // prevK[i-2] is always feasible, so no -inf checks are needed.
        int startIdx = 2 * (k - 1);
        for (int i = startIdx; i < m; i++) {
            currK[i] = max(currK[i - 1], pairLoads[i] + prevK[i - 2]);
        }
        swap(prevK, currK);
    }

    return prevK[m - 1];
}

int main() {
    int n, r;
    if (scanf("%d %d", &n, &r) != 2) return 0;
    vector<ll> segments(n);
    for (int i = 0; i < n; i++) {
        if (scanf("%lld", &segments[i]) != 1) return 0;
    }
    printf("%lld\n", maxTrainingLoad(n, r, segments));
    return 0;
}

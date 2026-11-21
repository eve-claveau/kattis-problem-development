// accepted solution in C++: bottom-up DP over the number of runs k
// dp_k[i] = max(dp_k[i-1], w(pair i) + dp_{k-1}[i-2])
// time O(N*R) and memory O(N)


#include <algorithm>
#include <climits>
#include <cmath>
#include <cstdlib>
#include <cstdio>
#include <vector>


using namespace std;
typedef long long ll;


static ll trainingIntensity(ll x, ll y) {
   // intensity of one run over two consecutive segments with difficulties x and y
   return 2LL * x * y - llabs(x - y);
}


ll maxTrainingIntensity(int n, int r, const vector<ll>& segments) {
   int m = n - 1;  // number of consecutive pairs (a run uses one pair)


   // pairIntensities[i] = intensity of the run on segments i and i+1
   vector<ll> pairIntensities(m);
   for (int i = 0; i < m; i++) {
       pairIntensities[i] = trainingIntensity(segments[i], segments[i + 1]);
   }


   // base case: k = 1 run using pairs 0...i
   // prevK[i] = best run among pairs 0...i (a running maximum)
   vector<ll> prevK(m);
   prevK[0] = pairIntensities[0];
   for (int i = 1; i < m; i++) {
       prevK[i] = max(prevK[i - 1], pairIntensities[i]);
   }


   // marks impossible states
   const ll negInf = LLONG_MIN / 4; // divided by 4 so that adding to it can never overflow
   vector<ll> currK(m);


   // for r == 1 this loop is skipped and prevK already holds the answer
   for (int k = 2; k <= r; k++) {
       // currK[i] = best total intensity with exactly k runs among pairs 0...i
       // everything starts as impossible and gets filled in
       fill(currK.begin(), currK.end(), negInf);


       // k runs need at least 2*(k-1)+1 pairs, since chosen pairs can't share a segment
       // so startIdx is the first index where k runs can fit (earlier states stay -inf)
       int startIdx = 2 * (k - 1);
       for (int i = startIdx; i < m; i++) {
           ll take = pairIntensities[i] + prevK[i - 2]; // option 1 (take): use pair i as the k-th run
           ll skip = currK[i - 1]; // option 2 (skip): don't use pair i


           currK[i] = max(take, skip);  // keep the better option
       }


       swap(prevK, currK);
   }


   // prevK[m-1] is the best total with exactly r runs using any of the pairs
   return prevK[m - 1];
}


int main() {
   int n, r;
   if (scanf("%d %d", &n, &r) != 2) return 0;  // number of segments, number of runs


   vector<ll> segments(n);  // difficulty of each segment
   for (int i = 0; i < n; i++) {
       if (scanf("%lld", &segments[i]) != 1) return 0;
   }


   printf("%lld\n", maxTrainingIntensity(n, r, segments));
   return 0;
}

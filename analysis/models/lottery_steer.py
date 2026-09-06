"""Custody lottery (DEP-06): winner = sum(c_i) mod N, c_i in 1..N, committed before reveal.
A coalition controlling k of N disputants sees all honest reveals first and may withhold
exactly one of its own reveals (two+ missing falls to the recovery cascade, which an
honest majority controls). Withholding one -> partial-reveal leaf: lottery over the
N-1 revealers with the same rule mod (N-1). Cost of withholding: one slice, swept
pro-rata to revealers (coalition recovers (k-1)/(N-1) of it).
Computes P(coalition member wins) with and without steering, exhaustively."""
import itertools, fractions

def winner(cs, mod):
    return sum(cs) % mod

def analyze(N, k):
    honest = N - k
    total = 0; base = 0; steer = 0; withheld = 0
    for cs in itertools.product(range(1, N+1), repeat=N):
        total += 1
        # indices 0..k-1 are coalition
        w = winner(cs, N)
        if w < k: base += 1; steer += 1; continue
        # try withholding each coalition member j: revealers = all except j, ordered
        # by sorted pubkey; remaining indices keep relative order, winner index maps
        # onto the remaining list.
        won = False
        for j in range(k):
            rem = [i for i in range(N) if i != j]
            wi = winner([cs[i] for i in rem], N-1)
            if rem[wi] < k: won = True; break
        if won: steer += 1; withheld += 1
    f = lambda a: f"{a/total:.3f}"
    print(f"N={N} k={k}: fair={f(base)} steered={f(steer)} (withholds in {f(withheld)} of cases)")

for N, k in [(3,1),(5,1),(5,2),(7,1),(7,2),(7,3)]:
    analyze(N, k)

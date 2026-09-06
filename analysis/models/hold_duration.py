"""Depositor hold duration when an operator goes silent.

Silence starts at a uniformly random point in a rotation cycle of length CYCLE blocks
(quorum_expiry E is at the end of the cycle). Each of Q members is independently
"live" (will act as soon as a path opens) with probability p.

Paths (DEP-03/05 tiers; F1 inactivity trigger optional):
  inactivity: t = N            needs majority live         (only if enabled)
  Tier 0:     t = E            needs majority live
  Tier 1:     t = E + 720      needs >= floor(Q/2) live    ("minority", assumed)
  Tier 2:     t = E + 4032     needs >= 1 live
  Tier 3:     t = E + 8064     operator solo; treated as unbounded hold (funds gone)
Every custody transfer then takes PIPE blocks (arm 144 + confirm + reveal + claim).
"""
import random, statistics
CYCLE, PIPE = 2016, 170
TIERS = [(0, 'maj'), (720, 'min'), (4032, 'one')]

def hold(Q, p, N, inact, rng):
    live = sum(rng.random() < p for _ in range(Q))
    maj = Q//2 + 1; mino = max(1, Q//2)
    need = {'maj': maj, 'min': mino, 'one': 1}
    E = rng.uniform(0, CYCLE)              # blocks until expiry
    if inact and live >= maj:
        return N + PIPE
    for off, key in TIERS:
        if live >= need[key]:
            return E + off + PIPE
    return None                            # Tier 3: operator keeps everything

def run(Q, p, N, inact, trials=20000, seed=1):
    rng = random.Random(seed)
    hs = [hold(Q, p, N, inact, rng) for _ in range(trials)]
    lost = hs.count(None)/trials
    ok = [h for h in hs if h is not None]
    return statistics.mean(ok)/144, statistics.quantiles(ok, n=20)[18]/144, lost

print(f"{'Q':>2} {'p':>4} {'N':>4} | {'mean d':>7} {'p95 d':>6} {'lost':>5} || {'mean d':>7} {'p95 d':>6} {'lost':>5}")
print(" "*17 + "expiry-only" + " "*13 + "with inactivity trigger")
for Q in (3,5,7):
    for p in (0.95, 0.8, 0.6):
        for N in (144, 432):
            a = run(Q,p,N,False); b = run(Q,p,N,True)
            print(f"{Q:>2} {p:>4} {N:>4} | {a[0]:>7.1f} {a[1]:>6.1f} {a[2]:>5.2f} || {b[0]:>7.1f} {b[1]:>6.1f} {b[2]:>5.2f}")

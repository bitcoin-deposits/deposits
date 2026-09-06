"""Do member-selection rules give the cascade teeth, and can quorums still be filled?

Network: N operators, vault sizes Pareto(alpha) (a few large, many small), each
running L ledgers of size v/L. Each ledger picks Q members from eligible operators.

Rules (applied by an honest operator when picking, and by a wallet when scoring):
  r : member's total vault must be >= r * guarded ledger's vault
  m : member may serve on at most m quorums  (None = unlimited)
  cap: 'capacity' rule -- sum over guarded ledgers of (ledger vault / 2) <= own vault

A ledger is DEFENDED if the cheapest majority of its members has more slashable
stake than the ledger's vault (the most a theft can take: reserves + collateral,
plus deposits <= reserves, which we fold in by comparing to vault since deposits
are backed by reserves already in it).
  single  : stake = member's full vault (a one-off theft; key slashed once)
  diluted : stake = member vault / quorums served (coalition mass theft; the same
            key signs on every quorum it sits on and is slashed once)
Reach (an honest anchor on each member's quorum) is assumed; this measures bite only.
"""
import random, statistics as st
from itertools import combinations

def make_net(N, L, alpha, seed):
    rng = random.Random(seed)
    vaults = sorted((rng.paretovariate(alpha) for _ in range(N)), reverse=True)
    ledgers = [(i, vaults[i]/L) for i in range(N) for _ in range(L)]
    return vaults, ledgers, rng

def form(vaults, ledgers, Q, r, m, cap, rng):
    N = len(vaults); served = [0]*N; guarded = [0.0]*N
    quorums = []
    order = list(range(len(ledgers))); rng.shuffle(order)
    for li in order:
        op, lv = ledgers[li]
        elig = [j for j in range(N) if j != op and vaults[j] >= r*lv
                and (m is None or served[j] < m)
                and (not cap or guarded[j] + lv/2 <= vaults[j])]
        if len(elig) < Q: quorums.append((li, None)); continue
        pick = rng.sample(elig, Q)
        for j in pick: served[j] += 1; guarded[j] += lv/2
        quorums.append((li, pick))
    return quorums, served

def evaluate(vaults, ledgers, quorums, served, Q):
    maj = Q//2 + 1
    tot_cap = sum(lv for _, lv in ledgers)
    unfilled = def_single = def_dil = 0.0
    for li, pick in quorums:
        op, lv = ledgers[li]
        if pick is None: unfilled += lv; continue
        s_single = sorted(vaults[j] for j in pick)[:maj]
        s_dil = sorted(vaults[j]/served[j] for j in pick)[:maj]
        if sum(s_single) >= lv: def_single += lv
        if sum(s_dil) >= lv: def_dil += lv
    return unfilled/tot_cap, def_single/tot_cap, def_dil/tot_cap

def run(N=200, L=3, Q=5, alpha=1.5, r=0.0, m=None, cap=False, trials=20):
    res = []
    for t in range(trials):
        vaults, ledgers, rng = make_net(N, L, alpha, t)
        q, served = form(vaults, ledgers, Q, r, m, cap, rng)
        res.append(evaluate(vaults, ledgers, q, served, Q))
    return tuple(st.mean(x[i] for x in res) for i in range(3))

if __name__ == '__main__':
    print("share of network capacity: unfilled | defended(single) | defended(diluted)")
    print(f"{'Q':>2} {'r':>5} {'m':>5} {'cap':>4} | {'unfilled':>8} {'single':>7} {'diluted':>8}")
    for Q in (3, 5, 7):
        for r, m, cap in [(0,None,False),(0.5,None,False),(1.0,None,False),
                          (0.5,5,False),(0.5,3,False),(1.0,3,False),
                          (0,None,True),(0.5,None,True)]:
            u, s, d = run(Q=Q, r=r, m=m, cap=cap)
            print(f"{Q:>2} {r:>5} {str(m):>5} {str(cap):>4} | {u:>8.2f} {s:>7.2f} {d:>8.2f}")
        print()
    print("sensitivity to vault inequality (Q=5, r=0.5, cap):")
    for alpha in (1.2, 1.5, 2.0, 3.0):
        u, s, d = run(Q=5, r=0.5, cap=True, alpha=alpha)
        print(f"  alpha={alpha}: unfilled={u:.2f} single={s:.2f} diluted={d:.2f}")

# ---------------------------------------------------------------------------
# Actual coalition: random fraction f of operators collude. Quorums were formed
# honestly under the rule. The coalition may rob any ledger where it holds a
# majority; robbing exposes the signing keys (slashed once, full vault, assuming
# reach). It picks the theft set greedily to maximise  sum(vault robbed) - sum(keys exposed).
def coalition_profit(vaults, ledgers, quorums, Q, f, rng):
    N = len(vaults); maj = Q//2 + 1
    col = set(rng.sample(range(N), int(f*N)))
    targets = []
    for li, pick in quorums:
        if pick is None: continue
        op, lv = ledgers[li]
        cs = [j for j in pick if j in col]
        if len(cs) >= maj:
            cs.sort(key=lambda j: vaults[j])
            targets.append((lv, cs[:maj]))      # cheapest signing majority
    # Start from robbing everything robbable (keys shared across thefts), then
    # drop targets whose removal raises profit; compare with greedy-add. Take best.
    def value(sel):
        keys = set(); g = 0.0
        for lv, ks in sel: g += lv; keys.update(ks)
        return g - sum(vaults[j] for j in keys), g, sum(vaults[j] for j in keys)
    sel = list(targets)
    while sel:
        base = value(sel)[0]; best = None
        for i in range(len(sel)):
            v = value(sel[:i]+sel[i+1:])[0]
            if v > base and (best is None or v > best[0]): best = (v, i)
        if best is None: break
        sel.pop(best[1])
    p_drop, g_drop, c_drop = value(sel) if sel else (0.0, 0.0, 0.0)
    gain, cost = (g_drop, c_drop) if p_drop > 0 else (0.0, 0.0)
    tot = sum(lv for _, lv in ledgers)
    return gain/tot, cost/tot, (gain-cost)/tot

def sweep(Q=5, N=200, L=3, alpha=1.5, trials=20):
    print(f"\ncoalition sweep Q={Q}: share of network capacity stolen / exposed / net")
    print(f"{'r':>4} {'f':>4} | {'stolen':>6} {'exposed':>7} {'net':>6}")
    for r in (0.0, 0.5, 1.0, 2.0):
        for f in (0.1, 0.2, 0.3, 0.5):
            acc = []
            for t in range(trials):
                vaults, ledgers, rng = make_net(N, L, alpha, t)
                q, served = form(vaults, ledgers, Q, r, None, False, rng)
                acc.append(coalition_profit(vaults, ledgers, q, Q, f, rng))
            g, c, n = (st.mean(a[i] for a in acc) for i in range(3))
            print(f"{r:>4} {f:>4} | {g:>6.3f} {c:>7.3f} {n:>6.3f}")
        print()

if __name__ == '__main__':
    for Q in (3,5,7): sweep(Q=Q)

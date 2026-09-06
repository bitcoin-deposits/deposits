"""Coalition economics, built from the DEP mechanics rather than the author's sim.

Facts the model respects (DEP-03, DEP-05, DEP-06):
  * Tier 0 = majority of quorum members, no operator, no timelock, no output
    restriction. A quorum majority can spend the WHOLE vault (reserves + collateral)
    anywhere. So an honest operator's capital is stolen outright if a coalition holds
    a majority of that operator's quorum.
  * The keys exposed by a theft are the SIGNERS (quorum members), not the ledger's
    operator. Each signer is slashed only on ledgers it OPERATES whose own quorum has
    an honest majority. A key whose own quorums are all-coalition is unslashable.
  * Members may serve on any number of quorums; min_member_collateral is a flat
    floor, not per membership.

Units: every operator has capital U = 1, split over L ledgers; per ledger reserves
R = rho/L and collateral C = (1-rho)/L. Honest deposit mass M = u * (accepted
reserves). Wallets spread deposits uniformly over ledgers they accept.

Honest-side policies for accepting a key as a quorum member / a ledger for deposits:
  blind     : accept anyone.
  fixpoint  : accept keys whose quorum has a majority of accepted keys, seeded by
              anchors (the natural 'honest-majority closure' metric). A coalition
              defeats it with t slashable seed keys certifying the rest.
  depth1    : accept keys whose quorum majority are ANCHORS (no chaining). Coalition
              keys that pass are fully slashable by anchors.
  depth1+mc : depth1 plus per-membership collateral c (fraction of U), slashable,
              locked per quorum served.

Coalition strategy under each policy: minimal number of slashable keys, closed
quorums for everything else, fronts (coalition-operated ledgers with 3 acceptable
coalition members) to attract deposits, and members placed on honest quorums where
honest operators draw from the acceptable pool.
"""
from math import comb

def p_maj(g, Q):            # P(majority of Q draws are coalition) at coalition share g
    need = Q//2 + 1
    return sum(comb(Q,i) * g**i * (1-g)**(Q-i) for i in range(need, Q+1))

def profit(policy, f, N=100, Q=5, L=3, rho=0.4, u=0.5, t=1, c=0.0, a=None):
    k = round(f*N); Nh = N - k
    maj = Q//2 + 1
    if policy == 'blind':
        acc_frac = f                       # all coalition keys acceptable
        cost_fixed = 0.0
    elif policy == 'fixpoint':
        acc_frac = f
        cost_fixed = t * 1.0               # t seed keys, whole capital slashed
    elif policy.startswith('depth1'):
        a = a if a is not None else max(maj, 1)   # certified coalition keys
        a = min(a, k)
        acc_frac = a / (a + Nh)            # honest keys all certified
        cost_fixed = a * 1.0
    else: raise ValueError
    # --- honest vaults stolen: honest operator draws Q members from acceptable pool
    pm = p_maj(acc_frac, Q)
    gain_vaults = Nh * 1.0 * pm            # each honest operator's full U across L ledgers
    # --- fronts: coalition-operated ledgers accepted for deposits
    F = k * L                              # every coalition key operates L fronts
    accepted_ledgers = F + Nh * L
    M = u * rho * accepted_ledgers / L     # deposit mass over accepted reserves
    gain_dep = M * F / accepted_ledgers    # uniform spread
    # --- per-membership collateral cost (depth1+mc only): 3 memberships per front,
    #     plus memberships coalition keys hold on honest quorums
    cost_mc = 0.0
    if policy == 'depth1+mc':
        honest_memberships = Q * Nh * L * acc_frac
        cost_mc = c * (maj * F + honest_memberships)
    return gain_vaults + gain_dep - cost_fixed - cost_mc, gain_vaults, gain_dep, cost_fixed + cost_mc

def max_safe_f(policy, **kw):
    last = 0.0
    for i in range(1, 100):
        f = i/100
        if profit(policy, f, **kw)[0] > 0: return last
        last = f
    return last

if __name__ == '__main__':
    print("policy            max safe f   (N=100 Q=5 L=3 rho=0.4 u=0.5)")
    for pol, kw in [('blind',{}), ('fixpoint',{'t':1}), ('fixpoint',{'t':3}),
                    ('depth1',{}), ('depth1+mc',{'c':0.05}), ('depth1+mc',{'c':0.15}),
                    ('depth1+mc',{'c':0.3})]:
        print(f"{pol:<10} {str(kw):<12} {max_safe_f(pol, **kw):.2f}")
    print("\nbreakdown at f=0.10, 0.30:")
    for pol, kw in [('blind',{}), ('fixpoint',{'t':3}), ('depth1',{}), ('depth1+mc',{'c':0.15})]:
        for f in (0.10, 0.30):
            p, gv, gd, cost = profit(pol, f, **kw)
            print(f"  {pol:<10} {str(kw):<12} f={f:.2f}  vaults={gv:6.2f} deposits={gd:6.2f} cost={cost:6.2f} profit={p:7.2f}")
    print("\ndepth1+mc: max safe f vs c (Q=5,L=3):")
    for c in (0.05,0.1,0.15,0.2,0.3,0.5):
        print(f"  c={c:.2f} -> {max_safe_f('depth1+mc', c=c):.2f}")
    print("\ndepth1+mc c=0.15: vs Q and L:")
    for Q in (3,5,7):
        for L in (1,3,5):
            print(f"  Q={Q} L={L} -> {max_safe_f('depth1+mc', c=0.15, Q=Q, L=L):.2f}")

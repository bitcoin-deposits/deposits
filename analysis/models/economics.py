"""Operator P&L under DEP-19/20: deposits fund the vault, swap-only obligations,
rotation exit. All amounts per ledger, per year, in units of deposit capacity D_max.

Revenue
  balance fees      y * D                     (y = annualised bps on balances)
  transfer fees     t * V_int                 (t = bps per internal transfer, V = annual volume)
  courier spread    s * V_swap                (s = spread on swaps through operator's courier)
  membership income 0.03 * fees of guarded ledgers (symmetric network: ~ what you pay out)
Costs
  member comp       0.03 * Q * (balance + transfer fees)
  rotation          R_per_year * (180 + 34*exits_per_rotation) vB * feerate
  inventory carry   c_inv * I                 (opportunity cost of external inventory)
  ops               fixed
Capital
  collateral        (1/rho - 1) * D_max  + (1-u)*D_max/... unfilled capacity funded by operator
  own = D_max/rho - D + I
"""
def pnl(D_max=1.0, rho=0.5, u=0.7, y=0.02, t=0.001, v_int=20, s=0.002, v_swap=10,
        Q=5, rotations=26, exits_per_rotation=20, feerate=20, inv_share=0.15,
        c_inv=0.0, ops_btc=0.0, symmetric_membership=True):
    D = u * D_max
    bal = y * D
    xfer = t * v_int * D            # volume expressed as multiples of balances
    spread = s * v_swap * D
    comp_out = 0.03 * Q * (bal + xfer)
    comp_in = comp_out if symmetric_membership else 0.0
    rot = rotations * (180 + 34 * exits_per_rotation) * feerate / 1e8
    I = inv_share * D
    own = D_max / rho - D + I
    rev = bal + xfer + spread + comp_in
    cost = comp_out + rot + c_inv * I + ops_btc
    net = rev - cost
    return dict(revenue=rev, balance=bal, transfer=xfer, spread=spread, cost=cost,
                rotation=rot, net=net, own_capital=own, roi=net/own,
                depositor_cost_bps=(bal + xfer) / D * 1e4)

def show(name, **kw):
    r = pnl(**kw)
    print(f"{name:<28} roi={r['roi']*100:5.1f}%  own={r['own_capital']:.2f}  "
          f"net={r['net']:.4f}  rot={r['rotation']:.4f}  depositor pays {r['depositor_cost_bps']:5.0f} bps/yr")

if __name__ == '__main__':
    print("D_max = 1 BTC per ledger unless noted; rho=0.5, u=0.7, Q=5, 26 rotations/yr, 20 sat/vB\n")
    show("parked, 1% balance only", y=0.01, t=0, v_int=0, s=0, v_swap=0)
    show("parked, 3% balance only", y=0.03, t=0, v_int=0, s=0, v_swap=0)
    show("consumer: 1%, 10bps x20 vol", y=0.01, t=0.001, v_int=20, s=0.002, v_swap=5)
    show("agent: 0.5%, 5bps x200 vol", y=0.005, t=0.0005, v_int=200, s=0.001, v_swap=50)
    show("courier-heavy: 0.5%, spread", y=0.005, t=0.0005, v_int=20, s=0.003, v_swap=100)
    show("consumer, rho=0.4", y=0.01, t=0.001, v_int=20, s=0.002, v_swap=5, rho=0.4)
    show("consumer, u=0.95", y=0.01, t=0.001, v_int=20, s=0.002, v_swap=5, u=0.95)
    show("consumer, no membership income", y=0.01, t=0.001, v_int=20, s=0.002, v_swap=5, symmetric_membership=False)
    print("\nsmall ledgers: rotation cost vs size (consumer profile)")
    for D_max in (0.01, 0.05, 0.1, 0.5):
        r = pnl(D_max=D_max, y=0.01, t=0.001, v_int=20, s=0.002, v_swap=5, exits_per_rotation=5)
        print(f"  D_max={D_max:.2f} BTC: roi={r['roi']*100:5.1f}%  rotation={r['rotation']/max(r['revenue'],1e-9)*100:4.0f}% of revenue")
    print("\nfee needed for 5% ROI, balance fee only (u=0.7):")
    for rho in (0.4, 0.5, 0.6):
        for y in [i/1000 for i in range(1, 200)]:
            if pnl(rho=rho, y=y, t=0, v_int=0, s=0, v_swap=0)['roi'] >= 0.05:
                print(f"  rho={rho}: y={y*100:.1f}%"); break

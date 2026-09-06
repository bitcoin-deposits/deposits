"""Operator capital requirement calculator (see 09-guidance and the ROI discussion)."""
def capital(L=3, D_max=1.0, rho=0.4, u=0.7, w=0.2, r=0.5, concurrent_disputes=1,
            rotations_per_year=26, feerate_sat_vb=20, dispute_allowance_btc=0.005,
            S=0.0, guarded_selffill=0.0):
    """S: self-fill per ledger (own coins deposited as bridge/courier inventory).
    guarded_selffill: share of obligations on quorums you serve that is their self-fill."""
    vault = D_max / rho
    vaults = L * vault
    cust_cap = D_max - S
    float_liquid = L * u * cust_cap * w
    self_fill = L * S
    arm = concurrent_disputes * r * (u * D_max + guarded_selffill * D_max)
    onchain = L * rotations_per_year * 180 * feerate_sat_vb / 1e8 + dispute_allowance_btc
    own = vaults + float_liquid + self_fill + arm + onchain
    held = L * u * cust_cap
    return dict(vault_each=vault, vaults=vaults, float_liquid=float_liquid, self_fill=self_fill,
                customer_capacity=L*cust_cap, arm_reserve=arm,
                onchain=onchain, own_capital=own, deposits_held=held,
                own_per_deposit=own/held, max_guarded_vault=2*vault)
if __name__ == '__main__':
    for k, v in capital().items(): print(f"{k:>20}: {v:.3f}")
    print()
    for S in (0.0, 0.25, 0.5):
        c = capital(S=S); print(f"S={S}: own={c['own_capital']:.2f} cust_cap={c['customer_capacity']:.2f} own/deposit={c['own_per_deposit']:.2f}")
    for rho in (0.4, 0.5, 0.6):
        c = capital(rho=rho); print(f"rho={rho}: own={c['own_capital']:.2f}  own/deposit={c['own_per_deposit']:.2f}")

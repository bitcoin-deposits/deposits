"""Operator capital requirement calculator (see 09-guidance and the ROI discussion)."""
def capital(L=3, D_max=1.0, rho=0.4, u=0.7, w=0.2, r=0.5, concurrent_disputes=1,
            rotations_per_year=26, feerate_sat_vb=20, dispute_allowance_btc=0.005):
    vault = D_max / rho
    vaults = L * vault
    float_liquid = L * u * D_max * w
    arm = concurrent_disputes * u * D_max * r
    onchain = L * rotations_per_year * 180 * feerate_sat_vb / 1e8 + dispute_allowance_btc
    own = vaults + float_liquid + arm + onchain
    held = L * u * D_max
    return dict(vault_each=vault, vaults=vaults, float_liquid=float_liquid, arm_reserve=arm,
                onchain=onchain, own_capital=own, deposits_held=held,
                own_per_deposit=own/held, max_guarded_vault=2*vault)
if __name__ == '__main__':
    for k, v in capital().items(): print(f"{k:>20}: {v:.3f}")
    print()
    for rho in (0.4, 0.5, 0.6):
        c = capital(rho=rho); print(f"rho={rho}: own={c['own_capital']:.2f}  own/deposit={c['own_per_deposit']:.2f}")

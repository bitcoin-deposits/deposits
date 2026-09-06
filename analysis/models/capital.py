"""Operator capital requirement calculator.

Deposited coins are held by the operator, not the quorum, so they fund the vault.
Net own capital = vault - customer deposits + liquidity buffer + arming reserve + fees.
Self-fill is a ledger entry against spare capacity; it costs capacity, not capital.
"""
def capital(L=3, D_max=1.0, rho=0.4, u=0.7, w=0.2, r=0.5, concurrent_disputes=1,
            rotations_per_year=26, feerate_sat_vb=20, dispute_allowance_btc=0.005,
            S=0.0, guarded_selffill=0.0):
    vault = D_max / rho
    cust_cap = D_max - S
    deposits = L * u * cust_cap
    vaults = L * vault
    buffer = w * deposits
    arm = concurrent_disputes * r * (u * D_max + guarded_selffill * D_max)
    onchain = L * rotations_per_year * 180 * feerate_sat_vb / 1e8 + dispute_allowance_btc
    own = vaults - deposits + buffer + arm + onchain
    return dict(vault_each=vault, vaults=vaults, deposits_held=deposits, deposits_fund_vault=deposits,
                liquidity_buffer=buffer, arm_reserve=arm, onchain=onchain,
                own_capital=own, own_per_deposit=own/deposits if deposits else float('inf'),
                customer_capacity=L*cust_cap, max_guarded_vault=2*vault)
if __name__ == '__main__':
    for k, v in capital().items(): print(f"{k:>20}: {v:.3f}")
    print()
    for rho in (0.4, 0.5, 0.6):
        for u in (0.7, 1.0):
            c = capital(rho=rho, u=u); print(f"rho={rho} u={u}: own={c['own_capital']:.2f} own/deposit={c['own_per_deposit']:.2f}")
    for S in (0.0, 0.25, 0.5):
        c = capital(S=S); print(f"S={S}: own={c['own_capital']:.2f} cust_cap={c['customer_capacity']:.2f} own/deposit={c['own_per_deposit']:.2f}")

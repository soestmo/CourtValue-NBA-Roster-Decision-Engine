import numpy as np

from schemas.canonical_player_schema import CostEfficiencyScore, PlayerContract, ProjectedContribution, PlayerSeasonStats


def compute_cost_efficiency(
    player: PlayerSeasonStats,
    contract: PlayerContract,
    projection: ProjectedContribution,
) -> CostEfficiencyScore:
    norm_salary = contract.salary / 50.0
    contribution = projection.projected_contribution_score / 100.0
    base_ratio = contribution / max(norm_salary, 0.05)

    years_penalty = 1.0 - 0.06 * max(contract.years_remaining - 2, 0)
    age_penalty = 1.0 - 0.07 * max(player.age - 30, 0)
    adjusted_ratio = max(base_ratio * years_penalty * age_penalty, 0.0)

    cost_eff = float(np.clip(adjusted_ratio * 55.0, 0, 100))
    surplus = float(np.clip((contribution * 100) - (norm_salary * 50), 0, 100))

    contract_risk_raw = (
        norm_salary * 40
        + max(player.age - 30, 0) * 6
        + max(contract.years_remaining - 2, 0) * 10
    )
    contract_risk = float(np.clip(contract_risk_raw, 0, 100))

    return CostEfficiencyScore(
        cost_efficiency_score=round(cost_eff, 2),
        surplus_value_score=round(surplus, 2),
        contract_risk_score=round(contract_risk, 2),
    )

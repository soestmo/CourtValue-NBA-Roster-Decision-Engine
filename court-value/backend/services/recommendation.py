from schemas.canonical_player_schema import (
    CostEfficiencyScore,
    PlayerRecommendation,
    PlayerSeasonStats,
    ProjectedContribution,
    RosterFitScore,
)


def build_recommendation(
    player: PlayerSeasonStats,
    projection: ProjectedContribution,
    cost: CostEfficiencyScore,
    fit: RosterFitScore,
) -> PlayerRecommendation:
    flags = set(fit.explanation_tags)

    if player.age >= 32:
        flags.add("AGE_DECLINE_RISK")
    if player.games_played <= 55:
        flags.add("AVAILABILITY_RISK")
    if cost.contract_risk_score >= 70:
        flags.add("HIGH_SALARY_BURDEN")

    strong_projection = projection.projected_contribution_score >= 65
    strong_cost = cost.cost_efficiency_score >= 60 and cost.contract_risk_score < 65
    strong_fit = fit.roster_fit_score >= 60

    weak_projection = projection.projected_contribution_score < 45
    poor_fit = fit.roster_fit_score < 45
    high_risk = cost.contract_risk_score >= 75

    if strong_projection and strong_cost and strong_fit and "HIGH_SALARY_BURDEN" not in flags:
        label = "TARGET"
        reason = "Projection, value, and fit all clear target thresholds with manageable risk."
    elif weak_projection or poor_fit or high_risk:
        label = "AVOID"
        reason = "At least one core decision dimension falls below minimum threshold for acquisition."
    else:
        label = "NEUTRAL"
        reason = "Mixed signal profile suggests situational interest rather than a firm target."

    return PlayerRecommendation(
        recommendation_label=label,
        risk_flags=sorted(flags),
        recommendation_reasoning=reason,
    )

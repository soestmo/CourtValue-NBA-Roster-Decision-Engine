from schemas.canonical_player_schema import PlayerContract, PlayerSeasonStats, ProjectedContribution, TeamContext
from services.cost_efficiency import compute_cost_efficiency
from services.recommendation import build_recommendation
from services.roster_fit import compute_roster_fit


def build_player(age: int = 27) -> PlayerSeasonStats:
    return PlayerSeasonStats(
        player_id=1,
        player_name="Test Player",
        age=age,
        minutes_per_game=32,
        games_played=74,
        usage_rate=24,
        true_shooting_pct=0.6,
        effective_fg_pct=0.56,
        assist_pct=18,
        rebound_pct=11,
        steal_pct=1.8,
        block_pct=1.0,
        turnover_pct=11,
        three_point_attempt_rate=0.44,
        free_throw_rate=0.26,
        bpm_proxy=3.1,
        on_off_net_proxy=4.0,
        primary_role="3-and-D Wing",
    )


def test_scoring_ranges() -> None:
    player = build_player()
    contract = PlayerContract(player_id=1, salary=22, years_remaining=3, contract_type="veteran_mid")
    projection = ProjectedContribution(
        projected_contribution_year_1=62,
        projected_contribution_year_2=60,
        projected_contribution_year_3=58,
        projection_uncertainty_low=55,
        projection_uncertainty_high=68,
        projected_contribution_score=72,
    )
    team = TeamContext(
        team_code="SAC",
        needs_spacing="high",
        needs_secondary_playmaking="medium",
        needs_wing_defense="high",
        needs_rim_protection="medium",
        contention_window="now_to_3_years",
    )

    cost = compute_cost_efficiency(player, contract, projection)
    fit = compute_roster_fit(player, team)
    rec = build_recommendation(player, projection, cost, fit)

    assert 0 <= cost.cost_efficiency_score <= 100
    assert 0 <= fit.roster_fit_score <= 100
    assert rec.recommendation_label in {"TARGET", "NEUTRAL", "AVOID"}

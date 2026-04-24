from schemas.canonical_player_schema import PlayerSeasonStats, RosterFitScore, TeamContext


def _weight(need: str) -> float:
    return {"low": 0.8, "medium": 1.0, "high": 1.2}[need]


def compute_roster_fit(player: PlayerSeasonStats, team_context: TeamContext) -> RosterFitScore:
    spacing_score = min(100.0, (player.three_point_attempt_rate * 100 + player.true_shooting_pct * 100) / 2)
    playmaking_score = min(100.0, player.assist_pct * 2.6)
    wing_def_score = min(100.0, player.steal_pct * 18 + player.block_pct * 10 + max(player.on_off_net_proxy, -5) * 3)
    rim_score = min(100.0, player.block_pct * 20 + player.rebound_pct * 2.2)

    offense = 0.55 * spacing_score * _weight(team_context.needs_spacing) + 0.45 * playmaking_score * _weight(team_context.needs_secondary_playmaking)
    defense = 0.6 * wing_def_score * _weight(team_context.needs_wing_defense) + 0.4 * rim_score * _weight(team_context.needs_rim_protection)

    if team_context.contention_window == "now_to_3_years":
        timeline = max(0.0, 100.0 - abs(player.age - 27) * 6.5)
    else:
        timeline = max(0.0, 100.0 - abs(player.age - 24) * 6.5)

    usage_penalty = max(0.0, (player.usage_rate - 27) * 2.8)
    redundancy_penalty = 0.55 * usage_penalty

    fit_score = 0.45 * offense + 0.4 * defense + 0.25 * timeline - 0.3 * redundancy_penalty
    fit_score = max(0.0, min(100.0, fit_score))

    tags: list[str] = []
    if spacing_score < 45:
        tags.append("LOW_SPACING")
    if defense < 45:
        tags.append("DEFENSIVE_WEAKNESS")
    if usage_penalty > 15:
        tags.append("USAGE_CONFLICT")
    if timeline < 45:
        tags.append("POOR_TIMELINE_ALIGNMENT")

    return RosterFitScore(
        roster_fit_score=round(fit_score, 2),
        fit_offense_score=round(min(offense, 100.0), 2),
        fit_defense_score=round(min(defense, 100.0), 2),
        fit_timeline_score=round(timeline, 2),
        fit_redundancy_penalty=round(min(redundancy_penalty, 100.0), 2),
        explanation_tags=tags,
    )

from typing import List, Literal

from pydantic import BaseModel, Field


class PlayerSeasonStats(BaseModel):
    player_id: int
    player_name: str
    age: int = Field(ge=18, le=45)
    minutes_per_game: float = Field(ge=0)
    games_played: int = Field(ge=0, le=82)
    usage_rate: float = Field(ge=0)
    true_shooting_pct: float = Field(ge=0, le=1)
    effective_fg_pct: float = Field(ge=0, le=1)
    assist_pct: float = Field(ge=0)
    rebound_pct: float = Field(ge=0)
    steal_pct: float = Field(ge=0)
    block_pct: float = Field(ge=0)
    turnover_pct: float = Field(ge=0)
    three_point_attempt_rate: float = Field(ge=0, le=1)
    free_throw_rate: float = Field(ge=0)
    bpm_proxy: float
    on_off_net_proxy: float
    primary_role: str


class PlayerContract(BaseModel):
    player_id: int
    salary: float = Field(ge=0)
    years_remaining: int = Field(ge=0)
    contract_type: str


class TeamContext(BaseModel):
    team_code: str
    needs_spacing: Literal["low", "medium", "high"]
    needs_secondary_playmaking: Literal["low", "medium", "high"]
    needs_wing_defense: Literal["low", "medium", "high"]
    needs_rim_protection: Literal["low", "medium", "high"]
    contention_window: str


class ProjectedContribution(BaseModel):
    projected_contribution_year_1: float
    projected_contribution_year_2: float
    projected_contribution_year_3: float
    projection_uncertainty_low: float
    projection_uncertainty_high: float
    projected_contribution_score: float = Field(ge=0, le=100)


class CostEfficiencyScore(BaseModel):
    cost_efficiency_score: float = Field(ge=0, le=100)
    surplus_value_score: float = Field(ge=0, le=100)
    contract_risk_score: float = Field(ge=0, le=100)


class RosterFitScore(BaseModel):
    roster_fit_score: float = Field(ge=0, le=100)
    fit_offense_score: float = Field(ge=0, le=100)
    fit_defense_score: float = Field(ge=0, le=100)
    fit_timeline_score: float = Field(ge=0, le=100)
    fit_redundancy_penalty: float = Field(ge=0, le=100)
    explanation_tags: List[str]


class PlayerRecommendation(BaseModel):
    recommendation_label: Literal["TARGET", "NEUTRAL", "AVOID"]
    risk_flags: List[str]
    recommendation_reasoning: str


class CanonicalPlayerEvaluation(BaseModel):
    player: PlayerSeasonStats
    contract: PlayerContract
    team_context: TeamContext
    projected_contribution: ProjectedContribution
    cost_efficiency: CostEfficiencyScore
    roster_fit: RosterFitScore
    recommendation: PlayerRecommendation

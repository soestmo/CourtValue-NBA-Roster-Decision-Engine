from __future__ import annotations

from typing import List

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from schemas.canonical_player_schema import (
    CanonicalPlayerEvaluation,
    PlayerContract,
    PlayerSeasonStats,
    TeamContext,
)
from schemas.model_explainability_schema import GlobalImportanceSummary, LocalExplanationSummary
from services.contribution_model import ContributionModelService
from services.cost_efficiency import compute_cost_efficiency
from services.data_loader import get_player_row, get_team_context, load_players, load_team_contexts
from services.explainability import global_importance, local_explanation
from services.recommendation import build_recommendation
from services.roster_fit import compute_roster_fit

app = FastAPI(title="CourtValue API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

players_df = load_players()
team_contexts_df = load_team_contexts()
contribution_service = ContributionModelService()
contribution_service.train(players_df)


def _build_player_schema(row) -> PlayerSeasonStats:
    return PlayerSeasonStats(
        player_id=int(row["player_id"]),
        player_name=row["player_name"],
        age=int(row["age"]),
        minutes_per_game=float(row["minutes_per_game"]),
        games_played=int(row["games_played"]),
        usage_rate=float(row["usage_rate"]),
        true_shooting_pct=float(row["true_shooting_pct"]),
        effective_fg_pct=float(row["effective_fg_pct"]),
        assist_pct=float(row["assist_pct"]),
        rebound_pct=float(row["rebound_pct"]),
        steal_pct=float(row["steal_pct"]),
        block_pct=float(row["block_pct"]),
        turnover_pct=float(row["turnover_pct"]),
        three_point_attempt_rate=float(row["three_point_attempt_rate"]),
        free_throw_rate=float(row["free_throw_rate"]),
        bpm_proxy=float(row["bpm_proxy"]),
        on_off_net_proxy=float(row["on_off_net_proxy"]),
        primary_role=row["primary_role"],
    )


def _build_contract_schema(row) -> PlayerContract:
    return PlayerContract(
        player_id=int(row["player_id"]),
        salary=float(row["salary"]),
        years_remaining=int(row["years_remaining"]),
        contract_type=row["contract_type"],
    )


def _build_team_context_schema(row) -> TeamContext:
    return TeamContext(
        team_code=row["team_code"],
        needs_spacing=row["needs_spacing"],
        needs_secondary_playmaking=row["needs_secondary_playmaking"],
        needs_wing_defense=row["needs_wing_defense"],
        needs_rim_protection=row["needs_rim_protection"],
        contention_window=row["contention_window"],
    )


def evaluate_player(player_id: int, team_code: str) -> CanonicalPlayerEvaluation:
    player_row = get_player_row(players_df, player_id)
    if player_row is None:
        raise HTTPException(status_code=404, detail=f"Player id {player_id} not found")

    team_context_row = get_team_context(team_contexts_df, team_code)
    if team_context_row is None:
        raise HTTPException(status_code=404, detail=f"Team context {team_code} not found")

    player = _build_player_schema(player_row)
    contract = _build_contract_schema(player_row)
    team_context = _build_team_context_schema(team_context_row)

    projection = contribution_service.predict_player(player_row)
    cost = compute_cost_efficiency(player, contract, projection)
    fit = compute_roster_fit(player, team_context)
    recommendation = build_recommendation(player, projection, cost, fit)

    return CanonicalPlayerEvaluation(
        player=player,
        contract=contract,
        team_context=team_context,
        projected_contribution=projection,
        cost_efficiency=cost,
        roster_fit=fit,
        recommendation=recommendation,
    )


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "players_loaded": int(len(players_df))}


@app.get("/players")
def list_players() -> List[dict]:
    return players_df[["player_id", "player_name", "primary_role", "age", "salary"]].to_dict(orient="records")


@app.get("/players/{player_id}")
def get_player(player_id: int) -> dict:
    row = get_player_row(players_df, player_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Player id {player_id} not found")
    return row.to_dict()


@app.get("/evaluate/{player_id}", response_model=CanonicalPlayerEvaluation)
def evaluate(player_id: int, team_context: str = Query(default="SAC")) -> CanonicalPlayerEvaluation:
    return evaluate_player(player_id, team_context)


@app.get("/compare", response_model=List[CanonicalPlayerEvaluation])
def compare(player_ids: str, team_context: str = Query(default="SAC")) -> List[CanonicalPlayerEvaluation]:
    parsed_ids = [int(pid.strip()) for pid in player_ids.split(",") if pid.strip()]
    return [evaluate_player(pid, team_context) for pid in parsed_ids]


@app.get("/model/feature-importance", response_model=List[GlobalImportanceSummary])
def model_feature_importance() -> List[GlobalImportanceSummary]:
    return global_importance(contribution_service, top_n=10)


@app.get("/explain/{player_id}", response_model=LocalExplanationSummary)
def explain_player(player_id: int) -> LocalExplanationSummary:
    row = get_player_row(players_df, player_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Player id {player_id} not found")
    return local_explanation(contribution_service, row, row["player_name"], int(row["player_id"]))

# Roster Decision Engine: Model and Features

## Modeling Boundary
- XGBoost is only used for projected contribution.
- Cost efficiency and roster fit remain deterministic.
- No agents in V1.

## Features
- age
- age_squared
- minutes_per_game
- games_played
- usage_rate
- true_shooting_pct
- effective_fg_pct
- assist_pct
- rebound_pct
- steal_pct
- block_pct
- turnover_pct
- three_point_attempt_rate
- free_throw_rate
- bpm_proxy
- on_off_net_proxy
- salary
- years_remaining

## Synthetic Training Target
`future_impact_proxy` combines:
- bpm_proxy,
- on_off_net_proxy,
- minutes_per_game,
- true_shooting_pct,
- age curve,
- games_played.

## Decision Outputs
- projected contribution (with 3-year view and uncertainty)
- cost efficiency, surplus value, contract risk
- roster fit (offense, defense, timeline, redundancy)
- recommendation label: TARGET / NEUTRAL / AVOID

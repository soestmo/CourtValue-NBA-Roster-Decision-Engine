from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor

from schemas.canonical_player_schema import ProjectedContribution
from services.feature_pipeline import build_feature_frame, build_future_impact_proxy


@dataclass
class ContributionArtifacts:
    model: XGBRegressor
    feature_df: pd.DataFrame
    target: pd.Series
    residual_mae: float
    target_min: float
    target_max: float


class ContributionModelService:
    def __init__(self) -> None:
        self.artifacts: ContributionArtifacts | None = None

    def train(self, player_df: pd.DataFrame) -> None:
        features = build_feature_frame(player_df)
        target = build_future_impact_proxy(player_df)
        model = XGBRegressor(
            n_estimators=250,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.95,
            colsample_bytree=0.95,
            random_state=42,
            objective="reg:squarederror",
        )
        model.fit(features, target)
        preds = model.predict(features)
        mae = float(mean_absolute_error(target, preds))
        self.artifacts = ContributionArtifacts(
            model=model,
            feature_df=features,
            target=target,
            residual_mae=mae,
            target_min=float(target.min()),
            target_max=float(target.max()),
        )

    def _require_artifacts(self) -> ContributionArtifacts:
        if self.artifacts is None:
            raise RuntimeError("Contribution model has not been trained.")
        return self.artifacts

    def predict_player(self, player_row: pd.Series) -> ProjectedContribution:
        artifacts = self._require_artifacts()
        row_df = pd.DataFrame([player_row.to_dict()])
        features = build_feature_frame(row_df)
        y1 = float(artifacts.model.predict(features)[0])
        age = float(player_row["age"])
        y2 = y1 * (0.97 if age < 29 else 0.94)
        y3 = y2 * (0.97 if age < 29 else 0.93)
        spread = artifacts.residual_mae * 1.5
        low = y1 - spread
        high = y1 + spread
        score = 100.0 * (y1 - artifacts.target_min) / max(artifacts.target_max - artifacts.target_min, 1e-9)
        score = float(np.clip(score, 0.0, 100.0))
        return ProjectedContribution(
            projected_contribution_year_1=round(y1, 2),
            projected_contribution_year_2=round(y2, 2),
            projected_contribution_year_3=round(y3, 2),
            projection_uncertainty_low=round(low, 2),
            projection_uncertainty_high=round(high, 2),
            projected_contribution_score=round(score, 2),
        )

    def feature_importance_gain(self, top_n: int = 10) -> list[tuple[str, float]]:
        artifacts = self._require_artifacts()
        booster = artifacts.model.get_booster()
        gain_scores = booster.get_score(importance_type="gain")
        remapped = [(k, float(v)) for k, v in gain_scores.items()]
        remapped.sort(key=lambda x: x[1], reverse=True)
        return remapped[:top_n]

from __future__ import annotations

import pandas as pd
import shap

from schemas.model_explainability_schema import FeatureAttribution, GlobalImportanceSummary, LocalExplanationSummary
from services.contribution_model import ContributionModelService
from services.feature_pipeline import build_feature_frame


def _interpret(feature_name: str, shap_value: float) -> str:
    direction = "supports" if shap_value >= 0 else "reduces"
    return f"{feature_name} {direction} the projected contribution estimate."


def global_importance(model_service: ContributionModelService, top_n: int = 10) -> list[GlobalImportanceSummary]:
    rows = model_service.feature_importance_gain(top_n=top_n)
    return [GlobalImportanceSummary(feature_name=k, importance_gain=round(v, 4)) for k, v in rows]


def local_explanation(
    model_service: ContributionModelService,
    player_row: pd.Series,
    player_name: str,
    player_id: int,
    top_n: int = 5,
) -> LocalExplanationSummary:
    artifacts = model_service._require_artifacts()
    feature_df = build_feature_frame(pd.DataFrame([player_row.to_dict()]))
    explainer = shap.TreeExplainer(artifacts.model)
    shap_values = explainer.shap_values(feature_df)
    base_value = float(explainer.expected_value)

    attributions: list[FeatureAttribution] = []
    values = shap_values[0]
    columns = feature_df.columns.tolist()
    for idx, feature_name in enumerate(columns):
        shap_value = float(values[idx])
        raw_value = float(feature_df.iloc[0, idx])
        attributions.append(
            FeatureAttribution(
                feature_name=feature_name,
                raw_value=round(raw_value, 4),
                shap_value=round(shap_value, 4),
                direction="positive" if shap_value >= 0 else "negative",
                interpretation=_interpret(feature_name, shap_value),
            )
        )

    positives = sorted([a for a in attributions if a.shap_value >= 0], key=lambda x: x.shap_value, reverse=True)[:top_n]
    negatives = sorted([a for a in attributions if a.shap_value < 0], key=lambda x: x.shap_value)[:top_n]
    pred = float(artifacts.model.predict(feature_df)[0])

    return LocalExplanationSummary(
        player_id=player_id,
        player_name=player_name,
        base_value=round(base_value, 4),
        predicted_value=round(pred, 4),
        top_positive_drivers=positives,
        top_negative_drivers=negatives,
    )

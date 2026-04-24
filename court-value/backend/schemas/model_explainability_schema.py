from typing import List, Literal

from pydantic import BaseModel


class FeatureAttribution(BaseModel):
    feature_name: str
    raw_value: float
    shap_value: float
    direction: Literal["positive", "negative"]
    interpretation: str


class GlobalImportanceSummary(BaseModel):
    feature_name: str
    importance_gain: float


class LocalExplanationSummary(BaseModel):
    player_id: int
    player_name: str
    base_value: float
    predicted_value: float
    top_positive_drivers: List[FeatureAttribution]
    top_negative_drivers: List[FeatureAttribution]


class ModelExplainabilityReport(BaseModel):
    global_importance: List[GlobalImportanceSummary]
    local_explanation: LocalExplanationSummary

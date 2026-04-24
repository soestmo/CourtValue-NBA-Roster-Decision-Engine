export type PlayerSummary = {
  player_id: number;
  player_name: string;
  primary_role: string;
  age: number;
  salary: number;
};

export type FeatureAttribution = {
  feature_name: string;
  raw_value: number;
  shap_value: number;
  direction: "positive" | "negative";
  interpretation: string;
};

export type GlobalImportanceSummary = {
  feature_name: string;
  importance_gain: number;
};

export type LocalExplanationSummary = {
  player_id: number;
  player_name: string;
  base_value: number;
  predicted_value: number;
  top_positive_drivers: FeatureAttribution[];
  top_negative_drivers: FeatureAttribution[];
};

export type CanonicalPlayerEvaluation = {
  player: {
    player_id: number;
    player_name: string;
    age: number;
    primary_role: string;
  };
  projected_contribution: {
    projected_contribution_year_1: number;
    projected_contribution_year_2: number;
    projected_contribution_year_3: number;
    projection_uncertainty_low: number;
    projection_uncertainty_high: number;
    projected_contribution_score: number;
  };
  cost_efficiency: {
    cost_efficiency_score: number;
    surplus_value_score: number;
    contract_risk_score: number;
  };
  roster_fit: {
    roster_fit_score: number;
  };
  recommendation: {
    recommendation_label: "TARGET" | "NEUTRAL" | "AVOID";
    risk_flags: string[];
    recommendation_reasoning: string;
  };
};

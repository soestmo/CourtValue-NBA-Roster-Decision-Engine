import type { CanonicalPlayerEvaluation } from "../types";

type Props = { evaluation: CanonicalPlayerEvaluation | null };

export default function PlayerEvaluationCard({ evaluation }: Props) {
  if (!evaluation) return null;

  const p = evaluation.projected_contribution;
  const c = evaluation.cost_efficiency;
  const r = evaluation.recommendation;

  return (
    <div className="card">
      <h3>{evaluation.player.player_name}</h3>
      <p><b>Recommendation:</b> {r.recommendation_label}</p>
      <p><b>Projected Contribution Score:</b> {p.projected_contribution_score}</p>
      <p><b>Y1-Y3:</b> {p.projected_contribution_year_1} / {p.projected_contribution_year_2} / {p.projected_contribution_year_3}</p>
      <p><b>Uncertainty:</b> {p.projection_uncertainty_low} to {p.projection_uncertainty_high}</p>
      <p><b>Cost Efficiency:</b> {c.cost_efficiency_score}</p>
      <p><b>Surplus Value:</b> {c.surplus_value_score}</p>
      <p><b>Contract Risk:</b> {c.contract_risk_score}</p>
      <p><b>Roster Fit:</b> {evaluation.roster_fit.roster_fit_score}</p>
      <p><b>Risk Flags:</b> {r.risk_flags.join(", ") || "None"}</p>
      <p><b>Reasoning:</b> {r.recommendation_reasoning}</p>
    </div>
  );
}

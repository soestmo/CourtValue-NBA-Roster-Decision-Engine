import type { LocalExplanationSummary } from "../types";

type Props = { explanation: LocalExplanationSummary | null };

export default function ShapDriverPanel({ explanation }: Props) {
  if (!explanation) return null;
  return (
    <div className="card">
      <h3>SHAP Driver Panel</h3>
      <p><b>Base:</b> {explanation.base_value} | <b>Predicted:</b> {explanation.predicted_value}</p>
      <div className="grid-two">
        <div>
          <h4>Top Positive Drivers</h4>
          <ul>
            {explanation.top_positive_drivers.map((d) => (
              <li key={`${d.feature_name}-pos`}>{d.feature_name}: +{d.shap_value} ({d.interpretation})</li>
            ))}
          </ul>
        </div>
        <div>
          <h4>Top Negative Drivers</h4>
          <ul>
            {explanation.top_negative_drivers.map((d) => (
              <li key={`${d.feature_name}-neg`}>{d.feature_name}: {d.shap_value} ({d.interpretation})</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

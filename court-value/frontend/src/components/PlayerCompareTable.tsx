import type { CanonicalPlayerEvaluation } from "../types";

type Props = { items: CanonicalPlayerEvaluation[] };

export default function PlayerCompareTable({ items }: Props) {
  if (!items.length) return null;

  return (
    <div className="card">
      <h3>Comparison</h3>
      <table>
        <thead>
          <tr>
            <th>Player</th>
            <th>Projection</th>
            <th>Cost Eff.</th>
            <th>Fit</th>
            <th>Recommendation</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.player.player_id}>
              <td>{item.player.player_name}</td>
              <td>{item.projected_contribution.projected_contribution_score}</td>
              <td>{item.cost_efficiency.cost_efficiency_score}</td>
              <td>{item.roster_fit.roster_fit_score}</td>
              <td>{item.recommendation.recommendation_label}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

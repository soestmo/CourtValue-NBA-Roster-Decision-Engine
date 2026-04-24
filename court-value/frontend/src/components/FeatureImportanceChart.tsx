import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { GlobalImportanceSummary } from "../types";

type Props = { data: GlobalImportanceSummary[] };

export default function FeatureImportanceChart({ data }: Props) {
  if (!data.length) return null;
  return (
    <div className="card" style={{ height: 360 }}>
      <h3>Global Feature Importance (Top 10)</h3>
      <ResponsiveContainer width="100%" height="90%">
        <BarChart data={data} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" />
          <YAxis type="category" dataKey="feature_name" width={160} />
          <Tooltip />
          <Bar dataKey="importance_gain" fill="#4f46e5" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

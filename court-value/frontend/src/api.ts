import type {
  CanonicalPlayerEvaluation,
  GlobalImportanceSummary,
  LocalExplanationSummary,
  PlayerSummary,
} from "./types";

const API_BASE = "http://localhost:8000";

export async function fetchPlayers(): Promise<PlayerSummary[]> {
  const res = await fetch(`${API_BASE}/players`);
  if (!res.ok) throw new Error("Failed to fetch players");
  return res.json();
}

export async function fetchEvaluation(playerId: number): Promise<CanonicalPlayerEvaluation> {
  const res = await fetch(`${API_BASE}/evaluate/${playerId}?team_context=SAC`);
  if (!res.ok) throw new Error("Failed to fetch evaluation");
  return res.json();
}

export async function fetchComparison(playerIds: number[]): Promise<CanonicalPlayerEvaluation[]> {
  const query = playerIds.join(",");
  const res = await fetch(`${API_BASE}/compare?player_ids=${query}&team_context=SAC`);
  if (!res.ok) throw new Error("Failed to fetch comparison");
  return res.json();
}

export async function fetchFeatureImportance(): Promise<GlobalImportanceSummary[]> {
  const res = await fetch(`${API_BASE}/model/feature-importance`);
  if (!res.ok) throw new Error("Failed to fetch feature importance");
  return res.json();
}

export async function fetchExplanation(playerId: number): Promise<LocalExplanationSummary> {
  const res = await fetch(`${API_BASE}/explain/${playerId}`);
  if (!res.ok) throw new Error("Failed to fetch explanation");
  return res.json();
}

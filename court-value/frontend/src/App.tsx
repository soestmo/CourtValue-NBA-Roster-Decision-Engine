import { useEffect, useState } from "react";
import { fetchComparison, fetchEvaluation, fetchExplanation, fetchFeatureImportance, fetchPlayers } from "./api";
import FeatureImportanceChart from "./components/FeatureImportanceChart";
import PlayerCompareTable from "./components/PlayerCompareTable";
import PlayerEvaluationCard from "./components/PlayerEvaluationCard";
import PlayerSearch from "./components/PlayerSearch";
import ShapDriverPanel from "./components/ShapDriverPanel";
import type {
  CanonicalPlayerEvaluation,
  GlobalImportanceSummary,
  LocalExplanationSummary,
  PlayerSummary,
} from "./types";

export default function App() {
  const [players, setPlayers] = useState<PlayerSummary[]>([]);
  const [selectedPlayerId, setSelectedPlayerId] = useState<number>(1);
  const [evaluation, setEvaluation] = useState<CanonicalPlayerEvaluation | null>(null);
  const [comparison, setComparison] = useState<CanonicalPlayerEvaluation[]>([]);
  const [importance, setImportance] = useState<GlobalImportanceSummary[]>([]);
  const [explanation, setExplanation] = useState<LocalExplanationSummary | null>(null);

  useEffect(() => {
    async function loadInitial() {
      const playerList = await fetchPlayers();
      setPlayers(playerList);
      if (playerList.length) {
        setSelectedPlayerId(playerList[0].player_id);
        const compareIds = playerList.slice(0, 3).map((p) => p.player_id);
        const [compareData, imp] = await Promise.all([
          fetchComparison(compareIds),
          fetchFeatureImportance(),
        ]);
        setComparison(compareData);
        setImportance(imp);
      }
    }
    loadInitial();
  }, []);

  useEffect(() => {
    async function loadPlayerDetails() {
      if (!selectedPlayerId) return;
      const [ev, exp] = await Promise.all([
        fetchEvaluation(selectedPlayerId),
        fetchExplanation(selectedPlayerId),
      ]);
      setEvaluation(ev);
      setExplanation(exp);
    }
    loadPlayerDetails();
  }, [selectedPlayerId]);

  return (
    <main className="container">
      <h1>CourtValue</h1>
      <p className="subtitle">NBA Roster Decision Engine</p>
      <PlayerSearch players={players} selectedPlayerId={selectedPlayerId} onChange={setSelectedPlayerId} />
      <PlayerEvaluationCard evaluation={evaluation} />
      <PlayerCompareTable items={comparison} />
      <FeatureImportanceChart data={importance} />
      <ShapDriverPanel explanation={explanation} />
    </main>
  );
}

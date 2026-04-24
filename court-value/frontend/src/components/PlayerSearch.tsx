import type { PlayerSummary } from "../types";

type Props = {
  players: PlayerSummary[];
  selectedPlayerId: number;
  onChange: (id: number) => void;
};

export default function PlayerSearch({ players, selectedPlayerId, onChange }: Props) {
  return (
    <div className="card">
      <h3>Player Selector</h3>
      <select
        value={selectedPlayerId}
        onChange={(e) => onChange(Number(e.target.value))}
        className="input"
      >
        {players.map((p) => (
          <option key={p.player_id} value={p.player_id}>
            {p.player_name} ({p.primary_role})
          </option>
        ))}
      </select>
    </div>
  );
}

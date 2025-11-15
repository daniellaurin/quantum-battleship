// src/api/quantumApi.ts
const API_BASE_URL = 'http://localhost:5001/api/quantum';

export interface QuantumGameState {
  game_id: string;
  grid_size: number;
  current_round: number;
  game_over: boolean;
  winner: number | null;
  player1_ships?: number[];
  player2_ships?: number[];
  player1_damage?: number[];
  player2_damage?: number[];
  player1_bombs?: number[];
  player2_bombs?: number[];
}

export interface BombResult {
  success: boolean;
  player: number;
  bomb_position: number;
  hit_ship: boolean;
  quantum_measurements: {
    circuit: string;
    counts: Record<string, number>;
    probabilities: number[];
    total_shots: number;
  };
  damage_results: {
    probabilities: number[];
    damage_percentages: number[];
    updated_damage: number[];
    ship_damage: Record<string, number>;
    destroyed_ships: number[];
    all_ships_destroyed: boolean;
  };
  game_over: boolean;
  winner: number | null;
  round: number;
}

export const quantumApi = {
  // Create new game
  createGame: async (): Promise<{ game_id: string }> => {
    const response = await fetch(`${API_BASE_URL}/game/new`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({}),
    });
    const data = await response.json();
    return data;
  },

  // Set ship positions
  setShips: async (gameId: string, player: number, positions: number[]): Promise<any> => {
    const response = await fetch(`${API_BASE_URL}/game/${gameId}/set-ships`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ player, positions }),
    });
    return response.json();
  },

  // Bomb a position
  bomb: async (gameId: string, player: number, position: number): Promise<BombResult> => {
    const response = await fetch(`${API_BASE_URL}/game/${gameId}/bomb`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ player, position }),
    });
    return response.json();
  },

  // Get game state
  getGameState: async (gameId: string, view: number = 0): Promise<{ state: QuantumGameState }> => {
    const response = await fetch(`${API_BASE_URL}/game/${gameId}?view=${view}`);
    return response.json();
  },

  // Get visualization
  getVisualization: async (gameId: string): Promise<any> => {
    const response = await fetch(`${API_BASE_URL}/game/${gameId}/visualize`);
    return response.json();
  },

  // Auto-setup (for testing)
  autoSetup: async (gameId: string): Promise<any> => {
    const response = await fetch(`${API_BASE_URL}/game/${gameId}/auto-setup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    return response.json();
  },
};
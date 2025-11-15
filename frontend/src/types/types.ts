// src/types/types.ts
export type ShipType = {
  name: string;
  size: number; // For quantum version, size = 1 (each ship is 1 cell)
  hits: number;
  orientation: 'horizontal' | 'vertical';
  position?: number; // Single position (0-4) for quantum version
  iconPath: string;
  damage?: number; // Damage percentage (0-100)
};

export type CellState = 'empty' | 'ship' | 'hit' | 'miss' | 'damaged';

export type Coords = {
  x: number;
  y: number;
};

export type QuantumShip = {
  name: string;
  position: number; // 0-4
  damage: number; // 0-100%
  iconPath: string;
};

export type GamePhase = 'setup' | 'player-turn' | 'ai-turn' | 'game-over';
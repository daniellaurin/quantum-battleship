export type ShipType = {
  name: string;
  size: number;
  hits: number;
  orientation: 'horizontal' | 'vertical';
  position?: Coords;
  iconPath: string;
};

export type CellState = 'empty' | 'ship' | 'hit' | 'miss';

export type Coords = {
  x: number;
  y: number;
};

export type ShipPlacement = {
  ship: ShipType;
  coords: Coords;
  orientation: 'horizontal' | 'vertical';
};

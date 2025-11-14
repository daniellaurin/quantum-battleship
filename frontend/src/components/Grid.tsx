import React from 'react';
import type { CellState, Coords, ShipType } from '../types/types';
import './Grid.css';

const GRID_SIZE = 10;

interface GridProps {
  grid: CellState[][];
  selectedShip: ShipType | null;
  onPlaceShip: (coords: Coords) => void;
}

const Grid: React.FC<GridProps> = ({ grid, selectedShip, onPlaceShip }) => {
  const [hoveredCells, setHoveredCells] = React.useState<Coords[]>([]);

  const handleMouseEnter = (x: number, y: number) => {
    if (!selectedShip) return;

    const cells: Coords[] = [];
    for (let i = 0; i < selectedShip.size; i++) {
      if (selectedShip.orientation === 'horizontal') {
        cells.push({ x: x + i, y });
      } else {
        cells.push({ x, y: y + i });
      }
    }
    setHoveredCells(cells);
  };

  const handleMouseLeave = () => {
    setHoveredCells([]);
  };

  const handleClick = (x: number, y: number) => {
    onPlaceShip({ x, y });
  };

  const renderGrid = () => {
    const cells = [];
    for (let y = 0; y < GRID_SIZE; y++) {
      for (let x = 0; x < GRID_SIZE; x++) {
        const isHovered = hoveredCells.some(cell => cell.x === x && cell.y === y);
        const cellState = grid[y][x];
        const className = `grid-cell ${cellState} ${isHovered ? 'preview' : ''}`;
        cells.push(
          <div
            key={`${x}-${y}`}
            className={className}
            onMouseEnter={() => handleMouseEnter(x, y)}
            onMouseLeave={handleMouseLeave}
            onClick={() => handleClick(x, y)}
          />
        );
      }
    }
    return cells;
  };

  return <div className="grid-container">{renderGrid()}</div>;
};

export default Grid;


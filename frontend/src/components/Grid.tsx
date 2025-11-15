// src/components/Grid.tsx
import React from 'react';
import './Grid.css';

interface GridProps {
  playerShips: number[];
  opponentDamage: number[];
  onCellClick?: (position: number) => void;
  isSetupPhase: boolean;
  selectedPosition?: number | null;
}

const Grid: React.FC<GridProps> = ({
  playerShips,
  opponentDamage,
  onCellClick,
  isSetupPhase,
  selectedPosition
}) => {
  const getCellClass = (position: number) => {
    const classes = ['quantum-cell'];

    if (isSetupPhase && playerShips.includes(position)) {
      classes.push('has-ship');
    }

    if (selectedPosition === position) {
      classes.push('selected');
    }

    const damage = opponentDamage[position];
    if (damage > 0) {
      if (damage >= 95) classes.push('destroyed');
      else if (damage >= 50) classes.push('critical');
      else if (damage > 0) classes.push('damaged');
    }

    return classes.join(' ');
  };

  const getCellContent = (position: number) => {
    const damage = opponentDamage[position];

    if (isSetupPhase && playerShips.includes(position)) {
      return '🚢';
    }

    if (damage > 0) {
      return `${damage.toFixed(0)}%`;
    }

    return position;
  };

  return (
    <div className="quantum-grid-container">
      <h3 className="grid-title">
        {isSetupPhase ? 'Place Your Ships (Select 3 Positions)' : 'Attack Grid'}
      </h3>
      <div className="quantum-grid">
        {[0, 1, 2, 3, 4].map((position) => (
          <div
            key={position}
            className={getCellClass(position)}
            onClick={() => onCellClick && onCellClick(position)}
          >
            <div className="cell-label">Position {position}</div>
            <div className="cell-content">{getCellContent(position)}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Grid;
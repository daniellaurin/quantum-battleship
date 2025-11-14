import React from 'react';
import type { ShipType } from '../types/types';
import './Ship.css';

interface ShipProps {
  ship: ShipType;
}

const Ship: React.FC<ShipProps> = ({ ship }) => {
  const healthPercentage = ((ship.size - ship.hits) / ship.size) * 100;

  return (
    <div className="ship">
      <div className="ship-info">
        <img src={ship.iconPath} alt={ship.name} className="ship-icon" />
        <span className="ship-name">{ship.name}</span>
        <span className="ship-size">({ship.size})</span>
      </div>
      <div className="health-bar">
        <div
          className="health-bar-fill"
          style={{ width: `${healthPercentage}%` }}
        />
      </div>
    </div>
  );
};

export default Ship;

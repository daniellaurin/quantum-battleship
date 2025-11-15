// src/components/Ship.tsx
import React from 'react';
import './Ship.css';

interface ShipProps {
  name: string;
  position: number;
  damage: number;
  iconPath: string;
}

const Ship: React.FC<ShipProps> = ({ name, position, damage, iconPath }) => {
  const healthPercentage = 100 - damage;

  const getStatusEmoji = () => {
    if (damage >= 95) return '💀';
    if (damage >= 50) return '🔥';
    if (damage > 0) return '⚠️';
    return '✅';
  };

  return (
    <div className="ship-card">
      <div className="ship-header">
        <img src={iconPath} alt={name} className="ship-icon" />
        <div className="ship-details">
          <h3>{name}</h3>
          <p className="ship-position">Position: {position}</p>
        </div>
        <span className="ship-status">{getStatusEmoji()}</span>
      </div>
      <div className="ship-health">
        <div className="health-label">
          <span>Health: {healthPercentage.toFixed(0)}%</span>
          <span>Damage: {damage.toFixed(1)}%</span>
        </div>
        <div className="health-bar">
          <div
            className="health-bar-fill"
            style={{
              width: `${healthPercentage}%`,
              backgroundColor: damage >= 95 ? '#ff4757' : damage >= 50 ? '#ffa502' : '#0077be'
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default Ship;
// src/components/ShipInventory.tsx
import React from 'react';
import type { QuantumShip } from '../types/types';
import './ShipInventory.css';

interface ShipInventoryProps {
  ships: QuantumShip[];
  playerDamage: number[];
}

const ShipInventory: React.FC<ShipInventoryProps> = ({ ships, playerDamage }) => {
  const getShipStatus = (damage: number) => {
    if (damage >= 95) return '💀 DESTROYED';
    if (damage >= 50) return '🔥 CRITICAL';
    if (damage > 0) return '⚠️ DAMAGED';
    return '✅ OPERATIONAL';
  };

  const getHealthColor = (damage: number) => {
    if (damage >= 95) return '#ff4757';
    if (damage >= 50) return '#ffa502';
    if (damage > 0) return '#ffd700';
    return '#0077be';
  };

  return (
    <div className="quantum-ship-inventory">
      <h2>⚛️ Your Quantum Fleet</h2>
      <div className="quantum-info">
        <p>🎯 3 Ships | 5 Grid Positions</p>
        <p>📊 Damage from Quantum Measurements</p>
      </div>

      {ships.length === 0 ? (
        <div className="empty-fleet">
          <div className="empty-icon">🚢</div>
          <h3>No Ships Deployed</h3>
          <p>Select 3 positions on the grid to place your quantum fleet!</p>
          <div className="instructions">
            <p><strong>How to Play:</strong></p>
            <ul>
              <li>Click 3 grid positions (0-4)</li>
              <li>Each position holds 1 ship</li>
              <li>Attack enemy positions</li>
              <li>Quantum circuits calculate damage</li>
              <li>Destroy all 3 enemy ships to win!</li>
            </ul>
          </div>
        </div>
      ) : (
        ships.map((ship, index) => {
          const damage = playerDamage[ship.position] || 0;
          const healthPercent = 100 - damage;

          return (
            <div key={index} className="quantum-ship-card">
              <div className="ship-header">
                <img src={ship.iconPath} alt={ship.name} className="ship-icon-small" />
                <div className="ship-info">
                  <h3>{ship.name}</h3>
                  <p className="ship-position">Position: {ship.position}</p>
                </div>
              </div>

              <div className="damage-display">
                <div className="damage-label">
                  <span>Damage: {damage.toFixed(1)}%</span>
                  <span>{getShipStatus(damage)}</span>
                </div>
                <div className="health-bar-quantum">
                  <div
                    className="health-fill-quantum"
                    style={{
                      width: `${healthPercent}%`,
                      backgroundColor: getHealthColor(damage)
                    }}
                  />
                </div>
              </div>
            </div>
          );
        })
      )}
    </div>
  );
};

export default ShipInventory;
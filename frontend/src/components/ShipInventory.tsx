import React from 'react';
import type { ShipType } from '../types/types';
import Ship from './Ship';
import './ShipInventory.css';

interface ShipInventoryProps {
  ships: ShipType[];
  onSelectShip: (ship: ShipType) => void;
  onRotateShip: () => void;
  selectedShip: ShipType | null;
}

const ShipInventory: React.FC<ShipInventoryProps> = ({ ships, onSelectShip, onRotateShip, selectedShip }) => {
  return (
    <div className="ship-inventory">
      <h2>Your Fleet</h2>
      {ships.map((ship) => (
        <div
          key={ship.name}
          className={`ship-wrapper ${selectedShip?.name === ship.name ? 'selected' : ''}`}
          onClick={() => onSelectShip(ship)}
        >
          <Ship ship={ship} />
        </div>
      ))}
      <button className="rotate-button" onClick={onRotateShip}>Rotate Ship</button>
    </div>
  );
};

export default ShipInventory;

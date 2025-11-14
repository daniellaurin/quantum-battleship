import React from 'react';
import type { ShipType } from '../types/types';
import Ship from './Ship';
import './ShipInventory.css';

interface ShipInventoryProps {
  onSelectShip: (ship: ShipType) => void;
  onRotateShip: () => void;
  selectedShip: ShipType | null;
}

const initialShips: ShipType[] = [
  { name: 'Carrier', size: 5, hits: 0, orientation: 'horizontal', iconPath: '/ships/carrier.png' },
  { name: 'Battleship', size: 4, hits: 0, orientation: 'horizontal', iconPath: '/ships/battleship.png' },
  { name: 'Cruiser', size: 3, hits: 0, orientation: 'horizontal', iconPath: '/ships/cruiser.png' },
  { name: 'Submarine', size: 3, hits: 0, orientation: 'horizontal', iconPath: '/ships/submarine.png' },
  { name: 'Destroyer', size: 2, hits: 0, orientation: 'horizontal', iconPath: '/ships/destroyer.png' },
];

const ShipInventory: React.FC<ShipInventoryProps> = ({ onSelectShip, onRotateShip, selectedShip }) => {
  return (
    <div className="ship-inventory">
      <h2>Your Fleet</h2>
      {initialShips.map((ship) => (
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

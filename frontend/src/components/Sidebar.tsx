import React from 'react';
import ShipInventory from './ShipInventory';
import './Sidebar.css';
import type { ShipType } from '../types/types';

interface SidebarProps {
  isOpen: boolean;
  ships: ShipType[];
  onSelectShip: (ship: ShipType) => void;
  onRotateShip: () => void;
  selectedShip: ShipType | null;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, ships, onSelectShip, onRotateShip, selectedShip }) => {
  return (
    <div className={`sidebar ${isOpen ? 'open' : ''}`}>
      <ShipInventory 
        ships={ships}
        onSelectShip={onSelectShip} 
        onRotateShip={onRotateShip}
        selectedShip={selectedShip}
      />
    </div>
  );
};

export default Sidebar;

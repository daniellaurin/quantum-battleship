// src/components/Sidebar.tsx
import React from 'react';
import ShipInventory from './ShipInventory';
import './Sidebar.css';
import type { QuantumShip } from '../types/types';

interface SidebarProps {
  isOpen: boolean;
  ships: QuantumShip[];
  playerDamage: number[];
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, ships, playerDamage }) => {
  return (
    <div className={`sidebar ${isOpen ? 'open' : ''}`}>
      <ShipInventory
        ships={ships}
        playerDamage={playerDamage}
      />
    </div>
  );
};

export default Sidebar;
// src/components/Header.tsx
import React from 'react';
import './Header.css';

interface HeaderProps {
  onRefresh: () => void;
}

const Header: React.FC<HeaderProps> = ({ onRefresh }) => {
  return (
    <header className="app-header">
      <button onClick={onRefresh} className="logo-button">
        <img src="/qiskit.png" alt="Qiskit logo" className="qiskit-logo" />
      </button>
      <h1>⚛️ Quantum Battleship</h1>
    </header>
  );
};

export default Header;
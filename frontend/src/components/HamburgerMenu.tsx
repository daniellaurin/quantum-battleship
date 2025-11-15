// src/components/HamburgerMenu.tsx
import React from 'react';
import './HamburgerMenu.css';

interface HamburgerMenuProps {
  isOpen: boolean;
  toggle: () => void;
}

const HamburgerMenu: React.FC<HamburgerMenuProps> = ({ isOpen, toggle }) => {
  return (
    <button className={`hamburger-menu ${isOpen ? 'open' : ''}`} onClick={toggle}>
      <div className="bar1" />
      <div className="bar2" />
      <div className="bar3" />
    </button>
  );
};

export default HamburgerMenu;
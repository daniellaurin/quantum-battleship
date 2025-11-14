import { useState } from 'react';
import './App.css';
import Grid from './components/Grid';
import HamburgerMenu from './components/HamburgerMenu';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Modal from './components/Modal';
import type { ShipType, CellState, Coords } from './types/types';

const GRID_SIZE = 10;
const initialGrid = Array(GRID_SIZE).fill(Array(GRID_SIZE).fill('empty'));

function App() {
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const [grid, setGrid] = useState<CellState[][]>(initialGrid);
  const [selectedShip, setSelectedShip] = useState<ShipType | null>(null);
  const [isRefreshModalOpen, setRefreshModalOpen] = useState(false);
  const [isWinModalOpen, setWinModalOpen] = useState(false);
  const [isLoseModalOpen, setLoseModalOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!isSidebarOpen);
  };

  const handleSelectShip = (ship: ShipType) => {
    setSelectedShip(ship);
  };

  const handleRotateShip = () => {
    if (selectedShip) {
      setSelectedShip({
        ...selectedShip,
        orientation: selectedShip.orientation === 'horizontal' ? 'vertical' : 'horizontal',
      });
    }
  };

  const handlePlaceShip = (coords: Coords) => {
    if (!selectedShip) return;

    const newGrid = grid.map(row => [...row]);
    const { x, y } = coords;
    const { size, orientation } = selectedShip;

    // Check if placement is valid
    for (let i = 0; i < size; i++) {
      if (orientation === 'horizontal') {
        if (x + i >= GRID_SIZE || newGrid[y][x + i] !== 'empty') return;
      } else {
        if (y + i >= GRID_SIZE || newGrid[y + i][x] !== 'empty') return;
      }
    }

    // Place ship
    for (let i = 0; i < size; i++) {
      if (orientation === 'horizontal') {
        newGrid[y][x + i] = 'ship';
      } else {
        newGrid[y + i][x] = 'ship';
      }
    }

    setGrid(newGrid);
    setSelectedShip(null);
  };

  const handleOpenRefreshModal = () => {
    setRefreshModalOpen(true);
  };

  const handleCloseRefreshModal = () => {
    setRefreshModalOpen(false);
  };

  const handleRefreshConfirm = () => {
    setGrid(initialGrid);
    setSelectedShip(null);
    setRefreshModalOpen(false);
    setWinModalOpen(false);
    setLoseModalOpen(false);
  };

  return (
    <div className="app">
      <div className="cloud" />
      <div className="cloud" />
      <div className="cloud" />
      <div className="birds" />
      <Header onRefresh={handleOpenRefreshModal} />
      <HamburgerMenu isOpen={isSidebarOpen} toggle={toggleSidebar} />
      <Sidebar 
        isOpen={isSidebarOpen} 
        onSelectShip={handleSelectShip} 
        onRotateShip={handleRotateShip}
        selectedShip={selectedShip}
      />
      <main className="game-container">
        <Grid grid={grid} selectedShip={selectedShip} onPlaceShip={handlePlaceShip} />
        <div className="temp-buttons">
          <button onClick={() => setWinModalOpen(true)}>You Win</button>
          <button onClick={() => setLoseModalOpen(true)}>You Lose</button>
        </div>
      </main>
      <Modal
        isOpen={isRefreshModalOpen}
        onClose={handleCloseRefreshModal}
        onConfirm={handleRefreshConfirm}
        title="Are you sure?"
      >
        This will reset the game and all your progress.
      </Modal>
      <Modal
        isOpen={isWinModalOpen}
        onClose={() => setWinModalOpen(false)}
        onConfirm={handleRefreshConfirm}
        title="You Win!"
      >
        Congratulations, you have defeated the enemy fleet!
      </Modal>
      <Modal
        isOpen={isLoseModalOpen}
        onClose={() => setLoseModalOpen(false)}
        onConfirm={handleRefreshConfirm}
        title="You Lose!"
      >
        The enemy fleet has defeated you. Better luck next time.
      </Modal>
    </div>
  );
}

export default App;
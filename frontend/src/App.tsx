import { useState, useEffect } from 'react';
import './App.css';
import Grid from './components/Grid';
import HamburgerMenu from './components/HamburgerMenu';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Modal from './components/Modal';
import GameStatus from './components/GameStatus';
import type { ShipType, CellState, Coords } from './types/types';

const GRID_SIZE = 10;
const initialGrid = Array(GRID_SIZE).fill(Array(GRID_SIZE).fill('empty'));

const initialShips: ShipType[] = [
  { name: 'carrier', size: 5, hits: 0, orientation: 'horizontal', iconPath: 'ships/carrier.png' },
  { name: 'battleship', size: 4, hits: 0, orientation: 'horizontal', iconPath: 'ships/battleship.png' },
  { name: 'cruiser', size: 3, hits: 0, orientation: 'horizontal', iconPath: 'ships/cruiser.png' },
  { name: 'submarine', size: 3, hits: 0, orientation: 'horizontal', iconPath: 'ships/submarine.png' },
  { name: 'destroyer', size: 2, hits: 0, orientation: 'horizontal', iconPath: 'ships/destroyer.png' },
];

function App() {
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const [grid, setGrid] = useState<CellState[][]>(initialGrid);
  const [ships, setShips] = useState<ShipType[]>(initialShips);
  const [selectedShip, setSelectedShip] = useState<ShipType | null>(null);
  const [isRefreshModalOpen, setRefreshModalOpen] = useState(false);
  const [isWinModalOpen, setWinModalOpen] = useState(false);
  const [isLoseModalOpen, setLoseModalOpen] = useState(false);
  const [isPlayerTurn, setPlayerTurn] = useState(true);
  const [turnCount, setTurnCount] = useState(1);
  const [allShipsPlaced, setAllShipsPlaced] = useState(false);

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

    const newShips = ships.filter(ship => ship.name !== selectedShip.name);
    setShips(newShips);
    setGrid(newGrid);
    setSelectedShip(null);

    if (newShips.length === 0) {
      setAllShipsPlaced(true);
    }
  };

  const handleAttack = (coords: Coords) => {
    if (!isPlayerTurn) return;

    // Dummy logic for now
    const newGrid = grid.map(row => [...row]);
    const { x, y } = coords;
    if (newGrid[y][x] === 'ship') {
      newGrid[y][x] = 'hit';
    } else {
      newGrid[y][x] = 'miss';
    }
    setGrid(newGrid);

    setPlayerTurn(false);
  };

  const handleOpponentTurn = () => {
    // A simple AI that attacks a random cell
    let x, y;
    do {
      x = Math.floor(Math.random() * GRID_SIZE);
      y = Math.floor(Math.random() * GRID_SIZE);
    } while (grid[y][x] === 'hit' || grid[y][x] === 'miss');

    const newGrid = grid.map(row => [...row]);
    if (newGrid[y][x] === 'ship') {
      newGrid[y][x] = 'hit';
    } else {
      newGrid[y][x] = 'miss';
    }
    setGrid(newGrid);
    setPlayerTurn(true);
    setTurnCount(turnCount + 1);
  };

  useEffect(() => {
    if (!isPlayerTurn && allShipsPlaced) {
      setTimeout(() => {
        handleOpponentTurn();
      }, 1000);
    }
  }, [isPlayerTurn, allShipsPlaced]);

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
                      <div className="background-animations">
                        <div className="cloud" />
                        <div className="cloud" />
                        <div className="cloud" />
                        <div className="birds" />
                        <div className="fish" />
                      </div>      <Header onRefresh={handleOpenRefreshModal} />
      <HamburgerMenu isOpen={isSidebarOpen} toggle={toggleSidebar} />
      <Sidebar 
        isOpen={isSidebarOpen} 
        ships={ships}
        onSelectShip={handleSelectShip} 
        onRotateShip={handleRotateShip}
        selectedShip={selectedShip}
      />
      <main className="game-container">
        <GameStatus
          isPlayerTurn={isPlayerTurn}
          turnCount={turnCount}
          shipsPlaced={allShipsPlaced}
        />
        <Grid
          grid={grid}
          selectedShip={selectedShip}
          allShipsPlaced={allShipsPlaced}
          onPlaceShip={handlePlaceShip}
          onAttack={handleAttack}
        />
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
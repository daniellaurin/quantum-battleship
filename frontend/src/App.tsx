// src/App.tsx - UPDATED WITH VISIBLE AI ATTACKS
import { useState, useEffect } from 'react';
import './App.css';
import Grid from './components/Grid';
import HamburgerMenu from './components/HamburgerMenu';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Modal from './components/Modal';
import { quantumApi, type BombResult } from './api/quantumApi';
import type { QuantumShip, GamePhase } from './types/types';

const QUANTUM_SHIPS: Omit<QuantumShip, 'position' | 'damage'>[] = [
  { name: 'Quantum Destroyer', iconPath: '/ships/destroyer.png' },
  { name: 'Quantum Cruiser', iconPath: '/ships/cruiser.png' },
  { name: 'Quantum Carrier', iconPath: '/ships/carrier.png' },
];

function App() {
  const [isSidebarOpen, setSidebarOpen] = useState(true);
  const [gameId, setGameId] = useState<string | null>(null);
  const [gamePhase, setGamePhase] = useState<GamePhase>('setup');

  // Ship positions
  const [playerShips, setPlayerShips] = useState<number[]>([]);
  const [selectedPositions, setSelectedPositions] = useState<number[]>([]);

  // Damage tracking
  const [playerDamage, setPlayerDamage] = useState<number[]>([0, 0, 0, 0, 0]);
  const [opponentDamage, setOpponentDamage] = useState<number[]>([0, 0, 0, 0, 0]);

  // Game state
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState<number | null>(null);
  const [lastBombResult, setLastBombResult] = useState<BombResult | null>(null);
  const [aiTarget, setAiTarget] = useState<number | null>(null);

  // Modals
  const [isRefreshModalOpen, setRefreshModalOpen] = useState(false);
  const [isWinModalOpen, setWinModalOpen] = useState(false);
  const [isLoseModalOpen, setLoseModalOpen] = useState(false);
  const [isQuantumModalOpen, setQuantumModalOpen] = useState(false);
  const [isAiAttackModalOpen, setAiAttackModalOpen] = useState(false);

  // Initialize game on mount
  useEffect(() => {
    const initGame = async () => {
      try {
        const { game_id } = await quantumApi.createGame();
        setGameId(game_id);
        console.log('✅ Game created:', game_id);
      } catch (error) {
        console.error('❌ Error creating game:', error);
        alert('Failed to connect to quantum backend. Make sure the server is running on port 5001!');
      }
    };

    initGame();
  }, []);

  const initializeGame = async () => {
    try {
      const { game_id } = await quantumApi.createGame();
      setGameId(game_id);
      console.log('✅ Game created:', game_id);
    } catch (error) {
      console.error('❌ Error creating game:', error);
      alert('Failed to connect to quantum backend. Make sure the server is running on port 5001!');
    }
  };

  const handleCellClick = async (position: number) => {
    if (!gameId) return;

    // Setup phase - place ships
    if (gamePhase === 'setup') {
      if (selectedPositions.includes(position)) {
        setSelectedPositions(selectedPositions.filter(p => p !== position));
      } else if (selectedPositions.length < 3) {
        const newPositions = [...selectedPositions, position];
        setSelectedPositions(newPositions);

        if (newPositions.length === 3) {
          try {
            await quantumApi.setShips(gameId, 1, newPositions);
            setPlayerShips(newPositions);
            await quantumApi.autoSetup(gameId);
            setGamePhase('player-turn');
            console.log('✅ Ships placed! Game starting...');
          } catch (error) {
            console.error('❌ Error placing ships:', error);
          }
        }
      }
      return;
    }

    // Player turn - attack
    if (gamePhase === 'player-turn' && !gameOver) {
      try {
        const result = await quantumApi.bomb(gameId, 1, position);
        setLastBombResult(result);
        setOpponentDamage(result.damage_results.updated_damage);

        // Show quantum measurements
        setQuantumModalOpen(true);

        if (result.game_over) {
          setGameOver(true);
          setWinner(result.winner);
          if (result.winner === 1) {
            setTimeout(() => setWinModalOpen(true), 1000);
          } else {
            setTimeout(() => setLoseModalOpen(true), 1000);
          }
        } else {
          // AI turn - with delay to show modal first
          setTimeout(() => {
            setQuantumModalOpen(false);
            aiTurn().catch(err => console.error('AI turn error:', err));
          }, 3000); // Wait 3 seconds before AI attacks
        }
      } catch (error) {
        console.error('❌ Error bombing:', error);
      }
    }
  };

  const aiTurn = async () => {
    if (!gameId || gameOver) return;

    setGamePhase('ai-turn');

    // AI randomly selects a position
    const aiPosition = Math.floor(Math.random() * 5);
    setAiTarget(aiPosition);

    // Show AI is attacking
    setAiAttackModalOpen(true);

    // Wait 2 seconds to show AI attack
    await new Promise(resolve => setTimeout(resolve, 2000));

    try {
      const result = await quantumApi.bomb(gameId, 2, aiPosition);
      setPlayerDamage(result.damage_results.updated_damage);
      setLastBombResult(result);

      // Keep modal open for 2 more seconds to show results
      await new Promise(resolve => setTimeout(resolve, 2000));
      setAiAttackModalOpen(false);

      if (result.game_over) {
        setGameOver(true);
        setWinner(result.winner);
        if (result.winner === 2) {
          setTimeout(() => setLoseModalOpen(true), 1000);
        }
      } else {
        setGamePhase('player-turn');
      }
    } catch (error) {
      console.error('❌ Error in AI turn:', error);
      setAiAttackModalOpen(false);
      setGamePhase('player-turn');
    }
  };

  const handleRefreshConfirm = () => {
    setGamePhase('setup');
    setSelectedPositions([]);
    setPlayerShips([]);
    setPlayerDamage([0, 0, 0, 0, 0]);
    setOpponentDamage([0, 0, 0, 0, 0]);
    setGameOver(false);
    setWinner(null);
    setLastBombResult(null);
    setAiTarget(null);
    setRefreshModalOpen(false);
    setWinModalOpen(false);
    setLoseModalOpen(false);
    initializeGame().catch(err => console.error('Restart error:', err));
  };

  const myShips: QuantumShip[] = playerShips.map((pos, idx) => ({
    ...QUANTUM_SHIPS[idx],
    position: pos,
    damage: playerDamage[pos],
  }));

  return (
    <div className="app">
      <div className="background-animations">
        <div className="cloud" />
        <div className="cloud" />
        <div className="cloud" />
        <div className="birds" />
        <div className="fish" />
      </div>

      <Header onRefresh={() => setRefreshModalOpen(true)} />
      <HamburgerMenu isOpen={isSidebarOpen} toggle={() => setSidebarOpen(!isSidebarOpen)} />
      <Sidebar
        isOpen={isSidebarOpen}
        ships={myShips}
        playerDamage={playerDamage}
      />

      <main className="game-container">
        <div className="game-status">
          {gamePhase === 'setup' && (
            <h2>🎯 Setup Phase: Select 3 positions for your ships ({selectedPositions.length}/3)</h2>
          )}
          {gamePhase === 'player-turn' && !gameOver && (
            <h2>⚛️ Your Turn: Select a position to attack!</h2>
          )}
          {gamePhase === 'ai-turn' && !gameOver && (
            <h2>🤖 AI Turn: Quantum attack incoming on position {aiTarget}...</h2>
          )}
          {gameOver && (
            <h2>🎮 Game Over! {winner === 1 ? 'You Win! 🎉' : 'You Lose! 💀'}</h2>
          )}
        </div>

        <Grid
          playerShips={gamePhase === 'setup' ? selectedPositions : playerShips}
          opponentDamage={opponentDamage}
          onCellClick={handleCellClick}
          isSetupPhase={gamePhase === 'setup'}
          selectedPosition={null}
        />

        {gamePhase !== 'setup' && (
          <div className="quantum-stats">
            <div className="stat-card">
              <h3>⚛️ Quantum Measurements</h3>
              <p><strong>Your Total Damage:</strong> {playerDamage.reduce((a, b) => a + b, 0).toFixed(1)}%</p>
              <p><strong>Enemy Total Damage:</strong> {opponentDamage.reduce((a, b) => a + b, 0).toFixed(1)}%</p>
              <br />
              <p><strong>Your Ships Destroyed:</strong> {playerShips.filter(pos => playerDamage[pos] >= 95).length}/3</p>
              <p><strong>Enemy Ships Destroyed:</strong> {opponentDamage.filter(d => d >= 95).length}/3</p>
            </div>
          </div>
        )}
      </main>

      {/* Player Attack Results Modal */}
      <Modal
        isOpen={isQuantumModalOpen}
        onClose={() => setQuantumModalOpen(false)}
        onConfirm={() => setQuantumModalOpen(false)}
        title="⚛️ Your Quantum Attack Results"
      >
        {lastBombResult && lastBombResult.player === 1 && (
          <div className="quantum-results">
            <p><strong>🎯 Target:</strong> Position {lastBombResult.bomb_position}</p>
            <p><strong>🚢 Hit Ship:</strong> {lastBombResult.hit_ship ? '✅ Yes' : '❌ No'}</p>
            <p><strong>⚛️ Quantum Probability:</strong> {(lastBombResult.quantum_measurements.probabilities[lastBombResult.bomb_position] * 100).toFixed(2)}%</p>
            <p><strong>💥 Damage Dealt:</strong> {lastBombResult.damage_results.damage_percentages[lastBombResult.bomb_position].toFixed(1)}%</p>
            <p><strong>💀 Enemy Ships Destroyed:</strong> {lastBombResult.damage_results.destroyed_ships.length}/3</p>
            <hr style={{margin: '15px 0'}} />
            <p style={{fontSize: '0.9em', color: '#666'}}>
              🤖 AI will attack in 3 seconds...
            </p>
          </div>
        )}
      </Modal>

      {/* AI Attack Modal */}
      <Modal
        isOpen={isAiAttackModalOpen}
        onClose={() => {}}
        onConfirm={() => {}}
        title="🤖 AI Quantum Attack!"
      >
        {lastBombResult && lastBombResult.player === 2 && (
          <div className="quantum-results">
            <p><strong>🎯 AI Targeted:</strong> Position {aiTarget}</p>
            <p><strong>🚢 Hit Your Ship:</strong> {lastBombResult.hit_ship ? '✅ Yes - They found you!' : '❌ Miss'}</p>
            <p><strong>⚛️ Quantum Probability:</strong> {(lastBombResult.quantum_measurements.probabilities[lastBombResult.bomb_position] * 100).toFixed(2)}%</p>
            <p><strong>💥 Damage to You:</strong> {lastBombResult.damage_results.damage_percentages[lastBombResult.bomb_position].toFixed(1)}%</p>
            <p><strong>💀 Your Ships Destroyed:</strong> {lastBombResult.damage_results.destroyed_ships.length}/3</p>
            <hr style={{margin: '15px 0'}} />
            <p style={{fontSize: '0.9em', color: '#666'}}>
              ⏳ Calculating quantum interference patterns...
            </p>
          </div>
        )}
      </Modal>

      <Modal
        isOpen={isRefreshModalOpen}
        onClose={() => setRefreshModalOpen(false)}
        onConfirm={handleRefreshConfirm}
        title="⚠️ Reset Game?"
      >
        This will reset the quantum game and all progress will be lost.
      </Modal>

      <Modal
        isOpen={isWinModalOpen}
        onClose={() => setWinModalOpen(false)}
        onConfirm={handleRefreshConfirm}
        title="🎉 Victory!"
      >
        You've destroyed all enemy ships using quantum mechanics! The Elitzur-Vaidman principle prevails!
      </Modal>

      <Modal
        isOpen={isLoseModalOpen}
        onClose={() => setLoseModalOpen(false)}
        onConfirm={handleRefreshConfirm}
        title="💀 Defeat!"
      >
        The enemy's quantum attacks have destroyed your fleet. Better luck next time, quantum warrior!
      </Modal>
    </div>
  );
}

export default App;
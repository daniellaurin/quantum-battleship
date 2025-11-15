import React from 'react';
import './GameStatus.css';

interface GameStatusProps {
  isPlayerTurn: boolean;
  turnCount: number;
  shipsPlaced: boolean;
}

const GameStatus: React.FC<GameStatusProps> = ({ isPlayerTurn, turnCount, shipsPlaced }) => {
  return (
    <div className="game-status">
      {shipsPlaced && (
        <>
          <div className={`turn-indicator ${isPlayerTurn ? 'player-turn' : 'opponent-turn'}`}>
            {isPlayerTurn ? 'Your Turn' : "Opponent's Turn"}
          </div>
          <div className="turn-counter">
            Turn: {turnCount}
          </div>
        </>
      )}
    </div>
  );
};

export default GameStatus;

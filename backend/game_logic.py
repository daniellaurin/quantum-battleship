"""
Game Logic for Quantum Battleship
Handles game setup, ship placement, and turn management
"""

from typing import List, Tuple, Optional
import random
from models import Game, GameBoard, Ship, ShipType, Orientation
from quantum_ai import QuantumAI, QuantumShipPlacer


class GameManager:
    """Manages game state and operations"""

    def __init__(self):
        self.games = {}  # Dictionary to store active games
        self.quantum_ai = {}  # Dictionary to store AI instances per game

    def create_game(self, game_id: str, player_name: str = "Player") -> Game:
        """Create a new game instance"""
        game = Game(game_id, player_name)
        self.games[game_id] = game
        self.quantum_ai[game_id] = QuantumAI(board_size=10)
        return game

    def get_game(self, game_id: str) -> Optional[Game]:
        """Retrieve a game by ID"""
        return self.games.get(game_id)

    def delete_game(self, game_id: str):
        """Delete a game instance"""
        if game_id in self.games:
            del self.games[game_id]
        if game_id in self.quantum_ai:
            del self.quantum_ai[game_id]

    def setup_ai_board(self, game_id: str, use_quantum: bool = True) -> bool:
        """
        Automatically place ships on AI board.
        Uses quantum placement if use_quantum is True.
        """
        game = self.get_game(game_id)
        if not game:
            return False

        ai_board = game.ai_board

        if use_quantum:
            placer = QuantumShipPlacer(board_size=10)

        # Standard ship configuration
        ship_types = [
            ShipType.CARRIER,
            ShipType.BATTLESHIP,
            ShipType.CRUISER,
            ShipType.SUBMARINE,
            ShipType.DESTROYER
        ]

        for ship_type in ship_types:
            placed = False
            attempts = 0
            max_attempts = 100

            while not placed and attempts < max_attempts:
                if use_quantum:
                    start_pos, orientation_str = placer.quantum_random_placement(ship_type.length)
                    orientation = Orientation.HORIZONTAL if orientation_str == "horizontal" else Orientation.VERTICAL
                else:
                    # Classical random placement
                    x = random.randint(0, 9)
                    y = random.randint(0, 9)
                    start_pos = (x, y)
                    orientation = random.choice([Orientation.HORIZONTAL, Orientation.VERTICAL])

                ship = Ship(ship_type, start_pos, orientation)
                placed = ai_board.place_ship(ship)
                attempts += 1

            if not placed:
                # Reset and try again
                game.ai_board = GameBoard()
                return self.setup_ai_board(game_id, use_quantum)

        return True

    def place_player_ship(self, game_id: str, ship_type_name: str,
                          start_x: int, start_y: int, orientation: str) -> dict:
        """
        Place a ship on the player's board.
        Returns success status and message.
        """
        game = self.get_game(game_id)
        if not game:
            return {"success": False, "message": "Game not found"}

        # Convert ship type name to enum
        try:
            ship_type = ShipType[ship_type_name.upper()]
        except KeyError:
            return {"success": False, "message": f"Invalid ship type: {ship_type_name}"}

        # Convert orientation
        orientation_enum = Orientation.HORIZONTAL if orientation.lower() == "horizontal" else Orientation.VERTICAL

        # Create ship
        ship = Ship(ship_type, (start_x, start_y), orientation_enum)

        # Try to place ship
        if game.player_board.place_ship(ship):
            return {
                "success": True,
                "message": f"{ship_type.ship_name} placed successfully",
                "ship": ship.to_dict()
            }
        else:
            return {
                "success": False,
                "message": "Invalid position: ship overlaps or goes out of bounds"
            }

    def player_shoot(self, game_id: str, x: int, y: int) -> dict:
        """
        Process player's shot at AI board.
        Returns shot result and updated game state.
        """
        game = self.get_game(game_id)
        if not game:
            return {"success": False, "message": "Game not found"}

        if game.game_over:
            return {"success": False, "message": "Game is already over"}

        if game.current_turn != "player":
            return {"success": False, "message": "Not your turn"}

        # Process shot
        result = game.ai_board.receive_shot((x, y))

        # Check if game is over
        game.check_game_over()

        # Switch turn if not game over
        if not game.game_over:
            game.switch_turn()

        return {
            "success": True,
            "shot_result": result,
            "game_over": game.game_over,
            "winner": game.winner,
            "next_turn": game.current_turn
        }

    def ai_shoot(self, game_id: str) -> dict:
        """
        Process AI's shot at player board.
        Returns shot result and updated game state.
        """
        game = self.get_game(game_id)
        ai = self.quantum_ai.get(game_id)

        if not game or not ai:
            return {"success": False, "message": "Game not found"}

        if game.game_over:
            return {"success": False, "message": "Game is already over"}

        if game.current_turn != "ai":
            return {"success": False, "message": "Not AI's turn"}

        # AI makes decision
        target = ai.make_move(game.player_board)

        # Process shot
        result = game.player_board.receive_shot(target)

        # Update AI based on result
        ai.process_shot_result(target, result)

        # Check if game is over
        game.check_game_over()

        # Switch turn if not game over
        if not game.game_over:
            game.switch_turn()

        return {
            "success": True,
            "target": target,
            "shot_result": result,
            "game_over": game.game_over,
            "winner": game.winner,
            "next_turn": game.current_turn
        }

    def auto_place_player_ships(self, game_id: str) -> dict:
        """
        Automatically place all ships on player board.
        Useful for quick setup or testing.
        """
        game = self.get_game(game_id)
        if not game:
            return {"success": False, "message": "Game not found"}

        # Reset player board
        game.player_board = GameBoard()

        ship_types = [
            ShipType.CARRIER,
            ShipType.BATTLESHIP,
            ShipType.CRUISER,
            ShipType.SUBMARINE,
            ShipType.DESTROYER
        ]

        for ship_type in ship_types:
            placed = False
            attempts = 0
            max_attempts = 100

            while not placed and attempts < max_attempts:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                orientation = random.choice([Orientation.HORIZONTAL, Orientation.VERTICAL])

                ship = Ship(ship_type, (x, y), orientation)
                placed = game.player_board.place_ship(ship)
                attempts += 1

        return {
            "success": True,
            "message": "All ships placed automatically",
            "board": game.player_board.to_dict(hide_ships=False)
        }

    def reset_game(self, game_id: str):
        """Reset a game to initial state"""
        game = self.get_game(game_id)
        if game:
            game.player_board = GameBoard()
            game.ai_board = GameBoard()
            game.current_turn = "player"
            game.game_over = False
            game.winner = None
            self.quantum_ai[game_id] = QuantumAI(board_size=10)


# Global game manager instance
game_manager = GameManager()
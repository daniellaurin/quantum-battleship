"""
Quantum Battleship Game Models
Object-Oriented Programming structure for ships, board, and quantum states
"""

from enum import Enum
from typing import List, Tuple, Optional
import numpy as np


class ShipType(Enum):
    """Enum for different ship types"""
    CARRIER = ("Carrier", 5)
    BATTLESHIP = ("Battleship", 4)
    CRUISER = ("Cruiser", 3)
    SUBMARINE = ("Submarine", 3)
    DESTROYER = ("Destroyer", 2)

    def __init__(self, ship_name: str, length: int):
        self.ship_name = ship_name
        self.length = length


class Orientation(Enum):
    """Ship orientation on the board"""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class CellState(Enum):
    """State of a cell on the board"""
    EMPTY = "empty"
    SHIP = "ship"
    HIT = "hit"
    MISS = "miss"
    QUANTUM_SUPERPOSITION = "quantum"  # Cell in superposition


class Ship:
    """Represents a battleship"""

    def __init__(self, ship_type: ShipType, start_pos: Tuple[int, int], orientation: Orientation):
        self.ship_type = ship_type
        self.start_pos = start_pos
        self.orientation = orientation
        self.length = ship_type.length
        self.hits = [False] * self.length
        self.is_quantum = False  # Whether ship is in quantum superposition

    @property
    def name(self) -> str:
        return self.ship_type.ship_name

    def get_coordinates(self) -> List[Tuple[int, int]]:
        """Get all coordinates occupied by this ship"""
        coords = []
        x, y = self.start_pos

        for i in range(self.length):
            if self.orientation == Orientation.HORIZONTAL:
                coords.append((x, y + i))
            else:  # VERTICAL
                coords.append((x + i, y))

        return coords

    def hit(self, position: Tuple[int, int]) -> bool:
        """Register a hit at the given position. Returns True if successful."""
        coords = self.get_coordinates()
        if position in coords:
            index = coords.index(position)
            self.hits[index] = True
            return True
        return False

    def is_sunk(self) -> bool:
        """Check if the ship is completely sunk"""
        return all(self.hits)

    def to_dict(self) -> dict:
        """Convert ship to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "type": self.ship_type.name,
            "length": self.length,
            "start_pos": self.start_pos,
            "orientation": self.orientation.value,
            "hits": self.hits,
            "is_sunk": self.is_sunk(),
            "is_quantum": self.is_quantum
        }


class GameBoard:
    """Represents a game board (10x10 grid)"""

    def __init__(self, size: int = 10):
        self.size = size
        self.grid = [[CellState.EMPTY for _ in range(size)] for _ in range(size)]
        self.ships: List[Ship] = []
        self.shots_taken: List[Tuple[int, int]] = []
        self.quantum_positions: List[Tuple[int, int]] = []  # Cells in superposition

    def is_valid_position(self, ship: Ship) -> bool:
        """Check if a ship can be placed at the given position"""
        coords = ship.get_coordinates()

        # Check if all coordinates are within bounds
        for x, y in coords:
            if x < 0 or x >= self.size or y < 0 or y >= self.size:
                return False

        # Check if any coordinate overlaps with existing ships
        for x, y in coords:
            if self.grid[x][y] == CellState.SHIP:
                return False

        return True

    def place_ship(self, ship: Ship) -> bool:
        """Place a ship on the board. Returns True if successful."""
        if not self.is_valid_position(ship):
            return False

        coords = ship.get_coordinates()
        for x, y in coords:
            self.grid[x][y] = CellState.SHIP

        self.ships.append(ship)
        return True

    def receive_shot(self, position: Tuple[int, int]) -> dict:
        """
        Process a shot at the given position.
        Returns result information.
        """
        x, y = position

        if (x, y) in self.shots_taken:
            return {
                "result": "already_shot",
                "message": "This position was already targeted"
            }

        self.shots_taken.append((x, y))

        # Check if any ship was hit
        hit_ship = None
        for ship in self.ships:
            if ship.hit((x, y)):
                hit_ship = ship
                self.grid[x][y] = CellState.HIT
                break

        if hit_ship:
            is_sunk = hit_ship.is_sunk()
            return {
                "result": "hit",
                "ship_name": hit_ship.name,
                "is_sunk": is_sunk,
                "message": f"Hit! {hit_ship.name} {'sunk!' if is_sunk else 'damaged!'}"
            }
        else:
            self.grid[x][y] = CellState.MISS
            return {
                "result": "miss",
                "message": "Miss!"
            }

    def all_ships_sunk(self) -> bool:
        """Check if all ships are sunk"""
        return all(ship.is_sunk() for ship in self.ships)

    def get_visible_grid(self, hide_ships: bool = True) -> List[List[str]]:
        """
        Get the grid state for display.
        If hide_ships is True, unshot ship positions appear as empty.
        """
        visible_grid = []

        for i in range(self.size):
            row = []
            for j in range(self.size):
                cell = self.grid[i][j]

                if hide_ships and cell == CellState.SHIP:
                    row.append(CellState.EMPTY.value)
                elif (i, j) in self.quantum_positions:
                    row.append(CellState.QUANTUM_SUPERPOSITION.value)
                else:
                    row.append(cell.value)

            visible_grid.append(row)

        return visible_grid

    def to_dict(self, hide_ships: bool = True) -> dict:
        """Convert board to dictionary for JSON serialization"""
        return {
            "size": self.size,
            "grid": self.get_visible_grid(hide_ships),
            "ships": [ship.to_dict() for ship in self.ships] if not hide_ships else [],
            "shots_taken": len(self.shots_taken),
            "ships_remaining": sum(1 for ship in self.ships if not ship.is_sunk())
        }


class Game:
    """Represents a complete game instance"""

    def __init__(self, game_id: str, player_name: str = "Player"):
        self.game_id = game_id
        self.player_name = player_name
        self.player_board = GameBoard()
        self.ai_board = GameBoard()
        self.current_turn = "player"  # "player" or "ai"
        self.game_over = False
        self.winner = None
        self.quantum_mode = True  # Whether quantum mechanics are enabled

    def switch_turn(self):
        """Switch between player and AI turns"""
        self.current_turn = "ai" if self.current_turn == "player" else "player"

    def check_game_over(self):
        """Check if the game is over and set winner"""
        if self.player_board.all_ships_sunk():
            self.game_over = True
            self.winner = "ai"
        elif self.ai_board.all_ships_sunk():
            self.game_over = True
            self.winner = "player"

    def to_dict(self) -> dict:
        """Convert game to dictionary for JSON serialization"""
        return {
            "game_id": self.game_id,
            "player_name": self.player_name,
            "player_board": self.player_board.to_dict(hide_ships=False),
            "ai_board": self.ai_board.to_dict(hide_ships=True),
            "current_turn": self.current_turn,
            "game_over": self.game_over,
            "winner": self.winner,
            "quantum_mode": self.quantum_mode
        }
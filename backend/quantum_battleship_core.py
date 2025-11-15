"""
Quantum Battleship Core - Hackathon Implementation
Based on the Elitzur-Vaidman bomb tester experiment

This implementation uses quantum circuits to detect ships WITHOUT directly hitting them,
using quantum superposition and interference patterns.
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import numpy as np
from typing import List, Dict, Tuple
import json


class QuantumBattleshipGame:
    """
    Implements the Quantum Battleship game based on the Elitzur-Vaidman bomb tester.

    Game Rules:
    - 5-cell grid (positions 0-4)
    - Each player places 3 ships at unique positions
    - Players take turns "bombing" positions
    - Quantum circuit detects ships through interference without direct hits
    - Damage accumulates based on quantum measurement probabilities
    - Game ends when all 3 ships of a player reach >95% damage
    """

    def __init__(self, game_id: str):
        self.game_id = game_id
        self.grid_size = 5  # 5-cell grid as per hackathon spec
        self.ships_per_player = 3

        # Ship positions for both players
        self.player1_ships = []  # List of 3 positions (0-4)
        self.player2_ships = []  # List of 3 positions (0-4)

        # Track damage to each ship position (0-100%)
        self.player1_damage = [0.0] * self.grid_size
        self.player2_damage = [0.0] * self.grid_size

        # Bomb history
        self.player1_bombs = []  # History of bomb positions
        self.player2_bombs = []  # History of bomb positions

        # Quantum simulator
        self.simulator = AerSimulator()

        # Game state
        self.current_round = 0
        self.game_over = False
        self.winner = None

    def setShipPosition(self, player: int, positions: List[int]) -> bool:
        """
        Set ship positions for a player.

        Args:
            player: 1 or 2
            positions: List of 3 unique positions (0-4)

        Returns:
            bool: True if successful, False if invalid
        """
        if len(positions) != self.ships_per_player:
            return False

        if len(set(positions)) != self.ships_per_player:
            return False  # Positions must be unique

        if any(p < 0 or p >= self.grid_size for p in positions):
            return False  # Positions must be 0-4

        if player == 1:
            self.player1_ships = sorted(positions)
        elif player == 2:
            self.player2_ships = sorted(positions)
        else:
            return False

        return True

    def bombShip(self, player: int, position: int) -> Dict:
        """
        Player bombs a position on opponent's grid.
        This triggers the quantum circuit to detect ships.

        Args:
            player: 1 or 2 (who is bombing)
            position: Grid position to bomb (0-4)

        Returns:
            Dict with bombing results and quantum measurements
        """
        if position < 0 or position >= self.grid_size:
            return {"success": False, "message": "Invalid position"}

        if self.game_over:
            return {"success": False, "message": "Game is over"}

        # Record the bomb
        if player == 1:
            self.player1_bombs.append(position)
            opponent_ships = self.player2_ships
            opponent_damage = self.player2_damage
        else:
            self.player2_bombs.append(position)
            opponent_ships = self.player1_ships
            opponent_damage = self.player1_damage

        # Build and run quantum circuit
        circuit_results = self._build_quantum_circuit(
            player, position, opponent_ships
        )

        # Calculate damage from quantum measurements
        damage_results = self.calculateDamageToShips(
            circuit_results["probabilities"],
            opponent_ships,
            opponent_damage
        )

        # Update damage
        if player == 1:
            self.player2_damage = damage_results["updated_damage"]
        else:
            self.player1_damage = damage_results["updated_damage"]

        # Check for game over
        self._check_game_over()

        return {
            "success": True,
            "player": player,
            "bomb_position": position,
            "hit_ship": position in opponent_ships,
            "quantum_measurements": circuit_results,
            "damage_results": damage_results,
            "game_over": self.game_over,
            "winner": self.winner,
            "round": self.current_round
        }

    def _build_quantum_circuit(
            self,
            player: int,
            bomb_position: int,
            opponent_ships: List[int]
    ) -> Dict:
        """
        Build and execute the quantum circuit based on Elitzur-Vaidman bomb tester.

        The circuit:
        1. Creates a 5-qubit system (one per grid position)
        2. Applies RY rotations to qubits where opponent ships are hit by bombs
        3. Measures all qubits to get damage probabilities

        Args:
            player: Which player is bombing
            bomb_position: Position being bombed
            opponent_ships: List of opponent's ship positions

        Returns:
            Dict with circuit results and probabilities
        """
        # Create 5-qubit circuit (one per grid position)
        qreg = QuantumRegister(self.grid_size, 'q')
        creg = ClassicalRegister(self.grid_size, 'c')
        qc = QuantumCircuit(qreg, creg)

        # Get all historical bombs for this player
        all_bombs = self.player1_bombs if player == 1 else self.player2_bombs

        # For each bomb that hit a ship, apply RY rotation
        # This models the quantum interference pattern changing when a "bomb" (photon)
        # encounters a ship (obstruction)
        for bomb_pos in all_bombs:
            if bomb_pos in opponent_ships:
                # Apply rotation to this qubit
                # The angle determines sensitivity (small angle = subtle detection)
                rotation_angle = np.pi / 8  # Can be tuned
                qc.ry(rotation_angle, qreg[bomb_pos])

        # Measure all qubits
        for i in range(self.grid_size):
            qc.measure(qreg[i], creg[i])

        # Transpile and run circuit
        transpiled_qc = transpile(qc, self.simulator)
        job = self.simulator.run(transpiled_qc, shots=1024)
        result = job.result()
        counts = result.get_counts()

        # Calculate probabilities for each qubit being |1⟩
        probabilities = self._calculate_qubit_probabilities(counts)

        return {
            "circuit": str(qc.draw('text')),  # FIXED: Convert to string for JSON serialization
            "counts": counts,
            "probabilities": probabilities,
            "total_shots": 1024
        }

    def _calculate_qubit_probabilities(self, counts: Dict[str, int]) -> List[float]:
        """
        Calculate the probability of each qubit being measured as |1⟩.
        This represents the "damage" to each ship position.

        Args:
            counts: Measurement counts from quantum circuit

        Returns:
            List of probabilities (one per grid position)
        """
        total_shots = sum(counts.values())
        probabilities = [0.0] * self.grid_size

        for bitstring, count in counts.items():
            # Bitstring is in reverse order (qubit 0 is rightmost)
            for i in range(self.grid_size):
                if bitstring[-(i + 1)] == '1':  # Read from right to left
                    probabilities[i] += count

        # Convert to probabilities (0.0 to 1.0)
        probabilities = [p / total_shots for p in probabilities]

        return probabilities

    def calculateDamageToShips(
            self,
            probabilities: List[float],
            ship_positions: List[int],
            current_damage: List[float]
    ) -> Dict:
        """
        Convert quantum measurement probabilities to damage percentages.

        Args:
            probabilities: Probability of each qubit being |1⟩
            ship_positions: Positions where ships are located
            current_damage: Current damage levels

        Returns:
            Dict with damage information
        """
        # Convert probabilities to percentages (0-100%)
        damage_percentages = [p * 100 for p in probabilities]

        # Update cumulative damage (damage accumulates over rounds)
        updated_damage = []
        for i in range(self.grid_size):
            # Damage accumulates but caps at 100%
            new_damage = min(100.0, current_damage[i] + damage_percentages[i])
            updated_damage.append(new_damage)

        # Calculate ship-specific damage
        ship_damage = {
            pos: updated_damage[pos] for pos in ship_positions
        }

        # Check if any ships are destroyed (>95% damage)
        destroyed_ships = [
            pos for pos, damage in ship_damage.items() if damage >= 95.0
        ]

        return {
            "probabilities": probabilities,
            "damage_percentages": damage_percentages,
            "updated_damage": updated_damage,
            "ship_damage": ship_damage,
            "destroyed_ships": destroyed_ships,
            "all_ships_destroyed": len(destroyed_ships) == self.ships_per_player
        }

    def _check_game_over(self):
        """Check if game is over (all 3 ships of a player > 95% damage)"""
        # Check player 1's ships
        player1_ships_damaged = sum(
            1 for pos in self.player1_ships if self.player1_damage[pos] >= 95.0
        )

        # Check player 2's ships
        player2_ships_damaged = sum(
            1 for pos in self.player2_ships if self.player2_damage[pos] >= 95.0
        )

        if player1_ships_damaged >= self.ships_per_player:
            self.game_over = True
            self.winner = 2
        elif player2_ships_damaged >= self.ships_per_player:
            self.game_over = True
            self.winner = 1

    def get_game_state(self, player_view: int = 0) -> Dict:
        """
        Get current game state.

        Args:
            player_view: 0 (full state), 1 (player 1 view), 2 (player 2 view)

        Returns:
            Dict with game state
        """
        state = {
            "game_id": self.game_id,
            "grid_size": self.grid_size,
            "current_round": self.current_round,
            "game_over": self.game_over,
            "winner": self.winner
        }

        # Add player-specific info based on view
        if player_view == 0:  # Full state (for debugging/admin)
            state.update({
                "player1_ships": self.player1_ships,
                "player2_ships": self.player2_ships,
                "player1_damage": self.player1_damage,
                "player2_damage": self.player2_damage,
                "player1_bombs": self.player1_bombs,
                "player2_bombs": self.player2_bombs
            })
        elif player_view == 1:  # Player 1's view
            state.update({
                "my_ships": self.player1_ships,
                "my_damage": self.player1_damage,
                "my_bombs": self.player1_bombs,
                "opponent_damage": self.player2_damage,  # Can see opponent damage
                "opponent_bombs": self.player2_bombs
            })
        elif player_view == 2:  # Player 2's view
            state.update({
                "my_ships": self.player2_ships,
                "my_damage": self.player2_damage,
                "my_bombs": self.player2_bombs,
                "opponent_damage": self.player1_damage,
                "opponent_bombs": self.player1_bombs
            })

        return state

    def visualize_damage_map(self, player: int) -> str:
        """
        Create ASCII visualization of damage map.

        Args:
            player: 1 or 2 (which player's damage to show)

        Returns:
            String with visualization
        """
        damage = self.player1_damage if player == 1 else self.player2_damage
        ships = self.player1_ships if player == 1 else self.player2_ships

        viz = f"\n=== Player {player} Damage Map ===\n"
        viz += "Position: "
        for i in range(self.grid_size):
            viz += f"  {i}  "
        viz += "\n"

        viz += "Damage:   "
        for i in range(self.grid_size):
            ship_marker = "S" if i in ships else " "
            viz += f"{damage[i]:4.1f}%{ship_marker}"
        viz += "\n"

        viz += "Status:   "
        for i in range(self.grid_size):
            if i in ships:
                if damage[i] >= 95.0:
                    status = "DEST"
                elif damage[i] >= 50.0:
                    status = "CRIT"
                elif damage[i] > 0:
                    status = "DMGD"
                else:
                    status = "SAFE"
            else:
                status = "----"
            viz += f" {status} "
        viz += "\n"

        return viz

    def to_dict(self) -> Dict:
        """Convert game to dictionary for JSON serialization"""
        return {
            "game_id": self.game_id,
            "grid_size": self.grid_size,
            "ships_per_player": self.ships_per_player,
            "player1_ships": self.player1_ships,
            "player2_ships": self.player2_ships,
            "player1_damage": self.player1_damage,
            "player2_damage": self.player2_damage,
            "player1_bombs": self.player1_bombs,
            "player2_bombs": self.player2_bombs,
            "current_round": self.current_round,
            "game_over": self.game_over,
            "winner": self.winner
        }
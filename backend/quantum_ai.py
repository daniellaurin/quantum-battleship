"""
Quantum AI for Battleship
Uses Qiskit quantum circuits to make intelligent targeting decisions
"""

from typing import List, Tuple, Optional
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from models import GameBoard, CellState
import random


class QuantumAI:
    """
    AI opponent that uses quantum computing concepts for decision making.
    Uses quantum superposition and measurement for targeting strategy.
    """

    def __init__(self, board_size: int = 10):
        self.board_size = board_size
        self.simulator = AerSimulator()
        self.probability_map = np.ones((board_size, board_size)) / (board_size * board_size)
        self.last_hit = None
        self.hunt_mode = False
        self.target_queue: List[Tuple[int, int]] = []

    def update_probability_map(self, board: GameBoard):
        """
        Update probability map based on current board state.
        Cells already shot have 0 probability.
        """
        for i in range(self.board_size):
            for j in range(self.board_size):
                if (i, j) in board.shots_taken:
                    self.probability_map[i][j] = 0

        # Normalize probabilities
        total = np.sum(self.probability_map)
        if total > 0:
            self.probability_map = self.probability_map / total

    def quantum_target_selection(self, num_targets: int = 1) -> List[Tuple[int, int]]:
        """
        Use quantum circuit to select target coordinates.
        Creates superposition of all possible positions and measures.
        """
        # Calculate number of qubits needed to represent board positions
        num_positions = self.board_size * self.board_size
        num_qubits = int(np.ceil(np.log2(num_positions)))

        # Create quantum circuit
        qreg = QuantumRegister(num_qubits, 'q')
        creg = ClassicalRegister(num_qubits, 'c')
        qc = QuantumCircuit(qreg, creg)

        # Create superposition of all states
        for i in range(num_qubits):
            qc.h(qreg[i])

        # Add phase based on probability map (simplified version)
        # In a real implementation, this would use amplitude amplification
        for i in range(num_qubits):
            qc.rz(np.pi / 4, qreg[i])

        # Measure
        qc.measure(qreg, creg)

        # Execute circuit
        job = self.simulator.run(qc, shots=num_targets * 10)
        result = job.result()
        counts = result.get_counts()

        # Convert measured binary states to board positions
        targets = []
        for bitstring in list(counts.keys())[:num_targets * 2]:
            position_index = int(bitstring, 2) % num_positions
            x = position_index // self.board_size
            y = position_index % self.board_size

            if 0 <= x < self.board_size and 0 <= y < self.board_size:
                targets.append((x, y))

        return targets[:num_targets]

    def get_adjacent_cells(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid adjacent cells (up, down, left, right)"""
        x, y = position
        adjacent = []

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.board_size and 0 <= new_y < self.board_size:
                adjacent.append((new_x, new_y))

        return adjacent

    def smart_target_mode(self, board: GameBoard) -> Tuple[int, int]:
        """
        Enhanced targeting when a ship has been hit.
        Targets adjacent cells to find and sink the ship.
        """
        if self.target_queue:
            # Continue targeting from queue
            target = self.target_queue.pop(0)
            while target in board.shots_taken and self.target_queue:
                target = self.target_queue.pop(0)

            if target not in board.shots_taken:
                return target

        if self.last_hit:
            # Add adjacent cells to target queue
            adjacent = self.get_adjacent_cells(self.last_hit)
            for cell in adjacent:
                if cell not in board.shots_taken and cell not in self.target_queue:
                    self.target_queue.append(cell)

            if self.target_queue:
                return self.target_queue.pop(0)

        # Fall back to hunt mode
        self.hunt_mode = False
        return self.hunt_mode_target(board)

    def hunt_mode_target(self, board: GameBoard) -> Tuple[int, int]:
        """
        Regular targeting mode using quantum selection and probability.
        """
        # Use quantum circuit to generate candidate positions
        quantum_targets = self.quantum_target_selection(num_targets=5)

        # Filter out already shot positions
        valid_targets = [t for t in quantum_targets if t not in board.shots_taken]

        if valid_targets:
            # Weight by probability map
            best_target = max(valid_targets,
                              key=lambda t: self.probability_map[t[0]][t[1]])
            return best_target

        # Fallback: random unshot position
        available = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if (i, j) not in board.shots_taken:
                    available.append((i, j))

        return random.choice(available) if available else (0, 0)

    def make_move(self, board: GameBoard) -> Tuple[int, int]:
        """
        Main method to determine AI's next move.
        Returns (x, y) coordinates to target.
        """
        # Update probability map
        self.update_probability_map(board)

        # Choose targeting strategy
        if self.hunt_mode and (self.target_queue or self.last_hit):
            target = self.smart_target_mode(board)
        else:
            target = self.hunt_mode_target(board)

        return target

    def process_shot_result(self, position: Tuple[int, int], result: dict):
        """
        Update AI state based on shot result.
        Adjusts strategy if a ship was hit.
        """
        if result["result"] == "hit":
            self.last_hit = position
            self.hunt_mode = True

            # Increase probability around hit
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    x, y = position[0] + dx, position[1] + dy
                    if 0 <= x < self.board_size and 0 <= y < self.board_size:
                        self.probability_map[x][y] *= 2.0

            # Add adjacent cells to target queue if ship not sunk
            if not result.get("is_sunk", False):
                adjacent = self.get_adjacent_cells(position)
                for cell in adjacent:
                    if cell not in self.target_queue:
                        self.target_queue.append(cell)

        elif result["result"] == "miss":
            # Decrease probability around miss
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    x, y = position[0] + dx, position[1] + dy
                    if 0 <= x < self.board_size and 0 <= y < self.board_size:
                        self.probability_map[x][y] *= 0.8

        # If ship was sunk, clear targeting mode
        if result.get("is_sunk", False):
            self.hunt_mode = False
            self.last_hit = None
            self.target_queue.clear()


class QuantumShipPlacer:
    """
    Uses quantum circuits to generate random but strategic ship placements.
    """

    def __init__(self, board_size: int = 10):
        self.board_size = board_size
        self.simulator = AerSimulator()

    def quantum_random_placement(self, ship_length: int) -> Tuple[Tuple[int, int], str]:
        """
        Use quantum randomness to determine ship placement.
        Returns (start_position, orientation).
        """
        # Create quantum circuit for randomness
        qc = QuantumCircuit(4, 4)

        # Create superposition
        for i in range(4):
            qc.h(i)

        # Add some entanglement for better randomness
        qc.cx(0, 1)
        qc.cx(2, 3)

        # Measure
        qc.measure(range(4), range(4))

        # Execute
        job = self.simulator.run(qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        measurement = list(counts.keys())[0]

        # Extract values from measurement
        x = int(measurement[0:2], 2) % self.board_size
        y = int(measurement[2:4], 2) % self.board_size
        orientation = "horizontal" if int(measurement[0], 2) == 0 else "vertical"

        # Ensure ship fits on board
        if orientation == "horizontal" and y + ship_length > self.board_size:
            y = self.board_size - ship_length
        elif orientation == "vertical" and x + ship_length > self.board_size:
            x = self.board_size - ship_length

        return ((x, y), orientation)
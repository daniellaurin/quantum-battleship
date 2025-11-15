"""
Quantum Battleship Flask API - Hackathon Implementation
Based on Elitzur-Vaidman bomb tester experiment
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from quantum_battleship_core import QuantumBattleshipGame
from typing import Dict
import random

app = Flask(__name__)
CORS(app)

# Store active games
games: Dict[str, QuantumBattleshipGame] = {}


@app.route('/')
def home():
    """API home endpoint"""
    return jsonify({
        "message": "Quantum Battleship API - Hackathon Implementation",
        "version": "1.0.0",
        "description": "Based on Elitzur-Vaidman bomb tester experiment",
        "game_rules": {
            "grid_size": 5,
            "ships_per_player": 3,
            "win_condition": "All 3 opponent ships >95% damage"
        },
        "endpoints": {
            "POST /api/quantum/game/new": "Create new quantum game",
            "GET /api/quantum/game/<game_id>": "Get game state",
            "POST /api/quantum/game/<game_id>/set-ships": "Set ship positions",
            "POST /api/quantum/game/<game_id>/bomb": "Bomb a position (triggers quantum circuit)",
            "GET /api/quantum/game/<game_id>/visualize": "Get damage visualization",
            "POST /api/quantum/game/<game_id>/auto-setup": "Auto-setup ships for testing"
        }
    })


@app.route('/api/quantum/game/new', methods=['POST'])
def create_quantum_game():
    """
    Create a new quantum battleship game.

    Body (optional):
    {
        "game_id": "custom-id"  // Optional custom game ID
    }
    """
    data = request.get_json() or {}

    # Generate or use custom game ID
    game_id = data.get('game_id', str(uuid.uuid4()))

    if game_id in games:
        return jsonify({
            "success": False,
            "message": "Game ID already exists"
        }), 400

    # Create new quantum game
    game = QuantumBattleshipGame(game_id)
    games[game_id] = game

    return jsonify({
        "success": True,
        "message": "Quantum game created",
        "game_id": game_id,
        "game_info": {
            "grid_size": game.grid_size,
            "ships_per_player": game.ships_per_player,
            "instructions": "Each player must place 3 ships on positions 0-4"
        }
    }), 201


@app.route('/api/quantum/game/<game_id>', methods=['GET'])
def get_quantum_game_state(game_id):
    """
    Get current game state.

    Query params:
    - view: 0 (full), 1 (player1), 2 (player2)
    """
    if game_id not in games:
        return jsonify({
            "success": False,
            "message": "Game not found"
        }), 404

    game = games[game_id]
    view = int(request.args.get('view', 0))

    state = game.get_game_state(player_view=view)

    return jsonify({
        "success": True,
        "state": state
    })


@app.route('/api/quantum/game/<game_id>/set-ships', methods=['POST'])
def set_ship_positions(game_id):
    """
    Set ship positions for a player.

    Body:
    {
        "player": 1 or 2,
        "positions": [0, 2, 4]  // 3 unique positions from 0-4
    }
    """
    if game_id not in games:
        return jsonify({
            "success": False,
            "message": "Game not found"
        }), 404

    game = games[game_id]
    data = request.get_json()

    if not data or 'player' not in data or 'positions' not in data:
        return jsonify({
            "success": False,
            "message": "Missing required fields: player, positions"
        }), 400

    player = data['player']
    positions = data['positions']

    # Validate input
    if player not in [1, 2]:
        return jsonify({
            "success": False,
            "message": "Player must be 1 or 2"
        }), 400

    if not isinstance(positions, list) or len(positions) != 3:
        return jsonify({
            "success": False,
            "message": "Must provide exactly 3 positions"
        }), 400

    # Set ship positions
    success = game.setShipPosition(player, positions)

    if not success:
        return jsonify({
            "success": False,
            "message": "Invalid positions. Must be 3 unique values from 0-4"
        }), 400

    return jsonify({
        "success": True,
        "message": f"Player {player} ships placed at positions {positions}",
        "player": player,
        "positions": positions
    })


@app.route('/api/quantum/game/<game_id>/bomb', methods=['POST'])
def bomb_position(game_id):
    """
    Bomb a position on opponent's grid.
    This triggers the quantum circuit and measurement.

    Body:
    {
        "player": 1 or 2,
        "position": 0-4
    }
    """
    if game_id not in games:
        return jsonify({
            "success": False,
            "message": "Game not found"
        }), 404

    game = games[game_id]
    data = request.get_json()

    if not data or 'player' not in data or 'position' not in data:
        return jsonify({
            "success": False,
            "message": "Missing required fields: player, position"
        }), 400

    player = data['player']
    position = data['position']

    # Validate
    if player not in [1, 2]:
        return jsonify({
            "success": False,
            "message": "Player must be 1 or 2"
        }), 400

    if not isinstance(position, int) or position < 0 or position >= 5:
        return jsonify({
            "success": False,
            "message": "Position must be 0-4"
        }), 400

    # Execute bomb (runs quantum circuit)
    result = game.bombShip(player, position)

    if not result["success"]:
        return jsonify(result), 400

    # Add visualization
    opponent = 2 if player == 1 else 1
    result["damage_visualization"] = game.visualize_damage_map(opponent)

    return jsonify(result)


@app.route('/api/quantum/game/<game_id>/visualize', methods=['GET'])
def visualize_game(game_id):
    """
    Get damage visualization for both players.

    Query params:
    - player: 1, 2, or 'both' (default)
    """
    if game_id not in games:
        return jsonify({
            "success": False,
            "message": "Game not found"
        }), 404

    game = games[game_id]
    player_param = request.args.get('player', 'both')

    visualization = {}

    if player_param in ['1', 'both']:
        visualization['player1'] = game.visualize_damage_map(1)

    if player_param in ['2', 'both']:
        visualization['player2'] = game.visualize_damage_map(2)

    return jsonify({
        "success": True,
        "visualization": visualization,
        "game_state": game.get_game_state(0)
    })


@app.route('/api/quantum/game/<game_id>/auto-setup', methods=['POST'])
def auto_setup_game(game_id):
    """
    Automatically setup ships for both players (for testing).
    Randomly places 3 ships for each player.
    """
    if game_id not in games:
        return jsonify({
            "success": False,
            "message": "Game not found"
        }), 404

    game = games[game_id]

    # Generate random unique positions for player 1
    player1_positions = random.sample(range(5), 3)
    game.setShipPosition(1, player1_positions)

    # Generate random unique positions for player 2
    player2_positions = random.sample(range(5), 3)
    game.setShipPosition(2, player2_positions)

    return jsonify({
        "success": True,
        "message": "Ships auto-placed for both players",
        "player1_ships": player1_positions,
        "player2_ships": player2_positions,
        "note": "In a real game, ships should be hidden from opponent"
    })


@app.route('/api/quantum/game/<game_id>/quantum-info', methods=['GET'])
def get_quantum_info(game_id):
    """
    Get information about the quantum circuit implementation.
    Educational endpoint to explain the quantum mechanics.
    """
    if game_id not in games:
        return jsonify({
            "success": False,
            "message": "Game not found"
        }), 404

    return jsonify({
        "success": True,
        "quantum_implementation": {
            "concept": "Elitzur-Vaidman bomb tester",
            "description": "Detect ships without directly hitting them using quantum interference",
            "circuit_details": {
                "qubits": 5,
                "purpose": "One qubit per grid position (0-4)",
                "gate_used": "RY (rotation around Y-axis)",
                "measurement": "All 5 qubits measured"
            },
            "how_it_works": [
                "1. Each grid position is represented by a qubit",
                "2. When a bomb hits a ship position, apply RY rotation to that qubit",
                "3. Multiple hits accumulate more rotations",
                "4. Measure all qubits to get probabilities",
                "5. Probability of |1⟩ represents damage to that position",
                "6. Damage accumulates over rounds",
                "7. Game ends when all 3 ships reach >95% damage"
            ],
            "quantum_advantage": "Quantum superposition and interference allow detection of ships through probability changes, simulating the bomb tester experiment"
        }
    })


@app.route('/api/quantum/game/<game_id>/reset', methods=['POST'])
def reset_quantum_game(game_id):
    """Reset a quantum game to initial state"""
    if game_id not in games:
        return jsonify({
            "success": False,
            "message": "Game not found"
        }), 404

    # Create new game with same ID
    games[game_id] = QuantumBattleshipGame(game_id)

    return jsonify({
        "success": True,
        "message": "Game reset successfully"
    })


@app.route('/api/quantum/game/<game_id>', methods=['DELETE'])
def delete_quantum_game(game_id):
    """Delete a quantum game"""
    if game_id not in games:
        return jsonify({
            "success": False,
            "message": "Game not found"
        }), 404

    del games[game_id]

    return jsonify({
        "success": True,
        "message": "Game deleted successfully"
    })


@app.route('/api/quantum/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "active_games": len(games),
        "quantum_backend": "qiskit_aer_simulator"
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "message": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "message": "Internal server error"
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print(" Quantum Battleship Server - Hackathon Implementation")
    print("   Based on Elitzur-Vaidman bomb tester experiment")
    print("=" * 60)
    print("\n Server starting on http://localhost:5000")
    print(" API documentation available at http://localhost:5000/")
    print("\n  Quantum Features:")
    print("   • 5-qubit quantum circuit")
    print("   • Elitzur-Vaidman bomb tester principle")
    print("   • Ship detection through quantum interference")
    print("   • Damage calculation from quantum measurements")
    print("\n" + "=" * 60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5001)
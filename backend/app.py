"""
Quantum Battleship Flask API
Main application file with REST API endpoints
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
from game_logic import game_manager
from models import ShipType

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication


# Store active games
# game_manager is already instantiated in game_logic.py


@app.route('/')
def home():
    """API home endpoint"""
    return jsonify({
        "message": "Quantum Battleship API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/game/new": "Create a new game",
            "GET /api/game/<game_id>": "Get game state",
            "POST /api/game/<game_id>/setup": "Auto-setup AI board",
            "POST /api/game/<game_id>/place-ship": "Place player ship",
            "POST /api/game/<game_id>/auto-place": "Auto-place all player ships",
            "POST /api/game/<game_id>/shoot": "Player shoots at AI board",
            "POST /api/game/<game_id>/ai-turn": "AI takes turn",
            "POST /api/game/<game_id>/reset": "Reset game",
            "DELETE /api/game/<game_id>": "Delete game"
        }
    })


@app.route('/api/game/new', methods=['POST'])
def create_new_game():
    """
    Create a new game instance.
    Body: { "player_name": "optional name" }
    """
    data = request.get_json() or {}
    player_name = data.get('player_name', 'Player')

    # Generate unique game ID
    game_id = str(uuid.uuid4())

    # Create game
    game = game_manager.create_game(game_id, player_name)

    return jsonify({
        "success": True,
        "message": "Game created successfully",
        "game_id": game_id,
        "game": game.to_dict()
    }), 201


@app.route('/api/game/<game_id>', methods=['GET'])
def get_game_state(game_id):
    """Get current game state"""
    game = game_manager.get_game(game_id)

    if not game:
        return jsonify({
            "success": False,
            "message": "Game not found"
        }), 404

    return jsonify({
        "success": True,
        "game": game.to_dict()
    })


@app.route('/api/game/<game_id>/setup', methods=['POST'])
def setup_game(game_id):
    """
    Setup AI board with ships.
    Body: { "use_quantum": true/false }
    """
    game = game_manager.get_game(game_id)

    if not game:
        return jsonify({
            "success": False,
            "message": "Game not found"
        }), 404

    data = request.get_json() or {}
    use_quantum = data.get('use_quantum', True)

    success = game_manager.setup_ai_board(game_id, use_quantum)

    return jsonify({
        "success": success,
        "message": "AI board setup complete" if success else "Failed to setup AI board",
        "quantum_mode": use_quantum
    })


@app.route('/api/game/<game_id>/place-ship', methods=['POST'])
def place_ship(game_id):
    """
    Place a ship on player's board.
    Body: {
        "ship_type": "CARRIER/BATTLESHIP/CRUISER/SUBMARINE/DESTROYER",
        "start_x": 0-9,
        "start_y": 0-9,
        "orientation": "horizontal/vertical"
    }
    """
    game = game_manager.get_game(game_id)

    if not game:
        return jsonify({
            "success": False,
            "message": "Game not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data provided"
        }), 400

    required_fields = ['ship_type', 'start_x', 'start_y', 'orientation']
    if not all(field in data for field in required_fields):
        return jsonify({
            "success": False,
            "message": f"Missing required fields. Required: {required_fields}"
        }), 400

    result = game_manager.place_player_ship(
        game_id,
        data['ship_type'],
        data['start_x'],
        data['start_y'],
        data['orientation']
    )

    return jsonify(result)


@app.route('/api/game/<game_id>/auto-place', methods=['POST'])
def auto_place_ships(game_id):
    """Automatically place all player ships"""
    result = game_manager.auto_place_player_ships(game_id)

    if not result["success"]:
        return jsonify(result), 404

    return jsonify(result)


@app.route('/api/game/<game_id>/shoot', methods=['POST'])
def player_shoot(game_id):
    """
    Player shoots at AI board.
    Body: { "x": 0-9, "y": 0-9 }
    """
    game = game_manager.get_game(game_id)

    if not game:
        return jsonify({
            "success": False,
            "message": "Game not found"
        }), 404

    data = request.get_json()

    if not data or 'x' not in data or 'y' not in data:
        return jsonify({
            "success": False,
            "message": "Missing coordinates (x, y)"
        }), 400

    x = data['x']
    y = data['y']

    if not (0 <= x <= 9 and 0 <= y <= 9):
        return jsonify({
            "success": False,
            "message": "Coordinates must be between 0 and 9"
        }), 400

    result = game_manager.player_shoot(game_id, x, y)

    return jsonify(result)


@app.route('/api/game/<game_id>/ai-turn', methods=['POST'])
def ai_turn(game_id):
    """AI takes its turn"""
    result = game_manager.ai_shoot(game_id)

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result)


@app.route('/api/game/<game_id>/reset', methods=['POST'])
def reset_game(game_id):
    """Reset game to initial state"""
    game = game_manager.get_game(game_id)

    if not game:
        return jsonify({
            "success": False,
            "message": "Game not found"
        }), 404

    game_manager.reset_game(game_id)

    return jsonify({
        "success": True,
        "message": "Game reset successfully"
    })


@app.route('/api/game/<game_id>', methods=['DELETE'])
def delete_game(game_id):
    """Delete a game"""
    game = game_manager.get_game(game_id)

    if not game:
        return jsonify({
            "success": False,
            "message": "Game not found"
        }), 404

    game_manager.delete_game(game_id)

    return jsonify({
        "success": True,
        "message": "Game deleted successfully"
    })


@app.route('/api/ships', methods=['GET'])
def get_ship_types():
    """Get available ship types and their properties"""
    ships = []
    for ship_type in ShipType:
        ships.append({
            "name": ship_type.name,
            "display_name": ship_type.ship_name,
            "length": ship_type.length
        })

    return jsonify({
        "success": True,
        "ships": ships
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "active_games": len(game_manager.games)
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "message": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "success": False,
        "message": "Internal server error"
    }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
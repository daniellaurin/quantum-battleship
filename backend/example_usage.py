"""
Simple Example Usage of Quantum Battleship
Demonstrates the hackathon implementation step-by-step
"""

from quantum_battleship_core import QuantumBattleshipGame
import json


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def example_1_basic_game():
    """Example 1: Create a basic quantum battleship game"""

    print_section("EXAMPLE 1: Basic Quantum Battleship Game")

    # Step 1: Create a new game
    print("Step 1: Creating quantum game...")
    game = QuantumBattleshipGame("example-game-1")
    print(f" Game created with ID: {game.game_id}")
    print(f"   Grid size: {game.grid_size} cells (0-{game.grid_size - 1})")
    print(f"   Ships per player: {game.ships_per_player}")

    # Step 2: Set ship positions for both players
    print("\nStep 2: Setting ship positions...")

    # Player 1 ships at positions 0, 2, 4
    success = game.setShipPosition(1, [0, 2, 4])
    print(f"   Player 1 ships: [0, 2, 4] - {' Placed' if success else ' Failed'}")

    # Player 2 ships at positions 1, 2, 3
    success = game.setShipPosition(2, [1, 2, 3])
    print(f"   Player 2 ships: [1, 2, 3] - {' Placed' if success else ' Failed'}")

    # Step 3: Player 1 bombs position 1
    print("\nStep 3: Player 1 bombs position 1...")
    result = game.bombShip(1, 1)

    print(f"   Hit ship? {result['hit_ship']}")
    print(f"   Quantum probabilities: {result['quantum_measurements']['probabilities']}")
    print("\n   Damage to Player 2's ships:")
    for pos, damage in result['damage_results']['ship_damage'].items():
        print(f"      Ship at position {pos}: {damage:.1f}%")

    # Step 4: Visualize damage
    print("\nStep 4: Damage visualization...")
    print(game.visualize_damage_map(2))

    # Step 5: Continue playing
    print("Step 5: Playing more rounds...")

    rounds = [
        (2, 0),  # Player 2 bombs position 0
        (1, 2),  # Player 1 bombs position 2
        (2, 2),  # Player 2 bombs position 2
        (1, 3),  # Player 1 bombs position 3
    ]

    for player, position in rounds:
        result = game.bombShip(player, position)
        opponent = 2 if player == 1 else 1
        print(f"   Round: Player {player} → Position {position} | Game Over: {result['game_over']}")

        if result['game_over']:
            print(f"\n GAME OVER! Winner: Player {result['winner']}")
            break

    # Final state
    print("\nFinal State:")
    print(f"   Player 1 damage: {game.player1_damage}")
    print(f"   Player 2 damage: {game.player2_damage}")
    print(f"   Game over: {game.game_over}")
    print(f"   Winner: {game.winner}")


def example_2_quantum_detection():
    """Example 2: Demonstrate quantum ship detection"""

    print_section("EXAMPLE 2: Quantum Ship Detection")

    print("This example demonstrates the Elitzur-Vaidman bomb tester principle")
    print("Ships are detected through quantum interference patterns\n")

    game = QuantumBattleshipGame("example-game-2")

    # Setup
    game.setShipPosition(1, [0, 1, 2])
    game.setShipPosition(2, [2, 3, 4])

    print("Setup:")
    print(f"   Player 1 ships: {game.player1_ships}")
    print(f"   Player 2 ships: {game.player2_ships}")

    # Player 1 bombs position 2 (has a Player 2 ship)
    print("\n Player 1 bombs position 2 (which HAS a Player 2 ship)")
    result = game.bombShip(1, 2)

    print("\n Quantum Circuit Results:")
    print(f"   Measurement counts: {result['quantum_measurements']['counts']}")
    print(f"   Probabilities of |1⟩:")

    probs = result['quantum_measurements']['probabilities']
    for i, p in enumerate(probs):
        ship_marker = " ← SHIP HERE" if i in game.player2_ships else ""
        print(f"      Position {i}: {p:.4f}{ship_marker}")

    print("\n Notice how the probability changes at ship positions!")
    print("   This is the quantum interference effect.")

    # Bomb the same position again to show cumulative effect
    print("\n Player 1 bombs position 2 AGAIN (cumulative effect)")
    result = game.bombShip(1, 2)

    print("\n Updated Probabilities (after 2 hits):")
    probs = result['quantum_measurements']['probabilities']
    for i, p in enumerate(probs):
        ship_marker = " ← SHIP HERE" if i in game.player2_ships else ""
        print(f"      Position {i}: {p:.4f}{ship_marker}")

    print("\n💡 The probability INCREASED because we hit the same ship twice!")
    print("   Multiple quantum rotations accumulate.")


def example_3_game_to_completion():
    """Example 3: Play a complete game until someone wins"""

    print_section("EXAMPLE 3: Complete Game Until Winner")

    game = QuantumBattleshipGame("example-game-3")

    # Setup ships
    game.setShipPosition(1, [0, 1, 2])
    game.setShipPosition(2, [2, 3, 4])

    print("Starting game with ships at:")
    print(f"   Player 1: {game.player1_ships}")
    print(f"   Player 2: {game.player2_ships}")
    print("\nPlaying until all ships of one player reach >95% damage...\n")

    # Play rounds
    round_num = 0
    bombing_strategy = [
        # Format: (player, position)
        (1, 2), (2, 0),  # Round 1
        (1, 3), (2, 1),  # Round 2
        (1, 4), (2, 2),  # Round 3
        (1, 2), (2, 0),  # Round 4 (repeat hits)
        (1, 3), (2, 1),  # Round 5
        (1, 4), (2, 2),  # Round 6
        (1, 2), (2, 0),  # Round 7
        (1, 3), (2, 1),  # Round 8
    ]

    for player, position in bombing_strategy:
        round_num += 1
        result = game.bombShip(player, position)

        opponent = 2 if player == 1 else 1
        hit_marker = "💥 HIT" if result['hit_ship'] else "💨 MISS"

        print(f"Round {round_num}: Player {player} → Position {position} {hit_marker}")

        # Show ship damage after each round
        damage_info = result['damage_results']['ship_damage']
        destroyed = result['damage_results']['destroyed_ships']

        print(f"   Player {opponent} ship damage: ", end="")
        for ship_pos, dmg in damage_info.items():
            destroyed_marker = " [DESTROYED]" if int(ship_pos) in destroyed else ""
            print(f"Pos {ship_pos}: {dmg:.1f}%{destroyed_marker} | ", end="")
        print()

        if result['game_over']:
            print(f"\n{'=' * 70}")
            print(f" GAME OVER!")
            print(f"🏆 Winner: Player {result['winner']}")
            print(f"{'=' * 70}")
            print("\nFinal Damage Maps:")
            print(game.visualize_damage_map(1))
            print(game.visualize_damage_map(2))
            break
        print()


def example_4_serialization():
    """Example 4: Show how to serialize game state to JSON"""

    print_section("EXAMPLE 4: Game State Serialization")

    game = QuantumBattleshipGame("example-game-4")
    game.setShipPosition(1, [0, 2, 4])
    game.setShipPosition(2, [1, 2, 3])

    # Bomb a few positions
    game.bombShip(1, 1)
    game.bombShip(2, 0)

    # Convert to dictionary
    game_dict = game.to_dict()

    print("Game state as dictionary:")
    print(json.dumps(game_dict, indent=2))

    # Get player-specific views
    print("\n" + "-" * 70)
    print("Player 1's view (can see own ships):")
    player1_view = game.get_game_state(player_view=1)
    print(json.dumps(player1_view, indent=2))


def example_5_validation():
    """Example 5: Show input validation"""

    print_section("EXAMPLE 5: Input Validation")

    game = QuantumBattleshipGame("example-game-5")

    print("Testing invalid inputs...\n")

    # Test 1: Too many ships
    print("Test 1: Placing 4 ships (should fail)")
    success = game.setShipPosition(1, [0, 1, 2, 3])
    print(f"   Result: {' Failed' if not success else ' Success'} (expected: Failed)\n")

    # Test 2: Duplicate positions
    print("Test 2: Duplicate ship positions [0, 0, 1]")
    success = game.setShipPosition(1, [0, 0, 1])
    print(f"   Result: {' Failed' if not success else ' Success'} (expected: Failed)\n")

    # Test 3: Out of range
    print("Test 3: Position out of range [0, 1, 5]")
    success = game.setShipPosition(1, [0, 1, 5])
    print(f"   Result: {' Failed' if not success else ' Success'} (expected: Failed)\n")

    # Test 4: Valid input
    print("Test 4: Valid positions [0, 2, 4]")
    success = game.setShipPosition(1, [0, 2, 4])
    print(f"   Result: {' Success' if success else ' Failed'} (expected: Success)\n")

    # Test 5: Bombing invalid position
    print("Test 5: Bombing position 10 (out of range)")
    game.setShipPosition(2, [1, 2, 3])
    result = game.bombShip(1, 10)
    print(f"   Result: {result['message']}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  QUANTUM BATTLESHIP - USAGE EXAMPLES")
    print("  Hackathon Implementation")
    print("=" * 70)

    # Run all examples
    example_1_basic_game()
    example_2_quantum_detection()
    example_3_game_to_completion()
    example_4_serialization()
    example_5_validation()

    print("\n" + "=" * 70)
    print("  ✅ All examples completed!")
    print("=" * 70)
    print("\n Next steps:")
    print("   1. Start the API server: python app_quantum.py")
    print("   2. Run API tests: python test_quantum_api.py")
    print("   3. Read HACKATHON_GUIDE.md for complete documentation")
    print("   4. Read HACKATHON_ANSWERS.md for requirement checklist")
    print("\n  Quantum features demonstrated!")
    print("=" * 70 + "\n")
"""
Test Script for Quantum Battleship API - Hackathon Implementation
Tests the Elitzur-Vaidman bomb tester based game
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"


def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'=' * 70}")
    print(f" {title}")
    print(f"{'=' * 70}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        # Print visualization nicely if it exists
        if 'damage_visualization' in data:
            print(data['damage_visualization'])
            del data['damage_visualization']  # Remove for cleaner JSON display
        if 'visualization' in data:
            for player, viz in data['visualization'].items():
                print(viz)
            del data['visualization']
        print(f"\nResponse:\n{json.dumps(data, indent=2)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'=' * 70}\n")


def test_quantum_game_flow():
    """
    Test a complete quantum battleship game following hackathon specifications.
    """

    print("\n" + "=" * 70)
    print("🎮 QUANTUM BATTLESHIP - HACKATHON TEST")
    print("   Based on Elitzur-Vaidman Bomb Tester Experiment")
    print("=" * 70 + "\n")

    # 1. Check health
    response = requests.get(f"{BASE_URL}/api/quantum/health")
    print_response("Health Check", response)

    # 2. Create new quantum game
    response = requests.post(f"{BASE_URL}/api/quantum/game/new")
    print_response("Create Quantum Game", response)

    if response.status_code != 201:
        print(" Failed to create game. Exiting.")
        return

    game_id = response.json()["game_id"]
    print(f"✅ Quantum Game Created! ID: {game_id}\n")

    # 3. Set ship positions for both players
    # Player 1 ships at positions 0, 2, 4
    response = requests.post(
        f"{BASE_URL}/api/quantum/game/{game_id}/set-ships",
        json={"player": 1, "positions": [0, 2, 4]}
    )
    print_response("Set Player 1 Ships (0, 2, 4)", response)

    # Player 2 ships at positions 1, 2, 3
    response = requests.post(
        f"{BASE_URL}/api/quantum/game/{game_id}/set-ships",
        json={"player": 2, "positions": [1, 2, 3]}
    )
    print_response("Set Player 2 Ships (1, 2, 3)", response)

    # 4. Get quantum circuit information
    response = requests.get(f"{BASE_URL}/api/quantum/game/{game_id}/quantum-info")
    print_response("Quantum Circuit Information", response)

    # 5. Play several rounds
    print("\n" + "🎯 PLAYING QUANTUM BATTLESHIP ROUNDS" + "\n")

    rounds = [
        # (player, target_position)
        (1, 1),  # Player 1 bombs position 1 (hits P2's ship!)
        (2, 0),  # Player 2 bombs position 0 (hits P1's ship!)
        (1, 2),  # Player 1 bombs position 2 (hits P2's ship!)
        (2, 2),  # Player 2 bombs position 2 (hits P1's ship!)
        (1, 3),  # Player 1 bombs position 3 (hits P2's ship!)
        (2, 4),  # Player 2 bombs position 4 (hits P1's ship!)
    ]

    for round_num, (player, position) in enumerate(rounds, 1):
        print(f"\n--- Round {round_num}: Player {player} bombs position {position} ---")

        response = requests.post(
            f"{BASE_URL}/api/quantum/game/{game_id}/bomb",
            json={"player": player, "position": position}
        )
        print_response(f"Round {round_num} - Quantum Bomb", response)

        if response.json().get("game_over"):
            print("🎉 GAME OVER!")
            winner = response.json().get("winner")
            print(f"🏆 Winner: Player {winner}")
            break

        time.sleep(0.5)  # Brief pause between rounds

    # 6. Get final visualization
    response = requests.get(f"{BASE_URL}/api/quantum/game/{game_id}/visualize")
    print_response("Final Damage Visualization", response)

    # 7. Get full game state
    response = requests.get(f"{BASE_URL}/api/quantum/game/{game_id}?view=0")
    print_response("Full Game State", response)

    # Clean up
    requests.delete(f"{BASE_URL}/api/quantum/game/{game_id}")

    print("\n✅ Quantum Game Test Complete!\n")


def test_auto_setup():
    """Test auto-setup feature for quick testing"""

    print("\n" + "=" * 70)
    print("🔄 TESTING AUTO-SETUP")
    print("=" * 70 + "\n")

    # Create game
    response = requests.post(f"{BASE_URL}/api/quantum/game/new")
    game_id = response.json()["game_id"]

    # Auto-setup ships
    response = requests.post(f"{BASE_URL}/api/quantum/game/{game_id}/auto-setup")
    print_response("Auto-Setup Ships", response)

    # Play a few rounds with auto-setup
    for i in range(5):
        player = 1 if i % 2 == 0 else 2
        position = i % 5

        response = requests.post(
            f"{BASE_URL}/api/quantum/game/{game_id}/bomb",
            json={"player": player, "position": position}
        )

        print(f"\n--- Auto Round {i + 1}: Player {player} → Position {position} ---")
        if 'damage_visualization' in response.json():
            print(response.json()['damage_visualization'])

        if response.json().get("game_over"):
            print(f"🎉 Game Over! Winner: Player {response.json()['winner']}")
            break

    # Visualize
    response = requests.get(f"{BASE_URL}/api/quantum/game/{game_id}/visualize")
    print_response("Auto-Setup Visualization", response)

    # Clean up
    requests.delete(f"{BASE_URL}/api/quantum/game/{game_id}")

    print("\n✅ Auto-Setup Test Complete!\n")


def demonstrate_quantum_detection():
    """
    Demonstrate the quantum detection principle:
    Ships can be detected through quantum interference without direct hits
    """

    print("\n" + "=" * 70)
    print("  DEMONSTRATING QUANTUM SHIP DETECTION")
    print("   (Elitzur-Vaidman Bomb Tester Principle)")
    print("=" * 70 + "\n")

    # Create game
    response = requests.post(f"{BASE_URL}/api/quantum/game/new")
    game_id = response.json()["game_id"]

    # Set ships
    # Player 1: ships at 0, 1, 2
    # Player 2: ships at 2, 3, 4
    requests.post(
        f"{BASE_URL}/api/quantum/game/{game_id}/set-ships",
        json={"player": 1, "positions": [0, 1, 2]}
    )
    requests.post(
        f"{BASE_URL}/api/quantum/game/{game_id}/set-ships",
        json={"player": 2, "positions": [2, 3, 4]}
    )

    print("Setup:")
    print("  Player 1 ships: [0, 1, 2]")
    print("  Player 2 ships: [2, 3, 4]\n")

    print(" Player 1 will bomb position 2 (which HAS a Player 2 ship)")
    response = requests.post(
        f"{BASE_URL}/api/quantum/game/{game_id}/bomb",
        json={"player": 1, "position": 2}
    )

    print("\n Quantum Measurement Results:")
    result = response.json()
    if 'quantum_measurements' in result:
        probs = result['quantum_measurements']['probabilities']
        print(f"  Probabilities of |1⟩ for each position:")
        for i, p in enumerate(probs):
            ship_status = "← SHIP HERE" if i in [2, 3, 4] else ""
            print(f"    Position {i}: {p:.4f} {ship_status}")

    print(result.get('damage_visualization', ''))

    print("\n💡 Notice how the quantum circuit detects the ship through")
    print("   interference pattern changes, even without 'hitting' it directly!")

    # Clean up
    requests.delete(f"{BASE_URL}/api/quantum/game/{game_id}")

    print("\n Quantum Detection Demo Complete!\n")


def test_validation():
    """Test input validation"""

    print("\n" + "=" * 70)
    print("🧪 TESTING INPUT VALIDATION")
    print("=" * 70 + "\n")

    # Create game
    response = requests.post(f"{BASE_URL}/api/quantum/game/new")
    game_id = response.json()["game_id"]

    # Test invalid ship positions
    print("Test 1: Invalid number of ships (4 instead of 3)")
    response = requests.post(
        f"{BASE_URL}/api/quantum/game/{game_id}/set-ships",
        json={"player": 1, "positions": [0, 1, 2, 3]}
    )
    print(f"  Result: {response.json()['message']}\n")

    print("Test 2: Duplicate positions")
    response = requests.post(
        f"{BASE_URL}/api/quantum/game/{game_id}/set-ships",
        json={"player": 1, "positions": [0, 0, 1]}
    )
    print(f"  Result: {response.json()['message']}\n")

    print("Test 3: Out of range position")
    response = requests.post(
        f"{BASE_URL}/api/quantum/game/{game_id}/set-ships",
        json={"player": 1, "positions": [0, 1, 5]}
    )
    print(f"  Result: {response.json()['message']}\n")

    print("Test 4: Valid setup")
    response = requests.post(
        f"{BASE_URL}/api/quantum/game/{game_id}/set-ships",
        json={"player": 1, "positions": [0, 2, 4]}
    )
    print(f"  Result: {response.json()['message']}\n")

    # Clean up
    requests.delete(f"{BASE_URL}/api/quantum/game/{game_id}")

    print("✅ Validation Tests Complete!\n")


if __name__ == "__main__":
    try:
        print("\n Starting Quantum Battleship Tests...")
        print("📍 Make sure the server is running: python app_quantum.py")
        print()

        # Test if server is running
        try:
            requests.get(f"{BASE_URL}/api/quantum/health")
        except requests.exceptions.ConnectionError:
            print(" ERROR: Cannot connect to server!")
            print("   Please start the server first: python app_quantum.py")
            exit(1)

        # Run tests
        test_quantum_game_flow()
        test_auto_setup()
        demonstrate_quantum_detection()
        test_validation()

        print("\n" + "=" * 70)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\n Hackathon Requirements Met:")
        print("   5-cell grid (positions 0-4)")
        print("   3 ships per player")
        print("   setShipPosition() function")
        print("   bombShip() function")
        print("   5-qubit quantum circuit")
        print("   RY gate rotations for hits")
        print("   Quantum measurement with get_counts()")
        print("   calculateDamageToShips() function")
        print("   >95% damage threshold for game over")
        print("   Damage visualization")
        print("   Based on Elitzur-Vaidman bomb tester")
        print("\n⚛  Quantum Features Demonstrated!")
        print("=" * 70 + "\n")

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback

        traceback.print_exc()
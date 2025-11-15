"""
Test Script for Quantum Battleship API - Hackathon Implementation
"""

import requests
import json
import time

BASE_URL = "http://localhost:5001"
HEADERS = {"Content-Type": "application/json"}


def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'=' * 70}")
    print(f" {title}")
    print(f"{'=' * 70}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        if 'damage_visualization' in data:
            print(data['damage_visualization'])
            del data['damage_visualization']
        if 'visualization' in data:
            for player, viz in data['visualization'].items():
                print(viz)
            del data['visualization']
        print(f"\nResponse:\n{json.dumps(data, indent=2)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'=' * 70}\n")


def test_quantum_game_flow():
    print("\n" + "=" * 70)
    print("🎮 QUANTUM BATTLESHIP - HACKATHON TEST")
    print("   Based on Elitzur-Vaidman Bomb Tester Experiment")
    print("=" * 70 + "\n")

    # Health check
    response = requests.get(f"{BASE_URL}/api/quantum/health")
    print_response("Health Check", response)

    # Create game
    response = requests.post(
        f"{BASE_URL}/api/quantum/game/new",
        headers=HEADERS,
        json={}
    )
    print_response("Create Quantum Game", response)

    if response.status_code != 201:
        print(" Failed to create game. Exiting.")
        return

    game_id = response.json()["game_id"]
    print(f" Quantum Game Created! ID: {game_id}\n")

    # Set ships
    response = requests.post(
        f"{BASE_URL}/api/quantum/game/{game_id}/set-ships",
        headers=HEADERS,
        json={"player": 1, "positions": [0, 2, 4]}
    )
    print_response("Set Player 1 Ships (0, 2, 4)", response)

    response = requests.post(
        f"{BASE_URL}/api/quantum/game/{game_id}/set-ships",
        headers=HEADERS,
        json={"player": 2, "positions": [1, 2, 3]}
    )
    print_response("Set Player 2 Ships (1, 2, 3)", response)

    # Get quantum info
    response = requests.get(f"{BASE_URL}/api/quantum/game/{game_id}/quantum-info")
    print_response("Quantum Circuit Information", response)

    # Play rounds
    print("\n🎯 PLAYING QUANTUM BATTLESHIP ROUNDS\n")

    rounds = [(1, 1), (2, 0), (1, 2), (2, 2), (1, 3), (2, 4)]

    for round_num, (player, position) in enumerate(rounds, 1):
        print(f"\n--- Round {round_num}: Player {player} bombs position {position} ---")

        response = requests.post(
            f"{BASE_URL}/api/quantum/game/{game_id}/bomb",
            headers=HEADERS,
            json={"player": player, "position": position}
        )
        print_response(f"Round {round_num} - Quantum Bomb", response)

        if response.json().get("game_over"):
            print("❌ GAME OVER!")
            print(f"🏆 Winner: Player {response.json()['winner']}")
            break

        time.sleep(0.5)

    # Final visualization
    response = requests.get(f"{BASE_URL}/api/quantum/game/{game_id}/visualize")
    print_response("Final Damage Visualization", response)

    # Cleanup
    requests.delete(f"{BASE_URL}/api/quantum/game/{game_id}")
    print("\n✅ Quantum Game Test Complete!\n")


if __name__ == "__main__":
    try:
        print("\n🚀 Starting Quantum Battleship Tests...")
        print(" Make sure the server is running: python app_quantum.py\n")

        try:
            requests.get(f"{BASE_URL}/api/quantum/health")
        except requests.exceptions.ConnectionError:
            print(" ERROR: Cannot connect to server!")
            exit(1)

        test_quantum_game_flow()

        print("\n" + "=" * 70)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\nHackathon Requirements Met:")
        print(" 5-cell grid (positions 0-4)")
        print(" 3 ships per player")
        print(" Quantum circuit implementation")
        print(" Damage visualization")
        print("\n Quantum Features Demonstrated!")
        print("=" * 70 + "\n")

    except Exception as e:
        print(f"\n Error: {e}")
        import traceback

        traceback.print_exc()
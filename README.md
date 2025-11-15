# ⚛️ Quantum Battleship 🚢

Welcome to Quantum Battleship, a unique take on the classic naval combat game, infused with the fascinating principles of quantum mechanics! This project explores two distinct game modes: a traditional Battleship experience enhanced with a Quantum AI, and a specialized "Quantum Battleship" game based on the Elitzur-Vaidman bomb tester experiment.

## ✨ Features

### 🎮 Classic Battleship with Quantum AI

Experience the familiar game of Battleship with an intelligent twist!

*   **Standard 10x10 Grid:** Play on the traditional battlefield.
*   **Intelligent Quantum AI Opponent:**
    *   **Quantum Ship Placement:** AI uses quantum randomness for unpredictable and strategic ship deployment. 🎲
    *   **Quantum Targeting Strategy:** AI employs quantum superposition and measurement to analyze the board and make optimal shot decisions, maintaining a probability map and adapting its strategy based on hits and misses. 🎯
*   **Player vs. AI:** Challenge a sophisticated AI that learns and adapts.
*   **Full Game Mechanics:** Ship placement, shooting, hit/miss detection, and game-over conditions.

### 🔬 Quantum Battleship (Elitzur-Vaidman Experiment)

Dive into the quantum realm with a game mode directly inspired by quantum physics!

*   **Elitzur-Vaidman Bomb Tester:** Detect opponent ships using quantum interference without directly "hitting" them. 🤯
*   **5-Cell Quantum Grid:** A simplified grid (0-4) where each position is represented by a qubit.
*   **Quantum Circuit Simulation:** Utilizes Qiskit to simulate quantum circuits, applying RY rotations to qubits corresponding to ship positions.
*   **Probabilistic Damage:** Damage accumulates based on quantum measurement probabilities, reflecting the likelihood of a ship's presence. 💥
*   **Unique Win Condition:** Game ends when all 3 of an opponent's ships reach over 95% damage through quantum detection.

## 🚀 Technologies Used

*   **Backend:**
    *   Python 🐍
    *   Flask (Web Framework)
    *   Qiskit (Quantum Computing Framework) ⚛️
    *   Numpy (Numerical Computing)
*   **Frontend:**
    *   React (JavaScript Library) ⚛️
    *   Vite (Build Tool)
    *   TypeScript
    *   CSS

## ⚙️ Setup & Installation

To get this quantum naval battle running on your machine, follow these steps:

### 📦 Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Classic Battleship API:**
    ```bash
    python app.py
    # or using the provided script: ./run.sh
    ```
    This will start the API for the Classic Battleship game, usually on `http://localhost:5001`.

4.  **Run the Quantum Battleship API (Elitzur-Vaidman):**
    ```bash
    python app_quantum.py
    ```
    This will start the API for the Quantum Battleship game, usually on `http://localhost:5001` (Note: you might need to adjust ports if running both simultaneously or use a proxy).

### 🌐 Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```
3.  **Start the React development server:**
    ```bash
    npm run dev
    ```
    This will typically open the application in your browser at `http://localhost:5173`.

## 🗺️ API Endpoints

Both backend applications expose RESTful API endpoints for game management, ship placement, shooting, and retrieving game states. Refer to `backend/app.py` and `backend/app_quantum.py` for detailed endpoint documentation.

## 🕹️ How to Play

*   **Classic Battleship:** Place your ships on the 10x10 grid, then take turns shooting at the AI's board. The AI will use its quantum intelligence to try and sink your fleet!
*   **Quantum Battleship:** Place your 3 ships on the 5-cell grid. Use the "bomb" action to interact with the quantum circuit and deduce the location of your opponent's ships through probability measurements.

## 🤝 Contributing

Ali - Daniel - Shaurya - Mujtaba


---
_Built for the Qiskit 2025 Hackathon_ 🚀

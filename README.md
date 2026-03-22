# 🧩 Sudoku Solver - DP + Backtracking

A modern, high-performance Sudoku solver built with Python and Tkinter. It utilizes a combination of **Dynamic Programming (Constraint Caching)** and **Backtracking** with the **Minimum Remaining Values (MRV)** heuristic to solve even the toughest puzzles efficiently.

## 📁 File Structure & Explanations

The project is organized into the following modules:

### 1. `main.py`
- **Purpose**: The entry point of the application.
- **Functionality**:
    - Sets up the environment and prints initialization logs.
    - Imports and launches the GUI application.
    - Handles top-level exceptions to ensure a graceful exit.

### 2. `sudoku_solver/gui.py`
- **Purpose**: Graphical User Interface (GUI) implementation.
- **Functionality**:
    - Built using `tkinter`.
    - Provides a responsive 9x9 grid for manual input or sample loading.
    - Features real-time visualization of the solving process (animation).
    - Includes controls for solving speed, clearing the grid, and loading sample puzzles of varying difficulty.
    - Manages multi-threading to keep the UI responsive while the solver is running.

### 3. `sudoku_solver/solver.py`
- **Purpose**: Core solving engine.
- **Functionality**:
    - Implements the `SudokuSolver` class.
    - Uses **Constraint Caching** (Row, Column, and Box sets) to achieve $O(1)$ validity checks.
    - Employs the **Minimum Remaining Values (MRV)** heuristic to prioritize cells with the fewest possibilities, significantly pruning the search space.
    - Supports visualization callbacks to sync the algorithm's state with the GUI.

### 4. `sudoku_solver/utils.py`
- **Purpose**: Utility functions and grid processing.
- **Functionality**:
    - Contains helper methods for validating individual cells and entire grids.
    - Includes logic for detecting conflicts (duplicates in rows, columns, or boxes).
    - Features a difficulty estimator based on the number of empty cells.
    - Provides string parsing and formatting tools for Sudoku grids.

## 🚀 How to Run

Ensure you have Python 3.x installed. No external dependencies are required as it uses standard libraries.

1. Navigate to the project root directory.
2. Run the application:
   ```bash
   python sudoku_solver/main.py
   ```

## ✨ Key Features
- **Real-time Visualization**: Watch the algorithm "think" as it explores the search space.
- **Fast Algorithm**: Intelligent backtracking optimized with MRV and constraint caching.
- **Sample Puzzles**: Quickly test the solver with Easy, Medium, and Hard presets.
- **Validation**: Instant feedback on invalid manual entries.
- **Multi-threaded**: Solve puzzles in the background without freezing the window.

# Pac-man with Search Algorithm

## Project Overview
This repository contains a project implementing the classic Pacman game, where search algorithms are applied to optimize the movement of ghosts chasing Pacman. The project was developed as a final assignment for the "Artificial Intelligence" course at the University of Technology and Education, Ho Chi Minh City. It explores various search algorithms to enhance ghost behavior in a 2D maze environment.

## Repository Details
- **GitHub Link**: [https://github.com/HueyAnthonyDisward/Pac-man-with-search-algorithm](https://github.com/HueyAnthonyDisward/Pac-man-with-search-algorithm)
- **Language/Tools**: Python, Pygame, heapq, collections
- **Purpose**: Implement and compare search algorithms (A*, BFS, Simulated Annealing, Backtracking with AC-3, and Reinforcement Learning) for ghost navigation in Pacman.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Required libraries: `pygame`, `heapq`, `collections`, `random`, `math`
- IDE: PyCharm (recommended)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/HueyAnthonyDisward/Pac-man-with-search-algorithm.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Pac-man-with-search-algorithm
   ```
3. Install the required dependencies:
   ```bash
   pip install pygame
   ```
4. Ensure all project files (e.g., game scripts, maze configurations) are in the root directory.

### Usage
- Run the main game script to start the Pacman game with implemented search algorithms for ghosts:
  ```bash
  python main.py
  ```
- The game features a 2D maze where Pacman navigates to eat dots while ghosts (Red, Sky Blue, Orange, Pink) chase using different search algorithms (A*, BFS, Simulated Annealing, Backtracking with AC-3).
- Interact with the game using keyboard inputs (arrow keys to move Pacman).
- Evaluate ghost performance based on their ability to chase Pacman, as detailed in the report.

## Methodology
The project implements the Pacman game with the following components:
- **Environment**: A 2D grid-based maze with walls ('1'), empty spaces/dots (' '), Pacman ('P'), and ghosts ('R', 'S', 'O', 'P').
- **Ghost Navigation**:
  - **A***: Informed search using a heuristic (Manhattan distance) to find the shortest path to Pacman.
  - **BFS**: Uninformed search exploring nodes level by level to find a path to Pacman.
  - **Simulated Annealing**: Probabilistic optimization to escape local optima while chasing Pacman.
  - **Backtracking with AC-3**: Constraint satisfaction to optimize the search space before backtracking to find a path.
  - **Reinforcement Learning**: Conceptual approach for ghosts to learn optimal chasing strategies (not fully implemented in code).
- **Game Logic**:
  - Pacman eats dots; game ends if all dots are eaten (level complete) or if Pacman is caught 3 times (game over).
  - Berry mechanic: Temporarily empowers Pacman to eat ghosts.

## Results
- Ghosts using A* and BFS showed effective pathfinding, with A* being more efficient due to its heuristic guidance.
- Simulated Annealing allowed ghosts to explore alternative paths, avoiding local traps but with higher computational cost.
- Backtracking with AC-3 optimized the search space, improving pathfinding efficiency for complex mazes.
- Detailed comparisons and visualizations are available in the report (`báo cáo (4).docx`).

## Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- **Instructor**: Dr. Phan Thị Huyền Trang
- **Team Members**: Nguyễn Trung Hiếu (22110138), Lê Hoàng Bảo Phúc (22110200)
- **Institution**: University of Technology and Education, Ho Chi Minh City
- **References**:
  - [A* Algorithm](https://www.iostream.co/article/thuat-giai-a-DVnHj)
  - [Search Algorithms](https://users.soict.hust.edu.vn/huonglt/AI/Chuong%203.%20Tim%20kiem%20co%20ban.pdf)
  - [BFS](https://wiki.vnoi.info/algo/graph-theory/breadth-first-search.md)
  - [Pygame Documentation](https://www.pygame.org/docs/)


import math


def manhattan_distance(pos1, pos2):
    """Tính khoảng cách Manhattan giữa hai điểm."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def ghost_hill_climbing(grid, ghost_position, pacman_position, max_steps=500):
    """
    Tìm đường đi từ Ghost đến Pacman bằng Hill-Climbing.

    grid: Bản đồ (ma trận).
    ghost_position: Vị trí ban đầu của Ghost.
    pacman_position: Vị trí của Pacman.
    max_steps: Số bước tối đa Ghost có thể di chuyển.
    """
    rows, cols = len(grid), len(grid[0])
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # Trái, Lên, Phải, Xuống
    path = []  # Lưu đường đi của Ghost
    visited = set()  # Lưu các vị trí đã thăm
    steps = 0

    while ghost_position != pacman_position and steps < max_steps:
        path.append(ghost_position)  # Lưu vị trí hiện tại vào đường đi
        visited.add(ghost_position)  # Đánh dấu đã thăm
        best_move = None
        min_distance = math.inf

        # Xét tất cả các hướng di chuyển
        for direction in directions:
            next_row = ghost_position[0] + direction[0]
            next_col = ghost_position[1] + direction[1]

            # Kiểm tra tính hợp lệ của ô tiếp theo
            if (
                    0 <= next_row < rows
                    and 0 <= next_col < cols
                    and grid[next_row][next_col] != '1'  # Không phải chướng ngại vật
                    and (next_row, next_col) not in visited  # Chưa thăm
            ):
                next_position = (next_row, next_col)
                distance = manhattan_distance(next_position, pacman_position)

                # Tìm bước đi có khoảng cách Manhattan nhỏ nhất
                if distance < min_distance:
                    min_distance = distance
                    best_move = next_position

        # Nếu không tìm thấy bước đi nào tốt hơn
        if not best_move:
            break  # Thoát khỏi vòng lặp nếu local optimum

        # Di chuyển Ghost đến bước đi tốt nhất
        ghost_position = best_move
        steps += 1

    # Kiểm tra nếu Ghost đã tìm thấy Pacman
    if ghost_position == pacman_position:
        path.append(pacman_position)

    return path

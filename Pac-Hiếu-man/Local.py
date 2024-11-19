import math
import random

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def simulated_annealing(grid, ghost_position, pacman_position, max_steps=500, initial_temp=200, cooling_rate=0.9999999):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # Trái, Lên, Phải, Xuống
    path = []  # Lưu đường đi của Ghost
    visited = set()  # Lưu các vị trí đã thăm
    steps = 0
    temp = initial_temp  # Bắt đầu với nhiệt độ cao

    # Đánh dấu vị trí ban đầu là đã thăm
    visited.add(ghost_position)

    while ghost_position != pacman_position and steps < max_steps:
        path.append(ghost_position)  # Lưu vị trí hiện tại vào đường đi
        best_move = None
        min_distance = math.inf
        possible_moves = []  # Lưu các bước di chuyển có khoảng cách Manhattan nhỏ nhất

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

                # Thêm các bước di chuyển có khoảng cách Manhattan nhỏ nhất
                if distance < min_distance:
                    min_distance = distance
                    best_move = next_position
                    possible_moves = [next_position]  # Reset list nếu tìm thấy bước di chuyển tốt nhất
                elif distance == min_distance:
                    possible_moves.append(next_position)

        # Nếu không tìm thấy bước đi nào hợp lý, thoát khỏi vòng lặp
        if not best_move:
            break

        # Chọn bước đi ngẫu nhiên nếu có nhiều lựa chọn
        next_move = random.choice(possible_moves)
        next_distance = manhattan_distance(next_move, pacman_position)
        delta = next_distance - min_distance

        # Quyết định có chấp nhận bước đi hay không dựa trên nhiệt độ và delta
        if delta < 0:  # Nếu bước đi mới tốt hơn (khoảng cách giảm)
            best_move = next_move
        else:  # Nếu bước đi mới tồi hơn, chấp nhận với xác suất P = exp(-delta / temp)
            probability = math.exp(-delta / temp)
            if random.random() < probability:
                best_move = next_move

        # Di chuyển Ghost đến bước đi đã chọn
        ghost_position = best_move
        steps += 1

        # Đánh dấu vị trí đã đi qua
        visited.add(ghost_position)

        # Giảm nhiệt độ (làm lạnh) từ từ nhưng không quá nhanh
        temp *= cooling_rate

        # Nếu nhiệt độ quá thấp, có thể thoát khỏi vòng lặp
        if temp < 0.01:
            break

    # Kiểm tra nếu Ghost đã tìm thấy Pacman
    if ghost_position == pacman_position:
        path.append(pacman_position)

    return path

import heapq

def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def best_first_search(grid, ghost_start, pacman_position):
    rows, cols = len(grid), len(grid[0])
    priority_queue = [(0, ghost_start, [ghost_start])]  # (heuristic, position, path)
    visited = set()

    # Định nghĩa các hướng di chuyển (lên, xuống, trái, phải)
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    while priority_queue:
        _, current, path = heapq.heappop(priority_queue)

        # Nếu Ghost đến vị trí của Pacman, trả về đường đi
        if current == pacman_position:
            return path

        # Đánh dấu vị trí hiện tại là đã thăm
        if current in visited:
            continue
        visited.add(current)

        for direction in directions:
            next_row, next_col = current[0] + direction[0], current[1] + direction[1]

            # Kiểm tra xem ô tiếp theo có hợp lệ và không phải tường ('1')
            if 0 <= next_row < rows and 0 <= next_col < cols and grid[next_row][next_col] != '1':
                next_position = (next_row, next_col)
                if next_position not in visited:
                    # Tính toán heuristic (khoảng cách Manhattan) từ ô tiếp theo đến Pacman
                    heuristic = manhattan_distance(next_position, pacman_position)
                    heapq.heappush(priority_queue, (heuristic, next_position, path + [next_position]))

    return []  # Trả về danh sách rỗng nếu không tìm thấy đường đi

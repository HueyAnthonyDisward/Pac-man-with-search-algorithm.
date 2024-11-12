import math


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def ids_search(grid, start, destination):
    rows, cols = len(grid), len(grid[0])

    # Các hướng di chuyển: lên, trái, xuống, phải

    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    def search(path, g_cost, depth_limit):
        current = path[-1]
        f_cost = g_cost + heuristic(current, destination)  # Hàm f = g + h

        # Nếu đường đi không hợp lệ, dừng tìm kiếm
        if f_cost > depth_limit:
            return f_cost

        # Nếu đến đích, trả về đường đi
        if current == destination:
            return path

        # Duyệt qua các hướng
        min_cost = math.inf
        for direction in directions:
            next_row, next_col = current[0] + direction[0], current[1] + direction[1]

            # Kiểm tra nếu ô tiếp theo hợp lệ: không vượt ra ngoài bản đồ và không phải tường
            if 0 <= next_row < rows and 0 <= next_col < cols and grid[next_row][next_col] != '1':
                next_position = (next_row, next_col)

                # Tiến hành tìm kiếm nếu vị trí chưa có trong đường đi
                if next_position not in path:
                    result = search(path + [next_position], g_cost + 1, depth_limit)

                    if isinstance(result, list):  # Nếu tìm thấy đường đi
                        return result

                    min_cost = min(min_cost, result)

        return min_cost

    # Bắt đầu tìm kiếm với độ sâu tăng dần
    depth_limit = heuristic(start, destination)
    while True:
        result = search([start], 0, depth_limit)

        if isinstance(result, list):  # Nếu tìm thấy đường đi
            return result
        if result == math.inf:  # Không tìm thấy đường đi
            return []

        depth_limit = result  # Tăng độ sâu và thử lại




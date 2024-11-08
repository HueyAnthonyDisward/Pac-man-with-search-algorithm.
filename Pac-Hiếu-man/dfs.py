from collections import deque

def dfs_search(grid, start, destination):
    """
    Tìm đường đi từ ghost đến Pacman sử dụng DFS với cấu trúc tương tự như BFS.
    :param grid: Ma trận biểu thị bản đồ, với giá trị '1' là tường và các ô khác có thể đi qua.
    :param start: Tuple (x, y) - vị trí bắt đầu (ghost).
    :param destination: Tuple (x, y) - vị trí đích (Pacman).
    :return: Danh sách các tọa độ từ ghost đến Pacman nếu tìm thấy đường đi, ngược lại trả về [].
    """
    rows, cols = len(grid), len(grid[0])
    stack = [(start, [start])]  # Sử dụng stack thay vì queue cho DFS
    visited = set()
    visited.add(start)

    # Các hướng di chuyển: lên, trái, xuống, phải
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    while stack:
        current, path = stack.pop()


        if current == destination:
            return path


        for direction in directions:
            next_row, next_col = current[0] + direction[0], current[1] + direction[1]


            if 0 <= next_row < rows and 0 <= next_col < cols and grid[next_row][next_col] != '1':
                next_position = (next_row, next_col)
                if next_position not in visited:
                    visited.add(next_position)
                    stack.append((next_position, path + [next_position]))

    return []
from collections import deque

def bfs_search(grid, start, destination):
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start, [start])])
    visited = set()
    visited.add(tuple(start))


    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    while queue:
        (current, path) = queue.popleft()  

        # Kiểm tra nếu đã đến đích
        if current == destination:
            return path

        # Thử di chuyển đến các hướng kế tiếp
        for direction in directions:
            next_row, next_col = current[0] + direction[0], current[1] + direction[1]

            # Kiểm tra nếu tọa độ tiếp theo nằm trong phạm vi và không phải là tường
            if 0 <= next_row < rows and 0 <= next_col < cols and grid[next_row][next_col] != '1':
                next_position = (next_row, next_col)
                if next_position not in visited:
                    visited.add(next_position)  # Đánh dấu là đã thăm
                    queue.append((next_position, path + [next_position]))  # Thêm vào hàng đợi với đường đi mới

    return []  # Nếu không tìm thấy đường đi, trả về danh sách rỗng

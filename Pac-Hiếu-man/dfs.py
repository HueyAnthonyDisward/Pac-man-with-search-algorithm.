def dfs_search(grid, start, destination):
    max_depth = 70  # Độ sâu tìm kiếm tối đa để tránh "mắc kẹt" quá sớm
    rows, cols = len(grid), len(grid[0])
    stack = [(start, [start], 0)]  # Stack lưu trạng thái vị trí, đường đi và độ sâu hiện tại
    visited = set()
    visited.add(tuple(start))
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    while stack:
        (current, path, depth) = stack.pop()

        # Kiểm tra nếu đã đạt điểm đích
        if current == destination:
            return path

        if depth < max_depth:
            for direction in directions:
                next_row, next_col = current[0] + direction[0], current[1] + direction[1]

                # Kiểm tra điểm hợp lệ và chưa thăm
                if 0 <= next_row < rows and 0 <= next_col < cols and grid[next_row][next_col] != '1':
                    next_position = (next_row, next_col)
                    if next_position not in visited:
                        visited.add(next_position)
                        stack.append((next_position, path + [next_position], depth + 1))

    # Trả về đường đi ngắn nhất tìm được hoặc danh sách rỗng nếu không có
    return []

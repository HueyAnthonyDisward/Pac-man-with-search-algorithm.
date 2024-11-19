def is_valid(grid, row, col, path):
    rows, cols = len(grid), len(grid[0])
    return 0 <= row < rows and 0 <= col < cols and grid[row][col] != '1' and (row, col) not in path


# AC-3 để làm sạch không gian tìm kiếm trước khi thực hiện backtracking
# Hàm AC-3 tối ưu hóa chỉ cần cập nhật khi có thay đổi
def ac3(grid, start, destination):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Các hướng di chuyển: lên, xuống, trái, phải

    possible_moves = {(r, c): [] for r in range(rows) for c in range(cols)}

    # Kiểm tra các ô hợp lệ có thể di chuyển từ mỗi ô
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '1':  # Không phải tường
                for direction in directions:
                    next_r, next_c = r + direction[0], c + direction[1]
                    if 0 <= next_r < rows and 0 <= next_c < cols and grid[next_r][next_c] != '1':
                        possible_moves[(r, c)].append((next_r, next_c))

    return possible_moves


# Hàm backtracking tìm đường đi từ vị trí của Ghost đến Pacman
def backtrack(grid, ghost_position, pacman_position, possible_moves, max_depth=100):
    rows, cols = len(grid), len(grid[0])

    # Hàm đệ quy tìm kiếm đường đi
    def search(path, depth):
        if depth > max_depth:  # Dừng lại nếu vượt quá độ sâu tối đa
            return None

        current = path[-1]  # Vị trí hiện tại
        if current == pacman_position:  # Nếu đã đến Pacman
            return path

        # Duyệt qua các hướng di chuyển hợp lệ từ vị trí hiện tại
        for next_row, next_col in possible_moves[current]:
            if (next_row, next_col) not in path:  # Kiểm tra nếu điểm chưa được duyệt
                # Tìm kiếm tiếp từ điểm mới
                result = search(path + [(next_row, next_col)], depth + 1)
                if result:  # Nếu tìm được đường đi hợp lệ
                    return result

        return None  # Nếu không tìm thấy đường đi hợp lệ

    # Bắt đầu tìm kiếm từ vị trí của Ghost
    return search([ghost_position], 0)



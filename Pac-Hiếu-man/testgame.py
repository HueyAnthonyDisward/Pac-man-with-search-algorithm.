import math



MAP = [

    [' ',' ',' ',' ',' ','1',' ','1','s','r','o','1',' ','1',' ',' ',' ',' ',' '],
    ['1',' ',' ',' ','1',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','P','1'],
]



def manhattan_distance(pos1, pos2):
    """Tính khoảng cách Manhattan giữa hai vị trí."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def ghost_local_search(grid, ghost_position, pacman_position):
    """
    Thuật toán Local Search cho ghost.
    Ghost tìm đường tới pacman dựa trên khoảng cách Manhattan.

    grid: Ma trận lưới trò chơi (0 là ô trống, 1 là tường).
    ghost_position: Vị trí hiện tại của ghost (dòng, cột).
    pacman_position: Vị trí của pacman (dòng, cột).

    Trả về bước đi tiếp theo của ghost dưới dạng (row, col).
    """
    rows, cols = len(grid), len(grid[0])
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # Trái, Lên, Phải, Xuống
    best_move = None
    min_distance = math.inf

    for direction in directions:
        next_row = ghost_position[0] + direction[0]
        next_col = ghost_position[1] + direction[1]

        # Kiểm tra xem bước tiếp theo có hợp lệ không
        if 0 <= next_row < rows and 0 <= next_col < cols and grid[next_row][next_col] != '1':
            next_position = (next_row, next_col)
            # Tính khoảng cách tới Pacman
            distance = manhattan_distance(next_position, pacman_position)

            # Cập nhật bước đi tốt nhất
            if distance < min_distance:
                min_distance = distance
                best_move = next_position

    return best_move if best_move else ghost_position


def find_path_to_pacman(grid):
    """
    Tìm đường đi từ vị trí R (ghost) đến P (Pacman) trên bản đồ sử dụng local search.

    grid: Bản đồ trò chơi (2D list).

    Trả về: Danh sách các bước đi từ R đến P.
    """
    # Tìm vị trí của R và P trong bản đồ
    ghost_position = None
    pacman_position = None
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 'r':
                ghost_position = (i, j)
            elif cell == 'P':
                pacman_position = (i, j)

    if not ghost_position or not pacman_position:
        return "Vị trí ghost hoặc Pacman không tồn tại trên bản đồ!"

    path = [ghost_position]  # Lưu lại các bước di chuyển
    while ghost_position != pacman_position:
        # Tìm bước tiếp theo bằng thuật toán local search
        next_position = ghost_local_search(grid, ghost_position, pacman_position)

        # Nếu không di chuyển được, thoát vòng lặp
        if next_position == ghost_position:
            return "Không thể tìm được đường đi đến Pacman!"

        # Cập nhật vị trí ghost và thêm vào đường đi
        ghost_position = next_position
        path.append(ghost_position)

    return path


# Sử dụng hàm với bản đồ
path = find_path_to_pacman(MAP)
if isinstance(path, list):
    print("Đường đi từ R đến P:")
    for step in path:
        print(step)
else:
    print(path)
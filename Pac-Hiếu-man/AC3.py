import heapq

def min_consistent_ac3(grid):
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Các hướng di chuyển: lên, xuống, trái, phải

    possible_moves = {(r, c): [] for r in range(rows) for c in range(cols) if grid[r][c] != '1'}

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '1':  # Không phải tường
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '1':
                        possible_moves[(r, c)].append((nr, nc))

    queue = list(possible_moves.keys())
    while queue:
        current = queue.pop(0)
        updated = False
        neighbors = possible_moves[current]

        if not neighbors:
            del possible_moves[current]
            updated = True

        for neighbor in neighbors:
            if neighbor in possible_moves and current not in possible_moves[neighbor]:
                possible_moves[neighbor].remove(current)
                updated = True

            if updated:
                queue.append(neighbor)

    return possible_moves


def heuristic(a, b):
    """Tính toán khoảng cách Manhattan giữa hai ô."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def backtrack_with_ac3(grid, ghost_position, pacman_position, max_depth=100):
    possible_moves = min_consistent_ac3(grid)

    def search(path, depth):
        if depth > max_depth:  # Giới hạn độ sâu
            return None
        current = path[-1]
        if current == pacman_position:  # Đạt được Pacman
            return path

        # Sử dụng hàng đợi ưu tiên để tìm nước đi tốt nhất dựa trên heuristic
        pq = []
        for next_pos in possible_moves.get(current, []):
            if next_pos not in path:
                # Ưu tiên bước đi gần Pac-Man hơn
                priority = heuristic(next_pos, pacman_position)
                heapq.heappush(pq, (priority, next_pos))

        # Duyệt qua các bước đi trong hàng đợi ưu tiên
        while pq:
            _, next_pos = heapq.heappop(pq)
            result = search(path + [next_pos], depth + 1)
            if result:
                return result

        return None

    return search([ghost_position], 0)

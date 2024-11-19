import heapq

def heuristic(a, b):
    # Khoảng cách Manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(grid, start, destination):
    rows, cols = len(grid), len(grid[0])
    open_list = []
    heapq.heappush(open_list, (0, start))  # (f_score, node)
    g_scores = {start: 0}  # Chi phí từ start đến mỗi node
    f_scores = {start: heuristic(start, destination)}  # f_score = g_score + h_score
    came_from = {}

    # Các hướng di chuyển: lên, trái, xuống, phải
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == destination:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # Đảo ngược lại để có đường đi từ start đến destination

        for direction in directions:
            next_row, next_col = current[0] + direction[0], current[1] + direction[1]

            if 0 <= next_row < rows and 0 <= next_col < cols and grid[next_row][next_col] != '1':
                next_position = (next_row, next_col)
                tentative_g_score = g_scores[current] + 1

                if next_position not in g_scores or tentative_g_score < g_scores[next_position]:
                    came_from[next_position] = current
                    g_scores[next_position] = tentative_g_score
                    f_scores[next_position] = tentative_g_score + heuristic(next_position, destination)
                    heapq.heappush(open_list, (f_scores[next_position], next_position))

    return []

import heapq

def heuristic(a, b):
    # Khoảng cách Manhattan : |x1 - x2| + |y1 - y2|
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(grid, start, destination):
    rows, cols = len(grid), len(grid[0])
    open_list = []
    heapq.heappush(open_list, (0, start))  # (f_score, node)
    g_scores = {start: 0}  # Chi phí từ start đến mỗi node
    f_scores = {start: heuristic(start, destination)}  # f_score = g_score + h_score
    came_from = {}

    '''
    grid: Lưới (grid) đại diện cho bản đồ, với các ô có thể là "0" (trống) hoặc "1" (chướng ngại vật).
    start: Vị trí bắt đầu (start node), là một tuple (x, y) chỉ tọa độ của điểm bắt đầu.
    destination: Vị trí đích (destination node), là một tuple (x, y) chỉ tọa độ của điểm đích.
    open_list: Một danh sách ưu tiên (sử dụng heapq để quản lý) chứa các ô sẽ được khám phá. Các phần tử là tuple (f_score, node) trong đó f_score = g_score + h_score.
    g_scores: Một từ điển (dictionary) lưu chi phí từ điểm bắt đầu đến mỗi điểm (node). Khởi tạo với điểm bắt đầu có g_score = 0.
    f_scores: Một từ điển lưu giá trị f_score cho mỗi điểm (node), tính bằng g_score + h_score.
    came_from: Một từ điển lưu trữ điểm đến của mỗi điểm (node) trong quá trình tìm kiếm. Dùng để xây dựng lại đường đi khi tìm thấy đích.
    
    '''
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
        '''
        Thuật toán tiếp tục lặp qua các điểm trong open_list, chọn điểm có f_score nhỏ nhất (sử dụng heapq).
        Nếu điểm current là điểm đích (destination), thuật toán sẽ xây dựng lại đường đi từ điểm đích về điểm bắt đầu, sử dụng từ điển came_from.
        Đường đi sẽ được đảo ngược ([::-1]) để có đường đi từ điểm bắt đầu đến điểm đích.
        '''
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

        '''
        Đối với mỗi điểm lân cận của current, thuật toán tính toán chi phí tạm thời tentative_g_score là chi phí từ điểm bắt đầu đến điểm lân cận này.
        Nếu điểm lân cận chưa được khám phá hoặc có chi phí g_score nhỏ hơn chi phí hiện tại, thuật toán cập nhật lại came_from, g_scores, và f_scores, sau đó thêm điểm này vào open_list.
        '''

    return []



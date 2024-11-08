from collections import deque

# Hàm bfs_search đã được định nghĩa ở trên
from bfs import bfs_search
from dfs import dfs_search
from settings import MAP
from Astar import a_star_search
'''
def convert_map(MAP):
    # Tạo ma trận mới với giá trị chuyển đổi
    converted_map = []

    for row in MAP:
        # Mỗi phần tử trong hàng, nếu là ' ' thì thay bằng 0, nếu là '1' thì thay bằng 1
        converted_row = [1 if cell == '1' else 0 for cell in row]
        converted_map.append(converted_row)



    return converted_map

for row in converted_map:
print(row)

# Gọi hàm để chuyển đổi MAP
converted_map = convert_map(MAP)

'''


# In ma trận đã chuyển đổi
mapping = MAP
start = (7, 9)
destination = (15, 9)

for row in mapping:
    print(row)
def test_bfs():
    path = bfs_search(mapping,start,destination)

    if path:
        print("Path found for bfs:", path)
    else:
        print("No path found")

def test_dfs():
    path = dfs_search(mapping,start,destination)
    if path:
        print("Path found for dfs:", path)
    else:
        print("No path found")

def test_astar():
    path = a_star_search(mapping,start,destination)
    if path:
        print("Path found for Astar:", path)
    else:
        print("No path found")

test_bfs()
test_dfs()
test_astar()
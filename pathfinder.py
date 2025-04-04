import sys
import math
import heapq
from collections import deque

# Constants
STUDENT_ID = 'a1851614'
DEGREE = 'UG'


DIRS = {(-1, 0), (1, 0), (0, -1), (0, 1)}  # UDLR

def read_map(file_path):
    with open(file_path) as f:
        lines = [line.strip() for line in f if line.strip()]
        
    rows, cols = map(int, lines[0].split())
    start = tuple(map(lambda x: int(x)-1, lines[1].split()))
    end = tuple(map(lambda x: int(x)-1, lines[2].split()))
    grid = [line.split() for line in lines[3:]]
    return rows, cols, start, end, grid




def elevation_cost(curr, next):
    diff = int(nxt) - int(curr)
    return 1 + max(0, diff)





def calc_heuristic(a, b, htype):
    dx, dy = abs(a[0]-b[0]), abs(a[1]-b[1])
    return dx + dy if htype == 'manhattan' else math.sqrt(dx**2 + dy**2)




def bfs(rows, cols, start, end, grid):
    queue = deque([(start, [start])])
    visited = set()
    visits = [[0]*cols for _ in range(rows)]
    first = [[None]*cols for _ in range(rows)]
    last = [[None]*cols for _ in range(rows)]
    order = 1

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        visits[x][y] += 1
        if first[x][y] is None:
            first[x][y] = order
        last[x][y] = order
        order += 1
        if (x, y) == end:
            return path, visits, first, last
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 'X' and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [(nx, ny)]))
    return None, visits, first, last




def ucs(rows, cols, start, end, grid):
    heap = [(0, 0, start, [start])]
    visited = set()
    visits = [[0]*cols for _ in range(rows)]
    first = [[None]*cols for _ in range(rows)]
    last = [[None]*cols for _ in range(rows)]
    order = 1

    while heap:
        cost, counter, (x, y), path = heapq.heappop(heap)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        visits[x][y] += 1
        if first[x][y] is None:
            first[x][y] = order
        last[x][y] = order
        order += 1
        if (x, y) == end:
            return path, visits, first, last
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 'X' and (nx, ny) not in visited:
                new_cost = cost + elevation_cost(grid[x][y], grid[nx][ny])
                heapq.heappush(heap, (new_cost, order, (nx, ny), path + [(nx, ny)]))
    return None, visits, first, last




def astar(rows, cols, start, end, grid, htype):
    heap = [(0, 0, 0, start, [start])]
    visited = set()
    visits = [[0]*cols for _ in range(rows)]
    first = [[None]*cols for _ in range(rows)]
    last = [[None]*cols for _ in range(rows)]
    order = 1

    while heap:
        f, g, counter, (x, y), path = heapq.heappop(heap)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        visits[x][y] += 1
        if first[x][y] is None:
            first[x][y] = order
        last[x][y] = order
        order += 1
        if (x, y) == end:
            return path, visits, first, last
        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 'X' and (nx, ny) not in visited:
                new_g = g + elevation_cost(grid[x][y], grid[nx][ny])
                h = heuristic((nx, ny), end, htype)
                heapq.heappush(heap, (new_g + h, new_g, order, (nx, ny), path + [(nx, ny)]))
    return None, visits, first, last





def print_debug(grid, path, visits, first, last):
    rows, cols = len(grid), len(grid[0])
    path_set = set(path or [])
    print("path:")
    for i in range(rows):
        print(' '.join('*' if (i, j) in path_set else grid[i][j] for j in range(cols)))
    def print_matrix(mat, label):
        print(label + ":")
        for i in range(rows):
            print(' '.join('X' if grid[i][j] == 'X' else (str(mat[i][j]).rjust(2) if mat[i][j] is not None else '.') for j in range(cols)))
    print_matrix(visits, "#visits")
    print_matrix(first, "first visit")
    print_matrix(last, "last visit")



def print_release(grid, path):
    rows, cols = len(grid), len(grid[0])
    path_set = set(path or [])
    for i in range(rows):
        print(' '.join('*' if (i, j) in path_set else grid[i][j] for j in range(cols)))


def main():
    if len(sys.argv) < 4:
        print("Usage: python pathfinder.py [mode] [map] [algorithm] [heuristic]")
        return

    mode, map_file, algo = sys.argv[1:4]
    heuristic_type = sys.argv[4] if len(sys.argv) > 4 else None
    rows, cols, start, end, grid = parse_map(map_file)

    if algo == 'bfs':
        path, visits, first, last = bfs(rows, cols, start, end, grid)
    elif algo == 'ucs':
        path, visits, first, last = ucs(rows, cols, start, end, grid)
    elif algo == 'astar':
        if heuristic_type not in ('manhattan', 'euclidean'):
            print("Please provide a valid heuristic: manhattan or euclidean")
            return
        path, visits, first, last = astar(rows, cols, start, end, grid, heuristic_type)
    else:
        print("Unsupported algorithm")
        return

    if mode == 'debug':
        if path:
            print_debug(grid, path, visits, first, last)
        else:
            print("path:\nnull")
            print_debug(grid, [], visits, first, last)
    else:
        print_release(grid, path) if path else print("null")

if __name__ == '__main__':
    main()

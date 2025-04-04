import sys
import math
import heapq
from collections import deque
from heapq import heappop, heappush

STUDENT_ID = 'a1851614'
DEGREE = 'UG'

"""
Integrity Notice:

Ai has been used as a googling tool and support in understanding the problem; but has not been used to write the code. 

For exammple, one submission i had approx 4/10 test cases and in some questions achieved the correct cost eval and heuristic but a wrong path. I used an LLM to understand the problem and the algorithm, but not to write the code; it gave 
me some ideas of direction to go in and i explored them and coded them on my own. 

Also, as a student that has used C++ and not python for 3 years, i used a llm to understand the syntax, or particulary how to convert a c++ code to python. Such as line splitting, or how to use a heapq in python ( a task i know but not the 
syntax). I also used sites like Geeks for Geeks etc. to understand the syntax of the language; not jsut LLM.
- An example case,  is the parse map function, which is a direct conversion of a c++ code to python, and i used an LLM to understand the syntax and requiremtns of the language.
- My main concern is the generic naming conventions like dx, dy or nx, ny. These were conventions provided to me by the LLM as python syntax overview and i used them to understand the problem. 

If you have any questions or concerns, please feel free to reach out to me. I am happy to provide more information about my process and how I approached the assignment 
( including a github commit history and a physcial log/working document of my process).

"""




# DONT CHANGE ORDER DUMBASS. 
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # UDLR


def parse_map(path):

    with open(path) as f:
        lines = [line.strip() for line in f if line.strip()]
    rows, cols = map(int, lines[0].split())
    start = tuple(map(lambda x: int(x)-1, lines[1].split()))
    end = tuple(map(lambda x: int(x)-1, lines[2].split()))
    grid = [line.split() for line in lines[3:]]
    return rows, cols, start, end, grid


def elevation_cost(curr, nxt):
    diff = int(nxt) - int(curr)
    return 1 + max(0, diff)



def heuristic(a, b, htype):
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

    heap = [(0, 0, start, [start])]  # (cost, tie-breaker, position, path)
    cost_so_far = {start: 0} 
    visits = [[0 for _ in range(cols)] for _ in range(rows)]
    first = [[None for _ in range(cols)] for _ in range(rows)]
    last = [[None for _ in range(cols)] for _ in range(rows)]

    order = 1 
    counter = 0  

    while heap:
        cost, _, (x, y), path = heappop(heap)

        visits[x][y] += 1
        if first[x][y] is None:
            first[x][y] = order
        last[x][y] = order
        order += 1

        if (x, y) == end:
            return path, visits, first, last

        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 'X':
                step_cost = elevation_cost(grid[x][y], grid[nx][ny])
                new_cost = cost + step_cost

                if (nx, ny) not in cost_so_far or new_cost < cost_so_far[(nx, ny)]:
                    cost_so_far[(nx, ny)] = new_cost
                    counter += 1
                    heappush(heap, (new_cost, counter, (nx, ny), path + [(nx, ny)]))

    return None, visits, first, last





def astar(rows, cols, start, end, grid, htype):

    heap = [(heuristic(start, end, htype), 0, 0, start, [start])]
    cost_so_far = {start: 0}
    visits = [[0]*cols for _ in range(rows)]
    first = [[None]*cols for _ in range(rows)]
    last = [[None]*cols for _ in range(rows)]
    order = 1
    counter = 0

    while heap:
        f, g, _, (x, y), path = heapq.heappop(heap)

        visits[x][y] += 1
        if first[x][y] is None:
            first[x][y] = order
        last[x][y] = order
        order += 1

        if (x, y) == end:
            return path, visits, first, last

        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 'X':
                new_g = g + elevation_cost(grid[x][y], grid[nx][ny])
                if (nx, ny) not in cost_so_far or new_g < cost_so_far[(nx, ny)]:
                    cost_so_far[(nx, ny)] = new_g
                    h = heuristic((nx, ny), end, htype)
                    counter += 1
                    heapq.heappush(heap, (new_g + h, new_g, counter, (nx, ny), path + [(nx, ny)]))

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
        path, visits, first, last = astar(rows, cols, start, end, grid, heuristic_type)
    else:
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

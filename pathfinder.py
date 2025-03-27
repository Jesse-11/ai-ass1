#!/usr/bin/python3.10.6
import math
from collections import deque
import heapq

STUDENT_ID = 'a1851614'
DEGREE = 'UG'

"""--------------------------Helper functions--------------------------"""

def parse_map(map_file):
    with open(map_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        rows, cols = map(int, lines[0].split())
        start = tuple(map(int, lines[1].split()))
        end = tuple(map(int, lines[2].split()))
        grid = [line.split() for line in lines[3:3+rows]]
    return {'rows': rows, 'cols': cols, 'start': start, 'end': end, 'grid': grid}


def euclidean_heuristic(i, j, end_i, end_j):
    return math.sqrt((i - end_i)**2 + (j - end_j)**2)

def manhattan_heuristic(i, j, end_i, end_j):
    return abs(i - end_i) + abs(j - end_j)

def reconstruct_path(parents, end):
    path = []
    while end in parents:
        path.append(end)
        end = parents[end]
    return list(reversed(path)) if path else None












""""--------------------------Search functions--------------------------"""

def search(map_data, algorithm, heuristic=None):
    grid = map_data['grid']
    start = map_data['start']
    end = map_data['end']
    rows, cols = map_data['rows'], map_data['cols']
    
    if grid[start[0]-1][start[1]-1] == 'X' or grid[end[0]-1][end[1]-1] == 'X':
        return None, [[0]*cols for _ in range(rows)], [[0]*cols for _ in range(rows)], [[0]*cols for _ in range(rows)]
    
    parents = {}
    visit_count = [[0]*cols for _ in range(rows)]
    first_visit = [[0]*cols for _ in range(rows)]
    last_visit = [[0]*cols for _ in range(rows)]
    counter = 1
    
    if algorithm == 'bfs':
        q = deque([start])
        parents[start] = None
        visit_count[start[0]-1][start[1]-1] = 1
        first_visit[start[0]-1][start[1]-1] = counter
        last_visit[start[0]-1][start[1]-1] = counter
        counter += 1
        
        while q:
            i, j = q.popleft()
            if (i, j) == end: break
            
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                ni, nj = i+dx, j+dy
                if 1<=ni<=rows and 1<=nj<=cols and grid[ni-1][nj-1] != 'X' and (ni, nj) not in parents:
                    parents[(ni, nj)] = (i, j)
                    q.append((ni, nj))
                    visit_count[ni-1][nj-1] += 1
                    if not first_visit[ni-1][nj-1]:
                        first_visit[ni-1][nj-1] = counter
                    last_visit[ni-1][nj-1] = counter
                    counter += 1
                    
    elif algorithm in ['ucs', 'astar']:
        heap = [(0, 0, start, 0)]
        g_values = {start: 0}
        parents[start] = None
        visit_count[start[0]-1][start[1]-1] = 1
        first_visit[start[0]-1][start[1]-1] = counter
        last_visit[start[0]-1][start[1]-1] = counter
        counter += 1
        
        while heap:
            _, _, (i, j), g = heapq.heappop(heap)
            if (i, j) == end: break
            if g > g_values.get((i, j), float('inf')): continue
            
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                ni, nj = i+dx, j+dy
                if 1<=ni<=rows and 1<=nj<=cols and grid[ni-1][nj-1] != 'X':
                    curr_e = int(grid[i-1][j-1])
                    next_e = int(grid[ni-1][nj-1])
                    cost = g + 1 + max(0, next_e - curr_e)
                    
                    if cost < g_values.get((ni, nj), float('inf')):
                        g_values[(ni, nj)] = cost
                        parents[(ni, nj)] = (i, j)
                        priority = cost
                        if algorithm == 'astar':
                            priority += heuristic(ni, nj, end[0], end[1])
                        heapq.heappush(heap, (priority, counter, (ni, nj), cost))
                        visit_count[ni-1][nj-1] += 1
                        if not first_visit[ni-1][nj-1]:
                            first_visit[ni-1][nj-1] = counter
                        last_visit[ni-1][nj-1] = counter
                        counter += 1
    
    path = reconstruct_path(parents, end)
    return path, visit_count, first_visit, last_visit

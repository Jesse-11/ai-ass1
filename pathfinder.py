import sys
import math
import heapq
from collections import deque

# Constants
STUDENT_ID = 'a1851614'
DEGREE = 'UG'

def read_map(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
    rows, cols = map(int, lines[0].strip().split())
    start = tuple(map(int, lines[1].strip().split()))
    start = (start[0] - 1, start[1] - 1)  # Convert to 0-indexed
    end = tuple(map(int, lines[2].strip().split()))
    end = (end[0] - 1, end[1] - 1)  # Convert to 0-indexed
    
    # Parse map
    map_data = []
    for i in range(3, 3 + rows):
        row = lines[i].strip().split()
        map_data.append(row)
    
    return map_data, start, end, rows, cols




def step_cost(map_data, current_pos, new_pos):
    # check if state is a wall, had issues with this not calculationg cost correct. Forved to be unreasoble in cost. 
    if map_data[new_pos[0]][new_pos[1]] == 'X':
        return float('inf')

    current_elev = int(map_data[current_pos[0]][current_pos[1]])
    new_elev = int(map_data[new_pos[0]][new_pos[1]])
    elev_diff = new_elev - current_elev
    return 1 + max(0, elev_diff)





def calc_heuristic(current_pos, goal_pos, heuristic):
    if heuristic == 'euclidean':
        return math.sqrt((current_pos[0] - goal_pos[0])**2 + (current_pos[1] - goal_pos[1])**2)
    else:  # manhattan
        return abs(current_pos[0] - goal_pos[0]) + abs(current_pos[1] - goal_pos[1])






def graph_search(map_data, start, end, rows, cols, algorithm, heuristic=None):
    visit_count = [[0 for _ in range(cols)] for _ in range(rows)]
    first_visit = [[0 for _ in range(cols)] for _ in range(rows)]
    last_visit = [[0 for _ in range(cols)] for _ in range(rows)]
    visit_order = 0
    
    parent = {}
    cost = {}
    parent[start] = None
    cost[start] = 0
    
    if algorithm == 'bfs':
        fringe = deque([start])
    else:
        fringe = []
        initial_cost = 0
        if algorithm == 'astar':
            initial_cost += calc_heuristic(start, end, heuristic)
        heapq.heappush(fringe, (initial_cost, visit_order, start))
    
    closed = set()
    
    while fringe:
        if algorithm == 'bfs':
            state = fringe.popleft()
            current_cost = cost[state]
        else:
            current_f_cost, _, state = heapq.heappop(fringe)
            current_cost = cost[state]
        
        row, col = state
        visit_order += 1
        visit_count[row][col] += 1
        if first_visit[row][col] == 0:
            first_visit[row][col] = visit_order
        last_visit[row][col] = visit_order
        
        if state == end:
            path = []
            current = end
            while current is not None:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path, visit_count, first_visit, last_visit
        
        if state not in closed:
            closed.add(state)
            
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
            for direction in directions:
                new_row = state[0] + direction[0]
                new_col = state[1] + direction[1]
                
                if (0 <= new_row < rows and 
                    0 <= new_col < cols):
                    
                    if map_data[new_row][new_col] == 'X':
                        continue
                        
                    new_state = (new_row, new_col)
                    step = step_cost(map_data, state, new_state)
                    
                    if algorithm == 'bfs':
                        new_cost = current_cost + 1
                    else:
                        new_cost = current_cost + step
                    
                    if new_state not in cost or new_cost < cost[new_state]:
                        cost[new_state] = new_cost
                        parent[new_state] = state
                        
                        if algorithm == 'bfs':
                            fringe.append(new_state)
                        elif algorithm == 'ucs':
                            heapq.heappush(fringe, (new_cost, visit_order, new_state))
                        elif algorithm == 'astar':
                            f_cost = new_cost + calc_heuristic(new_state, end, heuristic)
                            heapq.heappush(fringe, (f_cost, visit_order, new_state))
    
    return None, visit_count, first_visit, last_visit






def print_output(map_data, path, visit_count, first_visit, last_visit, mode):
    rows, cols = len(map_data), len(map_data[0])
    
    if path is None:
        if mode == 'debug':
            print("path:")
            print("null")
            
            print("#visits:")
            for i in range(rows):
                for j in range(cols):
                    if map_data[i][j] == 'X':
                        print('X', end=' ')
                    elif visit_count[i][j] == 0:
                        print('.', end=' ')
                    else:
                        print(visit_count[i][j], end=' ')
                print()
            
            print("first visit:")
            for i in range(rows):
                for j in range(cols):
                    if map_data[i][j] == 'X':
                        print('  X', end='')
                    elif first_visit[i][j] == 0:
                        print('  .', end='')
                    else:
                        print(f'{first_visit[i][j]:3d}', end='')
                print()
            
            print("last visit:")
            for i in range(rows):
                for j in range(cols):
                    if map_data[i][j] == 'X':
                        print('  X', end='')
                    elif last_visit[i][j] == 0:
                        print('  .', end='')
                    else:
                        print(f'{last_visit[i][j]:3d}', end='')
                print()
        else:
            print("null")
        return
    
    # Create path matrix
    path_matrix = [[False for _ in range(cols)] for _ in range(rows)]
    for pos in path:
        path_matrix[pos[0]][pos[1]] = True
    
    if mode == 'debug':
        print("path:")
    for i in range(rows):
        for j in range(cols):
            if path_matrix[i][j]:
                print('*', end=' ')
            else:
                print(map_data[i][j], end=' ')
        print()
    
    if mode == 'debug':
        print("#visits:")
        for i in range(rows):
            for j in range(cols):
                if map_data[i][j] == 'X':
                    print('X', end=' ')
                elif visit_count[i][j] == 0:
                    print('.', end=' ')
                else:
                    print(visit_count[i][j], end=' ')
            print()
        
        print("first visit:")
        for i in range(rows):
            for j in range(cols):
                if map_data[i][j] == 'X':
                    print('  X', end='')
                elif first_visit[i][j] == 0:
                    print('  .', end='')
                else:
                    print(f'{first_visit[i][j]:3d}', end='')
            print()
        
        print("last visit:")
        for i in range(rows):
            for j in range(cols):
                if map_data[i][j] == 'X':
                    print('  X', end='')
                elif last_visit[i][j] == 0:
                    print('  .', end='')
                else:
                    print(f'{last_visit[i][j]:3d}', end='')
            print()

def main():
    mode = sys.argv[1]
    map_file = sys.argv[2]
    algorithm = sys.argv[3]
    heuristic = sys.argv[4] if len(sys.argv) > 4 else None
    
    # Read map
    map_data, start, end, rows, cols = read_map(map_file)
    
    # Run search algorithm
    path, visit_count, first_visit, last_visit = graph_search(map_data, start, end, rows, cols, algorithm, heuristic)
    
    # Print output
    print_output(map_data, path, visit_count, first_visit, last_visit, mode)

if __name__ == "__main__":
    main()
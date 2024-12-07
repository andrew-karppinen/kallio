import heapq


def heuristic(a, b):
    """Manhattan distance heuristic for grid"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal, free_value):
    """A* algorithm implementation for a grid with specific constraints"""
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            return reconstruct_path(came_from, current, start)

        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Down, Left, Up
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] != free_value and neighbor != goal:
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []


def reconstruct_path(came_from, current, start):
    """Reconstruct path from start to goal, excluding the start point"""
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

if __name__ == '__main__':
    # Example usage
    grid = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 0, 0, 0]
    ]
    start = (0, 0)
    goal = (4, 4)
    free_value = 0

    path = astar(grid, start, goal, free_value)
    print("Path:", path)


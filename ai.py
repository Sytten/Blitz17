import heapq


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

def cost(game, current, next):

    cost = 1
    if next in game.spikes_locs:
        cost = 5

    return 1

def heuristic(game, goal, next):
    return 1

def a_star_search(game, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in game.board.neighbors(current):
            new_cost = cost_so_far[current] + cost(game, current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(game, goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]

    while current != start:
        current = came_from[current]
        path.append(current)
    # path.append(start) # optional
    path.reverse() # optional
    return path


def next_move(game, start, goal):
    came_from, cost_so_far = a_star_search(game, start, goal)

    path = reconstruct_path(came_from, start, goal)

    if len(path) < 2:
        return 'Stay'

    return game.board.direction_to(start, path[1])


# WHAT WHEN NO SOLUTION PLIZZ

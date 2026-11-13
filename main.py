
# aisc project done by saara tarini suyash

from collections import deque
import heapq
import time


# maze is premade

maze = [
    ['S', 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
    [0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 'G']
]

# ---------------- MAZE ENVIRONMENT ----------------

class MazeEnvironment:

    def __init__(self, maze):

        if not maze or not maze[0]:
            raise ValueError("Maze cannot be empty.")

        if any(len(row) != len(maze[0]) for row in maze):
            raise ValueError("Maze must be rectangular.")

        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])

        self.start = None
        self.goal = None

        for r in range(self.rows):
            for c in range(self.cols):

                if maze[r][c] == 'S':
                    if self.start is not None:
                        raise ValueError("Multiple start positions.")
                    self.start = (r, c)

                elif maze[r][c] == 'G':
                    if self.goal is not None:
                        raise ValueError("Multiple goal positions.")
                    self.goal = (r, c)

        if self.start is None or self.goal is None:
            raise ValueError("Maze must contain S and G.")

        self.actions = {
            "UP": (-1, 0),
            "DOWN": (1, 0),
            "LEFT": (0, -1),
            "RIGHT": (0, 1)
        }

    def is_valid_position(self, position):

        r, c = position

        return (
            0 <= r < self.rows
            and 0 <= c < self.cols
            and self.maze[r][c] != 1
        )

    def get_neighbors(self, position):

        neighbors = []

        for dr, dc in self.actions.values():

            next_position = (
                position[0] + dr,
                position[1] + dc
            )

            if self.is_valid_position(next_position):
                neighbors.append(next_position)

        return neighbors

    def get_next_position(self, position, action):

        if action not in self.actions:
            return None

        dr, dc = self.actions[action]

        next_position = (
            position[0] + dr,
            position[1] + dc
        )

        if self.is_valid_position(next_position):
            return next_position

        return None

    def is_goal(self, position):
        return position == self.goal

    def display(self, path=None, agent_position=None):

        display_maze = [row[:] for row in self.maze]

        if path:
            for r, c in path:
                if display_maze[r][c] not in ('S', 'G'):
                    display_maze[r][c] = '*'

        if agent_position is not None:
            r, c = agent_position

            if display_maze[r][c] not in ('S', 'G'):
                display_maze[r][c] = 'A'

        print("\nMaze:")

        for row in display_maze:
            print(" ".join(str(cell) for cell in row))


# ---------------- INTELLIGENT AGENT ----------------

class IntelligentAgent:

    def __init__(self, environment):

        self.environment = environment

        self.position = environment.start
        self.goal = environment.goal

        self.visited = {self.position}
        self.movement_history = []

        self.status = "ACTIVE"

    def perceive(self):

        return {
            "current_position": self.position,
            "goal_position": self.goal,
            "valid_neighbors":
                self.environment.get_neighbors(self.position),
            "visited_positions": self.visited.copy()
        }

    def act(self, action):

        if self.status != "ACTIVE":
            print("Agent is not active.")
            return False

        next_position = self.environment.get_next_position(
            self.position, action
        )

        if next_position is None:
            print("Invalid movement:", action)
            return False

        previous_position = self.position
        self.position = next_position

        self.visited.add(self.position)

        self.movement_history.append({
            "from": previous_position,
            "action": action,
            "to": self.position
        })

        print("agent moved to:", action)
        print("new position is now:", self.position)

        self.evaluate()

        return True

    def evaluate(self):

        if self.environment.is_goal(self.position):
            self.status = "SUCCESS"
            print("\ngoal was reached")

        return self.status

    def display_status(self):

        print("\n========== AGENT STATUS ==========")
        print("position:", self.position)
        print("goal:", self.goal)
        print("visited:", self.visited)
        print("movement history:", self.movement_history)
        print("status:", self.status)
        print("==================================")


# ============================================================
# SEARCH ALGORITHMS
# ============================================================

def reconstruct_path(parent, start, goal):

    path = []
    current = goal

    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()

    return path


def heuristic(position, goal):

    return (
        abs(position[0] - goal[0])
        + abs(position[1] - goal[1])
    )


# ---------------- 1. BFS ----------------

def bfs(environment, start, goal):

    start_time = time.perf_counter()

    queue = deque([start])
    visited = {start}
    parent = {}
    explored_nodes = 0

    while queue:

        current = queue.popleft()
        explored_nodes += 1

        if current == goal:
            return (
                reconstruct_path(parent, start, goal),
                explored_nodes,
                time.perf_counter() - start_time
            )

        for neighbor in environment.get_neighbors(current):

            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    return None, explored_nodes, time.perf_counter() - start_time


# ---------------- 2. DFS ----------------

def dfs(environment, start, goal):

    start_time = time.perf_counter()

    stack = [start]
    visited = {start}
    parent = {}
    explored_nodes = 0

    while stack:

        current = stack.pop()
        explored_nodes += 1

        if current == goal:
            return (
                reconstruct_path(parent, start, goal),
                explored_nodes,
                time.perf_counter() - start_time
            )

        for neighbor in environment.get_neighbors(current):

            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    return None, explored_nodes, time.perf_counter() - start_time


# ---------------- 3. GREEDY BEST-FIRST SEARCH ----------------

def greedy_best_first_search(environment, start, goal):

    start_time = time.perf_counter()

    priority_queue = []
    counter = 0

    heapq.heappush(
        priority_queue,
        (heuristic(start, goal), counter, start)
    )

    visited = {start}
    parent = {}
    explored_nodes = 0

    while priority_queue:

        _, _, current = heapq.heappop(priority_queue)
        explored_nodes += 1

        if current == goal:
            return (
                reconstruct_path(parent, start, goal),
                explored_nodes,
                time.perf_counter() - start_time
            )

        for neighbor in environment.get_neighbors(current):

            if neighbor not in visited:

                visited.add(neighbor)
                parent[neighbor] = current
                counter += 1

                heapq.heappush(
                    priority_queue,
                    (heuristic(neighbor, goal), counter, neighbor)
                )

    return None, explored_nodes, time.perf_counter() - start_time


# ---------------- 4. A* ----------------

def a_star(environment, start, goal):

    start_time = time.perf_counter()

    priority_queue = []
    counter = 0

    heapq.heappush(
        priority_queue,
        (heuristic(start, goal), counter, start)
    )

    g_score = {start: 0}
    parent = {}
    closed_set = set()
    explored_nodes = 0

    while priority_queue:

        _, _, current = heapq.heappop(priority_queue)

        if current in closed_set:
            continue

        closed_set.add(current)
        explored_nodes += 1

        if current == goal:
            return (
                reconstruct_path(parent, start, goal),
                explored_nodes,
                time.perf_counter() - start_time
            )

        for neighbor in environment.get_neighbors(current):

            if neighbor in closed_set:
                continue

            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbor, float('inf')):

                parent[neighbor] = current
                g_score[neighbor] = tentative_g

                f_score = tentative_g + heuristic(neighbor, goal)

                counter += 1

                heapq.heappush(
                    priority_queue,
                    (f_score, counter, neighbor)
                )

    return None, explored_nodes, time.perf_counter() - start_time


# ---------------- 5. HILL CLIMBING ----------------

def hill_climbing(environment, start, goal):

    start_time = time.perf_counter()

    current = start
    visited = {start}
    path = [start]
    explored_nodes = 0

    while current != goal:

        explored_nodes += 1

        neighbors = [
            neighbor
            for neighbor in environment.get_neighbors(current)
            if neighbor not in visited
        ]

        if not neighbors:
            return None, explored_nodes, time.perf_counter() - start_time

        best_neighbor = min(
            neighbors,
            key=lambda position: heuristic(position, goal)
        )

        if heuristic(best_neighbor, goal) >= heuristic(current, goal):
            return None, explored_nodes, time.perf_counter() - start_time

        current = best_neighbor
        visited.add(current)
        path.append(current)

    explored_nodes += 1

    return path, explored_nodes, time.perf_counter() - start_time


# ---------------- 6. IDDFS ----------------

def iddfs(environment, start, goal):

    start_time = time.perf_counter()
    explored_nodes = 0

    def depth_limited_search(current, depth_limit, path, parent):

        nonlocal explored_nodes
        explored_nodes += 1

        if current == goal:
            return True

        if depth_limit == 0:
            return False

        for neighbor in environment.get_neighbors(current):

            if neighbor not in path:

                parent[neighbor] = current
                path.add(neighbor)

                if depth_limited_search(
                    neighbor, depth_limit - 1, path, parent
                ):
                    return True

                path.remove(neighbor)
                parent.pop(neighbor)

        return False

    max_depth = environment.rows * environment.cols

    for depth_limit in range(max_depth + 1):

        path = {start}
        parent = {}

        if depth_limited_search(
            start, depth_limit, path, parent
        ):
            return (
                reconstruct_path(parent, start, goal),
                explored_nodes,
                time.perf_counter() - start_time
            )

    return None, explored_nodes, time.perf_counter() - start_time


# ============================================================
# DECISION-MAKING MODULE
# ============================================================

class DecisionMaker:

    def __init__(self):

        self.algorithms = {
            "1": ("bfs", bfs),
            "2": ("dfs", dfs),
            "3": ("greedy best",
                  greedy_best_first_search),
            "4": ("a*", a_star),
            "5": ("hill climbing", hill_climbing),
            "6": ("iterative deepening algo", iddfs)
        }

    # Select an algorithm
    def select_algorithm(self):

        print("\n")
        print("choose from any algorithm")
        print("\n")

        for key, (name, function) in self.algorithms.items():
            print(f"{key}. {name}")

        choice = input("\nenter algo: ")

        if choice not in self.algorithms:
            print("invalid choice")
            return None

        return choice

    # Calculate route
    def calculate_route(self, agent, choice):

        algorithm_name, algorithm_function = self.algorithms[choice]

        print("\nagent decision maker is awake now ")

        # Obtain current agent information
        observation = agent.perceive()

        start = observation["current_position"]
        goal = observation["goal_position"]

        print("current position:", start)
        print("destination:", goal)

        # Execute selected search algorithm
        path, explored_nodes, execution_time = algorithm_function(
            agent.environment,
            start,
            goal
        )

        if path is None:

            print("\ndecision maker says that algorithm cannot reach goal state")

            return None

        # Convert positions into movement actions
        actions = []

        action_map = {
            (-1, 0): "UP",
            (1, 0): "DOWN",
            (0, -1): "LEFT",
            (0, 1): "RIGHT"
        }

        for i in range(len(path) - 1):

            current = path[i]
            next_position = path[i + 1]

            difference = (
                next_position[0] - current[0],
                next_position[1] - current[1]
            )

            actions.append(action_map[difference])

        return {
            "algorithm": algorithm_name,
            "path": path,
            "actions": actions,
            "explored_nodes": explored_nodes,
            "execution_time": execution_time
        }


# ============================================================
# STEP 5: AUTONOMOUS AGENT CONTROLLER
# ============================================================

class AgentController:

    def __init__(self, agent, decision_maker):

        self.agent = agent
        self.decision_maker = decision_maker

    # Execute the calculated route
    def execute_route(self, result):

        if result is None:
            print("noroute available. agent cannot move.")
            return

        actions = result["actions"]

        print("\n")
        print("autonomous agent is awake now")
        print("\n")

        print("starting position:", self.agent.position)
        print("goal state:", self.agent.goal)

        print("\nagent will start moving now...\n")

        # Execute actions one by one
        for step, action in enumerate(actions, start=1):

            if self.agent.status != "ACTIVE":
                break

            print(f"\n---------- STEP {step} ----------")

            # Perceive current environment
            observation = self.agent.perceive()

            print("current position:",
                  observation["current_position"])

            print("available neighbours:",
                  observation["valid_neighbors"])

            print("agent decision:", action)

            # Execute selected action
            success = self.agent.act(action)

            if not success:
                print("movement failed, agent can't move. choose another algo")
                break

            # Display updated maze
            self.agent.environment.display(
                agent_position=self.agent.position
            )

            # Evaluate agent state
            if self.agent.evaluate() == "SUCCESS":
                break

        # Final evaluation
        self.show_final_results(result)

    # Display final performance
    def show_final_results(self, result):

        print("\n")
        print("          FINAL AGENT REPORT")
        print("\n")

        print("algo:", result["algorithm"])
        print("final position:", self.agent.position)
        print("goal state:", self.agent.goal)

        print("agent status:", self.agent.status)

        print("total moves executed:",
              len(self.agent.movement_history))

        print("planned path length:",
              len(result["actions"]))

        print("total nodes explored:",
              result["explored_nodes"])

        print("execution time for the search:",
              round(result["execution_time"], 8),
              "seconds")

        if self.agent.status == "SUCCESS":
            print("\nmaze was solved successfully by the agent")

        else:
            print("\nagent couldn't solve the maze :(")

        print("========================================")


# ============================================================
# STEP 5: MAIN PROGRAM
# ============================================================

environment = MazeEnvironment(maze)

agent = IntelligentAgent(environment)

decision_maker = DecisionMaker()

controller = AgentController(
    agent,
    decision_maker
)

print("\n")
print("       INTELLIGENT MAZE SOLVER")
print("\n")

print("agent starts")
print("the starting position is:", agent.position)
print("coordinates of goal state:", agent.goal)

# User selects the navigation strategy
choice = decision_maker.select_algorithm()

if choice is not None:

    # Agent calculates its route
    result = decision_maker.calculate_route(
        agent,
        choice
    )

    if result is not None:

        print("\ncalculated path:")
        print(result["path"])

        print("\ncalculated actions:")
        print(result["actions"])

        # Controller executes the route
        controller.execute_route(result)

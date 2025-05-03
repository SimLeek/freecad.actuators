import heapq
import math

try:
    from PySide2.QtWidgets import QWidget
    from PySide2.QtGui import QPainter, QPen
    from PySide2.QtCore import Qt, QPointF
    from PySide2.QtWidgets import QApplication, QVBoxLayout
except ImportError:
    from PySide.QtWidgets import QWidget
    from PySide.QtGui import QPainter, QPen
    from PySide.QtCore import Qt, QPointF
    from PySide.QtWidgets import QApplication, QVBoxLayout

import sys

class DiagramWidget(QWidget):
    def __init__(self, connections, line_thickness=2, line_separation_distance=20, allow_crossings=False, parent=None):
        """
        connections: list of tuples: [ ((start_x, start_y), (end_x, end_y)), ... ]
                     Coordinates are in pixels.
        line_thickness: pen width for drawn lines.
        line_separation_distance: used both as the cell size of the routing grid and for offsetting collisions.
        """
        super().__init__(parent)
        self.setup_function(connections, line_thickness, line_separation_distance, allow_crossings)

    def setup_function(self, connections, line_thickness, line_separation_distance, allow_crossings):
        self._connections = connections
        self.line_thickness = line_thickness
        self.line_separation_distance = line_separation_distance
        self.allow_crossings = allow_crossings

        # Determine grid dimensions based on current widget size.
        width = self.width() if self.width() > 0 else 400
        height = self.height() if self.height() > 0 else 400
        self.num_cols = width // line_separation_distance
        self.num_rows = height // line_separation_distance

        # Create a dense obstacles grid: obstacles[x][y] == 1 means occupied.
        self.obstacles = [[0 for _ in range(self.num_rows)] for _ in range(self.num_cols)]

        # Create searchers (one per connection) with grid positions.
        self.searchers = []
        start_positions = {}
        end_positions = {}
        for (start, end) in connections:
            start_grid = (start[0] // line_separation_distance, start[1] // line_separation_distance)
            end_grid = (end[0] // line_separation_distance, end[1] // line_separation_distance)
            if start_grid in start_positions:
                raise ValueError(f"Multiple connections starting at grid cell {start_grid}, latest: {start}")
            if end_grid in end_positions:
                raise ValueError(f"Multiple connections ending at grid cell {end_grid}, latest: {end}")
            start_positions[start_grid] = True
            end_positions[end_grid] = True
            self.searchers.append({
                'start': start_grid,
                'goal': end_grid,
                'start_pixel': start,
                'end_pixel': end,
                'current': start_grid,
                'route': [start_grid],  # store grid cells along the path
                'first_heading': None,  # (dx, dy) tuple when the first move is made
                'last_heading': None
            })
            # Mark the starting & ending cells as occupied.
            self.obstacles[start_grid[0]][start_grid[1]] = 1
            self.obstacles[end_grid[0]][end_grid[1]] = 1


        # Run the concurrent A* search routing.
        self._run_concurrent_astar()

        # Convert grid routes back to pixel coordinates (center each cell).
        self.routes = []
        for searcher in self.searchers:
            pixel_route = []
            pixel_route.append(QPointF(*searcher['start_pixel']))
            for cell in searcher['route']:
                x = cell[0] * self.line_separation_distance + self.line_separation_distance / 2
                y = cell[1] * self.line_separation_distance + self.line_separation_distance / 2
                pixel_route.append(QPointF(x, y))
            pixel_route.append(QPointF(*searcher['end_pixel']))
            self.routes.append(pixel_route)
        self.update()

    def get_details(self):
        """Return the original connection details."""
        return self._connections

    def _segments_intersect(self, p1, p2, q1, q2):
        """
        Check if the line segment p1-p2 intersects with q1-q2.
        p1, p2, q1, q2 are grid cell tuples (x, y).
        """

        def ccw(a, b, c):
            return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

        return (ccw(p1, q1, q2) != ccw(p2, q1, q2)) and (ccw(p1, p2, q1) != ccw(p1, p2, q2))

    def _run_concurrent_astar(self):
        """
        Execute A* routing for all searchers concurrently.
        The grid is defined by self.num_cols x self.num_rows cells.
        We mark cells as obstacles (set to 1) once a searcher leaves them.
        """
        max_iterations = (self.num_cols * self.num_rows) * 2
        iteration = 0

        while any(s['current'] != s['goal'] for s in self.searchers):
            iteration += 1
            if iteration > max_iterations:
                # If any searcher is stuck, report an error.
                for s in self.searchers:
                    if s['current'] != s['goal']:
                        raise RuntimeError(
                            f"Routing from {s['start']} to {s['goal']} failed. Honestly not sure how this is possible."
                        )
            # For each active searcher, compute an A* path from current to goal.
            planned_moves = {}
            paths = {}
            for idx, s in enumerate(self.searchers):
                if s['current'] == s['goal']:
                    continue
                path = self._astar(s['current'], s['goal'])
                if not path or len(path) < 2:
                    raise RuntimeError(
                        f"Routing from {s['start']} to {s['goal']} could not find a path from {s['current']}."
                    )
                paths[idx] = path
                # Plan to move one cell along the computed path.
                planned_moves[idx] = path[1]

            # (a) Resolve collisions: If two searchers plan to move into the same cell,
            # only the one with lower index moves.
            move_positions = {}
            for idx, pos in planned_moves.items():
                if pos is None:
                    continue
                if pos in move_positions:
                    planned_moves[idx] = None  # this searcher does not move this iteration
                else:
                    move_positions[pos] = idx

            # (b) Check for diagonal crossing collisions.
            # If searcher A moves from X to Y and searcher B moves from Y to X, then detect with _segments_intersect.
            if not self.allow_crossings:
                for idx_a, s_a in enumerate(self.searchers):
                    if idx_a not in planned_moves or planned_moves[idx_a] is None:
                        continue
                    for idx_b, s_b in enumerate(self.searchers):
                        if idx_b <= idx_a:
                            continue
                        if idx_b not in planned_moves or planned_moves[idx_b] is None:
                            continue
                        if planned_moves[idx_a] == s_b['current'] and planned_moves[idx_b] == s_a['current']:
                            # Use the _segments_intersect check on grid cells.
                            if self._segments_intersect(s_a['current'], planned_moves[idx_a],
                                                        s_b['current'], planned_moves[idx_b]):
                                planned_moves[idx_b] = None

            # Advance each searcher that has a planned move.
            for idx, s in enumerate(self.searchers):
                if s['current'] == s['goal']:
                    continue
                move = planned_moves.get(idx)
                if move is None:
                    # This searcher stays in place for this iteration.
                    continue

                prev = s['current']
                dx = move[0] - prev[0]
                dy = move[1] - prev[1]
                # Normalize dx and dy to -1, 0, or 1.
                dx = (dx > 0) - (dx < 0)
                dy = (dy > 0) - (dy < 0)
                current_heading = (dx, dy)
                if s['first_heading'] is None:
                    s['first_heading'] = current_heading
                    s['last_heading'] = current_heading
                elif current_heading != s['last_heading']:
                    # Heading changed; record the previous cell as an intermediate waypoint.
                    s['route'].append(prev)
                    s['last_heading'] = current_heading

                # Mark the cell we’re leaving as occupied.
                self.obstacles[prev[0]][prev[1]] = 1
                # Move the searcher.
                s['current'] = move
                s['route'].append(move)
                # Mark the new cell as occupied.
                self.obstacles[move[0]][move[1]] = 1

    def _astar(self, start, goal):
        """
        Perform an A* search on the grid from start to goal.
        start, goal: (x, y) tuples.
        Uses self.obstacles (dense grid) to determine if a cell is blocked.
        Allowed moves include diagonals.
        Returns a list of (x, y) tuples representing the path (including start and goal).
        """
        cols, rows = self.num_cols, self.num_rows

        def in_bounds(pos):
            x, y = pos
            return 0 <= x < cols and 0 <= y < rows

        def neighbors(pos, goal):
            x, y = pos
            results = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    new_pos = (x + dx, y + dy)
                    if in_bounds(new_pos) and (self.obstacles[new_pos[0]][new_pos[1]] == 0 or new_pos==goal):
                        pass
                        if (not self.allow_crossings) and dx!=0 and dy!=0 and self.obstacles[pos[0]][new_pos[1]] == 0 and self.obstacles[new_pos[0]][pos[1]] == 0:
                            results.append(new_pos)
                        elif dx==0 or dy==0:
                            results.append(new_pos)
                        else:
                            pass
            return results

        root = 2
        def heuristic(a, b):
            # Chebyshev distance (since diagonal moves are allowed)
            #return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
            return math.pow(abs(a[0] - b[0])**root+ abs(a[1] - b[1])**root, 1./root)

        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)
            if current == goal:
                break
            for next_pos in neighbors(current, goal):
                new_cost = cost_so_far[current] + 1  # cost per move is 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + heuristic(goal, next_pos)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current

        if goal not in came_from:
            return None  # No path found.

        # Reconstruct the path.
        current = goal
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black, self.line_thickness)
        painter.setPen(pen)
        # Draw each route as a series of connected line segments.
        for route in self.routes:
            if len(route) > 1:
                for i in range(len(route) - 1):
                    painter.drawLine(route[i], route[i + 1])


def main():
    app = QApplication(sys.argv)

    # Example connections:
    # Each connection is ((start_x, start_y), (end_x, end_y))
    example_connections = [
        ((40, 40), (100, 100)),  # Diagonal route
        ((200, 200), (50, 200)),  # Horizontal line
        ((200, 100), (100, 200)),  # Crossing diagonal
    ]

    # Create main window with a layout
    window = QWidget()
    window.setWindowTitle("Diagram Widget Example")
    window.resize(400, 400)
    layout = QVBoxLayout(window)

    # Create our custom DiagramWidget with the example connections.
    diagram = DiagramWidget(example_connections, line_thickness=2, line_separation_distance=10, allow_crossings=False)
    layout.addWidget(diagram)

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
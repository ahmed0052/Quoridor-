class GameState:
    # stores the complete game state pawns, walls, and info
    def __init__(self):
        self.pawns = [
            [0,4],
            [8,4]
        ]

        self.walls_available = [10,10]
        self.current_player = 0

        self.h_walls = [[False] * 9 for _ in range(9)]
        self.v_walls = [[False] * 9 for _ in range(9)]

    def print_board(self):
        for r in range(9):
            row_str = ""
            for c in range(9):
                if self.pawns[0] == [r, c]:
                    row_str += "1 "
                elif self.pawns[1] == [r, c]:
                    row_str += "2 "
                else:
                    row_str += ". "
            print(row_str)


class PawnMovement:
    # Handles pawn movement rules and valid move generation
    def __init__(self,state):
        self.state = state

    def is_in_bounds(self, x, y):
        return 0 <= x < 9 and 0 <= y < 9

    # Returns all legal moves including jumps and diagonal moves
    def get_valid_moves(self, player):
        x, y = self.state.pawns[player]
        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        opponent = 1 - player
        ox, oy = self.state.pawns[opponent]
        valid_moves = []

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            if not self.is_in_bounds(new_x, new_y):
                continue

            if self.is_wall_between(x, y, dx, dy):
                continue

            # Handle jumping over the opponent pawn
            if [new_x, new_y] == [ox, oy]:
                if self.is_wall_between(x, y, dx, dy):
                    continue
                jump_x = new_x + dx
                jump_y = new_y + dy

                if self.is_in_bounds(jump_x, jump_y) and not self.is_wall_between(new_x, new_y, dx, dy):
                    valid_moves.append([jump_x, jump_y])

                else:
                    # Used when direct jump is blocked by a wall
                    diagonal = self.get_diagonals(new_x, new_y, dx, dy)
                    valid_moves.extend(diagonal)

            else:
                valid_moves.append([new_x, new_y])

        return valid_moves

    # Checks if a wall blocks movement in the given direction
    def is_wall_between(self, x, y, dx, dy):
        if dx == -1:
            return x > 0 and self.state.h_walls[x-1][y]

        if dx == 1:
            return x < 8 and self.state.h_walls[x][y]

        if dy == -1:
            return y > 0 and self.state.v_walls[x][y-1]

        if dy == 1:
            return y < 8 and self.state.v_walls[x][y]

        return False

    def get_diagonals(self, x, y, dx, dy):
        diagonals = []
        if dx != 0: #vertical
            perp = [[0, -1], [0, 1]]

        else:       #horizontal
            perp = [[-1, 0], [1, 0]]

        for pdx, pdy in perp:
            diag_x = x + pdx
            diag_y = y + pdy
            if self.is_in_bounds(diag_x, diag_y) and not self.is_wall_between(x, y, pdx, pdy):
                diagonals.append([diag_x, diag_y])

        return diagonals

class GameLogic:
    # Controls pawn movement and win conditions
    def __init__(self, state):
        self.state = state
        self.motion = PawnMovement(state)

    def move_pawn(self, new_x, new_y):
        player = self.state.current_player
        valid_moves = self.motion.get_valid_moves(player)

        if[new_x, new_y] not in valid_moves:
            print("Invalid move")
            return False

        self.state.pawns[player] = [new_x, new_y]

        self.state.current_player = 1-self.state.current_player
        winner = self.check_winner()
        if winner is not None:
            print(f"Player {winner+1} wins")
        return True

    def check_winner(self):
        if self.state.pawns[0][0] == 8:
            return 0

        if self.state.pawns[1][0] == 0:
            return 1

        return None

class BFS:
    # Breadth First Search used to verify path availability
    def __init__(self, state):
        self.state = state

    # Ensures the player can still reach the goal row
    def has_path(self,player):
        start = self.state.pawns[player]
        goal_row = 8 if player == 0 else 0
        visited = []
        queue = [start]
        while queue:
            current = queue.pop(0)
            x,y = current
            if x == goal_row:
                return True
            if current in visited:
                continue
            visited.append(current)

            for neighbor in self.get_neighbors(x,y):
                if neighbor not in visited:
                    queue.append(neighbor)

        return False

    def get_neighbors(self,x,y):
        neighbors = []
        if x > 0 and not self.state.h_walls[x-1][y]:
            neighbors.append([x-1, y])

        if x < 8 and not self.state.h_walls[x][y]:
            neighbors.append([x+1, y])

        if y > 0 and not self.state.v_walls[x][y-1]:
            neighbors.append([x, y-1])

        if y < 8 and not self.state.v_walls[x][y]:
            neighbors.append([x, y+1])

        return neighbors

class WallsPlacer:
    # Handles wall placement and legality checks
    def __init__(self, state):
        self.state = state
        self.bfs = BFS(state)

    def place_wall(self, x, y, direction):
        if direction == "h":
            if not (0 <= x <= 8 and 0 <= y < 8):
                print("Invalid direction")
                return False

        elif direction == "v":
            if not (0 <= x < 8 and 0 <= y <= 8):
                print("Invalid direction")
                return False

        if self.is_overlap(x,y,direction):
            print("Wall overlaps another wall")
            return False

        self.apply_wall(x, y, direction)

        # Prevent illegal walls that completely block a player
        if not self.bfs.has_path(0) or not self.bfs.has_path(1):
            self.remove_wall(x, y, direction)
            print("Illegal move")
            return False
        self.state.walls_available[self.state.current_player] -= 1
        self.state.current_player = 1 - self.state.current_player
        return True

    def apply_wall(self, r, c, direction):
        if direction == "h":
            self.state.h_walls[r][c] = True
            self.state.h_walls[r][c + 1] = True
        elif direction == "v":
            self.state.v_walls[r][c] = True
            self.state.v_walls[r + 1][c] = True

    def remove_wall(self, r, c, direction):
        if direction == "h":
            self.state.h_walls[r][c] = False
            self.state.h_walls[r][c + 1] = False
        elif direction == "v":
            self.state.v_walls[r][c] = False
            self.state.v_walls[r + 1][c] = False

    def is_overlap(self, r, c, direction):
        if direction == "h":
            return self.state.h_walls[r][c] or self.state.h_walls[r][c + 1]
        elif direction == "v":
            return self.state.v_walls[r][c] or self.state.v_walls[r + 1][c]








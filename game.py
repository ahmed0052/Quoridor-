class GameState:
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
    def __init__(self,state):
        self.state = state
    def is_in_bounds(self, x, y):
        return 0 <= x < 9 and 0 <= y < 9
    def is_blocked(self, x, y, player):
        opponent = 1 - player
        return self.state.pawns[opponent] == [x,y]
    def get_valid_moves(self, player):
        x, y = self.state.pawns[player]
        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        valid_moves = []
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            if not self.is_in_bounds(new_x, new_y):
                continue

            if self.is_blocked(new_x, new_y, player):
                continue

            valid_moves.append([new_x, new_y])
        return valid_moves

class GameLogic:
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
        return True
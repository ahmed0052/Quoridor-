from game import GameState, GameLogic, BFS, WallsPlacer

state = GameState()
logic = GameLogic(state)

state.print_board()
print("---")

# move player 1 down
logic.move_pawn(1, 4)
state.print_board()
print("---")

# try an illegal move
logic.move_pawn(0, 0)
state.print_board()
print("---")

# BFS check
bfs = BFS(state)
print(bfs.has_path(0))
print(bfs.has_path(1))
print("---")

# wall placement
wall_placer = WallsPlacer(state)
wall_placer.place_wall(3, 3, "h")
print(state.h_walls[3][3])
print(state.h_walls[3][4])
print(state.h_walls[3][2])
print(state.walls_available)
print("---")

# fresh state for jump test — no walls interfering
state2 = GameState()
logic2 = GameLogic(state2)
state2.pawns[0] = [3, 4]
state2.pawns[1] = [4, 4]

print(logic2.motion.get_valid_moves(1))
print("---")
# should include [5, 4] — jump over opponent

# test diagonal fallback
state3 = GameState()
logic3 = GameLogic(state3)

# place pawns close together
state3.pawns[0] = [3, 4]
state3.pawns[1] = [4, 4]

# place a wall BELOW the opponent — blocks the straight jump
state3.h_walls[4][4] = True

print(logic3.motion.get_valid_moves(0))
# should NOT include [5, 4] — jump is blocked
# should include [4, 3] and [4, 5] — diagonal fallback

# win condition test
state4 = GameState()
logic4 = GameLogic(state4)
print("---")

# manually put player 0 at the last row
state4.pawns[0] = [7, 4]
state4.pawns[1] = [4, 4]
logic4.move_pawn(8, 4)


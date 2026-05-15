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
state.print_board()
print("walls left:", state.walls_available)
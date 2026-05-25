import pygame

WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0  )
BROWN      = (139, 90,  43 )
BEIGE      = (245, 222, 179)
RED        = (220, 50,  50 )
BLUE       = (50,  100, 220)
GREEN      = (50,  200, 100)
GRAY       = (180, 180, 180)
LIGHT_GRAY = (230, 230, 230)
YELLOW     = (255, 215, 0  )


# Computes responsive layout values based on screen size
def compute_layout(screen_w, screen_h):
    panel_width  = int(screen_w * 0.22)
    board_area_w = screen_w - panel_width
    board_area_h = screen_h
    tile_size    = min(board_area_w, board_area_h) // 10
    cell_size    = int(tile_size * 0.85)
    gap_size     = tile_size - cell_size
    board_size   = 9 * tile_size
    margin_x     = (board_area_w - board_size) // 2
    margin_y     = (board_area_h - board_size) // 2
    return {
        'tile_size'  : tile_size,
        'cell_size'  : cell_size,
        'gap_size'   : gap_size,
        'board_size' : board_size,
        'margin_x'   : margin_x,
        'margin_y'   : margin_y,
        'panel_width': panel_width,
        'panel_x'    : board_area_w,
        'screen_w'   : screen_w,
        'screen_h'   : screen_h,
    }


# Responsible for drawing the board, pawns, and walls
class Board:
    def __init__(self, screen, state, layout):
        self.screen = screen
        self.state  = state
        self.layout = layout

    def cell_to_pixel(self, row, col):
        x = self.layout['margin_x'] + col * self.layout['tile_size']
        y = self.layout['margin_y'] + row * self.layout['tile_size']
        return x, y

    def draw(self, winner=None):
        self.draw_cells()
        self.draw_walls()
        self.draw_pawns(winner)

    def draw_cells(self):
        cs = self.layout['cell_size']
        for row in range(9):
            for col in range(9):
                x, y = self.cell_to_pixel(row, col)
                pygame.draw.rect(self.screen, BEIGE, (x, y, cs, cs))
                pygame.draw.rect(self.screen, GRAY,  (x, y, cs, cs), 1)

    def draw_pawns(self, winner=None):
        cs = self.layout['cell_size']
        r, c = self.state.pawns[0]
        x, y = self.cell_to_pixel(r, c)
        center = (x + cs // 2, y + cs // 2)
        pygame.draw.circle(self.screen, RED, center, cs // 2 - 5)
        if winner == 0:
            pygame.draw.circle(self.screen, YELLOW, center, cs // 2 - 2, 4)

        r, c = self.state.pawns[1]
        x, y = self.cell_to_pixel(r, c)
        center = (x + cs // 2, y + cs // 2)
        pygame.draw.circle(self.screen, BLUE, center, cs // 2 - 5)
        if winner == 1:
            pygame.draw.circle(self.screen, YELLOW, center, cs // 2 - 2, 4)

    def draw_walls(self):
        cs = self.layout['cell_size']
        gs = self.layout['gap_size']
        for row in range(9):
            for col in range(9):
                if row < 8 and self.state.h_walls[row][col]:
                    x, y = self.cell_to_pixel(row, col)
                    pygame.draw.rect(self.screen, BROWN, (x, y + cs, cs, gs))
                if col < 8 and self.state.v_walls[row][col]:
                    x, y = self.cell_to_pixel(row, col)
                    pygame.draw.rect(self.screen, BROWN, (x + cs, y, gs, cs))

    # Shows a temporary wall preview before placement
    def draw_wall_preview(self, row, col, direction):
        cs = self.layout['cell_size']
        gs = self.layout['gap_size']
        if direction == 'h':
            if col >= 8 or row >= 9:
                return
            x, y = self.cell_to_pixel(row, col)
            pygame.draw.rect(self.screen, YELLOW, (x, y + cs, cs, gs))
            x2, y2 = self.cell_to_pixel(row, col + 1)
            pygame.draw.rect(self.screen, YELLOW, (x2, y2 + cs, cs, gs))
        elif direction == 'v':
            if row >= 8 or col >= 9:
                return
            x, y = self.cell_to_pixel(row, col)
            pygame.draw.rect(self.screen, YELLOW, (x + cs, y, gs, cs))
            x2, y2 = self.cell_to_pixel(row + 1, col)
            pygame.draw.rect(self.screen, YELLOW, (x2 + cs, y2, gs, cs))


# Side panel UI displaying game info and controls
class UI:
    def __init__(self, screen, state, layout):
        self.screen = screen
        self.state  = state
        self.layout = layout
        self.message       = ""
        self.message_timer = 0
        self._make_fonts()

    def _make_fonts(self):
        sh = self.layout['screen_h']
        self.font_large = pygame.font.SysFont('Arial', max(18, sh // 40))
        self.font_small = pygame.font.SysFont('Arial', max(14, sh // 55))

    def set_message(self, text):
        self.message       = text
        self.message_timer = 120

    def draw(self):
        L  = self.layout
        px = L['panel_x']
        sh = L['screen_h']
        pw = L['panel_width']

        pygame.draw.rect(self.screen, LIGHT_GRAY, (px, 0, pw, sh))

        self.screen.blit(
            self.font_large.render("QUORIDOR", True, BLACK),
            (px + 20, int(sh * 0.04)))

        turn_text  = "Player 1" if self.state.current_player == 0 else "Player 2"
        turn_color = RED if self.state.current_player == 0 else BLUE
        self.screen.blit(
            self.font_small.render("Current Turn:", True, BLACK),
            (px + 20, int(sh * 0.13)))
        self.screen.blit(
            self.font_large.render(turn_text, True, turn_color),
            (px + 20, int(sh * 0.17)))

        self.screen.blit(
            self.font_small.render("Walls Left:", True, BLACK),
            (px + 20, int(sh * 0.27)))
        self.screen.blit(
            self.font_small.render(f"Player 1: {self.state.walls_available[0]}", True, RED),
            (px + 20, int(sh * 0.31)))
        self.screen.blit(
            self.font_small.render(f"Player 2: {self.state.walls_available[1]}", True, BLUE),
            (px + 20, int(sh * 0.35)))

        self.screen.blit(
            self.font_small.render("Mode:", True, BLACK),
            (px + 20, int(sh * 0.43)))

        btn_y = int(sh * 0.54)
        pygame.draw.rect(self.screen, GREEN, (px + 20, btn_y, pw - 40, 40))
        self.screen.blit(
            self.font_small.render("Reset Game", True, WHITE),
            (px + 35, btn_y + 10))

        self.screen.blit(
            self.font_small.render("Controls:", True, BLACK),
            (px + 20, int(sh * 0.63)))
        self.screen.blit(
            self.font_small.render("W - toggle wall/move", True, GRAY),
            (px + 20, int(sh * 0.67)))
        self.screen.blit(
            self.font_small.render("H - horizontal wall", True, GRAY),
            (px + 20, int(sh * 0.71)))
        self.screen.blit(
            self.font_small.render("V - vertical wall", True, GRAY),
            (px + 20, int(sh * 0.75)))

        if self.message_timer > 0:
            self.screen.blit(
                self.font_small.render(self.message, True, RED),
                (px + 20, int(sh * 0.82)))
            self.message_timer -= 1


class DifficultyScreen:
    def __init__(self, screen, layout):
        self.screen   = screen
        self.layout   = layout
        self.selected = None
        sh = layout['screen_h']
        self.font_title  = pygame.font.SysFont('Arial', max(36, sh // 18))
        self.font_button = pygame.font.SysFont('Arial', max(18, sh // 35))

    def draw(self):
        sw = self.layout['screen_w']
        sh = self.layout['screen_h']
        self.screen.fill(WHITE)

        title = self.font_title.render("QUORIDOR", True, BLACK)
        self.screen.blit(title, (sw // 2 - title.get_width() // 2, int(sh * 0.10)))

        subtitle = self.font_button.render("Select Game Mode", True, GRAY)
        self.screen.blit(subtitle, (sw // 2 - subtitle.get_width() // 2, int(sh * 0.20)))

        buttons = [
            ('human',  "Human vs Human", GREEN),
            ('easy',   "AI - Easy",      BLUE),
            ('medium', "AI - Medium",    BROWN),
            ('hard',   "AI - Hard",      RED),
        ]
        for i, (mode, label, color) in enumerate(buttons):
            bx = sw // 2 - 150
            by = int(sh * 0.30) + i * int(sh * 0.13)
            pygame.draw.rect(self.screen, color, (bx, by, 300, 55))
            text = self.font_button.render(label, True, WHITE)
            self.screen.blit(text, (bx + 150 - text.get_width() // 2, by + 15))

        pygame.display.flip()

    def handle_click(self, px, py):
        sw = self.layout['screen_w']
        sh = self.layout['screen_h']
        modes = ['human', 'easy', 'medium', 'hard']
        for i, mode in enumerate(modes):
            bx = sw // 2 - 150
            by = int(sh * 0.30) + i * int(sh * 0.13)
            if bx <= px <= bx + 300 and by <= py <= by + 55:
                self.selected = mode


class WinScreen:
    def __init__(self, screen, winner, layout):
        self.screen = screen
        self.winner = winner
        self.layout = layout
        sh = layout['screen_h']
        self.font_title  = pygame.font.SysFont('Arial', max(48, sh // 14))
        self.font_button = pygame.font.SysFont('Arial', max(20, sh // 30))

    def draw(self):
        sw = self.layout['screen_w']
        sh = self.layout['screen_h']
        self.screen.fill(WHITE)

        color = RED if self.winner == 0 else BLUE
        title = self.font_title.render(f"Player {self.winner + 1} Wins!", True, color)
        self.screen.blit(title, (sw // 2 - title.get_width() // 2, int(sh * 0.25)))

        again_y = int(sh * 0.48)
        pygame.draw.rect(self.screen, GREEN, (sw // 2 - 150, again_y, 300, 55))
        again = self.font_button.render("Play Again", True, WHITE)
        self.screen.blit(again, (sw // 2 - again.get_width() // 2, again_y + 15))

        quit_y = int(sh * 0.62)
        pygame.draw.rect(self.screen, RED, (sw // 2 - 150, quit_y, 300, 55))
        quit_text = self.font_button.render("Quit", True, WHITE)
        self.screen.blit(quit_text, (sw // 2 - quit_text.get_width() // 2, quit_y + 15))

        pygame.display.flip()

    def handle_click(self, px, py):
        sw = self.layout['screen_w']
        sh = self.layout['screen_h']
        again_y = int(sh * 0.48)
        quit_y  = int(sh * 0.62)
        if sw // 2 - 150 <= px <= sw // 2 + 150 and again_y <= py <= again_y + 55:
            return 'again'
        if sw // 2 - 150 <= px <= sw // 2 + 150 and quit_y <= py <= quit_y + 55:
            return 'quit'
        return None


class Game:
    def __init__(self, screen, state, logic, wall_placer, layout, ai=None):
        self.screen      = screen
        self.state       = state
        self.logic       = logic
        self.wall_placer = wall_placer
        self.layout      = layout
        self.board       = Board(screen, state, layout)
        self.ui          = UI(screen, state, layout)
        self.mode        = 'move'
        self.wall_dir    = 'h'
        self.selected    = None
        self.game_over   = False
        self.winner      = None
        self.ai          = ai
        self.ai_thinking = False

    def pixel_to_cell(self, px, py):
        L   = self.layout
        col = (px - L['margin_x']) // L['tile_size']
        row = (py - L['margin_y']) // L['tile_size']
        return row, col

    def is_on_board(self, px, py):
        L = self.layout
        return (L['margin_x'] <= px <= L['margin_x'] + L['board_size'] and
                L['margin_y'] <= py <= L['margin_y'] + L['board_size'])

    def is_reset_button(self, px, py):
        L     = self.layout
        px0   = L['panel_x'] + 20
        btn_y = int(L['screen_h'] * 0.54)
        return px0 <= px <= px0 + L['panel_width'] - 40 and btn_y <= py <= btn_y + 40

    def handle_click(self, px, py):
        if self.game_over:
            return
        if self.ai_thinking:
            return
        if self.is_reset_button(px, py):
            self.reset()
            return
        if self.is_on_board(px, py):
            row, col = self.pixel_to_cell(px, py)
            if self.mode == 'move':
                self.handle_move(row, col)
            elif self.mode == 'wall':
                self.handle_wall(row, col)

    def handle_move(self, row, col):
        success = self.logic.move_pawn(row, col)
        if not success:
            self.ui.set_message("Invalid move!")
        else:
            winner = self.logic.check_winner()
            if winner is not None:
                self.game_over = True
                self.winner    = winner
                self.ui.set_message(f"Player {winner + 1} wins!")

    def handle_wall(self, row, col):
        if self.state.walls_available[self.state.current_player] == 0:
            self.ui.set_message("No walls left!")
            return
        success = self.wall_placer.place_wall(row, col, self.wall_dir)
        if not success:
            self.ui.set_message("Invalid wall!")

    def handle_key(self, key):
        if key == pygame.K_w:
            self.mode = 'wall' if self.mode == 'move' else 'move'
            self.ui.set_message(f"Mode: {self.mode}")
        elif key == pygame.K_h:
            self.wall_dir = 'h'
            self.ui.set_message("Wall: Horizontal")
        elif key == pygame.K_v:
            self.wall_dir = 'v'
            self.ui.set_message("Wall: Vertical")

    def reset(self):
        self.game_over = True
        self.winner    = None

    def draw(self):
        self.screen.fill(WHITE)
        self.board.draw(self.winner)
        self.ui.draw()

        L     = self.layout
        px    = L['panel_x']
        sh    = L['screen_h']
        mode_text = self.ui.font_small.render(
            f"Mode: {self.mode} ({self.wall_dir})", True, BLACK)
        self.screen.blit(mode_text, (px + 20, int(sh * 0.47)))

        if self.mode == 'move' and not self.game_over:
            player = self.state.current_player
            from game import PawnMovement
            movement    = PawnMovement(self.state)
            valid_moves = movement.get_valid_moves(player)
            cs = L['cell_size']
            for move in valid_moves:
                r, c = move
                x, y = self.board.cell_to_pixel(r, c)
                pygame.draw.rect(self.screen, GREEN, (x, y, cs, cs), 3)

        if self.mode == 'wall' and not self.game_over:
            mx, my = pygame.mouse.get_pos()
            if self.is_on_board(mx, my):
                row, col = self.pixel_to_cell(mx, my)
                self.board.draw_wall_preview(row, col, self.wall_dir)

        pygame.display.flip()

    def update(self):
        if self.game_over:
            return
        if self.ai is not None and self.state.current_player == self.ai.AiPlayer:
            self.ai_thinking = True
            self.ui.set_message("AI is thinking...")
            self.draw()

            best = self.ai.get_best_move()
            if best is not None:
                if best[0] == 'move':
                    self.logic.move_pawn(best[1][0], best[1][1])
                elif best[0] == 'wall':
                    self.wall_placer.place_wall(best[1], best[2], best[3])

            self.ai_thinking = False

            winner = self.logic.check_winner()
            if winner is not None:
                self.game_over = True
                self.winner    = winner
                self.ui.set_message(f"Player {winner + 1} wins!")
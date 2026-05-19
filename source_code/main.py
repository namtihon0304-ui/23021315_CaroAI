import pygame
import time
import sys

from config import *
from ai import EngineCaroAI

class GameCaroCoDien:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("CARO GAME")
        
        # Hệ font chuẩn không lỗi chữ trên mọi hệ điều hành
        self.font_name = "Arial"
        self.font_title = pygame.font.SysFont(self.font_name, 56, bold=True)
        self.font_large = pygame.font.SysFont(self.font_name, 36, bold=True)
        self.font_medium = pygame.font.SysFont(self.font_name, 20, bold=True)
        self.font_small = pygame.font.SysFont(self.font_name, 15, bold=False)
        self.font_bold_small = pygame.font.SysFont(self.font_name, 15, bold=True)
        
        # Quản lý trạng thái và dữ liệu game
        self.state = "LOADING"
        self.start_time = time.time()
        self.reset_game()
        
        self.ai_core = EngineCaroAI()
        self.telemetry = {}

    def reset_game(self):
        """Khởi tạo lại trạng thái bàn cờ mới"""
        self.board = [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.turn = "USER"  # USER hoặc AI
        self.game_over = False
        self.winner = None
        self.history = []
        self.redo_stack = []

    def draw_text(self, text, font, color, x, y, center=True):
        """Hàm trợ giúp vẽ chữ lên màn hình"""
        surface = font.render(str(text), True, color)
        rect = surface.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surface, rect)

    def draw_button(self, text, x, y, w, h, mouse_pos):
        """Hàm trợ giúp vẽ nút bấm có hiệu ứng hover"""
        rect = pygame.Rect(x, y, w, h)
        if rect.collidepoint(mouse_pos):
            # Tạo hiệu ứng màu tối hơn một chút khi di chuột vào
            color = (max(0, COLOR_PANEL[0]-20), max(0, COLOR_PANEL[1]-20), max(0, COLOR_PANEL[2]-20))
        else:
            color = COLOR_PANEL
            
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        pygame.draw.rect(self.screen, COLOR_GRID, rect, 2, border_radius=5)
        self.draw_text(text, self.font_medium, COLOR_TEXT_DARK, x + w//2, y + h//2)
        return rect

    def screen_loading(self):
        """Màn hình tải game ban đầu"""
        self.screen.fill(COLOR_BG)
        self.draw_text(TXT["LOADING"], self.font_large, COLOR_TEXT_DARK, WIDTH//2, HEIGHT//2)
        if time.time() - self.start_time > 1.5:
            self.state = "MENU"

    def screen_menu(self, mouse_pos):
        self.screen.fill(COLOR_BG)
        self.draw_text("CARO", self.font_title, COLOR_TEXT_DARK, WIDTH//2, HEIGHT//3)
        
        # Căn chỉnh lại vị trí 2 nút bấm cho cân đối ở trung tâm màn hình
        b_start = self.draw_button(TXT["PLAY"], WIDTH//2 - 150, HEIGHT//2 - 25, 300, 50, mouse_pos)
        b_quit  = self.draw_button(TXT["QUIT_GAME"], WIDTH//2 - 150, HEIGHT//2 + 55, 300, 50, mouse_pos)
        return b_start, b_quit

    def screen_difficulty(self, mouse_pos):
        """Màn hình chọn độ khó"""
        self.screen.fill(COLOR_BG)
        self.draw_text(TXT["SELECT_DIFFICULTY"], self.font_large, COLOR_TEXT_DARK, WIDTH//2, HEIGHT//6)
        
        b_easy   = self.draw_button(TXT["EASY"], WIDTH//2 - 150, HEIGHT//2 - 90, 300, 45, mouse_pos)
        b_normal = self.draw_button(TXT["NORMAL"], WIDTH//2 - 150, HEIGHT//2 - 30, 300, 45, mouse_pos)
        b_hard   = self.draw_button(TXT["HARD"], WIDTH//2 - 150, HEIGHT//2 + 30, 300, 45, mouse_pos)
        b_back   = self.draw_button(TXT["BACK"], WIDTH//2 - 150, HEIGHT//2 + 110, 300, 45, mouse_pos)
        return b_easy, b_normal, b_hard, b_back

    def screen_playing(self, mouse_pos):
        """Màn hình trận đấu chính thức kèm Telemetry bên phải"""
        self.screen.fill(COLOR_BG)
        
        # 1. Vẽ bàn cờ Caro ở phía bên trái
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, COLOR_BG, rect)
                pygame.draw.rect(self.screen, COLOR_GRID, rect, 1)
                
                # Vẽ quân cờ X hoặc O công thức căn giữa ô
                piece = self.board[r][c]
                if piece == 'X':
                    self.draw_text("X", self.font_large, COLOR_PLAYER_X, rect.centerx, rect.centery)
                elif piece == 'O':
                    self.draw_text("O", self.font_large, COLOR_AI_O, rect.centerx, rect.centery)

        # 2. Tính toán vị trí Sidebar (Bảng thông số) thích ứng theo BOARD_WIDTH
        sb_x = BOARD_WIDTH + 10
        sb_w = WIDTH - sb_x - 10
        
        # Vẽ nền panel bên phải
        pygame.draw.rect(self.screen, COLOR_PANEL, (BOARD_WIDTH, 0, WIDTH - BOARD_WIDTH, HEIGHT))
        pygame.draw.line(self.screen, COLOR_GRID, (BOARD_WIDTH, 0), (BOARD_WIDTH, HEIGHT), 3)

        # Khối tiêu đề AI Core System
        pygame.draw.rect(self.screen, COLOR_GRID, (sb_x, 15, sb_w, 35), border_radius=3)
        self.draw_text(TXT["AI_TITLE"], self.font_bold_small, WHITE, sb_x + sb_w//2, 32)

        # Hiển thị dữ liệu phân tích Telemetry từ AI Engine
        metrics = [
            ("Last Move:", self.telemetry.get("move", "None")),
            ("Eval Score:", self.telemetry.get("eval_score", "0")),
            ("Search Depth:", self.telemetry.get("search_depth", "0 plies")),
            ("States Explored:", self.telemetry.get("states_explored", "0")),
            ("Compute Time:", self.telemetry.get("execution_time", "0.00s")),
            ("Speed (NPS):", self.telemetry.get("nps", "0")),
            ("Algorithm:", self.telemetry.get("algo", "None"))
        ]
        
        y_offset = 65
        for label, val in metrics:
            self.draw_text(label, self.font_bold_small, COLOR_TEXT_DARK, sb_x + 15, y_offset, center=False)
            self.draw_text(val, self.font_small, COLOR_TEXT_DARK, sb_x + 140, y_offset, center=False)
            y_offset += 24

        # Khối trạng thái trận đấu (Match Status)
        pygame.draw.rect(self.screen, COLOR_GRID, (sb_x, 245, sb_w, 35), border_radius=3)
        self.draw_text(TXT["STATUS"], self.font_bold_small, WHITE, sb_x + sb_w//2, 262)

        # Hiển thị thông báo trạng thái hoặc người thắng cuộc
        if self.game_over:
            self.draw_text(TXT["GAME_OVER"], self.font_medium, COLOR_AI_O, sb_x + sb_w//2, 305)
            self.draw_text(TXT[self.winner], self.font_bold_small, COLOR_TEXT_DARK, sb_x + sb_w//2, 335)
            self.draw_text(TXT["RESTART_MSG"], self.font_small, GRAY, sb_x + sb_w//2, 355)
        else:
            turn_msg = TXT["USER_TURN"] if self.turn == "USER" else TXT["AI_TURN"]
            self.draw_text(turn_msg, self.font_bold_small, COLOR_PLAYER_X if self.turn == "USER" else COLOR_AI_O, sb_x + sb_w//2, 315)

        curr_mode = TXT[self.difficulty]
        self.draw_text(f"Level: {curr_mode}", self.font_small, COLOR_TEXT_DARK, sb_x + 20, 390, center=False)

        # Khối các nút chức năng điều khiển trò chơi (Cố định ở phần dưới thanh Sidebar)
        btn_undo = self.draw_button("UNDO", sb_x + 15, HEIGHT - 165, sb_w//2 - 20, 38, mouse_pos)
        btn_redo = self.draw_button("REDO", sb_x + sb_w//2 + 5, HEIGHT - 165, sb_w//2 - 20, 38, mouse_pos)
        btn_surr = self.draw_button(TXT["SURRENDER"], sb_x + 15, HEIGHT - 115, sb_w - 30, 38, mouse_pos)
        btn_back = self.draw_button(TXT["QUIT_MATCH"], sb_x + 15, HEIGHT - 65, sb_w - 30, 38, mouse_pos)
        
        return btn_undo, btn_redo, btn_surr, btn_back

    def run(self):
        """Vòng lặp chạy game chính (Main Loop)"""
        clock = pygame.time.Clock()
        
        while True:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()

            # Xử lý lượt đi tự động của AI khi ở trạng thái PLAYING
            if self.state == "PLAYING" and self.turn == "AI" and not self.game_over:
                self.screen_playing(mouse_pos)
                pygame.display.flip()
                
                # Gọi bộ não AI tính toán bước đi tốt nhất
                chosen, telemetry_data = self.ai_core.tim_nuoc_di_tot_nhat(self.board, self.difficulty)
                if chosen:
                    r, c = chosen
                    self.board[r][c] = 'O'
                    self.telemetry = telemetry_data
                    
                    term = self.ai_core.kiem_tra_ket_thuc(self.board)
                    if term == 'O':
                        self.game_over = True
                        self.winner = "AI_WIN"
                    elif term == "DRAW":
                        self.game_over = True
                        self.winner = "DRAW"
                    else:
                        self.turn = "USER"

            # Vòng lặp bắt sự kiện hệ thống từ người dùng
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # 1. Xử lý click chuột ở màn hình MENU
                    if self.state == "MENU":
                        b_start, b_quit = self.screen_menu(mouse_pos)
                        if b_start.collidepoint(mouse_pos):
                            self.state = "DIFFICULTY"
                        elif b_quit.collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit()

                    # 2. Xử lý click chuột ở màn hình CHỌN ĐỘ KHÓ
                    elif self.state == "DIFFICULTY":
                        b_easy, b_normal, b_hard, b_back = self.screen_difficulty(mouse_pos)
                        if b_easy.collidepoint(mouse_pos):
                            self.difficulty = "EASY"; self.reset_game(); self.state = "PLAYING"
                        elif b_normal.collidepoint(mouse_pos):
                            self.difficulty = "NORMAL"; self.reset_game(); self.state = "PLAYING"
                        elif b_hard.collidepoint(mouse_pos):
                            self.difficulty = "HARD"; self.reset_game(); self.state = "PLAYING"
                        elif b_back.collidepoint(mouse_pos):
                            self.state = "MENU"

                    # 3. Xử lý click chuột khi đang TRONG TRẬN ĐẤU (PLAYING)
                    elif self.state == "PLAYING":
                        b_undo, b_redo, b_surr, b_back = self.screen_playing(mouse_pos)
                        
                        # Click nút quay lại màn hình chọn độ khó
                        if b_back.collidepoint(mouse_pos):
                            self.state = "DIFFICULTY"
                            continue
                        
                        # Click nút xin đầu hàng (Surrender)
                        if b_surr.collidepoint(mouse_pos) and not self.game_over:
                            self.game_over = True
                            self.winner = "AI_WIN"
                            continue

                        # Click nút Hoàn tác (UNDO)
                        if b_undo.collidepoint(mouse_pos):
                            if self.history:
                                # Lưu trạng thái hiện tại vào stack REDO trước khi quay lại
                                self.redo_stack.append(([row[:] for row in self.board], self.telemetry.copy()))
                                prev_board, prev_telemetry = self.history.pop()
                                self.board = prev_board
                                self.telemetry = prev_telemetry
                                self.game_over = False
                                self.winner = None
                                self.turn = "USER"
                            continue

                        # Click nút Đi lại (REDO)
                        if b_redo.collidepoint(mouse_pos):
                            if self.redo_stack:
                                self.history.append(([row[:] for row in self.board], self.telemetry.copy()))
                                next_board, next_telemetry = self.redo_stack.pop()
                                self.board = next_board
                                self.telemetry = next_telemetry
                                
                                # Kiểm tra xem nước cờ redo có kết thúc trận đấu không
                                term = self.ai_core.kiem_tra_ket_thuc(self.board)
                                if term:
                                    self.game_over = True
                                    self.winner = "PLAYER_WIN" if term == 'X' else "AI_WIN" if term == 'O' else "DRAW"
                                else:
                                    self.turn = "USER"
                            continue

                        # Nếu trận đấu kết thúc, click bất kỳ vào vùng BÀN CỜ để khởi động lại nhanh trận đấu
                        if self.game_over and mouse_pos[0] < BOARD_WIDTH:
                            self.reset_game()
                            continue

                        # Người chơi bấm chọn ô cờ để đi quân 'X'
                        if self.turn == "USER" and not self.game_over and mouse_pos[0] < BOARD_WIDTH:
                            c = mouse_pos[0] // CELL_SIZE
                            r = mouse_pos[1] // CELL_SIZE
                            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == '.':
                                # Ghi lại lịch sử phục vụ tính năng UNDO
                                self.history.append(([row[:] for row in self.board], self.telemetry.copy()))
                                self.redo_stack.clear() # Đi nước mới thì xóa sạch Redo Stack
                                
                                self.board[r][c] = 'X'
                                
                                term = self.ai_core.kiem_tra_ket_thuc(self.board)
                                if term == 'X':
                                    self.game_over = True
                                    self.winner = "PLAYER_WIN"
                                elif term == "DRAW":
                                    self.game_over = True
                                    self.winner = "DRAW"
                                else:
                                    self.turn = "AI"

            # Thực hiện vẽ giao diện theo trạng thái màn hình hiện hành
            if self.state == "LOADING": self.screen_loading()
            elif self.state == "MENU": self.screen_menu(mouse_pos)
            elif self.state == "DIFFICULTY": self.screen_difficulty(mouse_pos)
            elif self.state == "PLAYING": self.screen_playing(mouse_pos)

            pygame.display.flip()

if __name__ == "__main__":
    game = GameCaroCoDien()
    game.run()
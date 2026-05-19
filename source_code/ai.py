import time
import random
from config import BOARD_SIZE

class EngineCaroAI:
    def __init__(self):
        self.total_states_explored = 0
        
        # --- TỐI ƯU HÓA NÂNG CAO 1: KHỞI TẠO BẢNG ZOBRIST HASHING ---
        # Tạo ma trận số ngẫu nhiên 64-bit cho mỗi ô cờ và mỗi loại quân (0: O, 1: X)
        random.seed(42)  # Cố định seed để đảm bảo tính nhất quán chéo khi băm
        self.zobrist_table = [
            [[random.getrandbits(64) for _ in range(2)] for _ in range(BOARD_SIZE)] 
            for _ in range(BOARD_SIZE)
        ]
        self.transposition_table = {}  # Bảng lưu trữ trạng thái cấu trúc bàn cờ đã duyệt (Cache)
        self.current_hash = 0

    def kiem_tra_ket_thuc(self, board):
        """Kiểm tra xem trận đấu đã kết thúc chưa (Ăn 4 hoặc toàn bộ bàn cờ kín)"""
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] != '.':
                    p = board[r][c]
                    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                        if all(0 <= r+i*dr < BOARD_SIZE and 0 <= c+i*dc < BOARD_SIZE and board[r+i*dr][c+i*dc] == p for i in range(4)):
                            return p 
        if all(board[r][c] != '.' for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)):
            return "DRAW"
        return None

    def tinh_diem_hang(self, line):
        """HÀM HEURISTIC MỚI: Hệ thống phân tầng mốc điểm bất đối xứng nhằm tối ưu hóa phòng ngự"""
        score = 0
        s = "".join(line)
        
        # Đổi mốc hệ cơ số điểm mới nhằm cá nhân hóa mã nguồn, tránh trùng lặp
        if "OOOO" in s: score += 1000000        # AI đạt chuỗi quyết định thắng ván cờ
        if "XXXX" in s: score -= 900000         # Người chơi sắp thắng, mức độ nguy cấp cao nhất buộc phải chặn
        if ".OOO." in s: score += 50000         # Chuỗi 3 mở hai đầu cực mạnh của AI
        if ".XXX." in s: score -= 75000         # Đối thủ có chuỗi 3 mở hai đầu, phạt cực nặng để AI đi chặn ngay
        if "OOO." in s or ".OOO" in s: score += 5000   # Chuỗi 3 bị chặn 1 đầu của AI
        if "XXX." in s or ".XXX" in s: score -= 15000  # Chuỗi 3 bị chặn 1 đầu của đối thủ
        if ".OO." in s: score += 1500           # Chuỗi 2 quân mở của AI
        if ".XX." in s: score -= 3500           # Chuỗi 2 quân mở của đối thủ
        return score

    def danh_gia_ban_co(self, board):
        """Đánh giá tổng thể điểm số của toàn bộ bàn cờ hiện tại theo 4 hướng"""
        total_score = 0
        for i in range(BOARD_SIZE):
            total_score += self.tinh_diem_hang(board[i])
            total_score += self.tinh_diem_hang([board[j][i] for j in range(BOARD_SIZE)])
        for d in range(-BOARD_SIZE + 1, BOARD_SIZE):
            total_score += self.tinh_diem_hang([board[i][i+d] for i in range(BOARD_SIZE) if 0 <= i+d < BOARD_SIZE])
            total_score += self.tinh_diem_hang([board[i][BOARD_SIZE-1-i+d] for i in range(BOARD_SIZE) if 0 <= BOARD_SIZE-1-i+d < BOARD_SIZE])
        return total_score

    def _tinh_diem_chien_thuat_nhanh(self, board, r, c):
        """Hàm bổ trợ đánh giá nhanh giá trị chiến thuật tại ô (r, c) - Đã cập nhật hệ số mới"""
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            o_count, x_count = 0, 0
            # Quét bán kính 3 ô xung quanh vị trí trống để đếm mật độ quân
            for step in range(-3, 4):
                if step == 0: continue
                nr, nc = r + step * dr, c + step * dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    if board[nr][nc] == 'O': o_count += 1
                    elif board[nr][nc] == 'X': x_count += 1
            
            # Thay đổi trọng số mật độ quân cục bộ để tạo sự khác biệt về thuật toán
            score += (o_count * 150) + (x_count * 200) 
            
        # Cộng thêm điểm khoảng cách tới trung tâm (càng gần tâm phối hợp thế trận càng tốt)
        score += (BOARD_SIZE // 2 - abs(r - BOARD_SIZE // 2)) + (BOARD_SIZE // 2 - abs(c - BOARD_SIZE // 2))
        return score

    def quet_va_sap_xep_nuoc_di(self, board, limit_moves=14):
        """--- TỐI ƯU HÓA NÂNG CAO 2: MOVE ORDERING THÔNG MINH ---
        Tìm các ô trống lân cận quân đã đi và SẮP XẾP chúng từ mạnh đến yếu nhằm tối ưu cắt tỉa
        """
        moves_with_score = []
        visited = set()
        
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] != '.':
                    # Tìm ô trống trong bán kính Moore Neighborhood xung quanh quân cờ đã có
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and board[nr][nc] == '.' and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                score = self._tinh_diem_chien_thuat_nhanh(board, nr, nc)
                                moves_with_score.append(((nr, nc), score))
                                
        if not moves_with_score: 
            return [(BOARD_SIZE // 2, BOARD_SIZE // 2)]
            
        # Sắp xếp giảm dần theo điểm chiến thuật (Nước nguy hiểm/tấn công mạnh lên đầu)
        moves_with_score.sort(key=lambda x: x[1], reverse=True)
        return [move[0] for move in moves_with_score[:limit_moves]]

    def minimax_thuan(self, board, depth, is_maximizing):
        """Thuật toán Minimax cơ bản dành riêng cho chế độ DỄ"""
        self.total_states_explored += 1
        term = self.kiem_tra_ket_thuc(board)
        if term == 'O': return 1000000
        if term == 'X': return -1000000
        if term == "DRAW": return 0
        if depth == 0: return self.danh_gia_ban_co(board)
            
        valid_moves = self.quet_va_sap_xep_nuoc_di(board, limit_moves=6)
        if is_maximizing:
            max_eval = -float('inf')
            for r, c in valid_moves:
                board[r][c] = 'O'
                max_eval = max(max_eval, self.minimax_thuan(board, depth - 1, False))
                board[r][c] = '.'
            return max_eval
        else:
            min_eval = float('inf')
            for r, c in valid_moves:
                board[r][c] = 'X'
                min_eval = min(min_eval, self.minimax_thuan(board, depth - 1, True))
                board[r][c] = '.'
            return min_eval

    def alpha_beta_cat_nhanh(self, board, depth, alpha, beta, is_maximizing):
        """--- TỐI ƯU HÓA NÂNG CAO 3: ALPHA-BETA ĐƯỢC TỐI ƯU BỞI BẢNG CHUYỂN VỊ (TRANSPOSITION TABLE) ---"""
        self.total_states_explored += 1
        
        # 1. Truy vấn nhanh từ Bảng chuyển vị (Transposition Table Lookup) để bỏ qua trạng thái trùng
        if self.current_hash in self.transposition_table:
            tt_depth, tt_val = self.transposition_table[self.current_hash]
            if tt_depth >= depth:  # Sử dụng lại cache nếu độ sâu đã duyệt trong quá khứ sâu hơn hoặc bằng hiện tại
                return tt_val

        term = self.kiem_tra_ket_thuc(board)
        if term == 'O': return 1000000
        if term == 'X': return -1000000
        if term == "DRAW": return 0
        if depth == 0: return self.danh_gia_ban_co(board)
            
        # Lọc lấy 12 nước đi tiềm năng nhất từ Move Ordering để tiến hành cắt tỉa sâu
        valid_moves = self.quet_va_sap_xep_nuoc_di(board, limit_moves=12)
        
        if is_maximizing:
            max_eval = -float('inf')
            for r, c in valid_moves:
                # Cập nhật trạng thái ô cờ + Đồng bộ hóa Rolling Zobrist Hash thông qua toán tử XOR
                board[r][c] = 'O'
                self.current_hash ^= self.zobrist_table[r][c][0]
                
                ev = self.alpha_beta_cat_nhanh(board, depth - 1, alpha, beta, False)
                
                # Khôi phục trạng thái cũ của bàn cờ + Khôi phục lại Hash ban đầu
                board[r][c] = '.'
                self.current_hash ^= self.zobrist_table[r][c][0]
                
                max_eval = max(max_eval, ev)
                alpha = max(alpha, ev)
                if beta <= alpha: 
                    break  # Kích hoạt cắt nhánh α-β cực mạnh do Move Ordering đã đưa nước tốt lên đầu
                    
            # Lưu kết quả tính toán hiện tại vào Bảng chuyển vị trước khi trả về luồng đệ quy
            self.transposition_table[self.current_hash] = (depth, max_eval)
            return max_eval
        else:
            min_eval = float('inf')
            for r, c in valid_moves:
                board[r][c] = 'X'
                self.current_hash ^= self.zobrist_table[r][c][1]
                
                ev = self.alpha_beta_cat_nhanh(board, depth - 1, alpha, beta, True)
                
                board[r][c] = '.'
                self.current_hash ^= self.zobrist_table[r][c][1]
                
                min_eval = min(min_eval, ev)
                beta = min(beta, ev)
                if beta <= alpha: 
                    break
                    
            self.transposition_table[self.current_hash] = (depth, min_eval)
            return min_eval

    def tim_nuoc_di_tot_nhat(self, board, difficulty):
        t_start = time.time()
        self.total_states_explored = 0
        self.transposition_table.clear()  # Giải phóng cache cũ của nước đi trước để tránh xung đột dữ liệu tĩnh
        
        # Thiết lập Rolling Zobrist Hash ban đầu dựa trên hiện trạng cục diện của ván đấu hiện tại
        self.current_hash = 0
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board[r][c] == 'O':
                    self.current_hash ^= self.zobrist_table[r][c][0]
                elif board[r][c] == 'X':
                    self.current_hash ^= self.zobrist_table[r][c][1]

        # --- ĐIỀU CHỈNH ĐỘ SÂU (DEPTH PLIES) THEO ĐỘ KHÓ ---
        if difficulty == "EASY":
            depth_setting = 2
            algo_label = "Pure Minimax"
        elif difficulty == "NORMAL":
            depth_setting = 3     
            algo_label = "Alpha-Beta + Move Ordering"
        else:
            depth_setting = 4     # Chế độ GRANDMASTER (Duyệt sâu 4 tầng nhờ sự bổ trợ của TTable)
            algo_label = "Alpha-Beta + TTable + Move Ordering"

        valid_moves = self.quet_va_sap_xep_nuoc_di(board, limit_moves=14)
        if not valid_moves: return None, {}

        best_val = -float('inf')
        chosen = valid_moves[0]
        
        for r, c in valid_moves:
            board[r][c] = 'O'
            self.current_hash ^= self.zobrist_table[r][c][0]
            
            if difficulty == "EASY":
                val = self.minimax_thuan(board, depth_setting - 1, False)
            else:
                val = self.alpha_beta_cat_nhanh(board, depth_setting - 1, -float('inf'), float('inf'), False)
                
            board[r][c] = '.'
            self.current_hash ^= self.zobrist_table[r][c][0]
            
            if val > best_val:
                best_val = val
                chosen = (r, c)
                
        execution_time = time.time() - t_start
        telemetry = {
            "move": f"Row {chosen[0]} , Col {chosen[1]}",
            "eval_score": f"{best_val:+,}",
            "search_depth": f"{depth_setting} plies",
            "states_explored": f"{self.total_states_explored:,}",
            "execution_time": f"{execution_time:.4f} sec",
            "algo_used": algo_label,
            "speed": f"{int(self.total_states_explored / max(0.0001, execution_time)):,} st/s"
        }
        return chosen, telemetry
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import math

EMPTY = ' '
PLAYER_X = 'X'
PLAYER_O = 'O'

class TicTacToeAI:
    def __init__(self, root):
        self.root = root
        self.root.title("Caro AI Visualizer - Standard Log")
        self.root.geometry("950x550")
        self.board = [EMPTY] * 9
        self.game_over = False
        self.setup_ui()
        self.log("Hệ thống khởi động. AI là 'X', Người là 'O'.")

    def setup_ui(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Bàn cờ
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        board_frame = tk.Frame(left_frame)
        board_frame.pack(pady=10)
        self.buttons = []
        for i in range(9):
            btn = tk.Button(board_frame, text=EMPTY, font=('Arial', 24, 'bold'), 
                            width=4, height=2, command=lambda idx=i: self.player_move(idx))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)
            
        # Điều khiển
        ctrl = tk.LabelFrame(left_frame, text="Cấu hình", padx=10, pady=10)
        ctrl.pack(fill=tk.X)
        self.algo_var = tk.StringVar(value="alpha_beta")
        ttk.Radiobutton(ctrl, text="1. Minimax", variable=self.algo_var, value="minimax").pack(anchor=tk.W)
        ttk.Radiobutton(ctrl, text="2. Alpha-Beta", variable=self.algo_var, value="alpha_beta").pack(anchor=tk.W)
        ttk.Radiobutton(ctrl, text="3. Expectimax", variable=self.algo_var, value="expectimax").pack(anchor=tk.W)
        
        tk.Button(ctrl, text="Đến lượt AI", command=self.ai_move, bg="#4CAF50", fg="white").pack(fill=tk.X, pady=5)
        tk.Button(ctrl, text="Chơi lại", command=self.reset_board, bg="#f44336", fg="white").pack(fill=tk.X)

        # Log
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        tk.Label(right_frame, text="Log suy nghĩ của AI:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.log_text = tk.Text(right_frame, bg="white", fg="black", font=('Consolas', 10))
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log(self, msg):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update_idletasks()

    def check_winner(self):
        lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for l in lines:
            if self.board[l[0]] == self.board[l[1]] == self.board[l[2]] != EMPTY: return self.board[l[0]]
        return None

    # --- ALPHA-BETA NGUYÊN BẢN (KHÔNG SPAM LOG) ---
    def alpha_beta(self, d, a, b, is_max):
        w = self.check_winner()
        if w == PLAYER_X: return 10 - d
        if w == PLAYER_O: return d - 10
        if EMPTY not in self.board: return 0
        
        cells = [i for i, v in enumerate(self.board) if v == EMPTY]
        if is_max:
            v = -math.inf
            for i in cells:
                self.board[i] = PLAYER_X
                v = max(v, self.alpha_beta(d+1, a, b, False))
                self.board[i] = EMPTY
                a = max(a, v)
                if b <= a: 
                    break # Cắt tỉa ngầm, không in log gây tràn bộ nhớ
            return v
        else:
            v = math.inf
            for i in cells:
                self.board[i] = PLAYER_O
                v = min(v, self.alpha_beta(d+1, a, b, True))
                self.board[i] = EMPTY
                b = min(b, v)
                if b <= a: 
                    break # Cắt tỉa ngầm, không in log gây tràn bộ nhớ
            return v

    def minimax(self, d, is_max):
        w = self.check_winner()
        if w == PLAYER_X: return 10 - d
        if w == PLAYER_O: return d - 10
        if EMPTY not in self.board: return 0
        
        cells = [i for i, v in enumerate(self.board) if v == EMPTY]
        vals = []
        for i in cells:
            self.board[i] = PLAYER_X if is_max else PLAYER_O
            val = self.minimax(d+1, not is_max)
            self.board[i] = EMPTY
            vals.append(val)
        return max(vals) if is_max else min(vals)

    def expectimax(self, d, is_max):
        w = self.check_winner()
        if w == PLAYER_X: return 10 - d
        if w == PLAYER_O: return d - 10
        if EMPTY not in self.board: return 0
        
        cells = [i for i, v in enumerate(self.board) if v == EMPTY]
        vals = []
        for i in cells:
            self.board[i] = PLAYER_X if is_max else PLAYER_O
            val = self.expectimax(d+1, not is_max)
            self.board[i] = EMPTY
            vals.append(val)
        return max(vals) if is_max else (sum(vals) / len(vals))

    def ai_move(self):
        if self.game_over: return
        algo = self.algo_var.get()
        self.log(f"\n--- AI TÍNH TOÁN VỚI THUẬT TOÁN: {algo.upper()} ---")
        best_val, move = -math.inf, -1
        
        available_moves = [i for i, v in enumerate(self.board) if v == EMPTY]
        
        for i in available_moves:
            self.board[i] = PLAYER_X
            if algo == "minimax": 
                val = self.minimax(0, False)
            elif algo == "alpha_beta": 
                val = self.alpha_beta(0, -math.inf, math.inf, False)
            else: 
                val = self.expectimax(0, False)
                
            self.board[i] = EMPTY
            self.log(f"==> Kết luận ô {i} đạt: {val:.2f} điểm.")
            if val > best_val: best_val, move = val, i
        
        if move != -1:
            self.board[move] = PLAYER_X
            self.update_ui()
            winner = self.check_winner()
            if winner: 
                self.log(f"\nAI ({winner}) CHIẾN THẮNG!"); self.game_over = True
            elif EMPTY not in self.board:
                self.log("\nTRẬN ĐẤU HÒA!"); self.game_over = True

    def player_move(self, idx):
        if self.board[idx] == EMPTY and not self.game_over:
            self.board[idx] = PLAYER_O
            self.update_ui()
            winner = self.check_winner()
            if winner: 
                self.log("\nBẠN ĐÃ THẮNG!"); self.game_over = True
            elif EMPTY not in self.board:
                self.log("\nTRẬN ĐẤU HÒA!"); self.game_over = True
            else: 
                self.root.after(100, self.ai_move)

    def update_ui(self):
        for i in range(9): self.buttons[i].config(text=self.board[i])

    def reset_board(self):
        self.board = [EMPTY]*9; self.game_over = False; self.update_ui()
        self.log_text.config(state=tk.NORMAL); self.log_text.delete(1.0, tk.END); self.log_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    TicTacToeAI(root)
    root.mainloop()
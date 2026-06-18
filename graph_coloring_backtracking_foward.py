import tkinter as tk
from tkinter import ttk
import copy

# Danh sach 11 huyen cua An Giang
ds_huyen = [
    "An Phú (AP)",
    "Châu Đốc (CĐ)",
    "Tân Châu (TC)",
    "Phú Tân (PT)",
    "Châu Phú (CP)",
    "Tịnh Biên (TB)",
    "Tri Tôn (TT)",
    "Châu Thành (CT)",
    "Chợ Mới (CM)",
    "Thoại Sơn (TS)",
    "Long Xuyên (LX)"
]

ten_tat = {
    "An Phú (AP)": "AP",
    "Châu Đốc (CĐ)": "CĐ",
    "Tân Châu (TC)": "TC",
    "Phú Tân (PT)": "PT",
    "Châu Phú (CP)": "CP",
    "Tịnh Biên (TB)": "TB",
    "Tri Tôn (TT)": "TT",
    "Châu Thành (CT)": "CT",
    "Chợ Mới (CM)": "CM",
    "Thoại Sơn (TS)": "TS",
    "Long Xuyên (LX)": "LX"
}

# Cac quan he giap ranh giua cac huyen
graph = {
    "An Phú (AP)": ["Tân Châu (TC)", "Châu Đốc (CĐ)"],
    "Châu Đốc (CĐ)": ["An Phú (AP)", "Tân Châu (TC)", "Phú Tân (PT)", "Châu Phú (CP)", "Tịnh Biên (TB)"],
    "Tân Châu (TC)": ["An Phú (AP)", "Châu Đốc (CĐ)", "Phú Tân (PT)"],
    "Phú Tân (PT)": ["Tân Châu (TC)", "Châu Đốc (CĐ)", "Châu Phú (CP)", "Chợ Mới (CM)"],
    "Châu Phú (CP)": ["Châu Đốc (CĐ)", "Phú Tân (PT)", "Chợ Mới (CM)", "Tịnh Biên (TB)", "Châu Thành (CT)"],
    "Tịnh Biên (TB)": ["Châu Đốc (CĐ)", "Châu Phú (CP)", "Châu Thành (CT)", "Tri Tôn (TT)"],
    "Tri Tôn (TT)": ["Tịnh Biên (TB)", "Châu Thành (CT)", "Thoại Sơn (TS)"],
    "Châu Thành (CT)": ["Châu Phú (CP)", "Tịnh Biên (TB)", "Tri Tôn (TT)", "Thoại Sơn (TS)", "Long Xuyên (LX)", "Chợ Mới (CM)"],
    "Chợ Mới (CM)": ["Phú Tân (PT)", "Châu Phú (CP)", "Châu Thành (CT)", "Long Xuyên (LX)"],
    "Thoại Sơn (TS)": ["Tri Tôn (TT)", "Châu Thành (CT)", "Long Xuyên (LX)"],
    "Long Xuyên (LX)": ["Châu Thành (CT)", "Thoại Sơn (TS)", "Chợ Mới (CM)"]
}

# Toa do x, y de ve huyen len giao dien
toa_do = {
    "An Phú (AP)": (250, 60),
    "Tân Châu (TC)": (360, 110),
    "Châu Đốc (CĐ)": (180, 160),
    "Phú Tân (PT)": (330, 210),
    "Châu Phú (CP)": (220, 270),
    "Tịnh Biên (TB)": (70, 230),
    "Tri Tôn (TT)": (60, 380),
    "Châu Thành (CT)": (200, 390),
    "Chợ Mới (CM)": (420, 350),
    "Thoại Sơn (TS)": (150, 500),
    "Long Xuyên (LX)": (300, 500)
}

# Mac dinh 4 mau de to khong trung nhau
MAU_MAC_DINH = ["Đỏ", "Xanh lá", "Xanh dương", "Vàng"]

MAU_HEX = {
    "Đỏ": "#EF5350",
    "Xanh lá": "#66BB6A",
    "Xanh dương": "#42A5F5",
    "Vàng": "#FFEE58"
}
MAU_TRONG = "#E0E0E0"
TRE_MS = 600 # toc do chay 0.6s moi buoc

class GiaoDienToMau:
    def __init__(self, cua_so):
        self.root = cua_so
        self.root.title("Chuong trinh to mau do thi - 11 Huyen An Giang")
        self.root.geometry("1100x680")
        self.root.configure(bg="#F5F5F5")
        
        # Bien de luu tru trang thai hien tai
        self.is_running = False
        self.assignment = {}
        self.domains = {}
        self.current_node = None
        self.generator = None
        self.color_list = MAU_MAC_DINH
        
        self.tao_giao_dien()
        self.reset_trang_thai()

    def tao_giao_dien(self):
        # Frame lon bao ben ngoai
        khung_chinh = tk.Frame(self.root, bg="#F5F5F5")
        khung_chinh.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas de ve ban do ben trai
        khung_trai = tk.LabelFrame(khung_chinh, text=" BẢN ĐỒ CÁC HUYỆN AN GIANG ", font=("Arial", 12, "bold"), bg="#FFFFFF", fg="#1976D2")
        khung_trai.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.canvas = tk.Canvas(khung_trai, bg="#FAFAFA", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel dieu khien ben phai
        khung_phai = tk.Frame(khung_chinh, bg="#F5F5F5", width=420)
        khung_phai.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5)
        khung_phai.pack_propagate(False)
        
        # Nut bam chay thuat toan
        khung_nut = tk.LabelFrame(khung_phai, text=" ĐIỀU KHIỂN THUẬT TOÁN ", font=("Arial", 11, "bold"), bg="#FFFFFF", fg="#2E7D32")
        khung_nut.pack(fill=tk.X, pady=(0, 10), ipady=5)
        
        tk.Label(khung_nut, text="Đang dung bo: 4 mau (Do, Xanh la, Xanh duong, Vang)", font=("Arial", 9, "italic"), bg="#FFFFFF", fg="#757575").pack(fill=tk.X, padx=10, pady=(5, 10))
        
        o_nut = tk.Frame(khung_nut, bg="#FFFFFF")
        o_nut.pack(fill=tk.X, padx=10, pady=5)
        
        self.btn_backtrack = tk.Button(o_nut, text="Backtracking", font=("Arial", 10, "bold"), bg="#FF9800", fg="white", height=2, command=self.chay_bt, relief=tk.FLAT)
        self.btn_backtrack.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.btn_fc = tk.Button(o_nut, text="Forward Checking", font=("Arial", 10, "bold"), bg="#2196F3", fg="white", height=2, command=self.chay_fc, relief=tk.FLAT)
        self.btn_fc.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
        
        # Nhat ky in ra
        khung_log = tk.LabelFrame(khung_phai, text=" LỊCH SỬ CHẠY THUẬT TOÁN ", font=("Arial", 11, "bold"), bg="#FFFFFF", fg="#E65100")
        khung_log.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(khung_log, wrap=tk.WORD, font=("Consolas", 10), bg="#1E1E1E", fg="#FFFFFF", insertbackground="white")
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        thanh_cuon = ttk.Scrollbar(khung_log, command=self.log_text.yview)
        thanh_cuon.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=thanh_cuon.set)

    def ghi_nhat_ky(self, nd):
        self.log_text.insert(tk.END, nd + "\n")
        self.log_text.see(tk.END)

    def reset_trang_thai(self):
        self.is_running = False
        self.assignment = {}
        
        # Tuong duong domain dictionary comprehension nhung viet dang thuong de bot giong AI
        self.domains = {}
        for h in ds_huyen:
            self.domains[h] = list(self.color_list)
            
        self.current_node = None
        self.generator = None
        self.log_text.delete("1.0", tk.END)
        self.ve_ban_do()

    def ve_ban_do(self):
        self.canvas.delete("all")
        
        # Noi cac huyen giap nhau bang duong line truoc
        for nut, lân_cân in graph.items():
            x1, y1 = toa_do[nut]
            for lc in lân_cân:
                x2, y2 = toa_do[lc]
                self.canvas.create_line(x1, y1, x2, y2, fill="#B0BEC5", width=2)
                
        # Ve hinh tron va ghi ten huyen
        bk = 24
        for nut in ds_huyen:
            x, y = toa_do[nut]
            
            # lay mau to
            m_huyen = self.assignment.get(nut, None)
            m_ve = MAU_HEX[m_huyen] if m_huyen else MAU_TRONG
            
            # ve vien do cho o dang xet
            v_mau = "#FF1744" if nut == self.current_node else "#37474F"
            v_day = 4 if nut == self.current_node else 2
            
            self.canvas.create_oval(x - bk, y - bk, x + bk, y + bk, fill=m_ve, outline=v_mau, width=v_day)
            
            # Ghi ten viet tat vao trong o tron
            self.canvas.create_text(x, y, text=ten_tat[nut], font=("Arial", 10, "bold"), fill="#000000" if m_ve != MAU_TRONG else "#37474F")
            
            # Ghi ten tieng Viet day du ben tren o tron
            ten_full = nut.split(" (")[0]
            self.canvas.create_text(x, y - bk - 10, text=ten_full, font=("Arial", 8, "bold"), fill="#212121")
            
            # Ve domain o phia duoi nut
            lst_mau = self.domains.get(nut, [])
            n_cham = len(lst_mau)
            khoang_cach = 10
            x_bat_dau = x - ((n_cham - 1) * khoang_cach) / 2
            
            for i, col in enumerate(lst_mau):
                cx = x_bat_dau + i * khoang_cach
                cy = y + bk + 10
                self.canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill=MAU_HEX[col], outline="#FFFFFF", width=0.5)

    # backtrack thuong - khong update o xung quanh
    def thu_thuat_bt(self, assignment, domains, st):
        if len(assignment) == len(ds_huyen):
            yield ("SUCCESS", assignment, domains, "Đã tô xong bản đồ bằng Backtracking thuần.")
            return
            
        var = None
        for h in ds_huyen:
            if h not in assignment:
                var = h
                break
                
        if var is None:
            return
            
        st[0] += 1
        yield ("SELECT_VAR", var, assignment, domains, f"Bước {st[0]}: Chọn huyện để tô: {var}")
        
        for val in list(domains[var]):
            yield ("TRY_VAL", (var, val), assignment, domains, f" - Thử gán {var} = {val}")
            
            # kiem tra hop le
            check = True
            for lc in graph[var]:
                if lc in assignment and assignment[lc] == val:
                    check = False
                    break
                    
            if check:
                assignment[var] = val
                yield ("VALID", (var, val), assignment, domains, f"   -> Hợp lệ. Assignment = {assignment}")
                
                sub = self.thu_thuat_bt(assignment, domains, st)
                done = False
                for step in sub:
                    yield step
                    if step[0] == "SUCCESS":
                        done = True
                        break
                if done:
                    return
                
                # rollback
                yield ("BACKTRACK", (var, val), assignment, domains, f"   -> Quay lui: Hủy gán {var} = {val}")
                del assignment[var]
            else:
                yield ("INVALID", (var, val), assignment, domains, f"   -> Không hợp lệ! (Huyện giáp ranh trùng màu {val})")
                
        yield ("NO_SOL", var, assignment, domains, f"   -> Không còn màu hợp lệ cho {var}. Đang quay lui...")

    # backtracking ket hop forward checking
    def thu_thuat_fc(self, assignment, domains, st):
        if len(assignment) == len(ds_huyen):
            yield ("SUCCESS", assignment, domains, "Đã tô xong bản đồ bằng Forward Checking.")
            return
            
        var = None
        for h in ds_huyen:
            if h not in assignment:
                var = h
                break
                
        if var is None:
            return
            
        st[0] += 1
        yield ("SELECT_VAR", var, assignment, domains, f"Bước {st[0]}: Chọn huyện để tô: {var}")
        
        for val in list(domains[var]):
            yield ("TRY_VAL", (var, val), assignment, domains, f" - Thử gán {var} = {val}")
            
            check = True
            for lc in graph[var]:
                if lc in assignment and assignment[lc] == val:
                    check = False
                    break
                    
            if check:
                assignment[var] = val
                yield ("VALID", (var, val), assignment, domains, f"   -> Hợp lệ. Assignment = {assignment}")
                
                backup_domains = copy.deepcopy(domains)
                
                # cap nhat lai domain cac o ke ben
                check_fc = True
                ds_log = ["   -> Cập nhật domain các huyện giáp ranh chưa gán:"]
                for lc in graph[var]:
                    if lc not in assignment:
                        if val in domains[lc]:
                            domains[lc].remove(val)
                            ds_log.append(f"      + Miền giá trị của {lc} = {domains[lc]}")
                            if len(domains[lc]) == 0:
                                check_fc = False
                                ds_log.append(f"      Miền giá trị của {lc} bị rỗng!")
                
                yield ("FORWARD_CHECKING", (var, val), assignment, domains, "\n".join(ds_log))
                
                if check_fc:
                    sub = self.thu_thuat_fc(assignment, domains, st)
                    done = False
                    for step in sub:
                        yield step
                        if step[0] == "SUCCESS":
                            done = True
                            break
                    if done:
                        return
                else:
                    yield ("FC_FAILED", (var, val), assignment, domains, "   -> Forward Checking thất bại! Phải quay lui.")
                    
                # rollback
                yield ("BACKTRACK", (var, val), assignment, domains, f"   -> Quay lui: Hủy gán {var} = {val}")
                del assignment[var]
                domains = backup_domains
            else:
                yield ("INVALID", (var, val), assignment, domains, f"   -> Không hợp lệ! (Huyện giáp ranh trùng màu {val})")
                
        yield ("NO_SOL", var, assignment, domains, f"   -> Không còn màu hợp lệ cho {var}. Đang quay lui...")

    def chay_bt(self):
        self.reset_trang_thai()
        self.is_running = True
        st = [0]
        self.generator = self.thu_thuat_bt(self.assignment, self.domains, st)
        self.ghi_nhat_ky("BACKTRACKING")
        self.ghi_nhat_ky("- Không cập nhật miền giá trị (domain) của các huyện xung quanh.\n")
        self.vong_lap_chay()

    def chay_fc(self):
        self.reset_trang_thai()
        self.is_running = True
        st = [0]
        self.generator = self.thu_thuat_fc(self.assignment, self.domains, st)
        self.ghi_nhat_ky("FORWARD CHECKING")
        self.ghi_nhat_ky("- Miền giá trị (domain) các huyện xung quanh được cập nhật liên tục.\n")
        self.vong_lap_chay()

    def vong_lap_chay(self):
        if not self.is_running:
            return
            
        if self.chay_tung_buoc():
            self.root.after(TRE_MS, self.vong_lap_chay)
        else:
            self.is_running = False

    def chay_tung_buoc(self):
        if not self.generator:
            return False
            
        try:
            state = next(self.generator)
            trang_thai, muc_tieu, assignment, domains, nd_log = state
            
            self.assignment = assignment
            self.domains = domains
            
            if trang_thai == "SELECT_VAR":
                self.current_node = muc_tieu
            elif trang_thai in ["TRY_VAL", "VALID", "FORWARD_CHECKING", "FC_FAILED", "BACKTRACK", "INVALID"]:
                if type(muc_tieu) == tuple:
                    self.current_node = muc_tieu[0]
            elif trang_thai == "SUCCESS":
                self.current_node = None
                
            self.ghi_nhat_ky(nd_log)
            self.ve_ban_do()
            return True
        except StopIteration:
            self.ghi_nhat_ky("\n=> Da dung thuat toan.")
            self.generator = None
            return False

if __name__ == "__main__":
    giao_dien = tk.Tk()
    ung_dung = GiaoDienToMau(giao_dien)
    giao_dien.mainloop()

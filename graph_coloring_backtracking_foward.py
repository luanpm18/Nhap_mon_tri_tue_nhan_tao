# -*- coding: utf-8 -*-
import sys
import tkinter as tk
from tkinter import ttk
import copy
import random
from collections import deque

sys.stdout.reconfigure(encoding="utf-8")

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
TRE_MS = 600  # toc do chay 0.6s moi buoc


class GiaoDienToMau:
    def __init__(self, cua_so):
        self.root = cua_so
        self.root.title("Tô màu đồ thị - 11 Huyện An Giang (BT / FC / AC-3 / Min-Conflicts)")
        self.root.geometry("1150x700")
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
        khung_chinh = tk.Frame(self.root, bg="#F5F5F5")
        khung_chinh.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas bản đồ bên trái
        khung_trai = tk.LabelFrame(khung_chinh, text=" BẢN ĐỒ CÁC HUYỆN AN GIANG ",
                                   font=("Arial", 12, "bold"), bg="#FFFFFF", fg="#1976D2")
        khung_trai.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.canvas = tk.Canvas(khung_trai, bg="#FAFAFA", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Panel điều khiển bên phải
        khung_phai = tk.Frame(khung_chinh, bg="#F5F5F5", width=440)
        khung_phai.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5)
        khung_phai.pack_propagate(False)

        # --- Khung nút bấm ---
        khung_nut = tk.LabelFrame(khung_phai, text=" ĐIỀU KHIỂN THUẬT TOÁN ",
                                  font=("Arial", 11, "bold"), bg="#FFFFFF", fg="#2E7D32")
        khung_nut.pack(fill=tk.X, pady=(0, 10), ipady=5)

        tk.Label(khung_nut,
                 text="Bộ màu: Đỏ · Xanh lá · Xanh dương · Vàng",
                 font=("Arial", 9, "italic"), bg="#FFFFFF", fg="#757575"
                 ).pack(fill=tk.X, padx=10, pady=(5, 8))

        # Hàng 1: BT và FC
        hang1 = tk.Frame(khung_nut, bg="#FFFFFF")
        hang1.pack(fill=tk.X, padx=10, pady=(0, 4))

        self.btn_backtrack = tk.Button(
            hang1, text="Backtracking", font=("Arial", 10, "bold"),
            bg="#FF9800", fg="white", height=2,
            command=self.chay_bt, relief=tk.FLAT)
        self.btn_backtrack.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        self.btn_fc = tk.Button(
            hang1, text="Forward Checking", font=("Arial", 10, "bold"),
            bg="#2196F3", fg="white", height=2,
            command=self.chay_fc, relief=tk.FLAT)
        self.btn_fc.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))

        # Hàng 2: AC-3 và Min-Conflicts
        hang2 = tk.Frame(khung_nut, bg="#FFFFFF")
        hang2.pack(fill=tk.X, padx=10, pady=(0, 6))

        self.btn_ac3 = tk.Button(
            hang2, text="AC-3", font=("Arial", 10, "bold"),
            bg="#9C27B0", fg="white", height=2,
            command=self.chay_ac3, relief=tk.FLAT)
        self.btn_ac3.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        self.btn_mc = tk.Button(
            hang2, text="Min-Conflicts", font=("Arial", 10, "bold"),
            bg="#009688", fg="white", height=2,
            command=self.chay_mc, relief=tk.FLAT)
        self.btn_mc.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))

        # --- Nhật ký ---
        khung_log = tk.LabelFrame(khung_phai, text=" LỊCH SỬ CHẠY THUẬT TOÁN ",
                                  font=("Arial", 11, "bold"), bg="#FFFFFF", fg="#E65100")
        khung_log.pack(fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(khung_log, wrap=tk.WORD, font=("Consolas", 10),
                                bg="#1E1E1E", fg="#FFFFFF", insertbackground="white")
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        thanh_cuon = ttk.Scrollbar(khung_log, command=self.log_text.yview)
        thanh_cuon.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=thanh_cuon.set)

    # ----------------------------------------------------------------
    # TIỆN ÍCH CHUNG
    # ----------------------------------------------------------------
    def ghi_nhat_ky(self, nd):
        self.log_text.insert(tk.END, nd + "\n")
        self.log_text.see(tk.END)

    def reset_trang_thai(self):
        self.is_running = False
        self.assignment = {}
        self.domains = {}
        for h in ds_huyen:
            self.domains[h] = list(self.color_list)
        self.current_node = None
        self.generator = None
        self.log_text.delete("1.0", tk.END)
        self.ve_ban_do()

    def ve_ban_do(self):
        self.canvas.delete("all")

        # Vẽ cạnh (đường nối)
        for nut, lan_can in graph.items():
            x1, y1 = toa_do[nut]
            for lc in lan_can:
                x2, y2 = toa_do[lc]
                self.canvas.create_line(x1, y1, x2, y2, fill="#B0BEC5", width=2)

        # Vẽ nút (huyện)
        bk = 24
        for nut in ds_huyen:
            x, y = toa_do[nut]
            m_huyen = self.assignment.get(nut, None)
            m_ve = MAU_HEX[m_huyen] if m_huyen else MAU_TRONG

            v_mau = "#FF1744" if nut == self.current_node else "#37474F"
            v_day = 4 if nut == self.current_node else 2

            self.canvas.create_oval(x - bk, y - bk, x + bk, y + bk,
                                    fill=m_ve, outline=v_mau, width=v_day)
            self.canvas.create_text(x, y, text=ten_tat[nut],
                                    font=("Arial", 10, "bold"),
                                    fill="#000000" if m_ve != MAU_TRONG else "#37474F")

            ten_full = nut.split(" (")[0]
            self.canvas.create_text(x, y - bk - 10, text=ten_full,
                                    font=("Arial", 8, "bold"), fill="#212121")

            # Vẽ chấm màu domain phía dưới nút
            lst_mau = self.domains.get(nut, [])
            n_cham = len(lst_mau)
            khoang_cach = 10
            x_bat_dau = x - ((n_cham - 1) * khoang_cach) / 2
            for i, col in enumerate(lst_mau):
                cx = x_bat_dau + i * khoang_cach
                cy = y + bk + 10
                self.canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4,
                                        fill=MAU_HEX[col], outline="#FFFFFF", width=0.5)

    # THUẬT TOÁN 1: BACKTRACKING
    def thu_thuat_bt(self, assignment, domains, st):
        if len(assignment) == len(ds_huyen):
            yield ("SUCCESS", None, assignment, domains, "Đã tô xong bản đồ bằng Backtracking thuần.")
            return

        var = None
        for h in ds_huyen:
            if h not in assignment:
                var = h
                break
        if var is None:
            return

        st[0] += 1
        yield ("SELECT_VAR", var, assignment, domains, f"Bước {st[0]}: Chọn huyện: {var}")

        for val in list(domains[var]):
            yield ("TRY_VAL", (var, val), assignment, domains, f" - Thử gán {var} = {val}")

            check = all(
                not (lc in assignment and assignment[lc] == val)
                for lc in graph[var]
            )

            if check:
                assignment[var] = val
                yield ("VALID", (var, val), assignment, domains,
                       f"   -> Hợp lệ. Assignment = {assignment}")

                sub = self.thu_thuat_bt(assignment, domains, st)
                done = False
                for step in sub:
                    yield step
                    if step[0] == "SUCCESS":
                        done = True
                        break
                if done:
                    return

                yield ("BACKTRACK", (var, val), assignment, domains,
                       f"   -> Quay lui: Hủy gán {var} = {val}")
                del assignment[var]
            else:
                yield ("INVALID", (var, val), assignment, domains,
                       f"   -> Không hợp lệ! (Huyện giáp ranh trùng màu {val})")

        yield ("NO_SOL", var, assignment, domains,
               f"   -> Không còn màu hợp lệ cho {var}. Đang quay lui...")

    # THUẬT TOÁN 2: BACKTRACKING + FORWARD CHECKING
    def thu_thuat_fc(self, assignment, domains, st):
        if len(assignment) == len(ds_huyen):
            yield ("SUCCESS", None, assignment, domains, "Đã tô xong bản đồ bằng Forward Checking.")
            return

        var = None
        for h in ds_huyen:
            if h not in assignment:
                var = h
                break
        if var is None:
            return

        st[0] += 1
        yield ("SELECT_VAR", var, assignment, domains, f"Bước {st[0]}: Chọn huyện: {var}")

        for val in list(domains[var]):
            yield ("TRY_VAL", (var, val), assignment, domains, f" - Thử gán {var} = {val}")

            check = all(
                not (lc in assignment and assignment[lc] == val)
                for lc in graph[var]
            )

            if check:
                assignment[var] = val
                yield ("VALID", (var, val), assignment, domains,
                       f"   -> Hợp lệ. Assignment = {assignment}")

                backup_domains = copy.deepcopy(domains)

                check_fc = True
                ds_log = ["   -> Cập nhật domain các huyện giáp ranh chưa gán (Forward Checking):"]
                for lc in graph[var]:
                    if lc not in assignment:
                        if val in domains[lc]:
                            domains[lc].remove(val)
                            ds_log.append(f"      + Domain[{lc}] = {domains[lc]}")
                            if len(domains[lc]) == 0:
                                check_fc = False
                                ds_log.append(f"      [!] Domain[{lc}] bị rỗng!")

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
                    yield ("FC_FAILED", (var, val), assignment, domains,
                           "   -> Forward Checking thất bại! Phải quay lui.")

                yield ("BACKTRACK", (var, val), assignment, domains,
                       f"   -> Quay lui: Hủy gán {var} = {val}")
                del assignment[var]
                domains = backup_domains
            else:
                yield ("INVALID", (var, val), assignment, domains,
                       f"   -> Không hợp lệ! (Huyện giáp ranh trùng màu {val})")

        yield ("NO_SOL", var, assignment, domains,
               f"   -> Không còn màu hợp lệ cho {var}. Đang quay lui...")

    # THUẬT TOÁN 3: AC-3 + BACKTRACKING
    def _rm_inconsistent(self, Xi, Xj, domains):
        """Xóa giá trị x khỏi Domain[Xi] nếu không có y ∈ Domain[Xj] sao cho x ≠ y."""
        removed = []
        for x in list(domains[Xi]):
            if not any(x != y for y in domains[Xj]):
                domains[Xi].remove(x)
                removed.append(x)
        return removed

    def thu_thuat_ac3(self, assignment, domains, st):
        """
        Generator AC-3 + Backtracking.

        Giai đoạn 1 – AC-3 toàn phần: thu hẹp domain trước khi bắt đầu gán.
        Giai đoạn 2 – Backtracking + AC-3 cục bộ: sau mỗi lần gán, lan truyền
                       ràng buộc tới hàng xóm qua local AC-3.
        """
        # --- GIAI ĐOẠN 1: AC-3 toàn phần ---
        yield ("AC3_START", None, assignment, domains,
               "=== AC-3 GIAI ĐOẠN 1: Thu hẹp domain toàn phần ===")

        queue = deque()
        for Xi in graph:
            for Xj in graph[Xi]:
                queue.append((Xi, Xj))

        while queue:
            (Xi, Xj) = queue.popleft()
            removed = self._rm_inconsistent(Xi, Xj, domains)
            if removed:
                if not domains[Xi]:
                    yield ("AC3_FAIL", Xi, assignment, domains,
                           f"  [!] AC-3: Domain[{Xi}] rỗng -> Không có lời giải!")
                    return
                msg = f"  [AC-3] Xóa {removed} khỏi Domain[{Xi}] (do hàng xóm {Xj})\n" \
                      f"         Domain[{Xi}] còn: {domains[Xi]}"
                yield ("AC3_PRUNE", Xi, assignment, domains, msg)
                for Xk in graph[Xi]:
                    if Xk != Xj:
                        queue.append((Xk, Xi))

        yield ("AC3_DONE", None, assignment, domains,
               "=== AC-3 hoàn tất. Bắt đầu Backtracking + AC-3 cục bộ ===\n")

        # Nếu AC-3 thu hẹp hoàn toàn → lời giải trực tiếp
        if all(len(domains[h]) == 1 for h in ds_huyen):
            for h in ds_huyen:
                assignment[h] = domains[h][0]
            yield ("SUCCESS", None, assignment, domains,
                   "AC-3 thu hẹp hoàn toàn → Lời giải trực tiếp!")
            return

        # --- GIAI ĐOẠN 2: Backtracking + AC-3 cục bộ ---
        yield from self._ac3_bt(assignment, domains, st)

    def _ac3_bt(self, assignment, domains, st):
        """Backtracking + AC-3 lan truyền cục bộ (dùng yield từ thu_thuat_ac3)."""
        if len(assignment) == len(ds_huyen):
            yield ("SUCCESS", None, assignment, domains,
                   "Đã tô xong bản đồ bằng AC-3 + Backtracking.")
            return

        var = next((h for h in ds_huyen if h not in assignment), None)
        if var is None:
            return

        st[0] += 1
        yield ("SELECT_VAR", var, assignment, domains,
               f"Bước {st[0]}: Chọn huyện: {var}  |  Domain = {domains[var]}")

        for val in list(domains[var]):
            # Kiểm tra hợp lệ với assignment hiện tại
            check = all(
                not (lc in assignment and assignment[lc] == val)
                for lc in graph[var]
            )

            if not check:
                yield ("INVALID", (var, val), assignment, domains,
                       f"   -> Bỏ qua '{val}' (trùng màu hàng xóm đã gán)")
                continue

            yield ("TRY_VAL", (var, val), assignment, domains,
                   f" - Thử gán {var} = {val}")
            assignment[var] = val
            yield ("VALID", (var, val), assignment, domains,
                   f"   -> Gán {var} = {val}")

            backup = copy.deepcopy(domains)

            # AC-3 cục bộ: lan truyền ràng buộc từ var sang hàng xóm
            local_queue = deque(
                (lc, var) for lc in graph[var] if lc not in assignment
            )
            ok = True
            ac3_logs = []
            while local_queue and ok:
                (Xi, Xj) = local_queue.popleft()
                removed = self._rm_inconsistent(Xi, Xj, domains)
                if removed:
                    if not domains[Xi]:
                        ok = False
                        ac3_logs.append(
                            f"      [!] Domain[{Xi}] rỗng sau khi xóa {removed}!")
                        break
                    ac3_logs.append(
                        f"      [AC-3 cục bộ] Xóa {removed} khỏi Domain[{Xi}] → còn {domains[Xi]}")
                    for Xk in graph[Xi]:
                        if Xk != Xj and Xk not in assignment:
                            local_queue.append((Xk, Xi))

            if ac3_logs:
                yield ("FORWARD_CHECKING", (var, val), assignment, domains,
                       "   -> AC-3 lan truyền ràng buộc:\n" + "\n".join(ac3_logs))

            if ok:
                sub = self._ac3_bt(assignment, domains, st)
                done = False
                for step in sub:
                    yield step
                    if step[0] == "SUCCESS":
                        done = True
                        break
                if done:
                    return
            else:
                yield ("FC_FAILED", (var, val), assignment, domains,
                       "   -> AC-3 cục bộ phát hiện mâu thuẫn! Quay lui.")

            yield ("BACKTRACK", (var, val), assignment, domains,
                   f"   -> Quay lui: Hủy gán {var} = {val}")
            del assignment[var]
            domains.update(backup)

        yield ("NO_SOL", var, assignment, domains,
               f"   -> Không còn màu hợp lệ cho {var}. Đang quay lui...")

    # THUẬT TOÁN 4: MIN-CONFLICTS
    def thu_thuat_mc(self, assignment, domains, max_steps=300, seed=42):
        """
        Generator Min-Conflicts.

        Bước 1: Gán màu ngẫu nhiên cho tất cả các huyện.
        Bước 2: Lặp — chọn ngẫu nhiên một huyện đang vi phạm ràng buộc,
                gán cho nó màu làm giảm số xung đột nhất.
        """
        random.seed(seed)
        colors = self.color_list

        # Khởi tạo gán màu ngẫu nhiên
        for h in ds_huyen:
            assignment[h] = random.choice(colors)

        def count_conflicts(var, val):
            return sum(1 for nb in graph[var] if assignment.get(nb) == val)

        def is_solution():
            return all(count_conflicts(v, assignment[v]) == 0 for v in ds_huyen)

        yield ("MC_INIT", None, assignment, domains,
               "=== MIN-CONFLICTS: Gán màu ngẫu nhiên ban đầu ===")

        init_log = []
        for h in ds_huyen:
            cf = count_conflicts(h, assignment[h])
            init_log.append(f"  {h}: {assignment[h]}  (conflicts: {cf})")
        total_cf = sum(count_conflicts(v, assignment[v]) for v in ds_huyen)
        init_log.append(f"\n  Tổng conflicts ban đầu: {total_cf}")
        yield ("MC_INIT_DONE", None, assignment, domains, "\n".join(init_log))

        # Highlight tất cả là "current" lúc init
        self.current_node = None

        if is_solution():
            yield ("SUCCESS", None, assignment, domains,
                   "Gán ngẫu nhiên may mắn ngay là lời giải!")
            return

        yield ("MC_LOOP", None, assignment, domains,
               "\n--- Bắt đầu vòng lặp Min-Conflicts ---")

        for i in range(1, max_steps + 1):
            if is_solution():
                yield ("SUCCESS", None, assignment, domains,
                       f"Tìm thấy lời giải sau {i - 1} bước Min-Conflicts!")
                return

            # Chọn ngẫu nhiên huyện đang vi phạm
            conflicted = [v for v in ds_huyen if count_conflicts(v, assignment[v]) > 0]
            var = random.choice(conflicted)

            # Tìm màu làm giảm conflicts nhiều nhất
            conflict_counts = {c: count_conflicts_with(var, c, assignment) for c in colors}
            min_c = min(conflict_counts.values())
            best = [c for c, cf in conflict_counts.items() if cf == min_c]
            new_val = random.choice(best)

            old_val = assignment[var]
            assignment[var] = new_val

            remaining = [v for v in ds_huyen if count_conflicts(v, assignment[v]) > 0]
            msg = (f"Bước {i:3d}: {var}\n"
                   f"   {old_val} -> {new_val}  "
                   f"(conflicts: {conflict_counts[old_val]} -> {min_c})\n"
                   f"   Huyện còn xung đột: {len(remaining)}")

            yield ("MC_STEP", var, assignment, domains, msg)

        yield ("MC_FAIL", None, assignment, domains,
               f"Thất bại sau {max_steps} bước Min-Conflicts.")


    def chay_bt(self):
        self.reset_trang_thai()
        self.is_running = True
        st = [0]
        self.generator = self.thu_thuat_bt(self.assignment, self.domains, st)
        self.ghi_nhat_ky("══════════════════════════════════════════")
        self.ghi_nhat_ky("  THUẬT TOÁN: BACKTRACKING THUẦN TÚY")
        self.ghi_nhat_ky("  Không cập nhật domain hàng xóm.")
        self.ghi_nhat_ky("══════════════════════════════════════════\n")
        self.vong_lap_chay()

    def chay_fc(self):
        self.reset_trang_thai()
        self.is_running = True
        st = [0]
        self.generator = self.thu_thuat_fc(self.assignment, self.domains, st)
        self.ghi_nhat_ky("══════════════════════════════════════════")
        self.ghi_nhat_ky("  THUẬT TOÁN: FORWARD CHECKING")
        self.ghi_nhat_ky("  Domain hàng xóm được cập nhật sau mỗi lần gán.")
        self.ghi_nhat_ky("══════════════════════════════════════════\n")
        self.vong_lap_chay()

    def chay_ac3(self):
        self.reset_trang_thai()
        self.is_running = True
        st = [0]
        self.generator = self.thu_thuat_ac3(self.assignment, self.domains, st)
        self.ghi_nhat_ky("══════════════════════════════════════════")
        self.ghi_nhat_ky("  THUẬT TOÁN: AC-3 + BACKTRACKING")
        self.ghi_nhat_ky("  Giai đoạn 1: AC-3 toàn phần thu hẹp domain.")
        self.ghi_nhat_ky("  Giai đoạn 2: BT + AC-3 cục bộ lan truyền.")
        self.ghi_nhat_ky("══════════════════════════════════════════\n")
        self.vong_lap_chay()

    def chay_mc(self):
        self.reset_trang_thai()
        self.is_running = True
        self.generator = self.thu_thuat_mc(self.assignment, self.domains,
                                           max_steps=300, seed=42)
        self.ghi_nhat_ky("══════════════════════════════════════════")
        self.ghi_nhat_ky("  THUẬT TOÁN: MIN-CONFLICTS")
        self.ghi_nhat_ky("  Gán màu ngẫu nhiên, rồi sửa xung đột dần.")
        self.ghi_nhat_ky("══════════════════════════════════════════\n")
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
            # Tất cả các state đều có dạng: (trang_thai, muc_tieu, assignment, domains, nd_log)
            trang_thai = state[0]
            muc_tieu   = state[1]
            assignment = state[2]
            domains    = state[3]
            nd_log     = state[4]

            self.assignment = assignment
            self.domains    = domains

            # Cập nhật nút đang xét (highlight đỏ trên canvas)
            if trang_thai in ("SELECT_VAR", "AC3_PRUNE", "AC3_FAIL"):
                self.current_node = muc_tieu
            elif trang_thai in ("TRY_VAL", "VALID", "FORWARD_CHECKING",
                                "FC_FAILED", "BACKTRACK", "INVALID"):
                self.current_node = muc_tieu[0] if isinstance(muc_tieu, tuple) else muc_tieu
            elif trang_thai == "MC_STEP":
                self.current_node = muc_tieu
            elif trang_thai in ("SUCCESS", "AC3_DONE", "AC3_START",
                                "MC_INIT", "MC_INIT_DONE", "MC_LOOP",
                                "MC_FAIL", "NO_SOL"):
                self.current_node = None

            self.ghi_nhat_ky(nd_log)
            self.ve_ban_do()
            return True

        except StopIteration:
            self.ghi_nhat_ky("\n=> Thuật toán đã kết thúc.")
            self.generator = None
            return False


def count_conflicts_with(var, val, assignment):
    return sum(1 for nb in graph[var] if assignment.get(nb) == val)


if __name__ == "__main__":
    giao_dien = tk.Tk()
    ung_dung = GiaoDienToMau(giao_dien)
    giao_dien.mainloop()

import random

# BÀI TÔ MÀU BẢN ĐỒ AN GIANG - THUẬT TOÁN MIN-CONFLICTS

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

graph = {
    "An Phú (AP)":      ["Tân Châu (TC)", "Châu Đốc (CĐ)"],
    "Châu Đốc (CĐ)":   ["An Phú (AP)", "Tân Châu (TC)", "Phú Tân (PT)", "Châu Phú (CP)", "Tịnh Biên (TB)"],
    "Tân Châu (TC)":   ["An Phú (AP)", "Châu Đốc (CĐ)", "Phú Tân (PT)"],
    "Phú Tân (PT)":    ["Tân Châu (TC)", "Châu Đốc (CĐ)", "Châu Phú (CP)", "Chợ Mới (CM)"],
    "Châu Phú (CP)":   ["Châu Đốc (CĐ)", "Phú Tân (PT)", "Chợ Mới (CM)", "Tịnh Biên (TB)", "Châu Thành (CT)"],
    "Tịnh Biên (TB)":  ["Châu Đốc (CĐ)", "Châu Phú (CP)", "Châu Thành (CT)", "Tri Tôn (TT)"],
    "Tri Tôn (TT)":    ["Tịnh Biên (TB)", "Châu Thành (CT)", "Thoại Sơn (TS)"],
    "Châu Thành (CT)": ["Châu Phú (CP)", "Tịnh Biên (TB)", "Tri Tôn (TT)", "Thoại Sơn (TS)", "Long Xuyên (LX)", "Chợ Mới (CM)"],
    "Chợ Mới (CM)":    ["Phú Tân (PT)", "Châu Phú (CP)", "Châu Thành (CT)", "Long Xuyên (LX)"],
    "Thoại Sơn (TS)":  ["Tri Tôn (TT)", "Châu Thành (CT)", "Long Xuyên (LX)"],
    "Long Xuyên (LX)": ["Châu Thành (CT)", "Thoại Sơn (TS)", "Chợ Mới (CM)"]
}

colors = ["Đỏ", "Xanh lá", "Xanh dương", "Vàng"]


# CONFLICTS(var, v, current, csp):
# Đếm số ràng buộc bị vi phạm nếu gán var = v trong current
def CONFLICTS(var, v, current):
    return sum(1 for neighbor in graph[var] if current.get(neighbor) == v)


# Kiểm tra current có phải là lời giải (không có xung đột nào)
def is_solution(current):
    return all(CONFLICTS(var, current[var], current) == 0 for var in ds_huyen)


# function MIN-CONFLICTS(csp, max_steps) returns a solution or failure
def MIN_CONFLICTS(max_steps):
    print("=" * 60)
    print("BÀI TÔ MÀU AN GIANG - THUẬT TOÁN MIN-CONFLICTS")
    print(f"Bộ màu: {colors}  |  max_steps = {max_steps}")
    print("=" * 60)

    # current <- an initial complete assignment for csp
    current = {var: random.choice(colors) for var in ds_huyen}

    print("\n[Khởi tạo] Gán màu ngẫu nhiên (current ban đầu):")
    for var in ds_huyen:
        xd = CONFLICTS(var, current[var], current)
        print(f"  {var}: {current[var]}  (conflicts với hàng xóm: {xd})")

    tong_xd = sum(CONFLICTS(v, current[v], current) for v in ds_huyen)
    so_huyen_xd = len([v for v in ds_huyen if CONFLICTS(v, current[v], current) > 0])
    print(f"\n  => Tổng conflicts (đếm 2 lần mỗi cạnh): {tong_xd}  |  Số huyện đang xung đột: {so_huyen_xd}")

    print("\n--- Vòng lặp Min-Conflicts ---")

    # for i = 1 to max_steps do
    for i in range(1, max_steps + 1):

        # if current is a solution for csp then return current
        if is_solution(current):
            print(f"\n=> current là lời giải! Dừng sau {i - 1} bước.")
            return current

        # var <- a randomly chosen conflicted variable from csp.VARIABLES
        conflicted = [var for var in ds_huyen if CONFLICTS(var, current[var], current) > 0]
        var = random.choice(conflicted)

        # value <- the value v for var that minimizes CONFLICTS(var, v, current, csp)
        conflict_counts = {v: CONFLICTS(var, v, current) for v in colors}
        min_conflict = min(conflict_counts.values())
        best_values = [v for v, c in conflict_counts.items() if c == min_conflict]
        value = random.choice(best_values)   # chọn ngẫu nhiên nếu có nhiều v tốt bằng nhau

        old_value = current[var]

        # set var = value in current
        current[var] = value

        # Đếm conflicted vars SAU khi gán
        conflicted_sau = [v for v in ds_huyen if CONFLICTS(v, current[v], current) > 0]

        print(f"Bước {i:3d}: var={var}  |  {old_value} -> {value}  "
              f"(conflicts: {conflict_counts[old_value]} -> {min_conflict})  "
              f"| huyện xung đột sau bước này: {len(conflicted_sau)}")

    # return failure
    print(f"\n=> THẤT BẠI sau {max_steps} bước.")
    return None


# ---- CHẠY ----
random.seed(42)
ket_qua = MIN_CONFLICTS(max_steps=500)

if ket_qua:
    print("\n" + "=" * 60)
    print("=> TÔ MÀU THÀNH CÔNG!")
    print("=" * 60)
    for var in ds_huyen:
        print(f"   {var}: {ket_qua[var]}")

    # Kiểm tra lại
    print("\n--- Kiểm tra hợp lệ ---")
    ok = True
    for var in ds_huyen:
        for nb in graph[var]:
            if ket_qua[var] == ket_qua[nb]:
                print(f"  [!] Xung đột: {var} và {nb} cùng màu {ket_qua[var]}")
                ok = False
    if ok:
        print("  Tất cả huyện hợp lệ - không có xung đột!")

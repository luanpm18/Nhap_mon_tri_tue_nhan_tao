import copy
from collections import deque

# BÀI TÔ MÀU BẢN ĐỒ AN GIANG - THUẬT TOÁN AC-3

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


# RM-INCONSISTENT-VALUES(Xi, Xj):
# Xóa x khỏi Domain[Xi] nếu không tồn tại y trong Domain[Xj] sao cho x != y
def rm_inconsistent_values(Xi, Xj, domains):
    removed = False
    for x in list(domains[Xi]):
        if not any(x != y for y in domains[Xj]):  # không có y nào hợp lệ
            domains[Xi].remove(x)
            removed = True
            print(f"   [RM] Xóa '{x}' khỏi Domain[{Xi}]  (Domain[{Xj}] = {domains[Xj]})")
    return removed


# AC-3: khởi tạo queue với tất cả cung, lặp đến khi queue rỗng
def ac3(domains):
    queue = deque()
    for Xi in graph:
        for Xj in graph[Xi]:
            queue.append((Xi, Xj))

    tong_cung = len(queue)
    buoc_co_thay_doi = 0
    tong_buoc = 0
    print(f"  Queue khởi tạo: {tong_cung} cung có hướng\n")

    while queue:
        (Xi, Xj) = queue.popleft()
        tong_buoc += 1

        if rm_inconsistent_values(Xi, Xj, domains):  # có giá trị bị xóa
            buoc_co_thay_doi += 1
            if not domains[Xi]:
                print(f"  [!] THẤT BẠI: Domain[{Xi}] rỗng!\n")
                return False
            # Thêm lại các cung (Xk, Xi) với Xk là hàng xóm của Xi
            for Xk in graph[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
                    print(f"   [+] Thêm cung ({Xk} --> {Xi}) vào queue")
            print(f"   => Domain[{Xi}] còn lại: {domains[Xi]}\n")

    print(f"  AC-3 hoàn tất: xét {tong_buoc} cung, có {buoc_co_thay_doi} cung làm thay đổi domain.")
    return True


# Backtracking kết hợp AC-3 lan truyền ràng buộc
def tim_huyen_chua_to(to_mau):
    for h in ds_huyen:
        if h not in to_mau:
            return h
    return None


def kiem_tra_hop_le(huyen, mau, to_mau):
    for lc in graph[huyen]:
        if lc in to_mau and to_mau[lc] == mau:
            return False
    return True


def backtrack(to_mau, domains, step):
    if len(to_mau) == len(ds_huyen):
        return to_mau

    huyen_xet = tim_huyen_chua_to(to_mau)
    if not huyen_xet:
        return None

    step[0] += 1
    print(f"\n[BT] Bước {step[0]}: {huyen_xet}  |  Domain = {domains[huyen_xet]}")

    for mau in list(domains[huyen_xet]):
        if kiem_tra_hop_le(huyen_xet, mau, to_mau):
            to_mau[huyen_xet] = mau
            print(f"  -> Gán {huyen_xet} = {mau}")

            backup = copy.deepcopy(domains)

            # AC-3 cục bộ sau khi gán: lan truyền ràng buộc tới hàng xóm
            local_queue = deque((lc, huyen_xet) for lc in graph[huyen_xet] if lc not in to_mau)
            ok = True
            while local_queue:
                (Xi, Xj) = local_queue.popleft()
                if rm_inconsistent_values(Xi, Xj, domains):
                    if not domains[Xi]:
                        ok = False
                        break
                    for Xk in graph[Xi]:
                        if Xk != Xj and Xk not in to_mau:
                            local_queue.append((Xk, Xi))

            if ok:
                result = backtrack(to_mau, domains, step)
                if result:
                    return result

            del to_mau[huyen_xet]
            domains.update(backup)
            print(f"  <- Quay lui: hủy {huyen_xet} = {mau}")
        else:
            print(f"  -> Bỏ qua '{mau}' (trùng màu hàng xóm)")

    return None


def chay():
    colors = ["Đỏ", "Xanh lá", "Xanh dương", "Vàng"]
    print("=" * 60)
    print("BÀI TÔ MÀU AN GIANG - THUẬT TOÁN AC-3")
    print(f"Bộ màu: {colors}")
    print("=" * 60)

    domains = {h: list(colors) for h in ds_huyen}

    print("\n--- GIAI ĐOẠN 1: AC-3 (thu hẹp miền giá trị) ---")
    if not ac3(domains):
        print("AC-3 phát hiện mâu thuẫn. Không có lời giải!")
        return

    print("\n--- Domain sau AC-3 ---")
    for h in ds_huyen:
        print(f"  {h}: {domains[h]}")

    if all(len(domains[h]) == 1 for h in ds_huyen):
        print("\n=> AC-3 thu hẹp hoàn toàn - lời giải trực tiếp:")
        for h in ds_huyen:
            print(f"   {h}: {domains[h][0]}")
        return

    print("\n--- GIAI ĐOẠN 2: Backtracking + AC-3 lan truyền ---")
    step = [0]
    result = backtrack({}, domains, step)

    print("\n" + "=" * 60)
    if result:
        print("=> TÔ MÀU THÀNH CÔNG!")
        print("=" * 60)
        for h, m in result.items():
            print(f"   {h}: {m}")
    else:
        print("=> THẤT BẠI!")


chay()

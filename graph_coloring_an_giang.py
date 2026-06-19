import copy

# Danh sach cac huyen/thi xa cua An Giang xua
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

# Ban do noi lien giua cac huyen
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

# Tinh toan bac lon nhat cua do thi de tim so mau toi da
max_d = 0
huyen_max_lc = ""
for h, lc in graph.items():
    if len(lc) > max_d:
        max_d = len(lc)
        huyen_max_lc = h

print("--- PHÂN TÍCH ĐỒ THỊ AN GIANG ---")
print(f"Tổng số huyện/thành phố: {len(ds_huyen)}")
print(f"Huyện có nhiều hàng xóm nhất: {huyen_max_lc} ({max_d} hàng xóm)")
print(f"Số màu tối đa cần dùng để luôn luôn tô được: {max_d + 1} màu")
print("Áp dụng định lý 4 màu cho đồ thị phẳng: chỉ cần 4 màu là đủ tô toàn bộ bản đồ")


# Tim huyen tiep theo chua duoc to mau
def tim_huyen_chua_to(to_mau):
    for h in ds_huyen:
        if h not in to_mau:
            return h
    return None

# Kiem tra xem co trung mau voi cac huyen ke ben da to hay chua
def kiem_tra_hop_le(huyen, mau, to_mau):
    for lc in graph[huyen]:
        if lc in to_mau and to_mau[lc] == mau:
            return False # bi trung mau
    return True

# Thuat toan de quy backtracking
def de_quy_to_mau(to_mau, m_mien, step, colors):
    if len(to_mau) == len(ds_huyen):
        return to_mau # da to xong het
        
    huyen_xet = tim_huyen_chua_to(to_mau)
    if not huyen_xet:
        return None
        
    step[0] += 1
    print(f"\nBước {step[0]}: Xét huyện {huyen_xet}")
    
    # Duyet qua cac mau con lai trong domain cua huyen nay
    for m in list(m_mien[huyen_xet]):
        print(f" - Thử tô màu {m} cho {huyen_xet}")
        
        if kiem_tra_hop_le(huyen_xet, m, to_mau):
            to_mau[huyen_xet] = m
            print(f"   -> Hợp lệ. Danh sách hiện tại: {to_mau}")
            
            # backup lai mien gia tri truoc khi forward check
            backup_mien = copy.deepcopy(m_mien)
            
            # Forward checking: xoa mau 'm' khoi cac huyen lan can chua to
            ok_fc = True
            print("   -> Cập nhật domain các huyện lân cận chưa gán màu:")
            for lc in graph[huyen_xet]:
                if lc not in to_mau:
                    if m in m_mien[lc]:
                        m_mien[lc].remove(m)
                        print(f"      + Miền giá trị của {lc} = {m_mien[lc]}")
                        if not m_mien[lc]:
                            ok_fc = False
                            print(f"      [!] Cảnh báo: Huyện {lc} bị hết màu để tô!")
            
            if ok_fc:
                kq = de_quy_to_mau(to_mau, m_mien, step, colors)
                if kq is not None:
                    return kq
            else:
                print("   -> Forward Checking thất bại! Phải quay lui thôi.")
                
            # Quay lui (backtrack) neu buoc tiep theo that bai
            print(f"   -> Quay lui: Hủy tô màu {m} của {huyen_xet}")
            del to_mau[huyen_xet]
            m_mien = backup_mien
        else:
            print(f"   -> Không hợp lệ! (Trùng màu {m} với huyện lân cận)")
            
    return None

# Ham chay tim kiem
def bat_dau_to_mau(colors):
    mien_gia_tri = {}
    for h in ds_huyen:
        mien_gia_tri[h] = list(colors)
        
    to_mau = {}
    buoc_dem = [0]
    
    print(f"\n=== CHẠY BACKTRACKING VỚI BỘ MÀU: {colors} ===")
    kq = de_quy_to_mau(to_mau, mien_gia_tri, buoc_dem, colors)
    
    if kq:
        print("\n=> TÔ MÀU THÀNH CÔNG!")
        for h, m in kq.items():
            print(f"   + {h}: {m}")
        return kq
    else:
        print("\n=> THẤT BẠI! Bộ màu này không đủ để tô màu bản đồ.")
        return None


# Thu chay voi 3 mau xem co duoc ko
colors_3 = ["Đỏ", "Xanh lá", "Xanh dương"]
kq_3 = bat_dau_to_mau(colors_3)

# Neu 3 mau fail thi thu 4 mau
if not kq_3:
    print("\n" + "="*50)
    print("Thử lại với 4 màu (Đỏ, Xanh lá, Xanh dương, Vàng)...")
    colors_4 = ["Đỏ", "Xanh lá", "Xanh dương", "Vàng"]
    kq_4 = bat_dau_to_mau(colors_4)

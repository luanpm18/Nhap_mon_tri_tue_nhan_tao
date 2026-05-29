# Trực Quan Hóa Các Thuật Toán Tìm Kiếm Áp Dụng Vào Bài Toán Máy Hút Bụi

## Giới thiệu
Project này mô phỏng và trực quan hóa quá trình hoạt động của các thuật toán tìm kiếm trong bài toán **Vacuum Cleaner Problem (Máy hút bụi)** thuộc lĩnh vực Trí tuệ nhân tạo (AI).

Chương trình cho phép người dùng:
- Tạo môi trường dạng ma trận
- Đặt vị trí máy hút bụi và các ô bẩn
- Quan sát trực tiếp cách các thuật toán tìm kiếm hoạt động
- So sánh hiệu quả giữa các thuật toán

Các thuật toán được áp dụng:
- BFS (Breadth-First Search)
- DFS (Depth-First Search)
- IDS (Iterative Deepening Search)
- UCS (Uniform Cost Search)

---

# Mục tiêu của project
- Hiểu cách hoạt động của các thuật toán tìm kiếm
- Minh họa trực quan quá trình duyệt trạng thái
- So sánh:
  - Số bước tìm kiếm
  - Đường đi tìm được
  - Hiệu suất của từng thuật toán

---

# Công nghệ sử dụng
- Ngôn ngữ: Python
- Giao diện: Tkinter
- Thuật toán AI Search

---

# Mô tả bài toán
Máy hút bụi hoạt động trong một môi trường dạng lưới gồm:
- Ô sạch
- Ô bẩn
- Vị trí bắt đầu của robot

Nhiệm vụ:
- Di chuyển qua các ô
- Hút sạch toàn bộ ô bẩn
- Tìm đường đi phù hợp dựa trên thuật toán tìm kiếm

Các hành động:
- Di chuyển lên
- Di chuyển xuống
- Di chuyển trái
- Di chuyển phải
- Hút bụi tại vị trí hiện tại


# Các thuật toán được sử dụng

## 1. BFS (Breadth-First Search)
- Duyệt theo chiều rộng
- Đảm bảo tìm được lời giải ngắn nhất nếu chi phí bằng nhau
- Tốn nhiều bộ nhớ

## 2. DFS (Depth-First Search)
- Duyệt theo chiều sâu
- Tốn ít bộ nhớ hơn BFS
- Không đảm bảo lời giải tối ưu

## 3. IDS (Iterative Deepening Search)
- Kết hợp ưu điểm của BFS và DFS
- Duyệt sâu dần theo từng mức depth
- Tìm được lời giải tối ưu với chi phí bộ nhớ thấp hơn BFS

## 4. UCS (Uniform Cost Search)
- Mở rộng node có chi phí nhỏ nhất trước
- Đảm bảo tìm được đường đi tối ưu
- Hoạt động tốt khi các hành động có chi phí khác nhau
- cost được tính bằng cách nếu đi vào ô sạch thì new_cost = cost_parent + 3, ngược lại new_cost = cost_parent + 1


# Chức năng chính
- Tạo ma trận môi trường
- Sinh ngẫu nhiên ô bẩn
- Chọn thuật toán cần chạy
- Hiển thị quá trình tìm kiếm theo thời gian thực
- Hiển thị:
  - Frontier
  - Reached
  - Đường đi kết quả
  - Số bước thực hiện


# Cách chạy chương trình


# Minh họa hoạt động
- Robot sẽ di chuyển trên ma trận
- Các ô đã duyệt sẽ được đánh dấu
- Khi tìm được lời giải, chương trình hiển thị:
  - Đường đi cuối cùng
  - Tổng số bước
  - Trạng thái sạch hoàn toàn

---

# Kiến thức áp dụng
Project áp dụng các kiến thức:
- Artificial Intelligence
- Search Algorithms
- State Space Search
- Data Structures:
  - Queue
  - Stack
  - Priority Queue
- GUI Programming với Tkinter

# Hướng phát triển
- Thêm thuật toán A*
- Thêm Greedy Best First Search
- Tối ưu giao diện
- So sánh thời gian chạy giữa các thuật toán
- Xuất thống kê kết quả

# Tác giả
Project được thực hiện nhằm mục đích học tập và nghiên cứu về:
- Trí tuệ nhân tạo
- Thuật toán tìm kiếm
- Trực quan hóa thuật toán bằng Python

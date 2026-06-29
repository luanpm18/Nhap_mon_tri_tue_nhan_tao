# Bài Tập Về Nhà - Môn Nhập Môn Trí Tuệ Nhân Tạo

Chào mừng đến với kho lưu trữ (repository) bài tập về nhà môn Nhập môn Trí tuệ Nhân tạo của mình. Dự án này tập trung vào việc mô phỏng và giải quyết bài toán **"Robot máy hút bụi thông minh"** ngoài ra còn có tô màu bản đồ và Tic Tac Toe thông qua việc triển khai các nhóm thuật toán tìm kiếm từ cơ bản đến nâng cao, đi kèm với một công cụ trực quan hóa (Visualizer) sinh động.

---

## 🎯 Mục Tiêu Của Project

* **Hiểu sâu lý thuyết:** Nắm vững nguyên lý hoạt động, cơ chế duyệt cây/đồ thị trạng thái của các thuật toán tìm kiếm trong AI.
* **Minh họa trực quan:** Trực quan hóa quá trình duyệt trạng thái trên không gian ma trận theo thời gian thực để dễ dàng quan sát cách các thuật toán hoạt động.
* **So sánh và Đánh giá hiệu suất:** Đưa ra cái nhìn khách quan về hiệu quả của từng thuật toán dựa trên 3 tiêu chí cốt lõi:
  * **Số bước tìm kiếm:** Tổng số trạng thái đã duyệt (độ phức tạp không gian/thời gian thực tế).
  * **Đường đi tìm được:** Chiều dài hoặc chi phí của lời giải tìm được (tính tối ưu).
  * **Hiệu suất tổng thể:** Tốc độ thực thi và khả năng phân bổ bộ nhớ của từng thuật toán.

---

## 📝 Mô Tả Bài Toán

Bài toán mô phỏng một Robot máy hút bụi hoạt động trong một môi trường không gian dạng lưới (Ma trận kích thước **4x4**), bao gồm các thành phần:
* **Ô sạch (Clean):** Đường đi trống mà robot có thể di chuyển qua.
* **Ô bẩn (Dirty):** Vị trí chứa rác cần được dọn dẹp.
* **Vị trí bắt đầu (Start):** Tọa độ xuất phát ban đầu của Robot.

### Nhiệm vụ của Robot:
1. Di chuyển thông minh qua các ô trong ma trận lưới.
2. Hút sạch toàn bộ các ô bẩn xuất hiện trong môi trường.
3. Tìm ra chuỗi đường đi phù hợp và tối ưu nhất dựa trên thuật toán tìm kiếm được lựa chọn.

### Các hành động (Actions) có thể thực hiện:
* **Di chuyển lên (Up)**
* **Di chuyển xuống (Down)**
* **Di chuyển trái (Left)**
* **Di chuyển phải (Right)**
* **Hút bụi (Suck):** Thực hiện tại vị trí hiện tại nếu ô đó có vết bẩn.

---

## 🧠 Các Thuật Toán Đã Triển Khai

Hệ thống triển khai đa dạng các chiến lược tìm kiếm từ cơ bản (mù) cho đến nâng cao (có thông tin và môi trường phức tạp):

### 1. Nhóm thuật toán tìm kiếm mù (Uninformed Search)
Phù hợp khi robot không có thông tin về khoảng cách hay chi phí tới mục tiêu:
* **BFS (Breadth-First Search):** Tìm kiếm theo chiều rộng, bảo đảm tìm thấy đường đi ngắn nhất (khi chi phí các bước bằng nhau).
* **DFS (Depth-First Search):** Tìm kiếm theo chiều sâu, tiết kiệm bộ nhớ nhưng không đảm bảo tìm được đường đi tối ưu.
* **IDS (Iterative Deepening Search):** Tìm kiếm sâu dần, kết hợp ưu điểm tiết kiệm bộ nhớ của DFS và tính tối ưu của BFS.
* **UCS (Uniform Cost Search):** Tìm kiếm với chi phí đồng đều, tối ưu khi chi phí di chuyển giữa các ô có sự khác biệt.

### 2. Nhóm thuật toán tìm kiếm có thông tin (Informed Search)
Sử dụng hàm Heuristic (ước lượng toán học) để tối ưu hóa và tăng tốc độ tìm kiếm:
* **Greedy Best-First Search:** Tìm kiếm tham lam, luôn ưu tiên chọn trạng thái có vẻ gần mục tiêu nhất dựa trên hàm Heuristic.
* **A\* Search:** Thuật toán tìm kiếm tối ưu phổ biến, kết hợp chi phí thực tế từ điểm đầu $g(n)$ và chi phí ước lượng đến đích $h(n)$.
* **IDA\* (Iterative Deepening A\*):** Phiên bản cải tiến nâng cấp từ A\*, giúp tối ưu hóa không gian bộ nhớ bằng cách duyệt sâu dần kết hợp giới hạn chi phí.

### 3. Nhóm thuật toán leo đồi (Hill Climbing)
Các thuật toán tìm kiếm cục bộ dựa trên việc liên tục di chuyển về phía có trạng thái tốt hơn:
* **Basic Hill Climbing:** Leo đồi cơ bản.
* **Steepest-Ascent Hill Climbing:** Leo đồi dốc nhất (đánh giá toàn bộ các trạng thái lân cận và chỉ chọn trạng thái tối ưu nhất).
* **Stochastic Hill Climbing:** Leo đồi ngẫu nhiên (chọn ngẫu nhiên một trong số các hướng đi tốt hơn hướng hiện tại).
* **Random-Restart Hill Climbing:** Leo đồi khởi tạo ngẫu nhiên (tự động thiết lập lại vị trí ban đầu ngẫu nhiên nếu rơi vào cực trị cục bộ để tiếp tục tìm kiếm giải pháp toàn cục).

### 4. Nhóm Tìm kiếm Mù (Uninformed Search)
Phù hợp khi tác nhân không có thông tin về khoảng cách hay chi phí tới mục tiêu:
* **Senseless:** Chiến lược duyệt mù khi không có thông tin định hướng.
* **Partial:** Tìm kiếm trong môi trường thông tin không đầy đủ.
* **And/Or Search:** Giải quyết các bài toán có sự lựa chọn giữa các hành động của tác nhân và sự biến đổi của môi trường.

### 5. Nhóm Ràng buộc (CSP - Constraint Satisfaction Problems)
Giải quyết các bài toán thỏa mãn ràng buộc bằng cách gán giá trị cho các biến sao cho không vi phạm quy tắc:
* **Backtracking:** Thuật toán quay lui cơ bản.
* **Forward Checking:** Kiểm tra khả năng vi phạm ràng buộc ngay tại bước gán giá trị hiện tại.
* **Min-conflict:** Thuật toán tìm kiếm cục bộ tối ưu hóa cho các bài toán CSP quy mô lớn.

### 6. Nhóm Đối kháng (Adversarial Search)
Giải quyết các bài toán trò chơi có đối thủ (Zero-sum game):
* **Minimax:** Thuật toán tối ưu cho trò chơi có đối thủ hoàn hảo.
* **Alpha-Beta Pruning:** Kỹ thuật cắt tỉa giúp giảm số lượng nút cần duyệt trong Minimax.
* **Expectimax:** Mở rộng cho các trò chơi có yếu tố ngẫu nhiên (may rủi).

---

## 💻 Công Nghệ Sử Dụng

* **Ngôn ngữ lập trình:** Python
* **Thư viện giao diện:** Tkinter (Thư viện tích hợp sẵn của Python giúp xây dựng GUI trực quan nhẹ nhàng, mượt mà).
* **Thuật toán cốt lõi:** AI Search Algorithms (Triển khai logic thuật toán thuần túy).

---

## 📸 Demo & Trực Quan Hóa (Visualizer)

Hệ thống sử dụng không gian mô phỏng ma trận **4x4** bằng Tkinter. Bạn có thể dễ dàng theo dõi từng bước chân của robot, các ô đang được duyệt, cũng như quá trình dọn sạch bụi bẩn trên bản đồ.

### Video Minh Họa Hoạt Động
1. Dưới đây là video ghi lại quá trình vận hành trực quan của các thuật toán:

<img width="800" height="449" alt="angghi2026-06-18225810-ezgif com-video-to-gif-converter" src="https://github.com/user-attachments/assets/09d08488-1d26-48e2-8f88-3509965e1735" />

2. Bài toán Tô màu tỉnh An Giang (CSP)
Mô phỏng việc tô màu bản đồ hành chính tỉnh An Giang sao cho không có hai huyện/thành phố nào kề nhau có cùng màu.


<img width="800" height="450" alt="Video Project 1" src="https://github.com/user-attachments/assets/c02afd13-1f1b-4ab0-be55-daa26f576c28" />


3. Trò chơi Caro (Đối kháng)
Robot thi đấu với người chơi dựa trên các thuật toán đối kháng để tìm nước đi tốt nhất.

<img width="800" height="450" alt="Đang ghi 2026-06-28 100843" src="https://github.com/user-attachments/assets/4d87dc8f-2339-495f-8267-3dd767693590" />




---

## 🛠️ Hướng Dẫn Cài Đặt và Chạy Chương Trình

1. **Clone repository về máy local:**
   Chạy file visualizer.ipynb sau đó nhập vào ma trận 4x4

   Chạy file graph_coloring_backtracking_foward.py

   Chạy minimax_alpha-beta_expectimax.py

Một ứng dụng trò chơi caro tương tác với trí tuệ nhân tạo

Ứng dụng được phát triển nhằm phục vụ mục đích học tập và nghiên cứu các thuật toán trong trò chơi, đặc biệt là các kỹ thuật tìm kiếm trong cây trạng thái và tối ưu hóa quyết định của AI.

Tính năng chính
Chế độ trò chơi
Chế độ Dễ: Sử dụng thuật toán Minimax thuần túy
Chế độ Trung bình: Sử dụng Alpha-Beta Pruning
Chế độ Khó: Alpha-Beta Pruning kết hợp heuristic lựa chọn nước đi thông minh
Chế độ Huấn luyện: Chế độ luyện tập giúp người chơi nâng cao kỹ năng
Giao diện
Bàn cờ 15x15 theo tiêu chuẩn trò chơi caro
Giao diện phong cách Cyberpunk hiện đại
Robot AI tương tác với người chơi thông qua bong bóng hội thoại
Hiệu ứng trạng thái robot thay đổi (bình thường, chiến thắng, thua cuộc)
Dòng chữ chạy khi kết thúc ván đấu
Hỗ trợ hai ngôn ngữ: Tiếng Việt và Tiếng Anh
Tính năng nâng cao
Hoàn tác (Undo) nước đi
Làm lại (Redo) nước đi
Hiển thị telemetry của AI (điểm đánh giá, độ sâu tìm kiếm, số nút duyệt, thời gian thực thi)
Chức năng đầu hàng trong trận đấu
Cấu trúc dự án
main.py

File chính chứa lớp AgentCaro – chịu trách nhiệm quản lý giao diện người dùng và luồng trò chơi.

Xử lý sự kiện chuột người chơi: tiếp nhận tọa độ click, ánh xạ chính xác từ vị trí pixel trên màn hình sang chỉ số hàng/cột trong ma trận bàn cờ.
Vẽ bàn cờ và các thành phần giao diện: vận hành vòng lặp render của Pygame để hiển thị lưới bàn cờ, quân X/O hiệu ứng Neon, bảng thông số thời gian thực và bong bóng hội thoại của Robot.
Quản lý trạng thái trò chơi (Menu, Chọn mức độ, Chơi, ...): xây dựng cơ chế máy trạng thái hữu hạn (Finite State Machine) để điều phối luồng từ màn hình khởi động đến các màn hình chức năng.
Lưu lịch sử nước đi hỗ trợ Undo/Redo: sử dụng cấu trúc dữ liệu dạng danh sách/ngăn xếp để lưu snapshot bàn cờ sau mỗi lượt đi, cho phép truy xuất lại trạng thái trước đó một cách chính xác.
ai.py

File chứa lớp AIEngine – triển khai toàn bộ logic trí tuệ nhân tạo dựa trên mô hình cây quyết định.

Kiểm tra điều kiện kết thúc (4 quân liên tiếp): sử dụng thuật toán quét ma trận theo 4 hướng (ngang, dọc, chéo chính, chéo phụ) để xác định trạng thái kết thúc ngay sau mỗi nước đi.
Đánh giá trạng thái bàn cờ dựa trên mẫu chiến thuật: áp dụng hàm heuristic tại các nút lá để chấm điểm cấu hình hiện tại thông qua kỹ thuật nhận diện mẫu (pattern matching).
Lọc nước đi cục bộ để thu hẹp không gian tìm kiếm: sử dụng hàm get_local_moves nhằm chỉ xét các ô trống trong phạm vi lân cận 2 ô quanh quân cờ, giúp giảm mạnh số nhánh của cây tìm kiếm.
Các thuật toán:
Pure Minimax: dùng cho chế độ Dễ, duyệt đệ quy cây trạng thái theo chiều sâu cố định. Tại nút MAX, AI chọn giá trị lớn nhất; tại nút MIN, giả lập người chơi chọn giá trị nhỏ nhất. Thuật toán không có cơ chế cắt tỉa nên phải duyệt toàn bộ nhánh.
Alpha-Beta Pruning: dùng cho chế độ Trung bình và Khó. Dựa trên hai giá trị biên alpha (giới hạn dưới của MAX) và beta (giới hạn trên của MIN). Khi phát hiện điều kiện alpha beta, thuật toán dừng mở rộng nhánh vì không còn giá trị tối ưu.
Move Ordering Heuristic: dùng trong chế độ Khó. Các nước đi được đánh giá sơ bộ và sắp xếp giảm dần theo mức độ tiềm năng trước khi duyệt, giúp tăng khả năng cắt tỉa sớm và tối ưu hiệu năng tìm kiếm.
config.py

File cấu hình hệ thống

Kích thước cửa sổ: 1100x720 pixels
Kích thước bàn cờ: 15x15 ô
Bảng màu thiết kế theo phong cách Cyberpunk
Hệ thống từ điển hỗ trợ hai ngôn ngữ
Yêu cầu hệ thống
Python 3.6 trở lên
Thư viện Pygame (phục vụ giao diện đồ họa)
Bộ hình ảnh robot (robot_normal.png, robot_win.png, robot_lose.png)
Cách chơi
Khởi động ứng dụng và chọn “BẮT ĐẦU CHƠI” hoặc “CHẾ ĐỘ TẬP SỰ”
Lựa chọn mức độ khó (Dễ, Trung bình, Khó)
Người chơi nhấp chuột vào bàn cờ để đặt quân X
AI thực hiện tính toán và đặt quân O
Người chơi thắng khi có 4 quân X liên tiếp theo hàng ngang, dọc hoặc chéo
AI thắng khi đạt 4 quân O liên tiếp
Trò chơi hòa khi bàn cờ được lấp đầy mà không có bên thắng
Đặc điểm kỹ thuật
Chiến lược AI
Nguyên lý đánh giá thế cờ: do không gian trạng thái của caro là rất lớn, AI sử dụng hàm lượng giá để ước lượng tại độ sâu giới hạn. Hàm điểm tổng quát được tính theo:
$E(s) = sum Score_{AI} - sum Score_{Player}$
Trọng số tấn công (AI - quân O): ưu tiên các cấu hình mang tính chủ động như:
OOOO → +100,000 điểm
.OOO. → +5,000 điểm
.OO. → +100 điểm
Trọng số phòng thủ (người chơi - quân X): chặn các thế nguy hiểm với điểm phạt lớn:
XXXX → -80,000 điểm
.XXX. → -4,000 điểm
Ưu tiên heuristic: khuyến khích chọn các vị trí gần trung tâm bàn cờ (ô 7,7), do đây là khu vực có nhiều hướng mở chiến thuật nhất.
Cơ chế cân bằng tấn công – phòng thủ: AI liên tục điều chỉnh chiến lược giữa xây dựng thế và chặn đòn tùy theo tình huống trên bàn cờ.
Hiệu năng
Chế độ Dễ: Minimax độ sâu 2, tối đa 6 nước đi. Không gian tìm kiếm được giới hạn nhằm kiểm soát độ phức tạp $O(b^d)$.
Chế độ Trung bình: Alpha-Beta độ sâu 2, tối đa 12 nước đi. Nhờ cắt tỉa alpha-beta, số nút duyệt giảm đáng kể so với Minimax.
Chế độ Khó: Alpha-Beta độ sâu 3 kết hợp Move Ordering, tối đa 8 nước đi mạnh nhất. Nhờ sắp xếp tối ưu, điều kiện cắt tỉa xảy ra sớm giúp giảm đáng kể số trạng thái phải duyệt, đưa độ phức tạp tiệm cận $O(b^{d/2})$.
Hệ thống Telemetry

Hệ thống hiển thị thông tin chi tiết mỗi nước đi của AI phục vụ phân tích và nghiên cứu:

Thuật toán sử dụng: Minimax, Alpha-Beta hoặc Alpha-Beta (Heuristic)
Nước đi được chọn: tọa độ dạng (hàng, cột)
Điểm đánh giá: giá trị từ hàm heuristic tại nút gốc
Độ sâu tìm kiếm: mức giới hạn của cây (depth = 2 hoặc 3)
Số trạng thái đã duyệt: số node thực tế trong quá trình tìm kiếm
Thời gian thực thi: thời gian tính toán (ms) từ lúc bắt đầu đến khi ra quyết định

## Tác giả

* Trịnh Quang Năng
* Dự án học tập về các thuật toán trò chơi AI (Minimax, Alpha-Beta Pruning)
Một ứng dụng trò chơi caro tương tác với trí tuệ nhân tạo

Ứng dụng được phát triển nhằm phục vụ mục đích học tập và nghiên cứu các thuật toán trong trò chơi, đặc biệt là các kỹ thuật tìm kiếm trong cây trạng thái và tối ưu hóa quyết định của AI.
Tính năng chính
Chế độ trò chơi
Chế độ Dễ: Sử dụng thuật toán Minimax thuần túy
Chế độ Trung bình: Sử dụng Alpha-Beta Pruning
Chế độ khó: Alpha-Beta Pruning kết hợp heuristic lựa chọn nước đi thông minh
Giao diện
Bàn cờ 15x15 theo tiêu chuẩn trò chơi caro
Giao diện đơn giản
Dòng chữ chạy khi kết thúc ván đấu
Hỗ trợ ngôn ngữ: Tiếng Anh
Tính năng nâng cao
Hoàn tác (Undo) nước đi
Làm lại (Redo) nước đi
Hiển thị telemetry của AI (điểm đánh giá, độ sâu tìm kiếm, số nút duyệt, thời gian thực thi)
Chức năng đầu hàng trong trận đấu

Cấu trúc dự án:
* main.py
Quản lý giao diện người dùng và luồng trò chơi:
1.Khởi Tạo Môi Trường Trò Chơi (Game Initialization)
2.Quản Lý Vòng Lặp Trò Chơi Thao Tác Thời Gian Thực (Game Loop)
3.Đầu Mối Kích Hoạt Và Chuyển Đổi Thuật Toán
4.Kiểm Soát Hiệu Năng Và Đảm Bảo Tiêu Chuẩn Thời Gian Thực
5.Cập Nhật Đồ Họa Và Giao Diện Người Dùng
6.Phân Định Thắng Thua

* ai.py
xử lý tất cả logic AI dựa trên nền tảng toán học cây quyết định
1.Cốt Lõi Của Hai Giải Thuật Tìm Kiếm (Minimax & Alpha-Beta)
2.Kiểm Soát Bùng Nổ Tổ Hợp Bằng Hàm Sinh Nước Đi
3.Định Hình "Trí Thông Minh" Của AI Qua Hàm Đánh Giá
4.Quản Lý Các Cấp Độ Khó (Difficulty Levels) và Độ Sâu Tìm Kiếm (Depth)
5.Cô Lập Logic Tính Toán
* config.py
File cấu hình hệ thống
Kích thước cửa sổ: 1100x720 pixels
Kích thước bàn cờ: 15x15 ô
1.Quản Lý Các Hằng Số Thuật Toán AI
2.Thiết Lập Quy Chuẩn Bàn Cờ Và Luật Chơi
3.Quản Lý Cấu Hình Giao Diện Và Đồ Họa
4.Quản Lý Điểm Số Của Hàm Đánh Giá
5.Tách Biệt Cấu Hình Với Logic Nghiệp Vụ

Yêu cầu hệ thống:
Python 3.13
Pygame (library vẽ giao diện)

Cách chơi	
1.Mở file main.py và Run
2.chọn "Play"
3.Chọn mức độ khó
4.Nhấp vào bàn cờ để đặt quân X
5.AI sẽ tư duy và đặt quân O
6.Người chơi thắng khi có 4 quân X liên tiếp (ngang, dọc, chéo)
7.AI thắng khi có 4 quân O liên tiếp
8.Ván hòa khi bàn cờ đầy mà không ai thắng

CHIẾN LƯỢC AI 
1. Nguyên Lý Đánh Giá Thế Cờ (Heuristic Engine)
Vì không gian trạng thái của trò chơi Caro vô cùng lớn, AI không thể
duyệt đến tận cùng ván đấu. Do đó, tại độ sâu giới hạn của cây quyết
định, AI sử dụng một hàm lượng giá để ước lượng điểm số của thế cờ
hiện tại.
Công thức tính điểm tổng quát:
Điểm số = Tổng điểm của AI (Quân O) - Tổng điểm của Người chơi (Quân X)

Hệ thống phân tầng điểm số được thiết lập bất đối xứng và đặt nặng tính
phòng ngự để ngăn chặn tối đa các nước cờ hiểm của con người:
* Chuỗi OOOO (AI đạt chuỗi quyết định thắng ván cờ): Cộng 1,000,000 điểm.
* Chuỗi XXXX (Đối thủ sắp thắng, mức độ nguy cấp cao nhất): Trừ 900,000 điểm.
  (Mức phạt này cực cao để ép AI bắt buộc phải đi chặn nước cờ của đối
  thủ thay vì lo tấn công).
* Chuỗi .XXX. (Đối thủ có chuỗi 3 mở hai đầu rất nguy hiểm): Trừ 75,000 điểm.
* Chuỗi .OOO. (AI tạo được thế chuỗi 3 mở hai đầu để chuẩn bị tấn công): Cộng 50,000 điểm.
* Chuỗi XXX. hoặc .XXX (Chuỗi 3 bị chặn một đầu của đối thủ): Trừ 15,000 điểm.
* Chuỗi OOO. hoặc .OOO (Chuỗi 3 bị chặn một đầu của AI): Cộng 5,000 điểm.
* Chuỗi .XX. (Chuỗi 2 quân mở của đối thủ): Trừ 3,500 điểm.
* Chuỗi .OO. (Chuỗi 2 quân mở của AI): Cộng 1,500 điểm.

Bên cạnh các mẫu chiến thuật, AI còn áp dụng Heuristic vị trí: Các ô cờ
càng nằm gần khu vực trung tâm bàn cờ (tọa độ index 7,7) sẽ được cộng
thêm điểm thưởng. Điều này thúc đẩy AI chủ động tranh chấp và kiểm soát
khu vực trung tâm ngay từ đầu trận đấu.

2. Bộ Lọc Thu Hẹp Không Gian Tìm Kiếm (Move Ordering)
Bàn cờ có tới 225 ô trống, nếu xét tất cả thì máy sẽ bị tràn bộ nhớ
hoặc xử lý rất chậm. Để tối ưu, AI sử dụng hàm quét lân cận (Moore
Neighborhood). Nó chi tìm và xem xét các ô trống nằm trong phạm vi ngay
sát cạnh các quân cờ đã được đánh trên bàn cờ.
Sau khi lọc được các ô trống tiềm năng, AI áp dụng hàm tính điểm chiến
thuật nhanh cho tung ô rồi thực hiện sắp xếp chúng theo thứ tự từ mạnh
đến yếu. Việc đưa các nước đi nguy hiểm hoặc có khả năng tấn công mạnh
lên đầu danh sách giúp cho thuật toán cắt tỉa nhánh diễn ra sớm hơn,
tiết kiệm tối đa tài nguyên tính toán.

3. Chiến Lược Thuật Toán Theo Cấp Độ
Tùy thuộc vào cấp độ khó do người chơi lựa chọn, bộ não AI sẽ thay đổi
thuật toán và độ sâu tìm kiếm tương ứng:
* Chế độ DỄ (EASY): AI sử dụng thuật toán Pure Minimax thuần túy với độ
  sâu duyệt giới hạn là 2 tầng. Phạm vi tìm kiếm bị giới hạn chặt chẽ
  (chỉ xét tối đa 6 nước đi tiềm năng nhất tại mỗi bước) để giảm tải và
  giữ cho trình độ của máy ở mức vừa phải, phù hợp cho người mới chơi.
* Chế độ TRUNG BÌNH (NORMAL): AI nâng độ sâu tìm kiếm lên 3 tầng. Thuật
  toán được đổi sang Alpha-Beta Pruning kết hợp sắp xếp nước đi. Số lượng
  nước đi tiềm năng mở rộng lên tối đa 12 nước. Nhờ khả năng cắt tỉa các
  nhánh không hiệu quả, AI tính sâu hơn nhưng vẫn đảm bảo tốc độ phản xạ nhanh.
* Chế độ KHÓ (HARD): Đây là cấp độ thông minh nhất của máy. AI vận hành
  thuật toán Alpha-Beta Pruning được tối ưu hóa chuyên sâu bằng Bảng
  chuyển vị (Transposition Table) kết hợp thuật toán băm Zobrist Hashing
  và sắp xếp nước đi. Đo sâu tìm kiếm đạt đến 4 tầng và không gian xét
  mở rộng lên 14 nước đi mạnh nhất.

4. Cơ Chế Tối Ưu Bộ Nhớ (Zobrist Hashing và Cache)
Điểm đặc biệt trong chiến lược của AI ở cấp độ Khó là khả năng ghi nhớ.
Hệ thống khởi tạo một bảng băm ngẫu nhiên 64-bit cho từng ô cờ và loại
quân. Khi người chơi và AI luân phiên hạ quân, thuật toán sẽ đồng bộ hóa
cấu trúc bàn cờ thông qua toán tử XOR để tạo ra một mã băm duy nhất cho
thế cờ đó.
Mã băm này được dùng làm chìa khóa lưu trữ vào Bảng chuyển vị (Transposition
Table) đóng vai trò như bộ nhớ đệm (Cache). Khi gặp lại một thế cờ đã từng
tính toán trước đó (ví dụ trường hợp hoán vị nước đi: đi ô A trước ô B hay
ô B trước ô A đều cho ra cùng kết quả), AI sẽ đọc ngay điểm số từ bộ nhớ
Cache thay vì phải thực hiện đệ quy duyệt lại từ đầu. Cơ chế này giúp AI có
thể nhìn xa tới 4 nước cờ mà thời gian xử lý vẫn diễn ra gần như tức thì.
## Tác giả
* Trịnh Quang Năng
* Dự án học tập về các thuật toán trò chơi AI (Minimax, Alpha-Beta Pruning)

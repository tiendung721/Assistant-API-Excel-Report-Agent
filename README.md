# Assistant-API-Excel-Report-Agent

Chương trình này xây dựng một AI Agent hoàn chỉnh sử dụng OpenAI Assistant API v2 để:

Phân tích file Excel không định dạng cố định

Tự động nhận diện các vùng dữ liệu

Giao tiếp phản hồi với người dùng để cải thiện

Sinh ra báo cáo tổng hợp bằng tiếng Việt theo định dạng chuyên nghiệp

📁 Cấu trúc thư mục

├── assistant_config.py              # Khởi tạo Assistant IDs và lưu vào file
├── extractor_assistant.py          # Tách section từ file Excel và giao tiếp phản hồi
├── extractor_memory.py             # Hệ thống ghi nhớ góp ý từ người dùng theo header
├── analyzer_assistant.py           # Phân tích nội dung từng vùng và sinh thống kê
├── planner_assistant.py            # Sinh báo cáo tổng hợp từ kết quả phân tích
├── main.py                         # Chương trình điều phối toàn bộ quá trình
├── .env                            # API key OpenAI
├── assistant_ids.json              # File lưu Assistant ID sau khi tạo
└── output/
    ├── extracted_sections.json         # Các vùng dữ liệu đã chia
    ├── analysis_result_interactive.json# Kết quả phân tích chi tiết
    └── final_report.txt                # Báo cáo tiếng Việt cuối cùng
    
⚙️ Cài đặt
Cài thư viện:

bash
Sao chép
Chỉnh sửa
pip install openai pandas python-dotenv
Tạo file .env với nội dung:

env
Sao chép
Chỉnh sửa
OPENAI_API_KEY=sk-xxxx

🚀 Hướng dẫn sử dụng

Bước 1: Tạo Assistant
Chạy một lần:

python assistant_config.py
→ Tạo ra 3 assistant: section_classifier, analyzer, planner và lưu assistant_ids.json.

Bước 2: Chạy chương trình chính

python main.py
Luồng hoạt động:

📂 Nhập file Excel

📌 Tự động chia vùng dữ liệu

User góp ý nếu cần → chương trình ghi nhớ góp ý

Nếu user agree, kết quả sẽ được lưu lại

📊 Phân tích từng vùng dữ liệu

Assistant gợi ý group_by (chiều phân tích chính)

User có thể xác nhận hoặc chọn lại chiều khác

📝 Sinh báo cáo tổng hợp

Dạng tiếng Việt, đầy đủ các phần: Tổng quan, Thống kê, Nhận định, Đề xuất

Ghi ra file final_report.txt

📌 Kết quả đầu ra

output/extracted_sections.json: Các vùng dữ liệu đã chia tự động từ file Excel
output/analysis_result_interactive.json :	Kết quả phân tích chi tiết từng section
output/final_report.txt	: Báo cáo tổng hợp tiếng Việt chuẩn chuyên nghiệp

🧠 Cơ chế học hỏi (Memory)
Mỗi góp ý của người dùng về section sẽ được lưu lại theo headers fingerprint.

Lần sau gặp bảng có header tương tự → assistant tự đề xuất thông minh hơn.

Nếu người dùng chọn agree, chương trình sẽ ghi lại thread_id để duy trì logic.

📚 Ví dụ định dạng báo cáo sinh ra

🔹 Khu vực: Region_1
Chiều phân tích chính: Ghi chú

1. Tổng quan dữ liệu
Dữ liệu cho thấy nhóm lò Lò 1,2,3 có thời gian dừng lò cao nhất...

2. Chi tiết thống kê
Ghi chú              | Tổng thời gian | Tần suất
Lò 1, Lò 2, Lò 3     | 31.5            | 4
Lò 8, Lò 9, Lò 10    | 16.5            | 4
...

3. Nhận định
Nhóm lò Lò 1,2,3 là nơi gặp sự cố nhiều nhất...

4. Đề xuất
Cần ưu tiên kiểm tra nhóm lò Lò 1–3 và theo dõi thêm lò 9...

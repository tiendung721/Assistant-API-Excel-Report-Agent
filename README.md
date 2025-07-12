
#  Tổng quan về Assistants API (2024–2025)

##  1. Assistants API là gì?

Assistants API là một giao diện lập trình ứng dụng (API) của OpenAI cho phép bạn xây dựng các **AI Assistant chuyên biệt**, hoạt động trực tiếp trong ứng dụng của bạn. Mỗi Assistant có thể:

-  Gọi các mô hình GPT tùy chọn (GPT-4, GPT-4o, GPT-3.5, v.v.)
-  Kết hợp với các công cụ nội bộ như:
  - `code_interpreter` – chạy Python
  - `file_search` – tìm kiếm file
  - `function_calling` – gọi hàm backend
-  Nhận và xử lý file do người dùng tải lên (Excel, PDF, CSV…)
-  Ghi nhớ lịch sử hội thoại (qua đối tượng `Thread`)

>  **Lưu ý:** Assistants API hiện đang ở giai đoạn Beta và sẽ **dần được thay thế** bởi một hệ thống mới là **Responses API**.  
> OpenAI dự kiến sẽ **ngưng hỗ trợ Assistants API vào giữa năm 2026**.

---

##  2. Các công cụ hỗ trợ (Tools)

| Công cụ             | Mô tả                                                                 |
|---------------------|----------------------------------------------------------------------|
|  `code_interpreter` | Chạy mã Python: phân tích dữ liệu, đọc Excel, sinh biểu đồ…          |
|  `file_search`      | Tìm kiếm văn bản trong file đã upload (PDF, CSV, Markdown…)         |
|  `function_calling` | Gọi các hàm backend bạn định nghĩa (API nội bộ, truy vấn database…) |

> ✅ Bạn có thể **kích hoạt nhiều công cụ cùng lúc** cho một Assistant.

---

##  3. Cách hoạt động của Assistants API

| Thành phần | Vai trò |
|------------|--------|
| **Assistant** | Bạn cấu hình assistant như một nhân vật AI: tên, hướng dẫn, model, tools |
| **Thread** | Một phiên hội thoại – lưu trữ lịch sử tin nhắn giữa user và assistant |
| **Message** | Một tin nhắn trong hội thoại – gồm nội dung văn bản hoặc file |
| **Run** | Một phiên assistant xử lý toàn bộ hội thoại để trả lời yêu cầu mới |
| **Run Step** | Từng bước assistant đã thực hiện trong một Run (hữu ích để debug) |

---

##  4. Các tính năng nổi bật

| Tính năng                   | Ý nghĩa |
|-----------------------------|--------|
| `Persistent Threads`     | Assistant nhớ toàn bộ hội thoại trước đó → cho phép hỏi tiếp nối |
| `Auto Truncation`        | Khi quá dài, assistant sẽ tự cắt ngữ cảnh phù hợp |
| `File input/output`      | Assistant có thể đọc file và sinh file mới (CSV, Excel, PNG…) |
| `Multi-tool integration` | Assistant có thể đồng thời chạy Python, gọi API và tìm kiếm file |
| `Run tracking`           | Bạn có thể kiểm tra từng bước Assistant thực hiện trong quá trình xử lý |

---

##  Kiến trúc tổng thể (mô hình luồng xử lý)

<img width="1360" height="453" alt="image" src="https://github.com/user-attachments/assets/d2d56d02-ff03-4e19-a060-1f6928fb392a" />


```
[Assistant]
     ↓
[Thread] ←→ [Message]
     ↓
    [Run] → [Run Step] → Tool / Output
```

---

####  Lưu ý 

- Nên chuẩn bị dần kế hoạch chuyển sang **Responses API**
- Tối ưu cấu trúc hội thoại để tránh giới hạn token trong `thread`
- Tận dụng tốt `function_calling` và `code_interpreter` để xây workflow linh hoạt


# Assistant-API-Excel-Report-Agent

Chương trình này xây dựng một AI Agent hoàn chỉnh sử dụng OpenAI Assistant API v2 để:

Phân tích file Excel không định dạng cố định

Tự động nhận diện các vùng dữ liệu

Giao tiếp phản hồi với người dùng để cải thiện

Sinh ra báo cáo tổng hợp bằng tiếng Việt theo định dạng chuyên nghiệp

## 📁 Cấu trúc thư mục 

assistant_config.py             # Khởi tạo Assistant IDs và lưu vào file

extractor_assistant.py          # Tách section từ file Excel và giao tiếp phản hồi

extractor_memory.py             # Hệ thống ghi nhớ góp ý từ người dùng theo header

analyzer_assistant.py           # Phân tích nội dung từng vùng và sinh thống kê

planner_assistant.py            # Sinh báo cáo tổng hợp từ kết quả phân tích

main.py                         # Chương trình điều phối toàn bộ quá trình

.env                            # API key OpenAI

assistant_ids.json              # File lưu Assistant ID sau khi tạo

output/extracted_sections.json          # Các vùng dữ liệu đã chia

output/analysis_result_interactive.json # Kết quả phân tích chi tiết

output/final_report.txt                 # Báo cáo tiếng Việt cuối cùng
    
## ⚙️ Cài đặt
Cài thư viện:

pip install openai pandas python-dotenv

Tạo file .env với nội dung:

OPENAI_API_KEY=sk-xxxx

## 🚀 Hướng dẫn sử dụng

Bước 1: Tạo Assistant
Chạy một lần:

python assistant_config.py

→ Tạo ra 3 assistant: section_classifier, analyzer, planner và lưu assistant_ids.json.

Bước 2: Chạy chương trình chính

python main.py

## ⚙️ Luồng hoạt động:

#### 📂 Nhập file Excel 

assistant_API không còn hỗ trợ mở file excel , sử dụng pandas 

#### 📌 Tự động chia vùng dữ liệu

User góp ý nếu cần → chương trình ghi nhớ góp ý

Nếu user agree, kết quả sẽ được lưu lại

#### 📊 Phân tích từng vùng dữ liệu

Assistant gợi ý group_by (chiều phân tích chính)

User có thể xác nhận hoặc chọn lại chiều khác

#### 📝 Sinh báo cáo tổng hợp

Dạng tiếng Việt, đầy đủ các phần: Tổng quan, Thống kê, Nhận định, Đề xuất

Ghi ra file final_report.txt

#### 📌 Kết quả đầu ra

output/extracted_sections.json: Các vùng dữ liệu đã chia tự động từ file Excel
output/analysis_result_interactive.json :	Kết quả phân tích chi tiết từng section
output/final_report.txt	: Báo cáo tổng hợp tiếng Việt chuẩn chuyên nghiệp

## 🧠 Cơ chế học hỏi (Memory)
Mỗi góp ý của người dùng về section sẽ được lưu lại theo headers fingerprint.

Lần sau gặp bảng có header tương tự → assistant tự đề xuất thông minh hơn.

Nếu người dùng chọn agree, chương trình sẽ ghi lại thread_id để duy trì logic.

## 📚 Ví dụ định dạng báo cáo sinh ra

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

# Note

- Assistant API (v1 và v2) sẽ dần được thay thế bởi Responses API — một phiên bản đơn giản hơn, linh hoạt hơn và dễ tích hợp hơn. OpenAI đang hoàn thiện Responses API để đạt đủ tính năng tương đương Assistants API, sau đó mới chính thức sunset Assistants. OpenAI dự kiến sẽ ngưng hỗ trợ Assistants API vào giữa năm 2026.
  
- Hiện tại Assistant API chỉ hỗ trợ học và ghi nhớ qua uy trì 1 thread_id , khởi tạo 1 thread khác thì assistant không còn khả năng học nữa . Nhưng điều này cũng đi kèm rủi ro bị giới hạn token nếu không kiểm soát tốt , Assistant trả lỗi rate_limit_exceeded : "Requested 36042, Limit 30000" .


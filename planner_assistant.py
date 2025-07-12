import os
import json
import time
from openai import OpenAI
from dotenv import load_dotenv
from assistant_config import load_assistant_ids

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    default_headers={"OpenAI-Beta": "assistants=v2"}
)

OUTPUT_REPORT = "output/final_report.txt"
os.makedirs("output", exist_ok=True)

PROMPT_TEMPLATE = """
Dưới đây là dữ liệu phân tích đã được trích xuất từ các bảng trong file Excel.

🎯 Nhiệm vụ của bạn:
Hãy viết một BẢN BÁO CÁO TỔNG HỢP CHUYÊN NGHIỆP BẰNG TIẾNG VIỆT, theo đúng cấu trúc bên dưới cho MỖI REGION.

Mỗi Region hãy trình bày đầy đủ 4 phần:
1. Tổng quan dữ liệu
2. Chi tiết thống kê
3. Nhận định
4. Đề xuất

⛔ KHÔNG sao chép lại JSON. KHÔNG trình bày dạng mã. KHÔNG markdown.
✍️ Viết như người làm báo cáo kỹ thuật chuyên môn trình bày nội bộ hoặc lãnh đạo.

📊 Dữ liệu phân tích:
=== PHÂN TÍCH BẮT ĐẦU ===
{data}
=== PHÂN TÍCH KẾT THÚC ===
"""

def truncate_summary_table(table_str, max_lines=5):
    lines = table_str.strip().split("\n")
    header = lines[0:2]
    body = [line for line in lines[2:] if "nan" not in line.lower()]
    return "\n".join(header + body[:max_lines])

def generate_report_from_analysis(analysis_data: dict, assistant_id: str) -> str:
    # Rút gọn bảng trước khi tạo prompt
    cleaned_data = {}
    for region, content in analysis_data.items():
        cleaned_data[region] = {
            "group_by": content.get("group_by", ""),
            "summary_table": truncate_summary_table(content.get("summary_table", "")),
            "description": content.get("description", "")
        }

    thread = client.beta.threads.create()
    limited_data = json.dumps(cleaned_data, ensure_ascii=False)
    if len(limited_data) > 7000:
        limited_data = limited_data[:7000] + "... (đã rút gọn)"

    prompt = PROMPT_TEMPLATE.replace("{data}", limited_data)

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )

    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)

    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            raise Exception("❌ Assistant thất bại khi sinh báo cáo.")
        time.sleep(1)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for msg in reversed(messages.data):
        for part in msg.content:
            if part.type == "text":
                return part.text.value.strip()

    raise ValueError("❌ Không tìm thấy nội dung phản hồi.")

def run_planner(analysis_path: str):
    if not os.path.exists(analysis_path):
        print("❌ Không tìm thấy file JSON.")
        return

    assistant_id = load_assistant_ids()["planner_id"]
    with open(analysis_path, "r", encoding="utf-8") as f:
        analysis = json.load(f)

    try:
        print("📝 Đang sinh báo cáo...")
        report = generate_report_from_analysis(analysis, assistant_id)
        with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ Đã lưu báo cáo vào: {OUTPUT_REPORT}")
    except Exception as e:
        print("❌ Lỗi khi sinh báo cáo:", e)

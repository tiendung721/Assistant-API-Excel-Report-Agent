import os
import json
import time
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from assistant_config import load_assistant_ids

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    default_headers={"OpenAI-Beta": "assistants=v2"}
)

OUTPUT_FILE = "output/analysis_result_interactive.json"
os.makedirs("output", exist_ok=True)

def extract_region_table(df, start_row, end_row, header_row):
    header = df.iloc[header_row - 1]
    data = df.iloc[start_row - 1:end_row].copy()
    data.columns = header
    data = data.reset_index(drop=True)
    return data

def analyze_section_by_column(markdown_table, assistant_id, group_by_column):
    thread = client.beta.threads.create()
    prompt = (
        f"Tôi gửi bạn bảng dữ liệu dạng markdown bên dưới.\n"
        f"Hãy phân tích bảng này theo cột **'{group_by_column}'** bằng cách:\n"
        "- Nhóm theo cột đó (`group_by`)\n"
        "- Sinh bảng tổng hợp và mô tả ngắn gọn bằng tiếng Việt\n"
        "Trả về đúng định dạng JSON hợp lệ, không kèm mô tả, không bọc markdown. Ví dụ:\n"
        "{\"group_by\": \"Tên nhân viên\", \"summary_table\": \"| Tên | Số công |...\", \"description\": \"Mô tả ngắn\"}\n\n"
        f"{markdown_table}"
    )
    client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)

    while True:
        status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if status.status == "completed":
            break
        elif status.status == "failed":
            raise Exception("❌ Assistant thất bại.")
        time.sleep(1)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for msg in reversed(messages.data):
        for part in msg.content:
            if part.type == "text":
                text = part.text.value.strip().strip("`").strip()
                print("📩 Assistant trả về:", text)
                if text.startswith("{") and text.endswith("}"):
                    try:
                        return json.loads(text)
                    except Exception as e:
                        print("❌ JSON decode error:", e)
    raise ValueError("❌ Không tìm thấy JSON kết quả.")

def run_analyzer(file_path: str, extracted_path: str):
    if not os.path.exists(file_path) or not os.path.exists(extracted_path):
        print("❌ Thiếu file Excel hoặc extracted_sections.json.")
        return

    assistant_id = load_assistant_ids()["analyzer_id"]
    df = pd.read_excel(file_path)
    with open(extracted_path, "r", encoding="utf-8") as f:
        extracted = json.load(f)

    results = {}

    for region_id, region in extracted["regions"].items():
        print(f"🔍 Đang phân tích {region_id}...")
        try:
            region_df = extract_region_table(
                df,
                region["start_row"],
                region["end_row"],
                region["header_row"]
            )
            print(f"📋 Các cột trong {region_id}:", list(region_df.columns))
            group_by = input(f"🧭 Nhập tên cột muốn group_by cho {region_id}: ").strip()
            markdown = region_df.head(100).to_markdown(index=False)
            analysis = analyze_section_by_column(markdown, assistant_id, group_by)
            results[region_id] = analysis
        except Exception as e:
            print(f"⚠️ Lỗi khi xử lý {region_id}:", e)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"✅ Đã lưu kết quả vào: {OUTPUT_FILE}")

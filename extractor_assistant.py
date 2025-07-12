import os
import json
import time
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from assistant_config import load_assistant_ids
from extractor_memory import (
    find_matching_pattern,
    add_pattern_entry,
    get_header_fingerprint
)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), default_headers={"OpenAI-Beta": "assistants=v2"})

OUTPUT_FILE = "output/extracted_sections.json"
THREAD_MEMORY_FILE = "memory_store/extractor_threads.json"
os.makedirs("output", exist_ok=True)
os.makedirs("memory_store", exist_ok=True)

def read_excel_as_markdown(file_path):
    df = pd.read_excel(file_path)
    if len(df) > 100:
        df = df.head(100)
    return df.to_markdown(index=False), df.columns.tolist()

def load_thread_id(fingerprint):
    if not os.path.exists(THREAD_MEMORY_FILE):
        return None
    with open(THREAD_MEMORY_FILE, "r") as f:
        data = json.load(f)
    return data.get(fingerprint)

def save_thread_id(fingerprint, thread_id):
    if os.path.exists(THREAD_MEMORY_FILE):
        with open(THREAD_MEMORY_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}
    data[fingerprint] = thread_id
    with open(THREAD_MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def call_assistant(prompt, assistant_id):
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)
    while True:
        status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if status.status == "completed":
            break
        time.sleep(1)
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for msg in reversed(messages.data):
        for part in msg.content:
            if part.type == "text":
                text = part.text.value.strip().strip("` \n")
                print("\n📨 Assistant trả lời:\n", text)
                if text.startswith("[") and text.endswith("]"):
                    try:
                        return json.loads(text), thread.id
                    except:
                        continue
    raise ValueError("❌ Không tìm thấy JSON hợp lệ.")

def save_sections(sections):
    output = {"regions": {}}
    for idx, sec in enumerate(sections):
        region_id = f"Region_{idx+1}"
        output["regions"][region_id] = {
            "region_id": region_id,
            "semantic_type": sec.get("label", "unknown"),
            "start_row": sec["start_row"],
            "end_row": sec["end_row"],
            "header_row": sec["header_row"]
        }
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"✅ Đã lưu kết quả vào: {OUTPUT_FILE}")

def run_extractor(file_path: str):
    if not os.path.exists(file_path):
        print("❌ Không tìm thấy file.")
        return

    markdown_table, headers = read_excel_as_markdown(file_path)
    header_fp = get_header_fingerprint(headers)
    assistant_id = load_assistant_ids()["section_classifier_id"]

    user_feedback = ""
    while True:
        prompt = (f"Góp ý trước đó: {user_feedback}\n\n" if user_feedback else "") + (
            f"Tôi gửi bạn bảng dữ liệu dạng markdown:\n\n{markdown_table}\n\n"
            "Yêu cầu: chia thành các vùng dữ liệu (sections), mỗi vùng gồm: start_row, end_row, header_row, label.\n"
            "Trả về đúng định dạng JSON list như sau, không kèm mô tả, không bọc markdown:\n"
            "[{\"start_row\": 2, \"end_row\": 20, \"header_row\": 3, \"label\": \"work_summary\"}]"
        )

        try:
            sections, thread_id = call_assistant(prompt, assistant_id)
            print("\n📋 Assistant đề xuất:")
            print(json.dumps(sections, indent=2, ensure_ascii=False))
            user_input = input("\n✅ Đã ổn chưa? (agree / góp ý): ").strip().lower()
            if user_input == "agree":
                save_sections(sections)
                add_pattern_entry(headers, sections, "agree", user_feedback)
                save_thread_id(header_fp, thread_id)
                break
            else:
                user_feedback = input("💬 Nhập góp ý để Assistant cải thiện: ").strip()
        except Exception as e:
            print("❌ Lỗi:", e)
            break

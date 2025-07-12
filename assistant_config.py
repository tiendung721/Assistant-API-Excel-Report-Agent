import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ Chưa thiết lập OPENAI_API_KEY trong file .env")

client = OpenAI(
    api_key=api_key,
    default_headers={"OpenAI-Beta": "assistants=v2"}
)

ASSISTANT_FILE = "assistant_ids.json"

def create_section_classifier():
    print("🚀 Tạo Assistant: Section Classifier")
    assistant = client.beta.assistants.create(
        name="Section Classifier",
        instructions="Bạn là AI chuyên phân tích bảng Excel và chia thành các vùng dữ liệu (sections), mỗi vùng có start_row, end_row, header_row, label.",
        model="gpt-4o"
    )
    return assistant.id

def create_analyzer():
    print("🔍 Tạo Assistant: Section Analyzer")
    assistant = client.beta.assistants.create(
        name="Section Analyzer",
        instructions="Bạn là AI phân tích nội dung bảng dữ liệu đã chia section. Hãy xác định chiều dữ liệu quan trọng (theo tần suất hoặc entropy), thống kê và mô tả kết quả.",
        model="gpt-4o"
    )
    return assistant.id

def create_planner():
    print("📝 Tạo Assistant: Report Planner")
    assistant = client.beta.assistants.create(
        name="Report Planner",
        instructions="Bạn viết báo cáo tổng hợp tiếng Việt dựa trên kết quả phân tích từng vùng dữ liệu.",
        model="gpt-4o"
    )
    return assistant.id

def init_assistants():
    assistants = {
        "section_classifier_id": create_section_classifier(),
        "analyzer_id": create_analyzer(),
        "planner_id": create_planner()
    }
    with open(ASSISTANT_FILE, "w", encoding="utf-8") as f:
        json.dump(assistants, f, indent=2)
    print(f"✅ Đã lưu assistant_ids vào: {ASSISTANT_FILE}")

def load_assistant_ids():
    with open(ASSISTANT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
if __name__ == "__main__":
    init_assistants()


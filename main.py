import os
from extractor_assistant import run_extractor
from analyzer_assistant import run_analyzer
from planner_assistant import run_planner

# Đường dẫn cố định cho các file trung gian
EXTRACTED_PATH = "output/extracted_sections.json"
ANALYSIS_PATH = "output/analysis_result_interactive.json"
FINAL_REPORT_PATH = "output/final_report.txt"

def main():
    print("🔧 Chương trình AI Agent phân tích báo cáo Excel")
    file_path = input("📂 Nhập đường dẫn file Excel đầu vào (.xlsx): ").strip()
    if not os.path.exists(file_path):
        print("❌ Không tìm thấy file.")
        return

    # Bước 1: Extractor
    print("\n🔍 Bước 1: Phân tích cấu trúc file và chia các vùng dữ liệu...")
    run_extractor(file_path)
    if not os.path.exists(EXTRACTED_PATH):
        print("❌ Không tìm thấy extracted_sections.json.")
        return

    # Bước 2: Analyzer
    print("\n📊 Bước 2: Phân tích nội dung từng vùng dữ liệu...")
    run_analyzer(file_path, EXTRACTED_PATH)
    if not os.path.exists(ANALYSIS_PATH):
        print("❌ Không tìm thấy analysis_result_interactive.json.")
        return

    # Bước 3: Planner
    print("\n📝 Bước 3: Sinh báo cáo tổng hợp...")
    run_planner(ANALYSIS_PATH)

    # Hiển thị kết quả cuối cùng
    if os.path.exists(FINAL_REPORT_PATH):
        print("\n📄 Nội dung báo cáo:")
        with open(FINAL_REPORT_PATH, "r", encoding="utf-8") as f:
            print("\n" + f.read())
    else:
        print("❌ Không tìm thấy báo cáo đầu ra.")

if __name__ == "__main__":
    main()

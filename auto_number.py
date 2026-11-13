import json
import base58
import datetime

# 该脚本用于自动更新README
# 作者：DeepSeek
# 版本：1.1.0

# ================= 配置区 =================
README_FILE = "./README.md"
# 需要更新的版本列表
TARGETS = {
    "sub": "sub",
    "sub_r18": "sub_r18",
    "sub_lite": "sub_lite",
    "sub_all": "sub_all",
    "sub_best": "sub_best" 
}
# ==========================================

def get_source_count(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            encoded_str = f.read().strip()
        data = json.loads(base58.b58decode(encoded_str).decode('utf-8'))
        return len(data.get("api_site", {}))
    except Exception:
        return None

def update_readme():
    counts = {}
    for file_name, id_name in TARGETS.items():
        count = get_source_count(f"./sub/{file_name}")
        if count is not None:
            counts[id_name] = count
            print(f"✅ {file_name} 找到 {count} 个源")

    if not counts:
        print("❌ 没有成功读取任何源，退出。")
        return

    # 获取今天的日期，格式为 26.11.13
    today_str = datetime.datetime.now().strftime("%y.%m.%d")
    
    with open(README_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.strip().startswith("|"):
            parts = line.split("|")
            # 假设格式: | 版本 | ID | R18源 | 影视源 | 源数量 | 上次更新 |
            # parts 列表索引: [0]空, [1]版本, [2]ID, [3]R18, [4]影视, [5]数量, [6]更新时间, [7]空
            if len(parts) >= 7:
                row_id = parts[2].strip()
                if row_id in counts:
                    # 更新数量列
                    parts[5] = f" {counts[row_id]} "
                    # 更新日期列
                    parts[6] = f" {today_str} "
                    line = "|".join(parts)
        new_lines.append(line)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"💾 README 更新完毕，日期已更新为 {today_str}")

if __name__ == "__main__":
    update_readme()
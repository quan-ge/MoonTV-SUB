import json
import base58
import re

# ================= 配置区 =================
README_FILE = "./README.md"
# 你需要更新的版本列表（文件名 : README里的标识）
TARGETS = {
    "sub": "sub",
    "sub_r18": "sub_r18",
    "sub_lite": "sub_lite",
    "sub_all": "sub_all",
    "sub_best": "sub_best" # 假设你也有 best 的统计
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
    # 1. 先读取所有源的数量
    counts = {}
    for file_name, id_name in TARGETS.items():
        count = get_source_count(f"./sub/{file_name}")
        if count is not None:
            counts[id_name] = count
            print(f"✅ {file_name} 找到 {count} 个源")

    if not counts:
        print("❌ 没有成功读取任何源，退出。")
        return

    # 2. 读取 README 并按行处理
    with open(README_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        # 如果这行是表格行，并且包含我们需要的 ID
        if line.strip().startswith("|"):
            # 按 | 切割
            parts = line.split("|")
            # 假设表格格式为: | 版本 | ID | R18源 | 影视源 | 源数量 | 上次更新 |
            # 那么 parts[2] 是 ID，parts[5] 是源数量
            if len(parts) >= 6:
                row_id = parts[2].strip()
                if row_id in counts:
                    # 替换数量列，保留前后的空格格式
                    parts[5] = f" {counts[row_id]} "
                    line = "|".join(parts)
        new_lines.append(line)

    # 3. 写回文件
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("💾 README 更新完毕")

if __name__ == "__main__":
    update_readme()
import json
import base58
import datetime

# 该脚本用于自动更新README
# 作者：DeepSeek、QuanGe
# 版本：1.2.0

# 自动更新源列表，自动将时间更新为当前时间

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

    today_str = datetime.datetime.now().strftime("%y.%m.%d")
    
    with open(README_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.strip().startswith("|"):
            parts = line.split("|")
            if len(parts) >= 7:
                row_id = parts[2].strip()
                if row_id in counts:
                    # 1. 总是更新数量
                    parts[5] = f" {counts[row_id]} "
                    
                    # 2. 询问是否更新日期
                    old_date = parts[6].strip()
                    if old_date != today_str: 
                        answer = input(f"❓ 发现 {row_id} 存在。是否将它的更新日期从 [{old_date}] 改为今天 [{today_str}]？(y/n): ")
                        if answer.lower() in ['y', '', 'yes', 'Y']:
                            parts[6] = f" {today_str} "
                            print(f"   -> 已更新 {row_id} 的日期。")
                        else:
                            print(f"   -> 保持 {row_id} 原日期不变。")
                    else:
                        print(f"✨ {row_id} 的日期已经是今天了，跳过询问。")
                        
                    line = "|".join(parts)
        new_lines.append(line)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("💾 README 已保存。")


if __name__ == "__main__":
    update_readme()
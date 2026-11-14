import os
import shutil

# 自动生成Pages文档
# 作者：DeepSeek、QuanGe
# 版本：1.2.0

# ---------------------配置区--------------------------

# 复制黑名单（完全匹配）
COPY_BLACKLIST = {"docs", ".git", "CNAME", "README.md"}
# 复制黑名单后缀（忽略大小写）
COPY_BLACKLIST_EXTS = {".py"}

# 清理白名单需要保留的文件/文件夹
CLEAN_KEEP = {".git", "README.md", "index.md", "CNAME"}

# -------------------------------------------------------

def copy_to_docs():
    source_dir = "."
    target_dir = "./docs"
    
    deleted_list = []
    copied_list = []
    
    # 1. 清理 docs 目录（保留 .git 和 README.md）
    if os.path.exists(target_dir):
        for item in os.listdir(target_dir):
            if item in CLEAN_KEEP:
                continue
                
            item_path = os.path.join(target_dir, item)
            deleted_list.append(item)
            
            if os.path.isdir(item_path):
                shutil.rmtree(item_path, ignore_errors=True)
            else:
                try:
                    os.remove(item_path)
                except Exception:
                    pass
    else:
        os.makedirs(target_dir)

    # 2. 开始复制
    for item in os.listdir(source_dir):
        if item in COPY_BLACKLIST:
            continue
        if os.path.splitext(item)[1].lower() in COPY_BLACKLIST_EXTS:
            continue
            
        src_path = os.path.join(source_dir, item)
        dst_path = os.path.join(target_dir, item)
        
        try:
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dst_path)
            copied_list.append(item)
        except Exception as e:
            print(f"❌ 复制 {item} 失败: {e}")

    # 3. 统一输出结果
    print("\n================ 执行报告 ================")
    if deleted_list:
        print(f"🗑️ 已从 {target_dir} 删除 {len(deleted_list)} 项:")
        for d in deleted_list:
            print(f"   - {d}")
    else:
        print(f"🗑️ {target_dir} 没有需要删除的内容。")

    if copied_list:
        print(f"\n📦 已复制 {len(copied_list)} 项到 {target_dir}:")
        for c in copied_list:
            print(f"   - {c}")
    else:
        print("\n📦 没有复制任何文件。")
    print("==========================================\n")

if __name__ == "__main__":
    print("🚀 开始清理并复制文件到 ./docs ...")
    copy_to_docs()
    print("🎉 复制完成！")
import os
import shutil

# 复制黑名单（完全匹配）
COPY_BLACKLIST = {"docs", ".git", "CNAME", "README.md"}
# 复制黑名单后缀（忽略大小写）
COPY_BLACKLIST_EXTS = {".py"}

# 清理白名单需要保留的文件/文件夹
CLEAN_KEEP = {".git", "README.md"}

def copy_to_docs():
    source_dir = "."
    target_dir = "./docs"
    
    # 1. 清理 docs 目录（保留 .git 和 README.md）
    if os.path.exists(target_dir):
        for item in os.listdir(target_dir):
            if item in CLEAN_KEEP:
                continue  # 保留白名单里的内容
                
            item_path = os.path.join(target_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path, ignore_errors=True)
            else:
                try:
                    os.remove(item_path)
                except Exception:
                    pass
        print(f"🗑️ 已清理 {target_dir} 目录（保留了 .git 和 README.md）")
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
                print(f"📁 已复制文件夹: {item}")
            else:
                shutil.copy2(src_path, dst_path)
                print(f"📄 已复制文件: {item}")
        except Exception as e:
            print(f"❌ 复制 {item} 失败: {e}")

if __name__ == "__main__":
    print("🚀 开始清理并复制文件到 ./docs ...")
    copy_to_docs()
    print("🎉 复制完成！")
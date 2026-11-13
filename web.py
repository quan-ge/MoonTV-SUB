import os
import shutil

# 黑名单（完全匹配）
BLACKLIST_ITEMS = {"web", ".git", "CNAME", "README.md"}
# 黑名单后缀（忽略大小写）
BLACKLIST_EXTS = {".py"}

def copy_to_web():
    source_dir = "."
    target_dir = "./web"
    
    # 1. 彻底删除 web 目录（忽略系统占用等报错）
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir, ignore_errors=True)
        print(f"🗑️ 已彻底删除 {target_dir} 目录")
        
    # 重新创建 web 目录
    os.makedirs(target_dir)
    
    # 2. 开始复制（忽略黑名单）
    for item in os.listdir(source_dir):
        if item in BLACKLIST_ITEMS:
            continue
        if os.path.splitext(item)[1].lower() in BLACKLIST_EXTS:
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
    print("🚀 开始清理并复制文件到 ./web ...")
    copy_to_web()
    print("🎉 复制完成！")

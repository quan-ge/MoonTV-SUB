import os

# 自动生成Pages文档首页
# 作者：DeepSeek、QuanGe
# 版本：1.1.1

def main():
    source_file = './README.md'
    target_dir = './docs'
    target_file = os.path.join(target_dir, 'index.md')
    split_marker = '---- 分割标记（以下为网页源码） ----'

    # 1. 检查源文件是否存在
    if not os.path.exists(source_file):
        print(f"❌ 错误：找不到源文件 {source_file}")
        return

    # 2. 检查并创建目标文件夹 (如果没有 docs 文件夹则自动创建)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"📁 已创建目标文件夹：{target_dir}")

    # 3. 读取源文件内容
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 4. 查找分割标记并截取内容
    if split_marker in content:
        # 找到标记的位置，分割字符串
        # split 会返回一个列表，[0]是标记前，[1]是标记后
        parts = content.split(split_marker, 1)
        new_content = parts[1].strip() # 取后半部分并去掉首尾多余空白
        print(f"✅ 找到分割标记，已删除上方内容。")
    else:
        # 如果没找到标记，提示一下，并原样复制（或者你可以选择直接退出）
        print(f"⚠️ 警告：未找到标记 '{split_marker}'，将完整复制原文件。")
        new_content = content

    # 5. 写入目标文件
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"🎉 处理完成！结果已保存至：{target_file}")

if __name__ == '__main__':
    main()
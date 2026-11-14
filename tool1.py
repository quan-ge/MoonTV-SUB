import json
import sys
from urllib.parse import urlparse

# TvBox订阅 -> LunaTV订阅
# 作者：DeepSeek、QuanGe
# 版本：1.1.1

def main():
    print("="*50)
    print("  TVBox 接口转换工具")
    print("="*50)
    print("请粘贴你的原始 JSON 列表，粘贴完成后：")
    print("  - Mac/Linux 用户请按 Ctrl+D")
    print("  - Windows 用户请按 Ctrl+Z 然后回车")
    print("-" * 50)

    # 读取多行输入
    input_lines = sys.stdin.readlines()
    
    if not input_lines:
        print("❌ 错误：没有读取到任何输入内容。")
        return

    raw_string = "".join(input_lines).strip()

    try:
        # 尝试解析输入的 JSON
        raw_data = json.loads(raw_string)
        
        if not isinstance(raw_data, list):
            print("❌ 错误：输入的 JSON 必须是一个列表（Array）格式。")
            return

        # 目标格式的基础结构
        target_data = {
            "cache_time": 7200,
            "api_site": {}
        }

        # 遍历原始数据并转换
        for item in raw_data:
            if "api" not in item or "name" not in item:
                print(f"⚠️ 警告：跳过了格式不正确的数据项 -> {item}")
                continue
                
            api_url = item["api"]
            name = item["name"]
            
            # 提取域名作为 key (例如: cj.rycjapi.com)
            parsed_url = urlparse(api_url)
            key = parsed_url.netloc

            # 写入目标字典（去掉了 detail_url 的生成）
            target_data["api_site"][key] = {
                "api": api_url,
                "name": name
            }

        # 打印结果
        print("\n✅ 转换成功！结果如下：\n")
        formatted_json = json.dumps(target_data, ensure_ascii=False, indent=2)
        print(formatted_json)

        # 保存到 tool1.json 文件
        output_filename = "tool1.json"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(formatted_json)
            
        print(f"\n💾 数据已成功保存到当前目录下的: {output_filename}")

    except json.JSONDecodeError as e:
        print(f"\n❌ JSON 解析失败，请检查你输入的内容是否是合法的 JSON 格式。")
        print(f"错误详情: {e}")

if __name__ == "__main__":
    main()
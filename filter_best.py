import json
import time
import requests
import base58
from concurrent.futures import ThreadPoolExecutor, as_completed

# 该脚本用于自动生成sub_best
# 作者：DeepSeek
# 版本：1.0.3

# ================= 配置区 =================
SOURCE_FILE = "./sub/sub_all"
TOP_N = 50        # 保留前 50 个最快的源
TIMEOUT = 6       # 超时时间 6 秒

# 强制不走代理
PROXIES = {"http": None, "https": None}
# ==========================================

def fetch_sources():
    print(f"正在从本地文件 {SOURCE_FILE} 获取并解码源列表...")
    try:
        with open(SOURCE_FILE, "r", encoding="utf-8") as f:
            encoded_str = f.read().strip()
        
        decoded_bytes = base58.b58decode(encoded_str)
        decoded_str = decoded_bytes.decode('utf-8')
        data = json.loads(decoded_str)
        
        # 提取 api_site 里面的数据，转换成列表方便遍历
        api_site_dict = data.get("api_site", {})
        sources_list = []
        for domain, info in api_site_dict.items():
            sources_list.append({
                "domain": domain,
                "api": info.get("api"),
                "name": info.get("name", "未知"),
                "detail": info.get("detail", ""),
                "is_adult": info.get("is_adult", False)
            })
        return sources_list, data.get("cache_time", 7200)
        
    except Exception as e:
        print(f"❌ 读取或解码失败: {e}")
        return [], 7200

def check_source(source_item):
    real_url = source_item.get("api", "")
    if not real_url:
        return {"source": source_item, "status": "empty", "time": 999}

    try:
        start_time = time.time()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        resp = requests.get(real_url, headers=headers, proxies=PROXIES, timeout=TIMEOUT)
        elapsed = time.time() - start_time
        
        if resp.status_code == 200 and len(resp.text) > 50:
            return {"source": source_item, "status": "ok", "time": elapsed}
        else:
            return {"source": source_item, "status": "bad_data", "time": 999}
            
    except Exception:
        return {"source": source_item, "status": "blocked", "time": 999}

def main():
    all_sources, cache_time = fetch_sources()
    if not all_sources:
        return
        
    print(f"成功提取 {len(all_sources)} 个源，开始直连测速...\n")
    
    results = []
    with ThreadPoolExecutor(max_workers=15) as executor:
        future_to_source = {executor.submit(check_source, src): src for src in all_sources}

        
        for future in as_completed(future_to_source):
            res = future.result()
            if res["status"] == "ok":
                results.append(res)
                print(f"✅ 存活 [{res['time']:.2f}s]: {res['source']['name']}")
            else:
                print(f"❌ 被墙/失效: {res['source']['name']}")

    # 按时间排序取前 TOP_N
    results.sort(key=lambda x: x["time"])
    best_results = results[:TOP_N]
    
    print(f"\n🎉 测速完毕！存活 {len(results)} 个，保留最快的 {len(best_results)} 个。")

    # 重新组装成 LunaTV 需要的格式
    best_api_site = {}
    for item in best_results:
        src = item["source"]
        best_api_site[src["domain"]] = {
            "api": src["api"],
            "name": src["name"]
        }
        if src["detail"]:
            best_api_site[src["domain"]]["detail"] = src["detail"]
        if src.get("is_adult"):
            best_api_site[src["domain"]]["is_adult"] = True
            

    final_data = {
        "cache_time": cache_time,
        "api_site": best_api_site
    }
    
    # 1. 转换为 JSON 字符串
    final_json_str = json.dumps(final_data, ensure_ascii=False)
    # 2. 整体 Base58 编码
    final_b58_bytes = base58.b58encode(final_json_str.encode('utf-8'))
    
    # 3. 写入文件（注意这里写入的是 Base58 字符串）
    with open("./sub/sub_best", "w", encoding="utf-8") as f:
        f.write(final_b58_bytes.decode('utf-8'))
        
    print("💾 已保存到 ./sub/sub_best（格式为整体 Base58 编码）")

if __name__ == "__main__":
    main()
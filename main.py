# 导入os模块，用来处理环境变量
import os

# --- 关键修正：在所有代码运行前，清除代理设置 ---
# 这几行代码会告诉本次运行的程序，忽略系统中的所有代理设置
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
# --- 修正结束 ---

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from apple_scraper.fetch_links import get_top_app_urls
from apple_scraper.fetch_details import get_app_details
from apple_scraper.utils import save_to_csv

MAX_APPS_PER_CATEGORY = 100

def run(category_name, category_id):
    print(f"📥 正在抓取【{category_name}】类别（ID: {category_id}），目标数量: {MAX_APPS_PER_CATEGORY}...")
    
    driver = None # 先声明driver变量
    try:
        # 这里的代码和之前一样
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        
        urls = get_top_app_urls(driver, category_name, category_id, max_apps=MAX_APPS_PER_CATEGORY)
        
        if not urls:
            print(f"🟡 未能为【{category_name}】获取到任何App链接，跳过后续步骤。")
            return

        all_app_data = []
        for url in urls:
            details = get_app_details(url) 
            if details:
                details['category'] = category_name
                details['url'] = url
                all_app_data.append(details)
        
        if all_app_data:
            save_to_csv(all_app_data, category_name)
        else:
            print(f"🟡 【{category_name}】的App详情均抓取失败。")
            
    except Exception as e:
        print(f"❌ 在处理【{category_name}】时发生未知错误: {e}")
    finally:
        # 确保浏览器最后被关闭
        if driver:
            driver.quit()

if __name__ == "__main__":
    categories_to_scrape = {
        "娱乐": "6016",
        "财务": "6015",
        "教育": "6017",
        "音乐": "6011",
        "游戏": "6014",   
        "工具": "6002",
        "摄影与录像": "6008",
        "健康健美": "6013",
        "生活": "6012",
        "社交": "6005",
        "购物": "6024",
        "旅游": "6003",
        "美食佳饮": "6023",
        "体育": "6004",
        "新闻": "6009",
        "参考": "6006",
        "医疗": "6020",
        "导航": "6010",
        "商务": "6000",
        "图书": "6018",
        "天气": "6001",
        "报刊杂志": "6021",
        "儿童": "6019",
        "效率": "6007",
        "贴纸": "6025"
    }
    
    for name, cid in categories_to_scrape.items():
        run(name, cid)
        print("-" * 40)
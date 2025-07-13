# /Users/osc7/Codes/GetAppData/apple_scraper/fetch_details.py

import requests
from bs4 import BeautifulSoup
import urllib.parse # 引入URL解析库

def get_app_details(app_url):
    """获取单个App的详细信息，修正了编码和CSS选择器"""
    try:
        print(f"    - [详情抓取] 正在处理: {app_url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        
        response = requests.get(app_url, headers=headers, timeout=10)
        
        # 关键修正 1: 强制指定UTF-8编码，解决所有乱码问题
        response.encoding = 'utf-8'
        
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # 关键修正 2: 使用更精确的CSS选择器
        
        # App 名称
        name_tag = soup.select_one('h1.product-header__title')
        app_name = name_tag.get_text(strip=True) if name_tag else "未知App名称"
        # URL解码，处理像 %E7%BA%A2%E6%9E%9C 这样的编码
        app_name = urllib.parse.unquote(app_name)

        # 开发者
        developer_tag = soup.select_one('.product-header__identity a')
        developer_text = developer_tag.get_text(strip=True) if developer_tag else "未知开发者"

        # 描述 (这个选择器更稳定)
        description_tag = soup.select_one('div[data-test-bidi] > p')
        description_text = description_tag.get_text(strip=True) if description_tag else "无描述"
        
        # 版本
        version_tag = soup.select_one('p.whats-new__latest__version')
        version_text = version_tag.get_text(strip=True).replace('版本', '').strip() if version_tag else "未知版本"
        
        print(f"      -> 名称: {app_name}, 开发者: {developer_text}, 版本: {version_text}")

        return {
            'app_name': app_name,
            'developer': developer_text,
            'description': description_text,
            'version': version_text,
        }
    except requests.RequestException as e:
        print(f"    - [错误] 请求App详情页失败: {app_url}, 错误: {e}")
        return None
    except Exception as e:
        print(f"    - [错误] 解析App详情页失败: {app_url}, 错误: {e}")
        return None
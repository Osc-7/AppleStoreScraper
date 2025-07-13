from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_top_app_urls(driver, category_name, category_id, max_apps=100):
    """
    通过模拟点击进入完整列表，再进行滚动加载，获取完整的App链接。
    """
    initial_url = f"https://apps.apple.com/cn/charts/iphone/{category_name}-apps/{category_id}"
    print(f"  - [最终方案] 1. 正在导航至初始页面: {initial_url}")
    driver.get(initial_url)
    driver.maximize_window()

    all_app_links = set()

    try:
        # --- 步骤 2: 找到并点击“免费 App 排行”的链接 ---
        print("  - [最终方案] 2. 正在寻找'免费 App 排行'的链接...")
        
        # 使用 WebDriverWait 来等待链接可被点击，增加稳定性
        free_chart_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[h2[text()='免费 App 排行']]"))
        )
        print("  - [最终方案]    链接已找到，正在点击...")
        free_chart_link.click()

        # --- 步骤 3: 在新页面上等待并滚动 ---
        print("  - [最终方案] 3. 已进入完整列表页，开始滚动加载...")
        # 等待新页面的列表容器出现
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "ol.l-row"))
        )
        
        retries = 3
        while len(all_app_links) < max_apps:
            links_before_scroll = len(all_app_links)

            elements = driver.find_elements(By.CSS_SELECTOR, "a.we-lockup.targeted-link")
            for elem in elements:
                href = elem.get_attribute('href')
                if href and href.startswith("https://apps.apple.com/cn/app/"):
                    all_app_links.add(href)

            print(f"  - [最终方案]    当前已找到 {len(all_app_links)} 个不重复的App。")

            if len(all_app_links) >= max_apps:
                print(f"  - [最终方案]    已达到目标数量 {max_apps}。")
                break

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            # 更新当前找到的链接数量
            current_elements = driver.find_elements(By.CSS_SELECTOR, "a.we-lockup.targeted-link")
            current_link_count = len(all_app_links)
            for elem in current_elements:
                href = elem.get_attribute('href')
                if href and href.startswith("https://apps.apple.com/cn/app/"):
                    all_app_links.add(href)
            
            # 如果滚动后数量没有增加，说明可能到底了
            if len(all_app_links) == links_before_scroll:
                retries -= 1
                print(f"  - [最终方案]    滚动后App数量未增加。剩余尝试次数: {retries}")
                if retries <= 0:
                    print("  - [最终方案]    已滚动到底部，或无法加载更多新内容。")
                    break
            else:
                retries = 3

    except Exception as e:
        print(f"  - [Selenium错误] 在抓取链接时发生错误: {e}")

    final_links = list(all_app_links)
    print(f"✅ [链接抓取完成] 共找到 {len(final_links)} 个不重复的App链接。")
    return final_links[:max_apps]
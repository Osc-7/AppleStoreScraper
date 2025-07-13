import csv
import os

def save_to_csv(data, category_name):
    """将App数据保存到CSV文件"""
    # 确保'results'文件夹存在
    if not os.path.exists('results'):
        os.makedirs('results')

    # 定义文件名
    filename = f"results/apple_store_top_100_{category_name}.csv"
    
    # 检查是否有数据需要写入
    if not data:
        print("  - [保存] 没有数据可以保存。")
        return

    # 获取表头（使用第一个数据项的键）
    headers = data[0].keys()

    print(f"  -> [保存] 正在将 {len(data)} 条记录保存到 {filename}...")

    try:
        # 关键：使用 encoding='utf-8-sig' 来正确处理中文，防止Excel打开乱码
        # newline='' 是为了防止写入时出现多余的空行
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            
            # 写入表头
            writer.writeheader()
            
            # 写入数据
            writer.writerows(data)
            
        print(f"✅ [成功] 数据已成功保存到 {filename}")

    except IOError as e:
        print(f"❌ [错误] 写入文件失败: {e}")
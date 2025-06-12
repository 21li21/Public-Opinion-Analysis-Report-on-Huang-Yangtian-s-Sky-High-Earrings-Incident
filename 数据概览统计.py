import sqlite3
import pandas as pd
from datetime import datetime

# 连接到SQLite数据库
conn = sqlite3.connect('/app/data/configs/mcp_sqlite.db')
cursor = conn.cursor()

# 查询数据总数量
cursor.execute("SELECT COUNT(*) FROM original_data")
total_count = cursor.fetchone()[0]

# 查询相关数据数量（is_relevant=1）
cursor.execute("SELECT COUNT(*) FROM original_data WHERE is_relevant=1")
relevant_count = cursor.fetchone()[0]
relevant_percentage = (relevant_count / total_count * 100) if total_count > 0 else 0

# 查询发布时间范围
cursor.execute("SELECT MIN(publish_time), MAX(publish_time) FROM original_data")
time_range = cursor.fetchone()
start_time = datetime.strptime(time_range[0], '%Y-%m-%d %H:%M:%S') if time_range[0] else None
end_time = datetime.strptime(time_range[1], '%Y-%m-%d %H:%M:%S') if time_range[1] else None

# 查询情感类型分布
sentiment_query = """
SELECT opinion_type, COUNT(*) as count 
FROM original_data 
WHERE is_relevant=1
GROUP BY opinion_type
ORDER BY count DESC
"""
sentiment_df = pd.read_sql(sentiment_query, conn)

# 查询平台分布
platform_query = """
SELECT source, COUNT(*) as count 
FROM original_data 
WHERE is_relevant=1
GROUP BY source
ORDER BY count DESC
"""
platform_df = pd.read_sql(platform_query, conn)

# 查询query分布
query_query = """
SELECT query, COUNT(*) as count 
FROM original_data 
WHERE is_relevant=1
GROUP BY query
ORDER BY count DESC
"""
query_df = pd.read_sql(query_query, conn)

# 准备输出内容
output_content = f"""# 黄杨钿甜'天价耳环'事件数据概览

## 1. 数据基本情况
- 总数据量: {total_count} 条
- 相关数据量: {relevant_count} 条 (占比 {relevant_percentage:.2f}%)
- 数据时间范围: {start_time.strftime('%Y-%m-%d %H:%M') if start_time else '无'} 至 {end_time.strftime('%Y-%m-%d %H:%M') if end_time else '无'}

## 2. 情感类型分布
{sentiment_df.to_markdown(index=False)}

## 3. 平台分布
{platform_df.to_markdown(index=False)}

## 4. 查询词分布
{query_df.to_markdown(index=False)}
"""

# 保存为Markdown文件
with open('数据概览统计.md', 'w', encoding='utf-8') as f:
    f.write(output_content)

print("数据概览统计.md 文件已成功生成。")

# 关闭数据库连接
conn.close()
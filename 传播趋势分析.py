import sqlite3
import pandas as pd
from datetime import datetime

# 连接到SQLite数据库
conn = sqlite3.connect('/app/data/configs/mcp_sqlite.db')

# 查询声量趋势（按小时统计）
hourly_query = """
SELECT 
    strftime('%Y-%m-%d %H:00:00', publish_time) as hour,
    COUNT(*) as volume,
    SUM(comment_count + like_count + share_count + fav_count) as interaction
FROM original_data
WHERE is_relevant=1
GROUP BY hour
ORDER BY hour
"""
hourly_df = pd.read_sql(hourly_query, conn)

# 查询情感类型分布趋势
sentiment_trend_query = """
SELECT 
    strftime('%Y-%m-%d %H:00:00', publish_time) as hour,
    opinion_type,
    COUNT(*) as count
FROM original_data
WHERE is_relevant=1
GROUP BY hour, opinion_type
ORDER BY hour
"""
sentiment_trend_df = pd.read_sql(sentiment_trend_query, conn)

# 查询高互动量内容
high_interaction_query = """
SELECT 
    title,
    content,
    detail_url,
    comment_count,
    like_count,
    share_count,
    fav_count,
    (comment_count + like_count + share_count + fav_count) as total_interaction,
    publish_time,
    source
FROM original_data
WHERE is_relevant=1
ORDER BY total_interaction DESC
LIMIT 5
"""
high_interaction_df = pd.read_sql(high_interaction_query, conn)

# 准备输出内容
output_content = "# 黄杨钿甜'天价耳环'事件传播趋势分析\n\n"
output_content += "## 1. 声量趋势（按小时统计）\n"
output_content += hourly_df.to_markdown(index=False) + "\n\n"

output_content += "## 2. 情感类型分布趋势\n"
output_content += sentiment_trend_df.to_markdown(index=False) + "\n\n"

output_content += "## 3. 高互动量内容分析\n"
output_content += high_interaction_df.to_markdown(index=False) + "\n\n"

# 保存为Markdown文件
with open('传播趋势分析.md', 'w', encoding='utf-8') as f:
    f.write(output_content)

print("传播趋势分析.md 文件已成功生成。")

# 关闭数据库连接
conn.close()
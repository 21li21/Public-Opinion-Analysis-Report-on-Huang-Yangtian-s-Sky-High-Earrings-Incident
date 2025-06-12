import sqlite3
import pandas as pd

# 连接到SQLite数据库
conn = sqlite3.connect('/app/data/configs/mcp_sqlite.db')

# 查询各平台声量分布
platform_volume_query = """
SELECT 
    source,
    COUNT(*) as volume,
    SUM(comment_count + like_count + share_count + fav_count) as interaction
FROM original_data
WHERE is_relevant=1
GROUP BY source
ORDER BY volume DESC
"""
platform_volume_df = pd.read_sql(platform_volume_query, conn)

# 查询各平台情感类型分布
platform_sentiment_query = """
SELECT 
    source,
    opinion_type,
    COUNT(*) as count
FROM original_data
WHERE is_relevant=1
GROUP BY source, opinion_type
ORDER BY source, count DESC
"""
platform_sentiment_df = pd.read_sql(platform_sentiment_query, conn)

# 查询各平台高互动量内容
platform_high_interaction_query = """
SELECT 
    source,
    title,
    content,
    detail_url,
    comment_count,
    like_count,
    share_count,
    fav_count,
    (comment_count + like_count + share_count + fav_count) as total_interaction
FROM original_data
WHERE is_relevant=1
ORDER BY source, total_interaction DESC
"""
platform_high_interaction_df = pd.read_sql(platform_high_interaction_query, conn)

# 准备输出内容
output_content = "# 黄杨钿甜'天价耳环'事件平台传播分析\n\n"
output_content += "## 1. 各平台声量及互动量分布\n"
output_content += platform_volume_df.to_markdown(index=False) + "\n\n"

output_content += "## 2. 各平台情感类型分布\n"
output_content += platform_sentiment_df.to_markdown(index=False) + "\n\n"

output_content += "## 3. 各平台高互动量内容\n"
output_content += platform_high_interaction_df.to_markdown(index=False) + "\n\n"

# 保存为Markdown文件
with open('平台传播分析.md', 'w', encoding='utf-8') as f:
    f.write(output_content)

print("平台传播分析.md 文件已成功生成。")

# 关闭数据库连接
conn.close()
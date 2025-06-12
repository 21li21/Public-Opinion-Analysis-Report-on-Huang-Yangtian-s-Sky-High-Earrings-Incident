import sqlite3
import pandas as pd
import jieba
from collections import Counter

# 连接到SQLite数据库
conn = sqlite3.connect('/app/data/configs/mcp_sqlite.db')

# 查询媒体报道内容
media_query = """
SELECT 
    title,
    content,
    detail_url,
    source
FROM original_data
WHERE is_relevant=1 AND source IN ('微信公众平台', '联网搜索')
"""
media_df = pd.read_sql(media_query, conn)

# 提取关键词
def extract_keywords(text):
    if not text or pd.isna(text):
        return []
    words = jieba.cut(text)
    keywords = [word for word in words if len(word) > 1 and not word.isdigit()]
    return keywords

# 分析标题和内容关键词
all_keywords = []
for _, row in media_df.iterrows():
    all_keywords.extend(extract_keywords(row['title']))
    all_keywords.extend(extract_keywords(row['content']))

# 统计关键词频率
keyword_counter = Counter(all_keywords)
top_keywords = keyword_counter.most_common(20)

# 准备输出内容
output_content = "# 黄杨钿甜'天价耳环'事件媒体聚焦点分析\n\n"
output_content += "## 1. 媒体报道关键词分析\n"
output_content += "| 关键词 | 出现频率 |\n"
output_content += "|--------|----------|\n"
for keyword, count in top_keywords:
    output_content += f"| {keyword} | {count} |\n"

output_content += "\n## 2. 媒体报道案例\n"
output_content += media_df.to_markdown(index=False) + "\n"

# 保存为Markdown文件
with open('媒体聚焦点分析.md', 'w', encoding='utf-8') as f:
    f.write(output_content)

print("媒体聚焦点分析.md 文件已成功生成。")

# 关闭数据库连接
conn.close()
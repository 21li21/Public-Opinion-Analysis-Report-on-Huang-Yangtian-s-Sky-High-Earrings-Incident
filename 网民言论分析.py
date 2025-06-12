import sqlite3
import pandas as pd
import jieba
from collections import Counter

# 连接到SQLite数据库
conn = sqlite3.connect('/app/data/configs/mcp_sqlite.db')

# 查询网民评论内容
comment_query = """
SELECT 
    title,
    content,
    detail_url,
    source,
    opinion_type
FROM original_data
WHERE is_relevant=1 AND source NOT IN ('微信公众平台', '联网搜索')
"""
comment_df = pd.read_sql(comment_query, conn)

# 提取关键词
def extract_keywords(text):
    if not text or pd.isna(text):
        return []
    words = jieba.cut(text)
    keywords = [word for word in words if len(word) > 1 and not word.isdigit()]
    return keywords

# 分析标题和内容关键词
all_keywords = []
for _, row in comment_df.iterrows():
    all_keywords.extend(extract_keywords(row['title']))
    all_keywords.extend(extract_keywords(row['content']))

# 统计关键词频率
keyword_counter = Counter(all_keywords)
top_keywords = keyword_counter.most_common(20)

# 准备输出内容
output_content = "# 黄杨钿甜'天价耳环'事件网民言论分析\n\n"
output_content += "## 1. 网民言论关键词分析\n"
output_content += "| 关键词 | 出现频率 |\n"
output_content += "|--------|----------|\n"
for keyword, count in top_keywords:
    output_content += f"| {keyword} | {count} |\n"

output_content += "\n## 2. 网民言论情感类型分布\n"
output_content += comment_df['opinion_type'].value_counts().to_markdown() + "\n"

output_content += "\n## 3. 网民言论案例\n"
output_content += comment_df.to_markdown(index=False) + "\n"

# 保存为Markdown文件
with open('网民言论分析.md', 'w', encoding='utf-8') as f:
    f.write(output_content)

print("网民言论分析.md 文件已成功生成。")

# 关闭数据库连接
conn.close()
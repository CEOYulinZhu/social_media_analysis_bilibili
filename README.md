# 社交媒体分析系统 - 哔哩哔哩评论数据挖掘

**数据挖掘与机器学习课程设计作业 - 祝钰霖**

## 项目简介

本项目是一个针对哔哩哔哩（Bilibili）视频评论的数据挖掘与分析系统，通过爬取、清洗、分析评论数据，实现多维度的社交媒体内容分析。项目采用Python开发，集成了数据采集、数据预处理、情感分析、关键词提取、用户行为分析等功能。

## 功能特性

### 🔍 数据采集模块 (`data_acquisition/`)
- **自动化爬虫**：基于Selenium的B站视频评论爬取
- **智能登录**：自动化登录B站账户
- **分页处理**：支持多页评论和二级回复的完整采集
- **数据存储**：自动保存为Excel格式，便于后续分析

### 🧹 数据清洗模块 (`data_cleansing/`)
- **数据去重**：移除空白和无效评论
- **表情符号处理**：智能去除各类Unicode表情符号
- **回复格式标准化**：清理"回复@用户"等格式化文本
- **批量处理**：支持多文件批量清洗

### 📊 数据分析模块 (`analysis/`)

#### 1. 情感分析 (`sentiment_analysis.py`)
- **情感极性分析**：基于SnowNLP的中文情感分析
- **情感分类**：自动标记正面/负面/中立情感
- **可视化展示**：
  - 情感得分分布直方图
  - 情感标签饼图
  - 时间趋势折线图
  - 情感与点赞数相关性分析

#### 2. 评论活跃度分析 (`comment_activity_analysis.py`)
- **时间维度分析**：按日期和小时统计评论活跃度
- **活跃点检测**：识别评论数量剧烈变化的时间点
- **聚类分析**：使用K-Means算法识别活跃时间段
- **趋势可视化**：多种图表展示活跃度变化

#### 3. 评论点赞分析 (`comment_like_analysis.py`)
- **点赞分布分析**：统计点赞数的分布特征
- **热门评论提取**：自动识别高点赞评论
- **词云生成**：基于热门评论生成关键词词云
- **长度相关性**：分析评论长度与点赞数的关系

#### 4. 关键词话题分析 (`top_keyword_analysis.py`)
- **高频词提取**：基于jieba分词的关键词统计
- **话题网络构建**：通过词语共现关系构建话题网络
- **网络可视化**：使用NetworkX生成话题关系图
- **停用词过滤**：智能过滤无意义词汇

## 项目结构

```
social_media_analysis/
├── data_acquisition/          # 数据采集模块
│   ├── __init__.py
│   └── data_acquisition.py    # 哔哩哔哩评论爬虫
├── data_cleansing/           # 数据清洗模块
│   ├── __init__.py
│   └── data_cleansing.py     # 数据预处理和清洗
├── analysis/                 # 数据分析模块
│   ├── __init__.py
│   ├── sentiment_analysis.py      # 情感分析
│   ├── comment_activity_analysis.py # 评论活跃度分析
│   ├── comment_like_analysis.py    # 点赞数分析
│   ├── top_keyword_analysis.py    # 关键词话题分析
│   └── stopwords.txt             # 中文停用词表
├── data_raw/                 # 原始数据存储
├── data_processed/           # 清洗后数据存储
└── README.md
```

## 技术栈

- **Web爬虫**: Selenium WebDriver
- **数据处理**: pandas, openpyxl
- **中文处理**: jieba, SnowNLP
- **数据可视化**: matplotlib, seaborn
- **机器学习**: scikit-learn (K-Means聚类)
- **网络分析**: NetworkX
- **词云生成**: WordCloud

## 安装依赖

```bash
pip install selenium pandas openpyxl jieba snownlp matplotlib seaborn scikit-learn networkx wordcloud
```

## 使用方法

### 1. 数据采集
```python
# 修改data_acquisition.py中的登录信息
# 运行爬虫采集评论数据
python data_acquisition/data_acquisition.py
```

### 2. 数据清洗
```python
# 清洗原始数据
python data_cleansing/data_cleansing.py
```

### 3. 数据分析
```python
# 情感分析
python analysis/sentiment_analysis.py

# 活跃度分析
python analysis/comment_activity_analysis.py

# 点赞分析
python analysis/comment_like_analysis.py

# 关键词分析
python analysis/top_keyword_analysis.py
```

## 数据字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | int | 评论唯一标识 |
| contents | str | 评论内容文本 |
| parent_id | str | 父评论ID（顶级评论为'null'） |
| pubdate | str | 评论发布时间 |
| like_count | int | 评论点赞数 |

## 分析结果示例

- **情感分析**：识别评论的情感倾向，统计正面/负面/中立评论比例
- **活跃时段**：发现用户评论的高峰时间段，如晚间8-10点
- **热门话题**：通过关键词网络分析识别讨论热点
- **用户行为**：分析点赞数与评论长度、情感的关系

## 注意事项

1. **合规使用**：请遵守B站robots.txt协议和相关法律法规
2. **频率控制**：建议在爬取时添加适当延时，避免对服务器造成压力
3. **账号安全**：使用时请注意保护个人账号信息
4. **字体设置**：确保系统已安装中文字体（如SimHei）以正确显示图表

## 开发环境

- Python 3.7+
- Windows 10/11
- Microsoft Edge WebDriver

## 贡献

欢迎提交Issue和Pull Request来改进项目功能。

## 许可证

本项目仅用于学术研究和学习目的。

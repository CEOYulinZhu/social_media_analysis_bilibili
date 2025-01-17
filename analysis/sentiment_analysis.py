# 情感分析
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from snownlp import SnowNLP

# 读取表格数据显示设置
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.width', None)  # 不限宽度，显示整齐
pd.set_option('display.max_colwidth', None)  # 显示完整内容

# 加载评论数据
data = pd.read_excel('../data_processed/7.xlsx')
print(data.head(n=1))


# 使用 snownlp 进行情感分析
def snownlp_sentiment(text):
    s = SnowNLP(str(text))
    return s.sentiments  # 返回一个浮动值0-1， 0为负面，1为正面


# 对所有评论进行情感分析
data['sentiment_score'] = data['contents'].apply(snownlp_sentiment)

# -可视化展示
# 设置中文字体
# matplotlib.rcParams['font.family'] = 'Microsoft YaHei'  # 或其他支持中文的字体
# matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题
# 设置Seaborn的绘图风格
# 明确指定Seaborn使用支持中文的字体 whitegrid ，是其中的一种风格，它会在图表北京添加白色网格，更容易地查看图中的数据分布
sns.set(style="whitegrid", font='Microsoft YaHei', rc={"axes.unicode_minus": False})

# 绘制情感得分的分布图（直方图）
plt.figure(figsize=(10, 6))  # 创建一个新的图形窗口并设置图表的大小。figsize参数指定了图表的宽度和高度。单位是英寸
# 核心部分
sns.histplot(data['sentiment_score'], bins=30, kde=True, color='skyblue', stat='density')
plt.title('情感得分分布', fontsize=15)  # 设置图表标题
plt.xlabel('情感得分（0：负面，1：正面）', fontsize=12)  # 设置x轴标签
plt.ylabel('密度', fontsize=12)  # 设置y轴标签
plt.show()


# 情感得分标签（正面/负面/中立）饼图
# 根据情感得分分类：正面/负面/中立
def sentiment_label(score):
    if score > 0.7:
        return '正面'
    elif score < 0.3:
        return '负面'
    else:
        return '中立'


# 打标签
data['sentiment_label'] = data['sentiment_score'].apply(sentiment_label)

# 计算每个标签的数量
sentiment_counts = data['sentiment_label'].value_counts()
print(f"sentiment_counts {sentiment_counts}")

# 绘制饼图
plt.figure(figsize=(8, 8))
# %1.1f 表示保留百分比小数点后保留1位  %%表示百分号字符本身 startangle设置饼图的起始角度，单位是度 colors指定饼图每一步的颜色
sentiment_counts.plot.pie(autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff6666', '#ffff66'])
plt.title('情感标签分布')  # 图表标题
plt.ylabel('')  # 去除y轴标签
plt.show()

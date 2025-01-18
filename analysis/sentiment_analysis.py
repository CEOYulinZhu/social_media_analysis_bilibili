# 情感分析

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from snownlp import SnowNLP


def load_data(file_path):
    """
    加载评论数据
    :param file_path: 评论数据的文件路径
    :return: 数据框df
    """
    # 读取表格数据显示设置
    pd.set_option('display.max_columns', None)  # 显示所有列
    pd.set_option('display.width', None)  # 不限宽度，显示整齐
    pd.set_option('display.max_colwidth', None)  # 显示完整内容

    df = pd.read_excel(file_path)
    print(df.head(n=1))  # 测试

    return df


def snownlp_sentiment(text):
    """
    使用 snownlp 进行情感分析
    :param text: 要进行情感分析的文本
    :return: 0-1的浮动值， 0：负面 1：正面
    """
    s = SnowNLP(str(text))
    return s.sentiments  # 返回一个浮动值0-1， 0为负面，1为正面


def sentiment_label(score):
    """
    根据情感得分进行分类：正面/负面/中立
    :param score:
    :return:
    """
    if score > 0.7:
        return '正面'
    elif score < 0.3:
        return '负面'
    else:
        return '中立'


# -可视化展示
def plot_sentiment_distribution():
    """
    绘制并展示情感得分的分布图（直方图）
    :return: 无
    """

    # 绘制情感得分的分布图（直方图）
    plt.figure(figsize=(10, 6))  # 创建一个新的图形窗口并设置图表的大小。figsize参数指定了图表的宽度和高度。单位是英寸
    # 核心部分  bins参数指定直方图的柱状条数 kde=True kde（核密度估计）在直方图上叠加一条平滑的概率密度曲线
    # stat='density' 表示直方图的y轴显示的概率密度，而不是频次，这样能够消除频率图带来的样本数量差异的影响
    sns.histplot(data['sentiment_score'], bins=10, kde=True, color='skyblue', stat='density')
    plt.title('情感得分分布', fontsize=15)  # 设置图表标题
    plt.xlabel('情感得分（0：负面，1：正面）', fontsize=12)  # 设置x轴标签
    plt.ylabel('密度', fontsize=12)  # 设置y轴标签
    plt.show()


def plot_sentiment_pie():
    """
    绘制并展示情感得分的饼状图
    :return: 无
    """
    # 打标签
    data['sentiment_label'] = data['sentiment_score'].apply(sentiment_label)

    # 计算每个标签的数量
    sentiment_counts = data['sentiment_label'].value_counts()
    # print(f"sentiment_counts {sentiment_counts}")

    # 绘制饼图
    plt.figure(figsize=(8, 8))
    # %1.1f 表示保留百分比小数点后保留1位  %%表示百分号字符本身 startangle设置饼图的起始角度，单位是度 colors指定饼图每一步的颜色
    sentiment_counts.plot.pie(autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff6666', '#ffff66'])
    plt.title('情感标签分布')  # 图表标题
    plt.ylabel('')  # 去除y轴标签
    plt.show()


def plot_comment_sentiment_trends():
    """
    绘制并展示评论与情感得分的时间趋势的折线图
    :return: 无
    """
    # 转换评论时间为datetime格式
    # errors='coerce' 遇到无法转换的值，将其转换为NaT（Not a Time）
    data['pubdate'] = pd.to_datetime(data['pubdate'], errors='coerce')

    # 按日期进行分组，统计每日评论数量及平均情感得分
    # groupby 根据某一列或多个列对数据进行分组
    # .dt 是 pandas 中的日期时间属性访问器，可以提取年份、日期、时间
    # .data 获取的是日期（年月日）
    # agg 是一个聚合函数 ，用于对分组后的数据执行多个操作，将数据根据每个日期分组后，执行不同的聚合操作，生成两个新的列
    daily_data = data.groupby(data['pubdate'].dt.date).agg(
        daily_count=('contents', 'count'),  # count 表示对每个分组的contents列进行计数操作
        avg_sentiment=('sentiment_score', 'mean')  # mean 是求均值的聚合方法 对每个分组的sentiment_score列进行求均值
    ).reset_index()  # 重置索引为默认索引 groupby 操作会将分组的列作为新的索引

    # 绘制评论数量与平均情感得分时间趋势图
    # plt.subplots 创建一个新的图形（Figure)和一组子图（Axes)
    # fig 图形对象 ax1 坐标轴对象（即子图）
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # 评论数量趋势
    ax1.set_xlabel('日期', fontsize=12)
    ax1.set_ylabel('评论数量', fontsize=12,
                   color='tab:blue')  # tab:blue 使用 matplotlib 中名为 tab的调色板中的蓝色，tab是一个简洁且有条理的颜色系列
    ax1.plot(daily_data['pubdate'], daily_data['daily_count'], color='tab:blue', label='评论数量')
    # 自定义坐标轴的刻度标签的样式
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # 平均情感得分趋势
    ax2 = ax1.twinx()  # twinx() 方法会返回一个新的坐标轴对象，它与原坐标轴ax1共享一个x轴
    ax2.set_ylabel('平均情感得分', fontsize=12, color='tab:green')
    ax2.plot(daily_data['pubdate'], daily_data['avg_sentiment'], color='tab:green', label='平均情感得分')
    ax2.tick_params(axis='y', labelcolor='tab:green')

    plt.title('评论数量与情感得分的时间趋势', fontsize=15)
    plt.show()


def plot_sentiment_like_scatter():
    """
    绘制并展示情感得分与点赞数关系的散点图
    :return:
    """
    plt.figure(figsize=(10, 6))

    # 绘制散点图
    sns.scatterplot(x=data['sentiment_score'], y=data['like_count'], color='orange')

    plt.title('情感得分与点赞数的关系', fontsize=15)
    plt.xlabel('情感得分', fontsize=12)
    plt.ylabel('点赞数', fontsize=12)
    plt.show()


def plot_sentiment_like_heatmap():
    """
    绘制并展示情感得分与点赞数相关性的热图
    :return: 无
    """
    # 计算皮尔逊相关系数
    # corr 计算数值框中数值型列之间的 皮尔逊相关系数
    correlation = data[['sentiment_score', 'like_count']].corr()
    print(f"type(correlation) {type(correlation)}")
    print(f"情感得分与点赞数的相关系数：\n{correlation}")

    # 可视化相关性矩阵，绘制热图
    plt.figure(figsize=(6, 5))
    # 绘制热图
    # annot=True 表示在热图的每个单元格内显示数值（相关系数的数值），默认情况下热图只显示颜色
    # cmap 指定热图的颜色映射方案
    # vmin vmax 设置热图颜色映射的数值范围
    sns.heatmap(correlation, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('情感得分与点赞数的相关性')
    plt.show()


if __name__ == '__main__':
    # 加载评论数据
    data = load_data(file_path='../data_processed/7.xlsx')

    # 设置Seaborn的绘图风格
    # 明确指定Seaborn使用支持中文的字体 whitegrid ，是其中的一种风格，它会在图表北京添加白色网格，更容易地查看图中的数据分布
    sns.set(style="whitegrid", font='SimHei', rc={"axes.unicode_minus": False})
    # 对所有评论进行情感分析
    data['sentiment_score'] = data['contents'].apply(snownlp_sentiment)

    # 测试
    plot_sentiment_distribution()
    plot_comment_sentiment_trends()
    plot_sentiment_pie()
    plot_sentiment_like_scatter()
    plot_sentiment_like_heatmap()

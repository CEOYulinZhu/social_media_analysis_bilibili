# 评论活跃度分析

import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def load_data(file_path):
    """
    加载评论数据，并将评论时间转换为datetime格式
    :param file_path: 评论数据的文件路径
    :return: 数据框df
    """
    df = pd.read_excel(file_path)
    df['pubdate'] = pd.to_datetime(df['pubdate'], errors='coerce')
    df['日期'] = df['pubdate'].dt.date
    df['小时'] = df['pubdate'].dt.hour
    return df


def plot_daily_comments(df):
    """
    按日期绘制评论数量变化趋势图
    :param df: 数据框df，包含评论数据
    """
    daily_comments = df.groupby('日期').size()
    plt.figure(figsize=(10, 6))
    daily_comments.plot(kind='line', title='评论数量变化趋势', xlabel='日期', ylabel='评论数量')
    plt.xticks(rotation=45)
    plt.show()


def plot_hourly_comments(df):
    """
    按小时绘制评论数量分布的柱状图
    :param df: 数据框df，包含评论数据
    """
    hourly_comments = df.groupby('小时').size()
    plt.figure(figsize=(10, 6))
    hourly_comments.plot(kind='bar', title='评论数量按小时分布', xlabel='小时', ylabel='评论数量')
    plt.xticks(rotation=0)
    plt.show()


def plot_active_points(df, threshold=100):
    """
    根据评论数量的差异，找出评论数剧烈变化的点，并绘制带标记的评论数量趋势图
    :param df: 数据框df，包含评论数据
    :param threshold: 设定评论数量变化的阈值，默认值为100
    """
    daily_comments = df.groupby('日期').size()
    comment_diff = daily_comments.diff()
    activity_peaks = comment_diff[comment_diff > threshold]

    plt.figure(figsize=(10, 6))
    daily_comments.plot(kind='line', title='评论数量变化趋势', xlabel='日期', ylabel='评论数量')
    plt.scatter(activity_peaks.index, activity_peaks.values, color='red', label='活跃点')
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()


def plot_activity_clusters(df):
    """
    使用KMeans聚类分析评论活跃的时间段，并绘制聚类结果
    :param df: 数据框df，包含评论数据
    """
    # 删除包含NaN 的行
    df = df.dropna(subset=['小时'])
    X = df[['小时']].values
    kmeans = KMeans(n_clusters=3)  # 聚成3个类
    df['活跃段'] = kmeans.fit_predict(X)

    plt.figure(figsize=(10, 6))
    df.groupby('小时').size().plot(kind='bar', color=df['活跃段'].map({0: 'blue', 1: 'green', 2: 'red'}),
                                   title='评论数量按小时和活跃段分布', xlabel='小时', ylabel='评论数量')
    plt.xticks(rotation=0)
    plt.show()


if __name__ == '__main__':

    # 设置中文字体为 SimHei（黑体），解决乱码问题
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    # 设置负号正常显示
    matplotlib.rcParams['axes.unicode_minus'] = False

    # 目标文件路径
    file_path = '../data_processed/7.xlsx'  # 请替换成你实际的文件路径

    # 加载数据
    df = load_data(file_path)

    # 绘制评论数量变化趋势图
    plot_daily_comments(df)

    # 绘制评论数量按小时分布的图
    plot_hourly_comments(df)

    # 绘制带有活动点标记的评论数量趋势图
    plot_active_points(df, threshold=100)

    # 绘制聚类结果
    plot_activity_clusters(df)

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


# 读取评论数据 (假设文件名为 'comments.xlsx')
def load_data(file_path):
    """
    加载评论数据，并将评论时间转换为datetime格式。
    :param file_path: 评论数据的文件路径
    :return: 数据框df
    """
    df = pd.read_excel(file_path)
    df['评论时间'] = pd.to_datetime(df['评论时间'], errors='coerce')
    df['日期'] = df['评论时间'].dt.date
    df['小时'] = df['评论时间'].dt.hour
    return df


# 按日期绘制评论数量变化趋势
def plot_daily_comments(df):
    """
    按日期绘制评论数量变化趋势图。
    :param df: 数据框df，包含评论数据
    """
    daily_comments = df.groupby('日期').size()
    plt.figure(figsize=(10, 6))
    daily_comments.plot(kind='line', title='评论数量变化趋势', xlabel='日期', ylabel='评论数量')
    plt.xticks(rotation=45)
    plt.show()


# 按小时绘制评论数量分布图
def plot_hourly_comments(df):
    """
    按小时绘制评论数量分布的柱状图。
    :param df: 数据框df，包含评论数据
    """
    hourly_comments = df.groupby('小时').size()
    plt.figure(figsize=(10, 6))
    hourly_comments.plot(kind='bar', title='评论数量按小时分布', xlabel='小时', ylabel='评论数量')
    plt.xticks(rotation=0)
    plt.show()


# 绘制带有活动点标记的评论数量趋势图
def plot_active_points(df, threshold=100):
    """
    根据评论数量的差异，找出评论数剧烈变化的点，并绘制带标记的评论数量趋势图。
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


# 聚类分析：按小时绘制评论时间段活跃的分布
def plot_activity_clusters(df):
    """
    使用KMeans聚类分析评论活跃的时间段，并绘制聚类结果。

    :param df: 数据框df，包含评论数据
    """
    X = df[['小时']].values
    kmeans = KMeans(n_clusters=3)  # 聚成3个类
    df['活跃段'] = kmeans.fit_predict(X)

    plt.figure(figsize=(10, 6))
    df.groupby('小时').size().plot(kind='bar', color=df['活跃段'].map({0: 'blue', 1: 'green', 2: 'red'}),
                                   title='评论数量按小时和活跃段分布', xlabel='小时', ylabel='评论数量')
    plt.xticks(rotation=0)
    plt.show()


# 主函数：加载数据并绘制所有分析图
def main(file_path):
    """
    主函数，加载数据并绘制所有分析图。

    :param file_path: 评论数据的文件路径
    """
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


# 调用主函数，传入文件路径
if __name__ == '__main__':
    file_path = 'comments.xlsx'  # 请替换成你实际的文件路径
    main(file_path)

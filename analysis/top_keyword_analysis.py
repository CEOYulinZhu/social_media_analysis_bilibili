# 热门关键词分析和话题分析

from collections import Counter
from itertools import combinations

import jieba
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


def load_data(file_path):
    """
    加载评论数据
    :param file_path: 评论数据的文件路径
    :return: 数据框df
    """
    df = pd.read_excel(file_path)
    return df


def clean_data(data):
    # 数据预处理：填充缺失值并确保为字符串
    data['contents'] = data['contents'].fillna('').astype(str)
    return data


def load_stopwords(stopwords_path='./stopwords.txt'):
    """
    加载停用词文件
    :param stopwords_path: str, 停用词文件路径
    :return: set, 停用词集合
    """
    try:
        with open(stopwords_path, 'r', encoding='utf-8') as f:
            return set([line.strip() for line in f])
    except FileNotFoundError:
        print("警告：未找到停用词文件，将跳过停用词过滤。")
        return set()


def extract_keywords(data, stopwords, top_n=20):
    """
    提取高频关键词
    :param data: pd.DataFrame, 包含评论内容的数据
    :param stopwords: set, 停用词集合
    :param top_n: int, 要提取的关键词数量
    :return: list of tuples, 关键词及其频率
    """
    # 拼接所有评论内容
    text = ' '.join(data['contents'])
    words = [word for word in jieba.cut(text) if word not in stopwords and len(word) > 1]
    # 统计词频
    word_counts = Counter(words)
    return word_counts.most_common(top_n)


def generate_topic_network(data, keywords, stopwords, min_cooccurrence=5):
    """
    根据评论生成关键词共现的话题网络。
    :param data: pd.DataFrame, 包含评论内容的 DataFrame
    :param keywords: list, 关键词列表
    :param stopwords: list, 停用词列表
    :param min_cooccurrence: int, 共现次数的最小阈值
    """

    # 提取关键词
    comments = data['contents']

    # 创建一个计数器，用于存储每对关键词的共现次数
    cooccurrence = Counter()

    # 遍历每一条评论
    for comment in comments:
        # 对每条评论进行分词，筛选出在关键词列表中且不在停用词列表中的词
        words = [word for word in jieba.cut(comment) if word in keywords and word not in stopwords]

        # 更新每对关键词的共现次数
        # combinations() 生成二元组
        cooccurrence.update(combinations(set(words), 2))

    # -构建共现网络
    # 创建一个无向图，用于存储共现的关键词之间的关系
    graph = nx.Graph()

    # 遍历每对关键词及其共现次数
    for (word1, word2), count in cooccurrence.items():
        # 只有共现次数大于 min_cooccurrence时，才建立边
        if count >= min_cooccurrence:
            # 在图中添加一条边，边的权重为共现次数
            graph.add_edge(word1, word2, weight=count)

    # -可视化网络
    # 使用spring_layout布局来确定节点位置 spring_layout 是一种常见的力导向布局算法，通过模拟节点间的弹簧力来调整节点的位置，使得图看起来更美观
    # k是节点之间的吸引力（相当于弹簧的强度）
    # iterations控制迭代次数，力导向算法通过迭代优化节点的位置，使得每个节点的总力接近平衡状态，直到达到一个稳定的布局
    pos = nx.spring_layout(graph, k=0.5, iterations=50)

    # 控制边的宽度 log(weight + 1)是为了避免共现次数为 0 时，边宽为0
    edge_widths = [min(np.log(weight + 1), 10) for _, _, weight in graph.edges(data='weight')]  # 控制边宽

    # 设置图像大小
    plt.figure(figsize=(15, 10))

    # 绘制节点
    nx.draw_networkx_nodes(graph, pos, node_size=1000, node_color="lightblue", alpha=0.9)

    # 绘制边
    nx.draw_networkx_edges(graph, pos, width=edge_widths, alpha=0.7, edge_color="black")

    # 绘制节点标签（显示关键词）
    nx.draw_networkx_labels(graph, pos, font_size=12, font_color="black")

    plt.title("关键词共现话题网络", fontsize=16)
    # 去掉坐标轴
    plt.axis("off")
    # 显示图像
    plt.show()


if __name__ == "__main__":
    # 设置中文字体，解决中文乱码问题
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']

    # 加载评论数据
    data = load_data('../data_processed/3.xlsx')

    # 数据清洗
    data = clean_data(data)

    # 加载停用词
    stopwords = load_stopwords('stopwords.txt')

    # 提取高频关键词
    top_keywords = extract_keywords(data, stopwords, top_n=15)
    print("高频关键词：", top_keywords)

    # 生成话题网络
    # 是用列表推导式从top_keywords中提取出每个关键词，以便进行话题网络的生成
    generate_topic_network(data, [kw[0] for kw in top_keywords], stopwords, min_cooccurrence=5)

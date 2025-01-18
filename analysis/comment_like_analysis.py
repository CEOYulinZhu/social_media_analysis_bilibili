import jieba
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from wordcloud import WordCloud


# 加载数据函数
def load_data(file_path):
    """
    加载xlsx文件并返回数据框。
    :param file_path: str, 文件路径
    :return: pd.DataFrame, 数据框
    """
    data = pd.read_excel(file_path)
    return data


# 数据清洗函数
def clean_data(data):
    """
    清洗数据，处理缺失值和异常值。
    :param data: pd.DataFrame, 原始数据
    :return: pd.DataFrame, 清洗后的数据
    """
    # 删除空值
    data = data.dropna(subset=['contents', 'like_count'])

    # # 剔除异常点赞数（如超过 99.9% 分位数）
    # upper_limit = data['like_count'].quantile(0.999)
    # data = data[data['like_count'] <= upper_limit]

    return data


# 点赞数分布绘图函数
def plot_like_distribution(data):
    """
    绘制点赞数分布图和箱线图。
    :param data: pd.DataFrame, 数据框
    """
    # 绘制直方图
    plt.figure(figsize=(10, 6))
    sns.histplot(data['like_count'], bins=50, kde=True, color='skyblue')
    plt.title('点赞数分布', fontsize=14)
    plt.xlabel('点赞数', fontsize=12)
    plt.ylabel('评论数量', fontsize=12)
    plt.show()

    # 绘制箱线图
    plt.figure(figsize=(10, 6))
    sns.boxplot(data['like_count'], color='lightcoral')
    plt.title('点赞数箱线图', fontsize=14)
    plt.show()


# 热门评论提取函数
def get_top_comments(data, top_n=10):
    """
    提取点赞数最高的评论。
    :param data: pd.DataFrame, 数据框
    :param top_n: int, 前N条评论
    :return: pd.DataFrame, 热门评论
    """
    top_comments = data.sort_values(by='like_count', ascending=False).head(top_n)
    return top_comments


# 评论内容关键词分析函数
def generate_wordcloud(data, font_path='msyh.ttc', stopwords_path='./stopwords.txt'):
    """
    生成热门评论的词云，并剔除无意义的助词。
    :param data: pd.DataFrame, 数据框
    :param font_path: str, 字体路径
    :param stopwords_path: str, 停用词文件路径
    """
    # 拼接所有热门评论内容
    text = ' '.join(data['contents'])

    # 加载停用词
    try:
        with open(stopwords_path, 'r', encoding='utf-8') as f:
            stopwords = set([line.strip() for line in f])
    except FileNotFoundError:
        stopwords = set()
        print("警告：未找到停用词文件，停用词过滤将被跳过。")

    # 分词并过滤停用词
    words = [word for word in jieba.cut(text) if word not in stopwords and len(word) > 1]

    # 转换为字符串
    filtered_text = ' '.join(words)

    # 绘制词云
    wordcloud = WordCloud(font_path=font_path, background_color='white', width=800, height=400).generate(filtered_text)

    # 展示词云
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


# 点赞数与内容长度关系分析函数
def analyze_length_vs_likes(data):
    """
    分析评论内容长度与点赞数的关系。
    :param data: pd.DataFrame, 数据框
    """
    # 计算评论长度
    data['content_length'] = data['contents'].str.len()

    # 绘制散点图
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=data['content_length'], y=data['like_count'], alpha=0.7, color='green')
    plt.title('点赞数与评论长度的关系', fontsize=14)
    plt.xlabel('评论长度', fontsize=12)
    plt.ylabel('点赞数', fontsize=12)
    plt.show()


if __name__ == '__main__':
    # 文件路径
    file_path = '../data_processed/7.xlsx'  # 替换为实际文件路径

    # 加载数据
    data = load_data(file_path)

    # 数据清洗
    data = clean_data(data)

    # 设置中文字体，解决乱码问题
    sns.set(style="whitegrid", font='SimHei', rc={"axes.unicode_minus": False})

    # 分析点赞数分布
    plot_like_distribution(data)

    # 提取热门评论
    top_comments = get_top_comments(data, top_n=50)
    print("热门评论：")
    print(top_comments[['contents', 'like_count']])

    # 生成词云
    generate_wordcloud(top_comments)

    # 分析点赞数与内容长度关系
    analyze_length_vs_likes(data)

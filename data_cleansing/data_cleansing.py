
import pandas as pd
import re
from pathlib import Path


# 去除评论内容为空的数据
def remove_empty(df):
    return df[df['contents'].notna()]


# 定义去除表情的正则表达式
def remove_emojis(text):
    # 只匹配常见的表情符号范围
    emoji_pattern = re.compile(
        "[\U0001F600-\U0001F64F"  # 表情符号
        "\U0001F300-\U0001F5FF"  # 符号和图像
        "\U0001F680-\U0001F6FF"  # 交通和地图符号
        "\U0001F700-\U0001F77F"  # 炼金符号
        "\U0001F780-\U0001F7FF"  # 几何图形扩展
        "\U0001F800-\U0001F8FF"  # 辅助箭头-C
        "\U0001F900-\U0001F9FF"  # 补充符号和图像
        "\U0001FA00-\U0001FA6F"  # 国际象棋符号
        "\U0001FA70-\U0001FAFF"  # 符号和图像扩展-A
        "]+", flags=re.UNICODE)  # 仅删除表情符号
    return emoji_pattern.sub(r'', str(text))  # 替换为''，即删除表情符号


# 去除回复部分的提示如‘回复@用户昵称：’这部分内容
def remove_replies(text):
    # 使用正则表达式去除以“回复”开头，以冒号结尾的部分
    return re.sub(r'^回复.*?:', '', text)


# 存储数据的文件夹
data_path = Path('../data_raw')
file_index = 1  # 文件名前缀
# 遍历文件夹
for file in data_path.iterdir():
    # 检测是否是文件,并且后缀为.xlsx 的表格
    if file.is_file() and file.suffix == '.xlsx':
        print(file)
        print(type(file))
        df = pd.read_excel(file)
        df = remove_empty(df=df)
        df['contents'] = df['contents'].apply(remove_replies)
        df['contents'] = df['contents'].apply(remove_emojis)

        # 保存处理后的数据
        df.to_excel(f'../data_processed/{file_index}.xlsx', index=False)
        file_index = file_index + 1


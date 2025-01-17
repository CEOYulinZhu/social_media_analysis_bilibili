# 情感分析

import pandas as pd
from snownlp import SnowNLP

# 读取表格数据显示设置
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.width', None)  # 不限宽度，显示整齐
pd.set_option('display.max_colwidth', None)  # 显示完整内容

# 加载评论数据
data = pd.read_excel('../data_raw/【 Six Degrees  官方MV 】派伟俊 & 周杰伦 命定浪漫合作曲.xlsx')
print(data.head(n=10))


# 使用 snownlp 进行情感分析
def snownlp_sentiment(text):
    s = SnowNLP(str(text))
    return s.sentiments  # 返回一个浮动值0-1， 0为负面，1为正面


# 测试
print(f">>> '就听个歌，开心开心，不知道为啥总有人出来拉踩' 情感得分：{snownlp_sentiment('讨饭狗被戳穿了又破防撒泼打滚了🤣🤣陶狗蜜碰瓷三件套之一的“苞米”也是如期而至了🤣🤣')}")

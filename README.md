# my_friends_wechat

从微信获取好友信息

## 读取好友们的微信签名，并制作词云

有人说看一个人是什么样子的，旧卡岸他的朋友是什么样子的。于是我把我的微信好友的签名做了一个词云，看看我的朋友们最近都在说什么，这大概也就是我现在的样子吧。

运行：

```bash
# 克隆仓库
git clone https://github.com/thiswind/my_friends_wechat.git

# 进入到克隆下来的仓库当中
cd my_friends_wechat

# 安装依赖
pip3 install --user -r requirements.txt # 安装依赖

# 运行程序
python3 get_friends_signature_word_cloud.py # 生成词云
```

将生成相应的html文件


## 运行截图

![](https://github.com/thiswind/my_friends_wechat/raw/master/assets/9b3a9464.png)
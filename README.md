# 支付宝支付微框架

## 简述
此项目目的是提供:

- 支付宝支付「简洁」API，简化参数
- 记录与支付宝交互相关数据
- 集合各种支付能力的接口，统一管理
- 灵活且扩展

## 功能
### 可支持支付能力

- [x] 手机网站支付
- [ ] 电脑网站支付
- [ ] 当面付
- [ ] ~~App支付~~

### Admin系统
- [ ] 查看交易订单详情
- [ ] 数据统计


## 使用

1、生成RSA密钥，使用`scripts/generate_RSA.py`或者使用[支付宝提供一键生成工具](ttps://doc.open.alipay.com/docs/doc.htm?treeId=291&articleId=105971&docType=1)，把应用公钥和私钥分别保存在`config/app_public_key.crt`和`config/app_private_key.crt`文件上

2、前往支付宝开放平台开发者中心进行密钥配置，提供自己的公钥，配置完成后可以获取支付宝公钥，把支付宝的公钥保存在`config/ali_public_key.crt`文件上

3、启动`MySql Server`，并在`config`文件夹下，找到对应的env配置文件配置好`db`的相关信息（username、password、host等）

4、初始化数据库

```
# 在alipay/alipay文件夹下
PYTHONPATH=. alembic -c config/alembic.ini revision --autogenerate -m "your comment"

PYTHONPATH=. alembic -c config/alembic.ini upgrade head
```

5、运行测试代码

```
# 在alipay/alipay/tests文件夹下
python runtests
```

6、假如测试都通过，则可以启动应用程序

```
python server.py --port=8080 --env=local
```

命令行参数描述

Arguments | Description | Value
------ | ------- | --------
port | 端口号 |
env | 环境 | local\|qa\|prod

7、如果是本地测试环境，为了能支持支付宝回调，体验整个流程，需要使用**内网穿透**技术

- natapp
- nginx

在`config/app.config.py`配置`PROXY_HOST`
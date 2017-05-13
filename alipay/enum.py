# coding=utf-8

def enum(name, **named):
    return type(str(name), (), dict(**named))

TradeStatus = enum(
    "TradeStatus",
    PENDING=0,      # 交易创建，等待买家付款
    CLOSED=1,       # 未付款交易超时关闭
    SUCCESS=2,      # 交易支付成功
    FINISHED=3,     # 交易结束，不可退款
    REFUND=4,       # 支付完成后全额退款
)

ChannelType = enum(
    "ChannelType",
    WAP=0,          # 手机网站支付
    WEB=1,
)

ProductType = enum(
    "ProductType",
    IMMATERIAL=0,   # 虚拟类商品
    MATERIAL=1,     # 实物类商品
)
import requests
import time
import hmac
import hashlib
import base64
import urllib.parse
import random
import json
import time

def init_txt():
    name = ["商品到货：", "购物车价格:", "最优下单价格:", "最优下单数量:",
            "最优下单总金额:", "原始价格:", "商品库存:", "商品sku:",
            "商品活动:", "优惠券:", "链接:", "历史最低价:", "数据获取时间:", "区域:"]
    all_name = ""
    with open("all.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        id = data.keys()
        print(id)
        for idx in id:
            # print(len(json_data))
            # print(ls)
            # print("-----------------------------------------")
            try:
                all_name +=  "商品到货：" + data[idx]['name'] + "\n" +\
                           "购物车价格:" + str(data[idx]['price']) + "\n" +\
                            "最优下单价格:" + str(data[idx]['best_price']) + "\n" +\
                           "最优下单数量:" + str(data[idx]['num']) + "\n" + \
                           "最优下单总金额:" + str(data[idx]['best_price']) + "\n" + \
                           "原始价格:" + str(data[idx]['price']) + "\n" + \
                           "商品库存:" + data[idx]['kc'] + "\n" + \
                           "商品sku:" + data[idx]['sku'] + "\n" + \
                            "商品活动:" + data[idx]['cx'] + "\n" + \
                             "优惠券:" + data[idx]['counpon'] + "\n" + \
                             "链接:" + data[idx]['url'] + "\n" + \
                          "历史最低价:" + str(data[idx]['lower']) + "\n" + \
                            "数据获取时间:" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "\n" + \
                            "区域:" + "湖南娄底市双峰县洪山殿镇" + "\n" + "\n"
            except Exception as e:
                print("json数据格式不正确：" + str(e))

    return all_name

def change(ls):
    name = ["商品到货：", "购物车价格:", "最优下单价格:", "最优下单数量:",
            "最优下单总金额:", "原始价格:", "商品库存:", "商品sku:",
            "商品活动:", "优惠券:", "链接:", "数据获取时间:", "区域:"]
    tmp = ls
    print(tmp)
    all_name = ""

    for idx in range(len(name)):
        if idx != 0:
            all_name += '\n'
        all_name += (name[idx] + str(tmp[idx]))
    send_message(all_name)
    print(all_name)

def add(ls):
    name = ["新增商品：", "购物车价格:", "最优下单价格:", "最优下单数量:",
            "最优下单总金额:", "原始价格:", "商品库存:", "商品sku:",
            "商品活动:", "优惠券:", "链接:", "数据获取时间:", "区域:"]
    tmp = ls
    print(tmp)
    all_name = ""

    for idx in range(len(name)):
        if idx != 0:
            all_name += '\n'
        all_name += (name[idx] + str(tmp[idx]))
    print(all_name)
    send_message(all_name)


    # all_name = ""
    #
    # all_name += "新增商品：" + data[idx]['name'] + "\n" + \
    #             "购物车价格:" + str(data[idx]['price']) + "\n" + \
    #             "最优下单价格:" + str(data[idx]['best_price']) + "\n" + \
    #             "最优下单数量:" + str(data[idx]['num']) + "\n" + \
    #             "最优下单总金额:" + str(data[idx]['best_price']) + "\n" + \
    #             "原始价格:" + str(data[idx]['price']) + "\n" + \
    #             "商品库存:" + data[idx]['kc'] + "\n" + \
    #             "商品sku:" + data[idx]['sku'] + "\n" + \
    #             "商品活动:" + data[idx]['cx'] + "\n" + \
    #             "优惠券:" + data[idx]['counpon'] + "\n" + \
    #             "链接:" + data[idx]['url'] + "\n" + \
    #             "数据获取时间:" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "\n" + \
    #             "区域:" + "湖南娄底市双峰县洪山殿镇" + "\n" + "\n"
    # #
    # send_message(all_name)
    # print(all_name)
    # print('ttt')



def get_sign(secret):
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign


def send(text):
    pass


def send_message(text):
    te = text.split("商品到货")
    tt = ""
    if te[0] != '':
        te = text.split("新增商品")
        for t in range(1, len(te)):
            i = te[t]
            i = "新增商品" + i
            tt += i + '\n'
            if t % 4 == 0 or t == len(te) - 1:
                # print(t)
                send(tt)
                time.sleep(4)
                tt = ""
        print("sending________")
    else:
        for t in range(1, len(te)):
            i = te[t]
            i = "商品到货" + i
            tt += i + '\n'
            if t % 4 == 0 or t == len(te)-1:
                # print(t)
                send(tt)
                time.sleep(4)
                tt = ""
        print("sending........")

def solve():
    text = init_txt()
    print(text)
    send_message(text)

def main():
    text = init_txt()
    print(text)
    send_message(text)


if __name__ == '__main__':
    solve()
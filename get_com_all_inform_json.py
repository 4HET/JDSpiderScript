import requests
import re
import json
import time
import send_message
import login


begin = ''
inform = {}
lower = {}
dic = {}

"""
第一步
获取购物车所有商品信息，以json形式存下，方便接下来的数据解析
"""
def get_car(cookie):  # 购物车
    url = "https://p.m.jd.com/cart/cart.action?fromnav=1"
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
        'referer': 'https://home.m.jd.com/',
        'cookie': cookie
    }
    response_data = requests.get(url=url, headers=header).text
    response_data = re.sub("\s", "", response_data)
    data = re.findall('window\.cartData=(.*?)window._PFM_TIMING', response_data)[0]
    data = str(data).strip()
    data = json.loads(data)
    with open('inform.json', 'w', encoding='utf-8') as fp:
        json.dump(data, fp=fp, ensure_ascii=False)
    print(data)

"""
获取优惠券
"""
def get_yh(cookie):    # 优惠券
    t = time.time() * 1000
    zs = int(t)
    xs = (t - zs) * 1000
    url = "https://wq.jd.com/deal/mshopcart/querycoupon?pingouchannel=0&venderid=8888&traceid=1387703542898687811&tabMenuType=1&_=1644749963631&sceneval=2&g_login_type=1&callback=queryCoupon_Cb8770&g_ty=ls"
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
        'referer': 'https://p.m.jd.com/',
        'cookie': cookie
    }
    param = {
        # 'pingouchannel': 0,
        # 'venderid': 8888,
        # 'traceid': int(get_car()),
        # 'tabMenuType': 1,
        # '_': zs,
        # 'sceneval': 2,
        # 'g_login_type': 1,
        # 'callback': 'queryCoupon_Cb' + str(xs),
        # 'g_ty': 'ls'
        'pingouchannel': 0,
        'venderid': 8888,
        'traceid': 1387817101833964961,
        'tabMenuType': 1,
        '_': 1644763717304,
        'sceneval': 2,
        'g_login_type': 1,
        'callback': 'queryCoupon_Cb7885',
        'g_ty': 'ls'
    }
    response_data = requests.get(url=url, headers=header, params=param).text
    response_data = re.sub("\s", "", response_data)
    rep = re.findall('queryCoupon_Cb8770\((.*?)\)', response_data)[0]
    counpon = json.loads(rep)
    for i in range(len(counpon["usableCoupons"])):
        yh = "满{}元减{}元".format(counpon["usableCoupons"][i]["quota"], counpon["usableCoupons"][i]["discount"])
        print(yh)
        print(counpon["usableCoupons"][i]["skuidlist"])
        for j in counpon["usableCoupons"][i]["skuidlist"]:
            try:
                inform[str(j)]["counpon"] += yh
                print("{}写入成功".format(j))
            except:
                print("{}写入失败".format(j))


def input_json_data_from_file(path):
    """
    从文件中获取json数据
    :param path: 文件路径
    :return json_data: 返回转换为json格式后的json数据
    """
    # 从文件中获取json，转化为str
    try:
        with open(path, "r", encoding="utf-8") as f:
            try:
                json_data = json.load(f)
            except Exception as e:
                print("json数据格式不正确：" + str(e))
        return json_data
    except Exception as e:
        print("文件不存在：" + str(e))


def output_value(jsons, key):
    """
    通过参数key，在jsons中进行匹配并输出该key对应的value
    :param jsons: 需要解析的json串
    :param key: 需要查找的key
    :return:
    """
    key_value = ""
    #如果是字典，遍历jsons的所有value，在当前层能找到key，则输出，找不到则去下一层找
    if isinstance(jsons, dict):
        for json_result in jsons.values():
            if key in jsons.keys():
                key_value = jsons.get(key)
            else:
                output_value(json_result, key)
    #如果是列表，则对列表中每个元素执行一遍对字典的操作
    elif isinstance(jsons, list):
        for json_array in jsons:
            output_value(json_array, key)
    # print(key_value)

    for i in key_value:
        if i["polyType"] == "1" or i["polyType"] == "3" or i["polyType"] == "4":
            # print(i)

            for item in i["polyItem"]["products"]:
                # print(item)
                id = item["mainSku"]["id"]
                inform[id] = {}

                inform[id]["name"] = item["mainSku"]["name"]
                inform[id]["url"] = item["mainSku"]["skuItemUrl"]
                inform[id]["price"] = eval(item["jdPrice"])
                _str = ''
                for i in [name["pnote"] for name in item["selectPromotion"]]:
                    _str += i
                inform[id]["cx"] =  _str
                inform[id]["counpon"] = ""
                inform[id]["kc"] = ""

                if item["areaStockState"]["attr_a"] == "34":
                    inform[id]["kc"] = "无货"
                else:
                    inform[id]["kc"] = "有货"
                inform[id]["sku"] = id
                inform[id]["best_num"] = 1
                inform[id]["best_price"] =  eval(item["jdPrice"])
                with open('lower.json', 'r', encoding='utf-8') as fp:
                    data = json.load(fp)
                inform[id]["lower"] = data


def get_best():
    all_id = inform.keys()
    # 计算最便宜的价格
    for i in all_id:
        price = inform[i]["price"]
        cx = inform[i]["cx"]
        counpon = inform[i]["counpon"]
        cou_man = re.findall("满([0-9]*)元减([0-9]*)元", cx)
        cnt = 0
        # 遍历所有满减情况，记录下最大满减的情况，此时最优就是价格减去最大折扣
        for j in range(len(cou_man)):
            if eval(cou_man[j][1]) >= eval(cou_man[cnt][1]):
                cnt = j
        try:
            # print(cx)
            # print("cou_man[cnt][1]:{}".format(cou_man[cnt][1]))
            low_cx = price - eval(cou_man[cnt][1])
        except:
            low_cx = price

        cnt = 0
        cou_meiman = re.findall("每满([0-9]*)元减([0-9]*)元", cx)
        # 遍历每满多少减多少的情况，并进行处理
        for j in range(len(cou_meiman)):
            if eval(cou_meiman[j][1]) >= eval(cou_meiman[cnt][1]):
                cnt = j

        sum = price
        num = 1
        down = price
        try:
            if eval(cou_meiman[cnt][0]) > price:
                num = eval(cou_meiman[cnt][0]) / price + 1
                sum = sum * num - eval(cou_meiman[cnt][1])
                down = sum / num
            elif eval(cou_meiman[cnt][0]) <= price:
                sum = sum - (int(price / eval(cou_meiman[cnt][0]))) * eval(cou_meiman[cnt][1])
                down = sum
                print(i)
                print(sum)
        except:
            sum = price
            num = 1
            down = price

        # 每满几件打折
        cnt = 0
        try:
            cou_meiman = re.findall("满([0-9]*)件总价([0-9]*)折", cx)[-1]
            num = eval(cou_meiman[0])
            sum = eval(cou_meiman[1] * price * 0.1)
            down = sum / num
        except:
            sum = price
            num = 1
            down = price

        # 进行数据更新
        if low_cx > down:
            inform[i]["best_price"] = sum
            inform[i]["num"] = num
        else:
            inform[i]["best_price"] = low_cx
            inform[i]["num"] = 1

        # 处理优惠券
        cnt = 0
        yx = re.findall("满([0-9]*)元减([0-9]*)元", counpon)
        for j in range(len(yx)):
            if eval(yx[j][1]) >= eval(yx[cnt][1]):
                cnt = j

        try:
            inform[i]["best_price"] -= eval(yx[cnt][1])
        except Exception as e:
            pass

        inform[i]["lower"] = min(inform[i]["best_price"], inform[i]["best_price"])

        lower[i] = inform[i]["lower"]

        if i not in begin:
            begin.append(i)
            print("add被调用.....")
            print(i)
            print(begin)
            send_message.add([inform[i]['name'], inform[i]['price'],inform[i]['best_price'],inform[i]['num'],
                                inform[i]['price'],inform[i]['num']*inform[i]['price'],inform[i]['kc'],
                                inform[i]['sku'],inform[i]['cx'],inform[i]['counpon'],inform[i]['url'],
                              str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),"湖南娄底市双峰县洪山殿镇"])

        try:
            if i in begin and (inform[i]['price'] != dic[i]['price'] or inform[i]['kc'] == "无货" and dic[i]['kc'] == "有货"):
                print("add被调用.....")
                print(i)
                print(begin)
                send_message.change([inform[i]['name'], inform[i]['price'], inform[i]['best_price'], inform[i]['num'],
                                  inform[i]['price'], inform[i]['num'] * inform[i]['price'], inform[i]['kc'],
                                  inform[i]['sku'], inform[i]['cx'], inform[i]['counpon'], inform[i]['url'],
                                  str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())), "湖南娄底市双峰县洪山殿镇"])
        except:
            pass


def update_lower():
    with open('lower.json', 'w', encoding='utf-8') as fp:
        json.dump(lower, fp=fp, ensure_ascii=False)

def find(path):
    json_data = input_json_data_from_file(path)

    print("……………………………………调用查找……………………………………")
    # 调用查找
    print("查找jsons中key的value值如下：")
    output_value(json_data, "sortedItems")
    print("……………………………………运行结束……………………………………")

def _main():
    with open('cookie.txt', 'r', encoding='utf-8') as fp:
        cookie_list = eval(fp.readline())
        print(cookie_list)
    with open('all.json', 'r', encoding='utf-8') as fp:
        global begin
        begin = json.load(fp)
    find('inform.json')
    begin = list(begin.keys())
    get_car()
    get_yh()
    get_best()
    print(inform)
    update_lower()
    with open('all.json', 'w', encoding='utf-8') as fp:
        json.dump(inform, fp=fp, ensure_ascii=False)


def main():

    with open('all.json', 'r', encoding='utf-8') as fp:
        global begin
        begin = json.load(fp)
        global dic
        for i in begin:
            # print(begin[i]["price"])
            # print(begin[i]["kc"])
            dic[i] = {}
            dic[i]["price"] = begin[i]["price"]
            dic[i]["kc"] = begin[i]["kc"]
            print("=================")
            print(dic[i]["price"])
            print(dic[i]["kc"])
            print("=================")
        begin = list(begin)
    print(dic)

    with open('cookie.txt', 'r', encoding='utf-8') as fp:
        cookie_list = eval(fp.readline())
        print(cookie_list)

    global cookie

    for i in cookie_list:

        cookie = i
        get_car(cookie)

        find('inform.json')
        get_yh(cookie)
        get_best()
        update_lower()
    with open('all.json', 'w', encoding='utf-8') as fp:
        json.dump(inform, fp=fp, ensure_ascii=False)

if __name__ == '__main__':
    main()
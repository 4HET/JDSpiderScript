import requests

import json
import time

def input_json_data_from_file(path):
    """
    从文件中获取json数据
    :param path: 文件路径
    :return json_data: 返回转换为json格式后的json数据
    """
    # 从文件中获取json，转化为str
    try:
        with open("inform.json", "r", encoding="utf-8") as f:
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
        if i["itemType"] == 1:
            item = i["item"]
            inform = {}
            # 商品名称
            inform["com_name"] = item.get("Name")
            # 购物车价格
            inform["cart_price"] = item.get("PriceShow")
            inform["cart_price"] = eval(inform["cart_price"][1:])
            # 最优下单价格
            inform["best_price"] = 0
            # 最优下单数量
            inform["best_num"] = 0
            # 最优下单总金额
            inform["beat_all_price"] = 0
            # 原始价格
            inform["ori_price"] = 0
            # 商品库存
            inform["stockState"] = item.get("stockState")
            # 商品sku
            inform["sku"] = item.get("Id")
            # 商品活动
            com_avtivity = ""
            canSelectPromotions = item["canSelectPromotions"]
            if canSelectPromotions != []:
                inform["com_avtivity"] = canSelectPromotions[0]["title"]
            #优惠券
            inform["coupon"] = ""
            # 商品链接
            inform["com_url"] = "https://item.jd.com/" + inform["sku"] + ".html"
            # 历史最低价
            inform["lowest_price"] = 0
            # 数据获取时间
            inform["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 数据获取区域
            inform["area"] = ""

            inform_list.append(inform)
            print(inform)


def main(path):
    json_data = input_json_data_from_file(path)

    print("……………………………………调用查找……………………………………")
    # 调用查找
    print("查找jsons中key的value值如下：")
    output_value(json_data, "sorted")
    output_value(json_data, "items")
    print("……………………………………运行结束……………………………………")


if __name__ == "__main__":
    inform_list = []

    main(r"../inform.json")
    print(inform_list)
    try:
        with open("inform.txt", "w", encoding="utf-8") as f:
            try:
                f.write(str(inform_list))
            except Exception as e:
                print("数据格式不正确：" + str(e))
    except Exception as e:
        print("文件不存在：" + str(e))
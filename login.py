from urllib import request
from selenium import webdriver
import cv2
import random
import time
import pyautogui
import json

def login():
    print("请输入账号的个数：")
    n = int(input())
    cookie_list = []
    for i in range(n):
        try:
            # 打开Chrome浏览器
            # print(int("tmp"))
            driver = webdriver.Chrome()
            driver.get("https://plogin.m.jd.com/login/login")


            # 获取cookie
            time.sleep(60)
            driver.refresh()
            cookie = [item['name'] + '=' + item['value'] for item in driver.get_cookies()]
            print(cookie)
            with open("cookie.txt", "w", encoding="utf-8") as f:
                try:
                    cookie_list.append(str(cookie).replace("'", "").replace(',',';'))
                    f.write(str(cookie_list))
                    print("cookie保存成功")
                except Exception as e:
                    print("数据格式不正确：" + str(e))
            print(cookie)
        except:
            login()

if __name__ == '__main__':
    login()
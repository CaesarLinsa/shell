# -*-coding:utf-8 -*-

import requests
from lxml import etree
import os


def get_url_list(url):
    """
    :return: 获取主页面上，子图的url列表
    """
    if not url.startswith("https:"):
        son_url = "https:%s" % url
    son_data = requests.get(url)
    son_data.encoding = "utf-8"
    tree = etree.HTML(son_data.text)
    urls = tree.xpath("//ul[@class='img']/li/a/@href")
    return urls


def get_url_data(son_url):
    """
    :param son_url: 子图的url
    :return: 请求返回内容
    """
    if not son_url.startswith("https:"):
        son_url = "https:%s" % son_url
    son_data = requests.get(son_url)
    son_data.encoding = "utf-8"
    return son_data.text


def get_img_info(son_data):
    """
    :param son_data: 子图url返回内容
    :return: 子图中图片src和alt信息
    class和center是html的类和标签
    """
    tree = etree.HTML(son_data)
    div = tree.xpath('//div[@class="content"]/center')
    src = div[0].xpath("img/@src")
    alt = div[0].xpath("img/@alt")[0]
    return alt, src


def get_img_sum(son_data):
    """
    :param son_data: 子图url返回内容
    :return: 子图的数量(页数)
    class='pages', pages可变
    """
    tree = etree.HTML(son_data)
    page_nums = tree.xpath('//div[@id="pages"]/a/text()')
    page_nums = [int(i) if i.isdigit() else 0 for i in page_nums]
    return max(page_nums)


def download_picture(title, son_url, dir="D:\\pictures"):
    """
    :param title: 子图中图片的alt
    :param son_url:  子图中的jpg的url
    :param dir: 图片存放目录
    :return: 下载图片到指定目录
    """
    sava_dir = os.path.join(dir, title.strip())
    if not os.path.exists(sava_dir):
        os.mkdir(sava_dir)
    if son_url.startswith("//"):
        son_url = "https:%s" % son_url
    if son_url.startswith("www"):
        son_url = "https://%s" % son_url
    r = requests.get(son_url)
    sava_path = os.path.join(sava_dir, son_url.split("/")[-1])
    with open(sava_path, 'wb')as jpg:
        jpg.write(r.content)


def run(i):
    """
    :param:  i 进程id
    :return:  主页-->主页的子图列表-->每个子图中图片页数、每个子图中图片-->
    按页数，从1到最后下载
    """
    url = "https://www.meitulu.com/guochan/"
    if i != 1:
        url = "%s%i.html" %(url,i)
    inner_urls = get_url_list(url)
    for ur in inner_urls:
        try:
            son_data = get_url_data(ur)
            alt, srcs = get_img_info(son_data)
            for src in srcs:
                download_picture(alt, src)
            num = get_img_sum(son_data)
            for index in range(2, num + 1):
                url = "%s_%d.html" % (ur.split(".html")[0], index)
                data = get_url_data(url)
                print(url)
                _, srcs = get_img_info(data)
                for src in srcs:
                    download_picture(alt, src)
        except Exception as e:
            print(str(e))
            continue


if __name__ == '__main__':
    from multiprocessing import Process, freeze_support
    freeze_support()
    # 手动查看总共有多少页，创建多少进程
    for i in range(1, 215):
        p = Process(target=run, args=(i,))
        p.start()

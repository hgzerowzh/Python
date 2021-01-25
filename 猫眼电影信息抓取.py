import re
import requests
import urllib3
import json

# 忽略警告
urllib3.disable_warnings()


def get_one_page(url, headers):
    """
    判断页面是否能正常访问，并得到页面转换成文本格式的内容
    :param url: 页面URL地址
    :param headers: 请求头
    :return: 页面转换成文本的内容
    """
    try:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(e)
        return None


def get_video_info(html_text):
    """
    获取需要的电影信息，保存为一个字典，并构造成生成器
    :param html_text: 单个页面的文本内容
    :return: 
    """
    try:
        pattern = re.compile('<dd>.*?>(?P<index>\d+)<.*?data-src="(?P<imglink>.*?)".*?data-val.*?">(?P<name>.*?)<.*?'
                             'star">(?P<star>.*?)<.*?releasetime">(?P<releasetime>.*?)<.*?'
                             'integer">(?P<x>.*?)<.*?fraction">(?P<y>.*?)<.*?</dd>', re.S)
        item = re.findall(pattern, html_text)
    except Exception as e:
        print(e)
    else:
        for i in item:
            yield {
                "序号": i[0],
                "电影名": i[2],
                "主演": i[3].strip()[3:],
                "上映时间": i[4][5:],
                "评分": i[5]+i[6],
                "图像链接": i[1],
             }


def save_as_file(data):
    """
    将数据写入文件
    :param data: 单条电影信息
    :return: 
    """
    with open("movie_info.txt", "a+", encoding="utf-8") as f:
        info = json.dumps(data, ensure_ascii=False)  # 不以ascii码方式显示
        f.write(info + "\n")


def main(n):
    """
    主函数，负责整个脚本的逻辑
    :param n: 要获取的的页数
    :return: 
    """
    url = "http://maoyan.com/board/4?offset=" + str((n-1)*10)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
        "Referer": "http://maoyan.com/board",
    }
    html_text = get_one_page(url, headers)
    for i in get_video_info(html_text):
        print(i)
        save_as_file(i)


if __name__ == '__main__':
    for i in range(1, 11):
        main(i)
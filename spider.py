import re

import requests
from scrapy import Selector


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Referer': 'referer'
}

for num in range(0, 481, 12):
    url = "https://www.pearvideo.com/category_loading.jsp?reqType=5&categoryId=5&start={}".format(num)
    repnose = requests.get(url, headers=headers).text
    res = Selector(text=repnose)
    li = res.xpath(("//li"))
    for table in li:
        li_id = table.xpath("./div/a/@href").get().split("_")[-1]  
        title = table.xpath("./div/div/a/text()").get()     
        headers['Referer'] = 'https://www.pearvideo.com/video_{}'.format(li_id)
        url_id = 'cont-{}'.format(li_id)
        # li_id2 = video.xpath("./div/div/a/@href").get().split("_")[-1]
        li_url = "https://www.pearvideo.com/videoStatus.jsp?contId={}".format(li_id)
        video = requests.get(li_url, headers=headers).text
        video_url = re.findall('"srcUrl":"(.*?)"}}', video)[0]
        num_id = re.findall('/\d.*/(\d.*?)-', video_url)[0]
        num_url = video_url.replace(num_id, url_id)
        # print(title)
        # print(num_url)
        video_num_url = requests.get(num_url, headers=headers).content
        print("正在下载{}".format(title))
        with open("./" + title + ".mp4", 'wb')as f:
            f.write(video_num_url)
        print("{}下载完成".format(title))



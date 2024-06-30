import requests
from bs4 import BeautifulSoup
import json
import tqdm
from tqdm import tqdm
import time

# url = "https://www.vinmec.com/vi/thong-tin-duoc/su-dung-thuoc-toan/tac-dung-thuoc-ankitamol/?link_type=related_posts"


def get_data(url):
    _url = "https://www.vinmec.com/vi" + url
    response = requests.get(_url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    h1_tag = soup.find('h1')

    # Get the text within the h1 tag
    title = h1_tag.text.strip()

    # Find the div with class 'block-content cms pageview-highest'
    # content_div = soup.find('div', class_='block-content cms pageview-highest')

    content_div = soup.find('div', class_="block-content cms pageview-highest")    # Get all the text within the div
    print(content_div)
    text = content_div.get_text(separator='\n')
    text = text.split("XEM THÊM")[0]
    text = "\n".join([line.strip() for line in text.split('\n') if line.strip() != ''])
    text = text.strip()
    data = {
        "title": title,
        "content": text,
        "url": _url    
    }

    return data

corpus = []


# with open("vimec.json", "r") as f:
# #     data = json.load(f)

# for item in tqdm(data):
#     try:
#         url = item['url']
#         data = get_data(url)
#         corpus.append(data)
#         time.sleep(0.1)
#     except:
#         print("Error at: ", url)
#         continue


# # Save the text to a file json
# with open('vinmec_full.json', 'a') as f:
#     json.dump(corpus, f, ensure_ascii=False, indent=4)

url = "/tin-tuc/thong-tin-suc-khoe/nhi/nao-la-hoi-chung-rubella-bam-sinh/"
# url = '/tin-tuc/thong-tin-suc-khoe/san-phu-khoa-va-ho-tro-sinh-san/chu-vi-vong-dau-thai-nhi-theo-tung-tuan-thai/'
# url = "/tin-tuc/thong-tin-suc-khoe/suc-khoe-tong-quat/cac-bien-phap-danh-gia-chan-thuong-so-nao/"

data = get_data(url)
print(data)
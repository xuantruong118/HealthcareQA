import json


with open("new/vinmec_article_content_split_main.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    print(len(data))
    print(data[68])
    
    title_all = [item['title'] for item in data]
    
    # get radom 320 titles
    import random
    random.seed(10)
    title_all = random.sample(title_all, 200)
    
with open('title.txt', 'w', encoding='utf-8') as f:
    for title in title_all:
        f.write(title + '\n')
        
        
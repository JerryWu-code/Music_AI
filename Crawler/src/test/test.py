import requests
import time
import json
from bs4 import BeautifulSoup

def get_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
    else:
        return None
    return soup, soup.prettify()

def parse_loops(soup):
    # parse loops from the website use BeautifulSoup

    tags_parents = soup.find_all('div', class_='tag-wrapper')

    result = {}
    records = {}
    for tags_parent in tags_parents:
        record = {}
        tags = tags_parent.find_all('a')
        # extract the text from the tags
        tags_text = [tag.get_text(strip=True) for tag in tags]
        bpm = tags_text[0].strip().split(' bpm')[0]
        genre = tags_text[1].strip().split(' Loops')[0]
        category = tags_text[2].strip().split(' Loops')[0]
        # size = tags_text[3].strip()
        key = tags_text[5].strip().split('Key : ')[1]

        description_ = tags_parent.find_next_sibling('div', class_='desc-wrapper')  # 使用find_next_sibling查找描述
        if description_:
            descs = description_.find_all('p')
            description = [desc.get_text(strip=True) for desc in descs][0].split('Description : ')[1].strip()

        player_wrapper = tags_parent.find_next_sibling('div', class_='player-wrapper')  # 使用find_next_sibling查找播放器部分
        if player_wrapper:
            link = player_wrapper.find('div', class_='player-title-wrapper-mbl').find('a')['href'] if player_wrapper else None

        mp3_div = tags_parent.find_next_sibling('div', class_='player-wrapper')  # 使用find_next_sibling查找MP3链接
        if mp3_div:
            mp3_link = mp3_div['rel']
            name = mp3_link.split('/')[-1].split('.')[0]

        # get the record
        category = category
        if name:
            record_parent_key = name
            record['bpm'] = bpm
            record['genre'] = genre
            record['key'] = key
            record['description'] = description
            record['url'] = link
            records[record_parent_key] = record
    result[category] = records
    print(result)
    return result


def running(url, output_file):
    while True:
        # parse loops from the website use BeautifulSoup
        pass
        with open(output_file, 'a') as f:
            pass
        time.sleep(3)  # 每1秒爬取一次

def main():
    url = "https://www.looperman.com/loops?page=5&cid=12&dir=d"
    # output_file1 = 'loops.txt'
    # with open(output_file1, 'a') as f:
        # f.write(content)
    output_file2 = 'parse.txt'
    soup, content = get_url(url)

    result = parse_loops(soup)
    with open(output_file2, 'a') as f:
        f.write(json.dumps(result, indent=4))

if __name__ == '__main__':
    main()
    
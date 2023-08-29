import re
import requests
from bs4 import BeautifulSoup



def create_soup(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def print_news(index, title, link):
    print("{}. {}".format(index, title))
    print("  (링크 : {})".format(link))

def scrape_weather():
    print("[오늘의 날씨]")
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%ED%96%89%EC%8B%A0%EB%8F%99+%EB%82%A0%EC%94%A8"
    soup = create_soup(url)
    # 흐림, 어제보다 00°좋아요
    cast = soup.find("p", attrs={"class":"summary"}).get_text()
    # 현재 00°C  (최저 00° / 최고 00°)
    curr_temp = soup.find("div", attrs={"class":"temperature_text"}).get_text() # .replace("도씨", "")
    min_temp = soup.find("span", attrs={"class":"lowest"}).get_text() # 최저 온도
    max_temp = soup.find("span", attrs={"class":"highest"}).get_text() # 최고 온도
    # 오전 강수확률 00% / 오후 강수확률 00%
    rain_rate = soup.find("div", attrs={"class":"day_data"})
    morning_rain_rate = rain_rate.find_all("span", attrs={"class":"rainfall"})[0].get_text() # 오전 강수 확률
    afternoon_rain_rate = rain_rate.find_all("span", attrs={"class":"rainfall"})[1].get_text() # 오후 강수 확률

    # 미세먼지 00㎍/m³좋음
    # 초미세먼지 00㎍/m³좋음
    dust = soup.find("ul", attrs={"class":"today_chart_list"})
    fine_dust = dust.find_all("li")[0].get_text() # 미세먼지 농도
    ultra_fine_dust = dust.find_all("li")[1].get_text() # 초미세먼지 농도


    # 출력
    print("",cast)
    print("{} (최저 {} / 최고 {})".format(curr_temp, min_temp, max_temp))
    print(" 강수확률 : 오전 {} / 오후 {}".format(morning_rain_rate, afternoon_rain_rate))
    print()
    print("{}".format(fine_dust))
    print("{}".format(ultra_fine_dust))
    print()


def screpe_headline_news():
    print("[헤드라인 뉴스]")
    url = "https://news.daum.net"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"list_newsissue"}).find_all("li", limit=3)
    for index, news in enumerate(news_list,1):
        title = news.find("a", attrs={"class":"link_txt"}).get_text().strip()
        link = news.find("a")["href"]
        print_news(index, title, link)
    print()


def screpe_it_news():
    print("[IT 뉴스]")
    url = "https://news.daum.net/digital#1"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"list_newsmajor"}).find_all("li", limit=3) # 3개 가져오기
    for index, news in enumerate(news_list,1):
        title = news.find("a", attrs={"class":"link_txt"}).get_text().strip()
        link = news.find("a")["href"]
        print_news(index, title, link)
    print()

# [오늘의 영어 회화]
# (영어 지문)
# jason : how do you think bla bla..?
# kim : well, I think ...

# (한글 지문)
# jason : 어쩌구 저쩌구 어떻게 생각하세요?
# Kim : 글쎄요, 저는 어쩌구 저쩌구

def scrape_english():
    print("[오늘의 영어 회화]")
    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_gnb_eng_I_others_english&logger_kw=haceng_submain_gnb_eng_I_others_english"
    soup = create_soup(url)
    sentences = soup.find_all("div", attrs={"id":re.compile("^conv_kor_t")})
    print("(영어 지문)")
    for sentence in sentences[len(sentences)//2:]: # 8 문장이 있다고 가정할 때, 5~8(index기준 4~7)까지 잘라서 가져옴
        print(sentence.get_text().strip())
    
    print()
    print("(한글 지문)")
    for sentence in sentences[:len(sentences)//2]: # 8 문장이 있다고 가정할 때, 1~4(index기준 0~3)까지 잘라서 가져옴
        print(sentence.get_text().strip())

    print()



if __name__ == "__main__":
    scrape_weather() # 오늘의 날씨 정보 가져오기
    screpe_headline_news() # 헤드라인 뉴스 정보 가져오기
    screpe_it_news() # IT 뉴스 정보 가져오기
    scrape_english() # 오늘의 영어 회화 가져오기
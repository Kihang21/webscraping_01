import requests
from bs4 import BeautifulSoup


# [오늘의 날씨]
# 흐림, 어제보다 00°좋아요
# 현재 00°C  (최저 00° / 최고 00°)
# 오전 강수확률 00% / 오후 강수확률 00%

# 미세먼지 00㎍/m³좋음
# 초미세먼지 00㎍/m³좋음

def scrape_weather():
    print("[오늘의 날씨]")
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%ED%96%89%EC%8B%A0%EB%8F%99+%EB%82%A0%EC%94%A8"
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
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


if __name__ == "__main__":
    scrape_weather() # 오늘의 날씨 정보 가져오기
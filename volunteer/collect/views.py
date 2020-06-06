from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
# Create your views here.
def get_info():
    total_page = 138 # 총 138 페이지
    total_result = []
    for i in range(10):
        print(f'{i}번째 페이지 크롤링')
        response = requests.post('https://www.1365.go.kr/vols/1572247904127/partcptn/timeCptn.do', 
            data={
                'cPage' : i+1,
        })
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")
        ul = soup.find("ul", {"class" : "list_wrap"}) #리스트를 담고 있는 ul 
        total_list = ul.find_all("li")
        for list in total_list:
            item = {}
            item['timeApprove'] = list.find("span", {"class" : "tag blue"}).string
            item['ing'] = list.find("span", {"class" : "ing"}).find("strong").string
            item['title'] = list.find("dt", {"class" : "tit_board_list"}).text
            item['institution'] = list.find_all("dl")[1].find("dd").string
            item['apply_period'] = list.find_all("dl")[2].find("dd").string.strip()
            item['volunteer_period'] = list.find_all("dl")[3].find("dd").string.strip()

            total_result.append(item)

    print(total_result)
    return total_result

def get_volunteer_list(request):
    volunteer_list = get_info()
    return render(request, 'volunteer.html',
    { 'volunteer_list' : volunteer_list })
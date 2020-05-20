from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
# Create your views here.
def get_info():
    response = requests.get('https://www.1365.go.kr/vols/1572247904127/partcptn/timeCptn.do')
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    dl = soup.find("dl", {"class" : "txts"}) #가장 큰 클래스 
    details = dl.find({"class" : "board_data normal"}) #세부사항
    names = dl.find({"class" : "tit_board_list"}) #봉사활동 제목
    volunteer_detail_explain=details.find("dt") #세부사항 1
    volunteer_detail_info=details.find("dd") #세부사항 2
    result=[]
    detail = []
    description = ""
    for info in volunteer_detail_info:
        for explain in volunteer_detail_explain:
            description = info + explain
            detail.append(description)
    for name in names:
        volunteer_dic={}
        volunteer_dic['name'] = name.string
        for d in detail:
            volunteer_dic['detail'] = d.string
        result.append(volunteer_dic)
    return result


def get_volunteer_list(request):
    volunteer_list = get_info()
    return render(request, 'volunteer.html',
    { 'volunteer_list' : volunteer_list })
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
# Create your views here.
def get_info():
    response = requests.get('https://www.mohw.go.kr/react/popup_200128.html')
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    tbody = soup.find("tbody", {"class" : "tb_center"})  
    hospital_list= tbody.find_all("tr")
    result=[]
    for hospital in hospital_list:
        hospital_dic={}
        info = hospital.find_all("td")
        # print(info[0].string, info[1].string, info[2].string, info[3].string, info[4].string)
        hospital_dic['region'] = info[0].string
        hospital_dic['local'] = info[1].string
        hospital_dic['name'] = info[2].string
        hospital_dic['type'] = info[3].string
        hospital_dic['number'] = info[4].string
        result.append(hospital_dic)
    return result

def get_hospital_list(request):
    hospital_list = get_info()
    return render(request, 'hospital.html',
    { 'hospital_list' : hospital_list })
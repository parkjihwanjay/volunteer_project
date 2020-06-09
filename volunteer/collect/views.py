from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.contrib import auth
# Create your views here.
def home(request):
    return render(request, 'home.html')
def get_info():
    total_page = 138 # 총 138 페이지
    total_result = []
    for i in range(1):
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

    return total_result

def get_volunteer_list(request):
    volunteer_list = get_info()
    return render(request, 'volunteer.html',
    { 'volunteer_list' : volunteer_list })

def signup(request):
    if request.method=='POST':
        found_user = User.objects.filter(username=request.POST['username'])
        if len(found_user) > 0:
            error = '해당 아이디는 이미 존재합니다.'
            return render(request, 'registration/signup.html', {
                'error' : error,
            })
        new_user = User.objects.create_user(
            username = request.POST['username'],
            password = request.POST['password'],
        )
        auth.login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')
    else:
        return render(request, 'registration/signup.html')

def login(request):
    if request.method == 'POST':
        found_user = auth.authenticate(
            username = request.POST['username'],
            password = request.POST['password'],
        )
        if found_user is None:
            error = "아이디 또는 비밀번호가 틀렸습니다"
            return render(request, 'registration/login.html', {
                'error' : error,
            })
        else:
            auth.login(request, found_user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        return render(request, 'registration/login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')
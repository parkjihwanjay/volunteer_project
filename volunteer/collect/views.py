from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.contrib import auth
# Create your views here.
def home(request):
    return render(request, 'home.html')
def get_info(searchHopeArea1, searchHopeSrvc1, searchSrvcTarget):
    total_page = 138 # 총 138 페이지
    total_result = []
    for i in range(1):
        print(f'{i}번째 페이지 크롤링')
        response = requests.post('https://www.1365.go.kr/vols/1572247904127/partcptn/timeCptn.do', 
            data={
                'cPage' : i+1,
                'searchHopeArea1' : searchHopeArea1,
                'searchHopeSrvc1' : searchHopeSrvc1,
                'searchSrvcTarget' :searchSrvcTarget
        })
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")
        ul = soup.find("ul", {"class" : "list_wrap"}) #리스트를 담고 있는 ul 
        total_list = ul.find_all("li")
        if len(total_list) == 1:
            return 0

        for list in total_list:
            item = {}
            item['timeApprove'] = list.find("span", {"class" : "tag blue"}).string
            item['ing'] = list.find("span", {"class" : "ing"}).find("strong").string
            item['title'] = list.find("dt", {"class" : "tit_board_list"}).text
            item['close_day'] = list.find("div", {"class" : "close_dDay"}).text
            item['institution'] = list.find_all("dl")[1].find("dd").string
            item['apply_period'] = list.find_all("dl")[2].find("dd").string.strip()
            item['volunteer_period'] = list.find_all("dl")[3].find("dd").string.strip()
            input = list.find('input')
            # page_num = a['href'].split(':')[1][5:11]
            page_num = input['value']
            item['page_num'] = page_num
            item['next_page'] = f'https://www.1365.go.kr/vols/1572247904127/partcptn/timeCptn.do?type=show&progrmRegistNo={page_num}'
            # https://www.1365.go.kr/vols/1572247904127/partcptn/timeCptn.do?type=show&progrmRegistNo=2641014

            total_result.append(item)

    return total_result

def get_info2():
    response = requests.post('https://www.vms.or.kr/partspace/recruit.do')
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    ul = soup.find("ul", {"class" : "list_wrap"}) #리스트를 담고 있는 ul 
    total_list = ul.find_all("li")
    if len(total_list) == 1:
        return 0

    for list in total_list:
        item = {}
        item['timeApprove'] = '시간인증'
        item['ing'] = list.find("span", {"class" : "status"}).string
        item['title'] = list.find("dt", {"class" : "tit_board_list"}).text
        item['close_day'] = list.find("div", {"class" : "close_dDay"}).text
        item['institution'] = list.find_all("dl")[2].find("dd").string
        item['apply_period'] = list.find_all("dl")[2].find("dd").string.strip()
        item['volunteer_period'] = list.find_all("dl")[3].find("dd").string.strip()
        input = list.find('input')
        # page_num = a['href'].split(':')[1][5:11]
        page_num = input['value']
        item['page_num'] = page_num
        item['next_page'] = f'https://www.1365.go.kr/vols/1572247904127/partcptn/timeCptn.do?type=show&progrmRegistNo={page_num}'
        # https://www.1365.go.kr/vols/1572247904127/partcptn/timeCptn.do?type=show&progrmRegistNo=2641014

        total_result.append(item)

    return total_result
def get_volunteer_list(request):
    if request.method == 'GET':
        volunteer_list = get_info2()
    else:
        try:
            searchHopeArea1 = request.POST['region']
            searchHopeSrvc1 = request.POST['category']
            searchSrvcTarget = request.POST['clients']
        except:
            searchHopeArea1 = ""
            searchHopeSrvc1 = ""
            searchSrvcTarget = ""

        # if request.POST['region']:
        # if request.POST['category']:
        # if request.POST['clients']:
            
        volunteer_list = get_info(searchHopeArea1, searchHopeSrvc1, searchSrvcTarget)
        if volunteer_list == 0:
            return render(request, 'volunteer.html',
        { 'error' : '입력하신 검색어에 대한 조회결과가 없습니다' })

    return render(request, 'volunteer.html',
    { 'volunteer_list' : volunteer_list })

def detail(request, page_num):
    import requests

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://www.1365.go.kr',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.1365.go.kr/vols/P9210/partcptn/timeCptn.do',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = (
        ('type', 'show'),
        ('progrmRegistNo', page_num),
    )

    data = [
    ('jsonUrl', '/vols/P9210/mber/volsMberJson.do'),
    ('cPage', '1'),
    ('searchFlag', 'search'),
    ('requstSe', ''),
    ('reqConfirm', ''),
    ('firstSearch', 'N'),
    ('hopea1', ''),
    ('hopea2', ''),
    ('flag', 'A01'),
    ('listType', ''),
    ('titleNm', '\uC0C1\uC138\uBCF4\uAE30'),
    ('searchHopeArea1', ''),
    ('searchHopeArea2', ''),
    ('searchHopeSrvc1', ''),
    ('searchHopeSrvc2', ''),
    ('searchSrvcTarget', ''),
    ('searchSrvcStts', '0'),
    ('searchProgrmBgnde', '2020-06-10'),
    ('searchProgrmEndde', '2020-09-10'),
    ('adultPosblAt', 'Y'),
    ('yngbgsPosblAt', 'Y'),
    ('searchKeyword', ''),
    ('searchNanmmbyNm', ''),
    ('searchRequstSe', 'on'),
    ]

    # response = requests.post(f'https://www.1365.go.kr/vols/1572247904127/partcptn/timeCptn.do?type=show&progrmRegistNo={page_num}', headers=headers, params=params, cookies=cookies, data=data)
    response = requests.post('https://www.1365.go.kr/vols/1572247904127/partcptn/timeCptn.do', headers=headers, params=params, data=data)
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup)

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


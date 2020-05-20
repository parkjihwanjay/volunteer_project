## git은 여러분들 컴퓨터에 깔린 프로그램
* .git 폴더에 위치한 모든 파일들의 변화를 감지
* 버전관리
* 그 전의 버전으로 돌아갈 수 있다.

## github은 git을 통해 관리한 코드를 올릴 수 있는 온라인 저장소
* 다른 사람들과 협업

> $ git init
* 해당 위치에 .git 폴더를 만든다
* 한번만 치면 된다.

> $ git status
* 현재 파일들이 stage에 올라갔는지 아닌지 확인
* stage -> version을 만들기 위해 대기하는 공간

> $ git add .
* 현재 위치의 모든 파일들을 stage에 올리겠다
* git add 특정파일 -> 특정 파일만 stage에 올리겠다

> $ git commit -m 'first commit'
* stage에 올라간 파일들을 특정 버전으로 만들겠다
* ' '안에 여러분들 메시지를 적으면 된다

> $ git remote add origin 'https...'
* https..의 원격 저장소와 현재 .git을 연결하겠다
* 그리고 https..를 앞으로 origin으로 부르겠다

> $git push origin master
* 현재까지 만든 버전들을 origin(원격 저장소)에 올리겠다

> $ git clone 'https..'
* 'https..'에 있는 저장소의 파일들을 복제하겠다
* collaborater로 추가가 돼있어야 한다.

> $ git pull origin master
* 현재 원격저장소의 코드를 내 컴퓨터에 가져오겠다.
* push를 하기 전 원격저장소의 상태와 내 컴퓨터의 코드의 상태를 맞춰야한다.
* 누군가 push를 했다면 pull을 받고 작업을 진행하자


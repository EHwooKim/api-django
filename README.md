# API

$ pip install django-rest-framework [공식문서]( https://www.django-rest-framework.org/ )





# dumpdata

* dumpdata : 데이터를 복제뜬다

$ python manage.py dumpdata musics 이렇게 하면 쫙 목록 나오고

$ python manage.py dumpdata musics > musics.json 이렇게하면  json 파일로 생성되고 이렇게만하면 보기 힘들어서

$ python manage.py dumpdata --indent 2 musics > musics.json 이렇게 쓰면 편안



* data 읽을 때는
  * 앱 안에 fixtures 폴더를 만들어서 해당 json파일을 넣고
  * python manage.py loaddata musics 하면 된다.
* 있어보이는 api url
  * `  path('api/v1/', include('musics.urls')),` : api/버전1/
* view에서 api_view까지 하고 `serializers` 파일을 만들어서 정의하고   다시 view에 가서 사용

* `postman` 설치 (다양한 요청을 보낼 수 있는 프로그램)
  * 이거로 한거를 코드로 옮기는게 편하다..?
* `API` 문서화작업
  * pip install drf-yasg    [git]( https://github.com/axnsan12/drf-yasg )
* 요청에 따른 url
  * GET reviews/   리뷰 목록
  * POST reviews/ 리뷰 등록하기
  * GET reviews/1/ 1번 리뷰 가져오기
  * PUT reviews/1/  1번 리뷰 수정하기
  * DELETE reviews/1/ 1번 리뷰 삭제하기

# Interface

* GUI - `Graphic User Interface`
  * 그래픽 - 유저랑 상호작용하는 인터페이스
* CLI - `Command Line Interface`
  * 명령어 인터페이스
* API -`Application Programming Interface`
  * 프로그래밍으로 인터페이스

# REST API

## 01. REST API

* [공식문서](https://www.django-rest-framework.org/)

### 기본설정

```bash
$ pip install djangorestframework
```

```python
# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
    ...
]
```

```python
# pjt08/urls.py
urlpatterns = [
    ...
    path('api/v1/', include(movies.urls)),
]
```

### url

```python
# movies/urls.py
urlpatterns = [
    path('genres/', views.genre_index),
    path('genres/<int:genre_pk>/', views.genre_detail),
    path('movies/', views.movie_index),
    path('movies/<int:movie_pk>/', views.movie_detail),
    path('movies/<int:movie_pk>/reviews/', views.review_create),
    path('reviews/<int:review_pk>/', views.review_update_delete),
	...
]
```

* `review_update_delete`의 경우 같은 주소로 보내지만 요청 박식(`PUT`, `DELETE`)에 따라 다르게 작동한다

### serializers

* `movies`앱에 `serializers.py` 파일 추가

```python
# movies/serializers.py
from rest_framework import serializers
from .models import Movie, Genre, Review

class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id','title', 'audience', 'poster_url', 'description', 'genre']

class GenreDetailSerializers(serializers.ModelSerializer):
    movie_set = MovieSerializers(many=True)
    class Meta:
        model = Genre
        fields = ['id', 'movie_set']

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['content', 'score']
```

* `model form`과 비슷한 느낌

* `GenreDtailSerializers` 

  * genre_id, **movie정보** 를 보여주기 위해 `movie_set`을 생성하여 fields로 넘겨주었다.

  * `genre`와 `movie`의 역참조 관계 때문에 `movie_set`라고 이르믈 붙여줬고 이렇게 해야 정상 작동한다.

  * 변수명을 다르게 하고 싶다면

    ```python
    class GenreDetailSerializers(serializers.ModelSerializer):
        movies = MovieSerializers(many=True, source='movie_set')
        class Meta:
            model = Genre
            fields = ['id', 'movies']
    
    ```

    * 위와 같이 변수명을 정하고 source에` movie_set`을 넣어주면 된다.

  

### views

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GenreSerializers, MovieSerializers, GenreDetailSerializers, ReviewSerializers
from .models import Genre, Movie, Review

@api_view(['GET'])
def genre_index(request):
    genre = Genre.objects.all()
    serializer = GenreSerializers(genre, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def genre_detail(request, genre_pk):
    genre = get_object_or_404(Genre, id=genre_pk)
    serializer = GenreDetailSerializers(genre)
    return Response(serializer.data)
...
@api_view(['POST'])
def review_create(request, movie_pk):
    serializer = ReviewSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie_id=movie_pk)
    return Response({"message": "작성되었습니다"})

@api_view(['PUT', 'DELETE'])
def review_update_delete(request, review_pk):
    review = get_object_or_404(Review, id=review_pk)
    if request.method == 'PUT':
        serializer = ReviewSerializers(data=request.data, instance=review)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    else:
        review.delete()
        return Response({'message':'삭제되었습니다'})
```

* `api_view` : 요청 방식을 판단하기 위한 데코레이터
* `Response` : `serializer.data`와 같이 변경사항을 보여줄 수도있고 딕셔너리 형태로 `message`를 보여줄 수도 있다.
* `~_index` 의 경우 해당 목록에 값이 여러개가 들어가기 때문에 `many=True` 옵션을 주었다
* `raise_exception=True` 필수값이 비어있는 상태로 요청이 들어올 경우 경고 메세지를 띄워준다.
* `review_create`
  * `model form`처럼 `save(commit=False)` 없이 바로 `movie_id=movie_pk` 가능하다.

## 02. API 문서화

### 기본설정

```bash
$pip install drf-yasg
```

```python
# settings.py
INSTALLED_APPS = [
    ...
    'drf_yasg',
    ...
]
```

* `settings.py`에서는 `-`가 아닌 `_`를 써야 인식된다.

```python
# movies/urls.py
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Movie API",
      default_version='v1',
      description="Movie 정보",
   ),
)
urlpatterns = [
    ...
    path('redoc/', schema_view.with_ui('redoc')),
    path('swagger/', schema_view.with_ui('swagger')),    
]
```



## +. POSTMAN

![postman](./readme_images/postman.png)

* url `/` 끝까지 제대로 해서 요청보내기

* `POST` 요청을 보낼 때는 `Body`에서 보내야 form-data 형태로 보낼 수 있다.







# Dumpdata

* dumpdata : 데이터를 복제뜬다

$ python manage.py dumpdata musics 이렇게 하면 목록 나오고

$ python manage.py dumpdata musics > musics.json 이렇게하면  json 파일로 생성되고 이렇게만하면 보기 힘들어서

$ python manage.py dumpdata --indent 2 musics > musics.json 이렇게 쓰면 편안



* data 읽을 때는
  * 앱 안에 fixtures 폴더를 만들어서 해당 json파일을 넣고
  * python manage.py loaddata musics 하면 된다.

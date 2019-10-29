from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Music, Artist, Review
from .serializers import MusicSerializers, ArtistSerializers, ArtistDetailSerializers, ReviewSerializer
# Create your views here.


@api_view(['GET']) # HTTP method의 GET요청만. POST일떄는 결과 안나온다.
def musics_index(request):
    '''
    음악 목록 정보 신기하다
    '''
    musics = Music.objects.all()
    # 여기서 return render했었지만 우리는 지금 api하는거니까
    serializer = MusicSerializers(musics, many=True)  # 이거는 QuertSet이라 many=Ture한거고
    return Response(serializer.data)

@api_view(['GET'])
def musics_detail(request, music_pk):
    '''
    음악 상세 정보
    '''
    music = get_object_or_404(Music, pk=music_pk)     
    serializer = MusicSerializers(music)             # 이거는 하나 받는거라 many 옵션 필요없다.
    return Response(serializer.data)

# 아티스트 목록
@api_view(['GET'])
def artists_index(request):
    '''
    아티스트 목록
    '''
    artists = Artist.objects.all()
    serializer = ArtistSerializers(artists, many=True)
    return Response(serializer.data)

# 아티스트 상세보기
@api_view(['GET'])
def artist_detail(request, artist_pk):
    '''
    아티스트 상세보기
    '''
    artist = get_object_or_404(Artist, pk=artist_pk)
    serializer = ArtistDetailSerializers(artist)
    return Response(serializer.data)

# 음악에 대한 리뷰 작성 (POST로 처리해야겠지)
@api_view(['POST'])
def review_create(request, music_pk):
    # model_form처럼 serializer를 이용하여 저장을 할거야. form 을 던지지는 않지만 POST요청으로 들어오는 데이터가 있으니까
    # request.POST 는 form을 통해 들어왔을 때 쓰는거고 여기서는 request.data에 원하는 정보가 있다
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):  # 비어있는 상태로 요청을 보내면 메세지 보여주는거
        # commit False가 아니라 인자로 id값 넘겨주면 된다. 
        serializer.save(music_id=music_pk)

    # return Response(serializer.data)
    # 이렇게 원하는 메세지를 보여줄 수도 있다. "딕셔너리 형태"
    return Response({'message': 'review가 등록 되었습니다.'})


@api_view(['PUT', 'DELETE'])
def review_update_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'PUT':
        serializer = ReviewSerializer(data=request.data, instance=review)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    else:
        review.delete()
        return Response({'message': '성공적으로 삭제되었습니다.'})

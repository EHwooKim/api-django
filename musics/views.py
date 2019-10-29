from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Music
from .serializers import MusicSerializers
# Create your views here.


@api_view(['GET']) # HTTP method의 GET요청만. POST일떄는 결과 안나온다.
def index(request):
    musics = Music.objects.all()
    # 여기서 return render했었지만 우리는 지금 api하는거니까
    serializer = MusicSerializers(musics, many=True)  # 이거는 QuertSet이라 many=Ture한거고
    return Response(serializer.data)

@api_view(['GET'])
def detail(request, music_pk):
    music = get_object_or_404(Music, pk=music_pk)     
    serializer = MusicSerializers(music)             # 이거는 하나 받는거라 many 옵션 필요없다.
    return Response(serializer.data)
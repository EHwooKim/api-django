from rest_framework import serializers
from .models import Music, Artist, Review


class MusicSerializers(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['id', 'title', 'artist_id']

class ArtistSerializers(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id','name']

# 아티스트 상세정보를 이렇게 따로 만들어서 사용해도되지만
# class ArtistDetailSerializers(serializers.ModelSerializer):
#     music_set = MusicSerializers(many=True)
#     class Meta:
#         model = Artist
#         fields = ('id', 'name', 'music_set')

# 상속을 활용해도 되겠지
class ArtistDetailSerializers(serializers.ModelSerializer):
    music_set = MusicSerializers(many=True)
    class Meta(ArtistSerializers.Meta):
        fields = ArtistSerializers.Meta.fields + ['music_set']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['content']
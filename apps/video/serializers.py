from rest_framework import serializers

from .models import *

class PostSerializer(serializers.ModelSerializer):
    user_image = serializers.ImageField(source='user.image')

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = instance.user.username
        # if instance.user.image:
        #     rep['user_image'] = instance.user.image
        # else:
        #     rep['user_image'] = 'null'
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        rep['post_likes'] = instance.post_likes.all().count()
        rep['favorites'] = instance.favorites.filter().count()
        rep['categories'] = CategorySerializer(instance.categories.all(), many=True).data
        # rep['videos'] = instance.videos
        
        return rep

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user_image = serializers.ImageField(source='user.image')

    class Meta:
        model = Comment
        exclude = ['user']
    
    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = instance.user.username
        rep['post'] = instance.post.title
        rep['comment_likes'] = instance.comment_likes.all().count()

        return rep

class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = '__all__'
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = instance.user.username
        # rep['posts'] = PostSerializer(instance.post).data
        return rep

class LikeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeComment
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    user_image = serializers.ImageField(source='user.image')

    class Meta:
        model = Favorite
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['post_id'] = instance.post.id
        rep['user'] = instance.user.username
        rep['post'] = instance.post.title
        return rep
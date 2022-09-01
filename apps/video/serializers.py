from rest_framework import serializers

from .models import *

class PostSerializer(serializers.ModelSerializer):
    user_image = serializers.ImageField(source='user.image', required=False)

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = instance.user.username
        rep['user_id'] = instance.user.id
        # if instance.user.image:
        #     rep['user_image'] = instance.user.image
        # else:
        #     rep['user_image'] = 'null'
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        rep['post_likes'] = instance.post_likes.all().count()
        rep['liked_by'] = LikePostSerializer(instance.post_likes.filter(), many=True).data
        rep['favorited_by'] = FavoriteSerializer(instance.favorites.filter(), many=True).data
        # rep['liked_by'] = instance.post_likes.all()
        rep['favorites'] = instance.favorites.filter().count()
        rep['categories'] = CategorySerializer(instance.categories.all(), many=True).data
        # rep['videos'] = instance.videos
        print(LikePostSerializer(instance.post_likes.filter(), many=True).data)
        print(CategorySerializer(instance.categories.all(), many=True).data)
        
        return rep

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user_image = serializers.ImageField(source='user.image', required=False)

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
        # fields = '__all__'
        exclude = ['id']
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['username'] = instance.user.username
        # rep['user_id'] = instance.user.id
        # rep['posts'] = PostSerializer(instance.post).data
        return rep

class LikeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeComment
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    user_image = serializers.ImageField(source='user.image')
    video = serializers.FileField(source='post.video')

    class Meta:
        model = Favorite
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['post_id'] = instance.post.id
        rep['user'] = instance.user.username
        rep['post'] = instance.post.title
        rep['favorites'] = instance.post.favorites.filter().count()
        rep['post_likes'] = instance.post.post_likes.all().count()
        rep['comments'] = CommentSerializer(instance.post.comments.all(), many=True).data

        return rep
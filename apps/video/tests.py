from unittest import TestCase
from datetime import datetime
from .models import Post



class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create( title='Dog', video_tags='Bob')
   
    def test_title_label_test(self):
        post=Post.objects.get(id=1)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEquals(field_label,'title')

    

    def test_title_label_test(self):
        post=Post.objects.get(id=1)
        field_label = post._meta.get_field('video_tags').verbose_name
        self.assertEquals(field_label,'video tags')
    
    
    
    def test_title_max_length_test(self):
        post=Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEquals(max_length,100)

    def test_video_tags_length_test(self):
        post=Post.objects.get(id=1)
        max_length = post._meta.get_field('video_tags').max_length
        self.assertEquals(max_length,1000)
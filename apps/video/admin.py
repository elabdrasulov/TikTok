from django.contrib import admin

from .models import *

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(LikePost)
admin.site.register(LikeComment)
admin.site.register(Favorite)
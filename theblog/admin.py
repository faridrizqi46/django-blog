from django.contrib import admin
from .models import Post, Category, Profile, Comment, coba
from tinymce.widgets import TinyMCE

class MyModelAdmin(admin.ModelAdmin):
    class Media:
        from django.conf import settings
        js = (
            settings.STATIC_URL + 'theblog/js/config.js',
        )

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(coba, MyModelAdmin)

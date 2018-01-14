from django.contrib import admin

from blog.models import Post,Category

admin.site.site_header = "WordPlease Backoffice"
admin.site.register(Post)
admin.site.register(Category)
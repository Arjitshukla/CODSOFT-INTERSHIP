from django.contrib import admin
from blogapp.models import Post,BlogComment
# Register your models here.
admin.site.register((Post,BlogComment))
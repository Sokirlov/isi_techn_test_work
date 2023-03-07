from django.contrib import admin
from .models import Thread, Message

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',  'created', 'updated']
    list_display_links = ['name',  'created', 'updated',]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'thread', 'sender', 'created', 'is_read']
    list_display_links = ['thread', 'sender',]
    list_editable = ['is_read',]
    list_per_page = 10
    list_max_show_all = 500
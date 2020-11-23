# -*- coding: utf-8 -*-
from django.contrib import admin
from forum.models import *

class ForumAdmin(admin.ModelAdmin):
    pass

admin.site.register(Forum, ForumAdmin)

class ThreadAdmin(admin.ModelAdmin):
    list_display = ("title", "publication_date",)
    list_filter = ("forum", "year", "month")
    
admin.site.register(Thread, ThreadAdmin)


class MSAdminInline(admin.StackedInline):
    model = MessageStore
    extra = 0
    
class MessageAdmin(admin.ModelAdmin):
    list_display = ("user", "thread", "publication_date")
    list_filter = ("forum", "year", "month")
    inlines = [MSAdminInline, ]
    
admin.site.register(Message, MessageAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display=("nick", "text", "publication_date", "ua")

admin.site.register(Comment, CommentAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
       

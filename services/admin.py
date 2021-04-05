from django.contrib import admin
from .models import *


class ConversationAdmin(admin.ModelAdmin):
    model = Conversation
    list_display = ['conversation_name', 'messenger', 'hr_conversation']


admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Messenger)


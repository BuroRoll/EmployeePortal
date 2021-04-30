from django.contrib import admin

from .models import Messenger, Conversation, System


class ConversationAdmin(admin.ModelAdmin):
    model = Conversation
    list_display = ['conversation_name', 'messenger', 'hr_conversation', 'conversation_for_accesses',
                    'conversation_for_info']


admin.site.register(System)
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Messenger)

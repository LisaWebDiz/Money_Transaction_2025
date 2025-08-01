from django.contrib import admin

from app.models import Operation


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'type', 'amount', 'timestamp', 'resulting_balance')
    list_display_links = ('id', 'sender')
    list_filter = ('sender', 'receiver', 'type')
    search_fields = ('amount',)
    readonly_fields = ['sender', 'receiver', 'type', 'amount', 'timestamp', 'resulting_balance']

    def has_add_permission(self, request):
        return False

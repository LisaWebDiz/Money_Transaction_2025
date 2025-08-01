from django.contrib import admin

from app.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance')
    list_display_links = ('id', 'user')
    list_filter = ('user', )
    search_fields = ('balance',)

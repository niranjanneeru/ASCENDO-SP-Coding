from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedTabularInline

from ascendo_web_page.game.models import Response
from .models import Profile


class ResponseAdmin(NestedTabularInline):
    model = Response
    fields = ('question', 'answer', 'create_date', 'status')
    extra = 0


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(NestedModelAdmin):
    inlines = [ResponseAdmin]
    search_fields = ['name', 'college', 'nick_name']
    list_display = ['name', 'college']
    list_filter = ['language', 'code', 'has_completed']

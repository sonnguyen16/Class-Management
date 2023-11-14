from django.contrib import admin
from django.forms import Textarea
from django.utils.html import format_html
from .models import Class, User, Attendance, Homework, DoHomework

class ClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_by']
    search_fields = ['name']
    readonly_fields = ['created_by']

    def save_model(self, request, obj, form, change):
        if not change:  # chỉ đặt created_by trong quá trình tạo mới, không phải trong quá trình sửa đổi
            obj.created_by = request.user.username
        super().save_model(request, obj, form, change)

    def display_created_by(self, obj):
        return format_html("<pre>{}</pre>", obj.created_by)

    display_created_by.short_description = "Created By"

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'time']
    search_fields = ['user_id__email']

class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['id', 'class_id', 'title', 'description', 'file']
    search_fields = ['title', 'class_id__name']
    
class DoHomeworkAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'homework_id', 'file', 'score', 'comment']
    search_fields = ['user_id__email', 'homework_id__title']

admin.site.register(Class, ClassAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(DoHomework, DoHomeworkAdmin)

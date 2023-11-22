from django.contrib import admin
from django.forms import Textarea
from .models import Class, User, Attendance, Homework, DoHomework, User_Class, Notification
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('id', 'email', 'get_role')
    add_form_template = 'admin/auth/user/add_form.html'
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'role'),
        }),
    )
    def get_role(self, obj):
        return obj.get_role_display()

    get_role.short_description = 'Role'

class ClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_by']
    search_fields = ['name']

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'time']
    search_fields = ['user_id__email']

class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['id', 'class_id', 'title', 'description', 'file']
    search_fields = ['title', 'class_id__class_name']  # Sửa thành 'class_id__class_name'

    
class DoHomeworkAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'homework_id', 'file', 'score', 'comment']
    search_fields = ['user_id__email', 'homework_id__title']

class User_ClassAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'class_id']
    search_fields = ['user_id__email', 'class_id__class_name']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'link', 'created_at']
    search_fields = ['user__email', 'content']

# Đăng ký custom UserAdmin
# Đăng ký User trước khi hủy đăng ký
admin.site.register(User, UserAdmin)

# Hủy đăng ký User
admin.site.unregister(User)

# Đăng ký custom UserAdmin
admin.site.register(User, CustomUserAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(DoHomework, DoHomeworkAdmin)
admin.site.register(User_Class, User_ClassAdmin)
admin.site.register(Notification, NotificationAdmin)

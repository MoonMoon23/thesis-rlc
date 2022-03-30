from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from .forms import FacultyCreationForm, FacultyChangeForm
from .models import Faculty, Office, Applications, Progress_Reports, Involvement, Projects

class GroupInline(admin.StackedInline):
    model = Faculty
    can_delete = False
    verbose_name_plural = 'Offices'


class GroupAdmin(BaseGroupAdmin):
    inlines = (GroupInline, )

class FacultyAdmin(UserAdmin):
    add_form = FacultyCreationForm
    form = FacultyChangeForm
    model = Faculty
    list_display = ('faculty_id', 'last_name', 'first_name', 'designation', 'rank','department')
    list_filter = ('department', 'designation', 'rank',)
    fieldsets = (
        (None, {'fields': ('faculty_id', 'first_name', 'middle_name','last_name', 'email', 'password', 'designation', 'rank', 'status', 'remarks', 'department', 'college', 'access_level')}),
        ('Permissions', {'fields': ('is_staff','is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('faculty_id', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('faculty_id',)
    ordering = ('faculty_id',)

    verbose_name_plural = 'Faculty Members'


# Register models to admin site
#admin.site.unregister(Group)
admin.site.register(Office)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Applications)
admin.site.register(Progress_Reports)
admin.site.register(Projects)
admin.site.register(Involvement)


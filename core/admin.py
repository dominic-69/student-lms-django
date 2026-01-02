from django.contrib import admin
from .models import Course, Enrollment, Note, LeaveRequest

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course')


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'course')


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'from_date',
        'to_date',
        'status',
        'applied_at'
    )
    list_filter = ('status',)
    search_fields = ('student__username',)
    actions = ['approve_leave', 'reject_leave']

    def approve_leave(self, request, queryset):
        queryset.update(status='APPROVED')

    def reject_leave(self, request, queryset):
        queryset.update(status='REJECTED')

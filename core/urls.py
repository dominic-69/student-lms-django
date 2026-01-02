from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # passssssssssssssssssssss resettttt
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='auth/password_reset.html'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='auth/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='auth/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='auth/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # userrrrrrrrrrrrrrrrrrrrrrrrrrrr
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings_view, name='settings'),

    path('enroll/<int:course_id>/', views.enroll_course, name='enroll'),

    path('add-note/', views.add_note, name='add_note'),
    path('edit-note/<int:note_id>/', views.edit_note, name='edit_note'),
    path('delete-note/<int:note_id>/', views.delete_note, name='delete_note'),

    path('apply-leave/', views.apply_leave, name='apply_leave'),

    #adminnn
    
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/add-course/', views.add_course, name='add_course'),
    path('admin/leaves/', views.admin_leave_requests, name='admin_leave_requests'),

    path(
        'leave/<int:leave_id>/<str:status>/',
        views.update_leave_status,
        name='update_leave_status'
    ),
]

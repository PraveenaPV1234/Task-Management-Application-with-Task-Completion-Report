from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    TaskListAPIView,
    TaskUpdateAPIView,
    TaskReportAPIView,
    admin_dashboard,
    user_list,
    task_list,
    create_account,
    promote_user,

    assign_user_to_admin,
    create_task,
)

urlpatterns = [
    # API Endpoints
    path('tasks/', TaskListAPIView.as_view(), name='task_list_api'),
    path('tasks/<int:id>/', TaskUpdateAPIView.as_view(), name='task_update_api'),
    path('tasks/<int:id>/report/', TaskReportAPIView.as_view(), name='task_report_api'),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Admin Panel URLs
    path('dashboard/', admin_dashboard, name='dashboard'),
    path('users/', user_list, name='user_list'),
    path('tasks-panel/', task_list, name='task_list'), 
    path('create-account/', create_account, name='create_account'),
    path('promote-user/', promote_user, name='promote_user'),
    path('assign-user/', assign_user_to_admin, name='assign_user'),
    path('create-task/', create_task, name='create_task'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
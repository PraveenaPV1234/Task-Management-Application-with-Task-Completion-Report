from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Task, Profile
from .serializers import TaskSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden
# User Task View
class TaskListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
# User Task Update View
class TaskUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            task = Task.objects.get(id=id, assigned_to=request.user)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=404)

        if request.data.get('status') == 'Completed':
            task.status = 'Completed'
            task.completion_report = request.data.get('completion_report')
            task.worked_hours = request.data.get('worked_hours')
            task.save()
            return Response({'message': 'Task marked as completed'})
        return Response({'error': 'Invalid status update'})
# Admin/SuperAdmin View Task Report
class TaskReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({'error': 'Unauthorized'}, status=403)
        try:
            task = Task.objects.get(id=id, status='Completed')
        except Task.DoesNotExist:
            return Response({'error': 'Report not found'}, status=404)
        return Response({
            'completion_report': task.completion_report,
            'worked_hours': task.worked_hours
        })

# admin panel views 
@login_required
def admin_dashboard(request):
    if request.user.is_authenticated and not request.user.is_staff and not request.user.is_superuser:
        tasks = Task.objects.filter(assigned_to=request.user)
    else:
        tasks = [] 
    return render(request, 'admin_panel/dashboard.html', {'tasks': tasks})

@login_required
def user_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Forbidden: You do not have permission to view this page.")
    users = User.objects.all()
    return render(request, 'admin_panel/users.html', {'users': users})

@login_required
def task_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("Forbidden: You do not have permission to view this page.")
    
    if request.user.is_superuser:
        tasks = Task.objects.all()
    else:  # Admin
        tasks = Task.objects.filter(assigned_to__profile__assigned_admin=request.user)
    
    return render(request, 'admin_panel/tasks.html', {'tasks': tasks})
@login_required
def create_account(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Forbidden")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        role = request.POST.get('role')

        new_user = User.objects.create_user(username=username, password=password, email=email)
        if role == 'admin':
            new_user.is_staff = True
        new_user.save()
        messages.success(request, f'{role.capitalize()} created successfully.')
        return redirect('user_list')
    
    return render(request, 'admin_panel/create_account.html')
@login_required
def promote_user(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Forbidden: You do not have permission to view this page.")
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            user.is_staff = True
            user.save()
            messages.success(request, f'{user.username} promoted to Admin.')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
        return redirect('promote_user')
    users = User.objects.filter(is_staff=False, is_superuser=False)
    return render(request, 'admin_panel/promote_user.html', {'users': users})
@login_required
def assign_user_to_admin(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Forbidden: You do not have permission to view this page.")
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        admin_id = request.POST.get('admin_id')
        try:
            user = User.objects.get(id=user_id)
            admin = User.objects.get(id=admin_id, is_staff=True)
            profile, created = Profile.objects.get_or_create(user=user)
            profile.assigned_admin = admin
            profile.save()
            messages.success(request, 'User assigned to admin successfully.')
        except User.DoesNotExist:
            messages.error(request, 'User or Admin not found.')
        return redirect('user_list')
    users = User.objects.filter(is_superuser=False)
    admins = User.objects.filter(is_staff=True, is_superuser=False)
    return render(request, 'admin_panel/assign_user.html', {'users': users, 'admins': admins})

@login_required
def create_task(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("Forbidden: You do not have permission to view this page.")
    
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST['due_date']
        assigned_to_id = request.POST['assigned_to']

        try:
            assigned_to = User.objects.get(id=assigned_to_id)
            # Optional: ensure the user belongs to this admin
            if request.user.is_staff and assigned_to.profile.assigned_admin != request.user:
                return HttpResponseForbidden("Forbidden: You do not have permission to view this page.")
        except User.DoesNotExist:
            return render(request, 'admin_panel/create_task.html', {'error': 'Invalid user selected'})

        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            assigned_to=assigned_to
        )
        messages.success(request, 'Task created and assigned successfully.')
        return redirect('task_list')

    users = User.objects.filter(profile__assigned_admin=request.user)
    return render(request, 'admin_panel/create_task.html', {'users': users})
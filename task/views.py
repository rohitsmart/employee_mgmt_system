from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from task.models import Task
import json
from .decorators import jwt_auth_required
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.http import require_http_methods
from project.views import Project

@csrf_exempt
@jwt_auth_required
@require_POST
def create_task(request):
    if request.method=='POST':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User is unauthenticated'})
            module_id = request.GET.get('id')           #here we are creating the module with the project_id
            if not module_id:
                return JsonResponse({'message': 'Module ID not provided'})
            logged_in_user = user  
            project = Project.objects.get(user=logged_in_user).id
            data = json.loads(request.body)
            task_name= data.get('task_name')
            task_detail = data.get('task_detail')
            status=data.get('status')
            
            task=Task.objects.create(
                task_name=task_name,
                task_detail=task_detail,
                status=status,
                user_id=user,
                project_id=project,
                module_id=module_id
            )
            task.save()
            return JsonResponse({'message':'task created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error':'only the POST method is allowed'})    
    
@jwt_auth_required
@require_http_methods(['PUT'])
@csrf_exempt 
def update_task(request):
    if request.method=='PUT':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User is unauthenticated'})
            task_id=request.GET.get('id')
            if not task_id:
                return JsonResponse({'message':'task not found'})
            data = json.loads(request.body)
            task= Task.objects.get(id=task_id)
            task.task_name = data.get('task_name')
            task.task_detail=data.get('task_detail')
            task.status=data.get('status')
            task.save()
            return JsonResponse({'message':'task updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'message':'only PUT method is allowed'})    

@jwt_auth_required
@require_GET
def get_task(request):
    if request.method=='GET':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User is unauthenticated'})
            task_id=request.GET.get('id')
            if not task_id:
                return JsonResponse({'message':'task not found'})
            task =Task.objects.get(id=task_id)
            return JsonResponse({
                'task_name':task.task_name,
                'task_detail':task.task_detail,
                'status':task.status
            })
        except Task.DoesNotExist:
            return JsonResponse({'error': 'task not found'})
    else:
        return JsonResponse({'message':'only GET method are allowed to fetch the task'})  
    
@csrf_exempt 
@jwt_auth_required
@require_http_methods(['DELETE'])
def delete_task(request):
    if request.method=='DELETE':
        try:
            
            task_id=request.GET.get('id')  
            if not task_id:
                return JsonResponse({'message':'task not found'})
            project=Task.objects.get(id=task_id)
            project.delete()
            return JsonResponse({'message':'task deleted successfully'})
        except Task.DoesNotExist:
            return JsonResponse({'error':'task not found'})
    else:
        return JsonResponse({'error':'only DELETE method are allowed to delete the task'})      
                    
# Create your views here.

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from assign.models import Assign
from project.models import Project
from module.models import Module
from recruit.models import AuthorizeToModule
from task.models import Task
from .decorators import jwt_auth_required
from users.decorators import role_required


@csrf_exempt
@require_POST
@jwt_auth_required
@role_required('employee')
def assign_task(request):      #here we assign the task by task id , tsk can only be assigned by the tl or pm  or admin
    if request.method == 'POST':
        try:
            user = request.user
            if not user:
                return JsonResponse({'error': 'User not found'})
            if user.role != 'admin':
                return JsonResponse({'error': 'only admin are allowed to access this'})
            task_id = request.GET.get('id')
            task=Task.objects.filter(id=task_id).first()
            if not task:
                  return JsonResponse({'message':'task not found'})
            existing_task = Assign.objects.filter(task_id=task_id).exists()
            if existing_task:
                  return JsonResponse({'message': 'Task ID is already assigned'})
        
            data = json.loads(request.body)
            assigned_to = data.get('assigned_to')
            assigned_by = data.get('assigned_by')
            assign_date = data.get('assign_date')  
            deadline = data.get('deadline')
            status = data.get('status')
            comment = data.get('comment')
            
            existing_assignment = Assign.objects.filter(task_id=task_id, assigned_to=assigned_to).exists()
            if existing_assignment:
                return JsonResponse({'message': 'Task is already assigned to {}'})
            # Creating the new model object here
            assign = Assign.objects.create(        
                assigned_to=assigned_to,
                assigned_by=assigned_by,
                assign_date=assign_date,
                deadline=deadline,
                status=status,
                comment=comment,
                task_id=task_id,               
            )
            assign.save()
            return JsonResponse({'message': ' task successfully assign to the employee'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Only POST requests are allowed'})

@csrf_exempt
@require_http_methods(["DELETE"])
@jwt_auth_required
@role_required('employee')
def unassign_task(request):          #this api also only accessed by the tl or pm or admin
    if request.method == 'DELETE':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User not found'})
            authorizeToModule=AuthorizeToModule.objects.filter(employee_id=user).exists()
            if not authorizeToModule:
                return JsonResponse({'error': 'you are not authorized to add device'})
            assign_id = request.GET.get('id')
            if not assign_id:
                return JsonResponse({'message':'module id not found'})
            assign = Assign.objects.get(id=assign_id)
            assign.delete()
            return JsonResponse({'message': 'Module deleted successfully'})
        except Assign.DoesNotExist:
         return JsonResponse({'error': 'Module not found'})
    else:
       return JsonResponse({'error':'only DELETE method are allowed'}) 
   
@csrf_exempt
@require_http_methods(['PUT'])
@jwt_auth_required
def update_assignTask(request):          
    if request.method == 'PUT':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User not found'})
            assign_id = request.GET.get('id')
            if not assign_id:
                return JsonResponse({'message':'task not assigned'})
            data = json.loads(request.body)
            assign = Assign.objects.get(id=assign_id)
            assign.assigned_to= data.get('assigned_to')
            assign.assign_date = data.get('assign_date')
            assign.deadline = data.get('deadline')
            assign.status = data.get('status')
            assign.comment = data.get('comment')
            assign.save()
            return JsonResponse({'message': 'task assign updated successfully'})
        except Assign.DoesNotExist:
            return JsonResponse({'error': 'task assign not found'})
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed for updating assignment'})   

@require_GET
@jwt_auth_required
def get_assignedTask(request):
    if request.method=='GET':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User not found'})
            # assign_id = request.GET.get('id')
            # if not assign_id:
            #     return JsonResponse({'message':' assign task not found'})
            assigns=Assign.objects.all()
            if not assigns:
                return JsonResponse({'message': 'assign task not found'})
            assign_task = []
            for assign in assigns:
                assign_task.append({
                    'assigned_to': assign.assigned_to,
                    'assigned_by': assign.assigned_by,
                    'assign_date': assign.assign_date,
                    'deadline': assign.deadline,
                    'status': assign.status,
                    'comment ': assign.comment                    
                })
                return JsonResponse({'assign_task': assign_task})
        except Assign.DoesNotExist:
            return JsonResponse({'error':'assign task not found'})

# Create your views here.

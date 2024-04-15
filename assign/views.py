from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from assign.models import Assign
from project.models import Project
from module.models import Module
from task.models import Task
from .decorators import jwt_auth_required
@csrf_exempt
@require_POST
@jwt_auth_required
def assign_task(request):      #here we assign the task by task id
    if request.method == 'POST':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'error': 'User not found'})
            task_id = request.GET.get('id')
            task=Task.objects.filter(id=task_id).first()
            if not task_id:
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
            print(6)
             # Check if the task is already assigned to the specified user
            existing_assignment = Assign.objects.filter(task_id=task_id, assigned_to=assigned_to).exists()
            print(7)
            if existing_assignment:
                return JsonResponse({'message': 'Task is already assigned to {}'})
            print(8)
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
            print(9)
            assign.save()
            return JsonResponse({'message': ' task successfully assign to the employee'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Only POST requests are allowed'})

@csrf_exempt
@require_http_methods(["DELETE"])
@jwt_auth_required
def unassign_task(request):
    if request.method == 'DELETE':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User not found'})
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
def update_assignTask(request):          #updating the device according to the device id
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
            # assign.assigned_by = data.get('assigned_by')    #here the assign_by name may be not be updated 
            assign.assign_date = data.get('assigned_date')
            assign.deadline = data.get('deadline')
            assign.status = data.get('status')
            assign.comment = data.get('comment')
            assign.save()
            return JsonResponse({'message': 'task assign updated successfully'})
        except Assign.DoesNotExist:
            return JsonResponse({'error': 'task assign not found'})
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed for updating assignment'})   


# Create your views here.

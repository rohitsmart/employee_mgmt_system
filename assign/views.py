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
def assign_task(request):
    try:
        print(1)
        user = request.user_id
        print(2)
        if not user:
            return JsonResponse({'error': 'User not found'})
        logged_in_user = user  # Assuming you already have the logged-in user object
        project = Project.objects.get(user=logged_in_user)
        print(3)
        current_project=project.project
        print(0)
        module = Module.objects.get(project=current_project)
        print(4)
        current_module=module
        task=Task.objects.get(module=current_module)
        print(5)

        if request.method == 'POST':
            data = json.loads(request.body)
            assigned_to = data.get('assigned_to')
            assigned_by = data.get('assigned_by')
            assign_date = data.get('assign_date')  
            deadline = data.get('deadline')
            status = data.get('status')
            comment = data.get('comment')
            
            # Creating the new model object here
            assign = Assign.objects.create(          
                assigned_to=assigned_to,
                assigned_by=assigned_by,
                assign_date=assign_date,
                deadline=deadline,
                status=status,
                comment=comment,
                project_id=project,
                module_id=module,
                task_id=task,               
            )
            assign.save()
            return JsonResponse({'message': ' task successfully assign to the employee'})
    except Exception as e:
        return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Only POST requests are allowed'})

# Create your views here.

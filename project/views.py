from rest_framework.decorators import api_view, permission_classes,authentication_classes
# from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from module.models import Module
from project.models import Project
from users.models import User
from recruit.models import AuthorizeToModule
import json
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from django.utils import timezone
# from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.http import require_http_methods
from .decorators import jwt_auth_required,role_required


@csrf_exempt
@require_POST
@jwt_auth_required
@role_required('employee')
def create_module(request):
    if request.method == 'POST':
        try:           
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User not found'})
            project_id = request.GET.get('id')           #here we are creating the module with the project_id
            authorizeToModule=AuthorizeToModule.objects.filter(employee_id=user).exists()
            if not authorizeToModule:
                return JsonResponse({'error': 'you are not authorized to add device'})
            if not project_id:
                return JsonResponse({'message': 'Project ID not provided'})
            data = json.loads(request.body)
            module_name = data.get('module_name') 
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            description = data.get('description')
            assigned_hours = data.get('assigned_hours')
            actual_hours = data.get('actual_hours')
            
            # Creating the new model object here
            module = Module.objects.create(          
                module_name=module_name,
                project_id=project_id,
                user_id=user,
                start_date=start_date,
                end_date=end_date,
                description=description,
                assigned_hours=assigned_hours,
                actual_hours=actual_hours
            )
            module.save()
            
            return JsonResponse({'message': 'Module created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})
@csrf_exempt
@require_http_methods(["DELETE"])
@jwt_auth_required
@role_required('employee')
def delete_module(request):
    if request.method == 'DELETE':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User not found'})
            authorizeToModule=AuthorizeToModule.objects.filter(employee_id=user).exists()
            if not authorizeToModule:
                return JsonResponse({'error': 'you are not authorized to add device'})
            module_id = request.GET.get('id')
            if not id:
                return JsonResponse({'message':'module id not found'})
            module = Module.objects.get(id=module_id)
            module.delete()
            return JsonResponse({'message': 'Module deleted successfully'})
        except Module.DoesNotExist:
         return JsonResponse({'error': 'Module not found'})
    else:
       return JsonResponse({'error':'only DELETE method are allowed'}) 
   
@csrf_exempt
@require_http_methods(["PUT"])
@jwt_auth_required
@role_required('employee')
def update_module(request):
    if request.method == 'PUT':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User not found'})
            authorizeToModule=AuthorizeToModule.objects.filter(employee_id=user).exists()
            if not authorizeToModule:
                return JsonResponse({'error': 'you are not authorized to add device'})
            module_id = request.GET.get('id')
            if not id:
                return JsonResponse({'message':'module id not found'})
            data = json.loads(request.body)
            module = Module.objects.get(id=module_id)
            module.module_name = data.get('module_name')
            module.start_date = data.get('start_date')
            module.end_date = data.get('end_date')
            module.description = data.get('description')
            module.assigned_hours = data.get('assigned_hours')
            module.actual_hours = data.get('actual_hours')
            module.save()
            return JsonResponse({'message': 'Module updated successfully'})
        except Module.DoesNotExist:
            return JsonResponse({'error': 'Module not found'})
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed for updating module'})

@require_GET
@jwt_auth_required
@role_required('employee')
def get_module(request):
    if request.method == 'GET':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User not found'})
            authorizeToModule=AuthorizeToModule.objects.filter(employee_id=user).exists()
            if not authorizeToModule:
                return JsonResponse({'error': 'you are not authorized to add device'})
            module_id = request.GET.get('id')
            if not id:
                return JsonResponse({'message':'module id not found'})
            module = Module.objects.get(id=module_id)
            return JsonResponse({'module_name': module.module_name, 
                             'start_date':module.start_date,
                             'end_date':module.end_date,
                             'description':module.description,
                             'assigned_hours':module.assigned_hours,
                             'actual_hours':module.actual_hours
                             })
        except Module.DoesNotExist:
            return JsonResponse({'error': 'Module not found'})
    else:
        return JsonResponse({'error':'only GET method is allowed for fetching the module'})
    
@csrf_exempt
@require_POST
@jwt_auth_required
@role_required('employee')
def create_project(request):
    try:
        user = request.user_id
        if not user:
            return JsonResponse({'error': 'User not found'})
        authorizeToModule=AuthorizeToModule.objects.filter(employee_id=user).exists()
        if not authorizeToModule:
                return JsonResponse({'error': 'you are not authorized to add device'})
        if request.method == 'POST':
            data = json.loads(request.body)
            project_name = data.get('project_name')
            description = data.get('description')
            number_of_module = data.get('number_of_module')  
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            status = data.get('status')
            
            project = Project.objects.create(          
                project_name=project_name,
                user_id=user,
                start_date=start_date,
                end_date=end_date,
                description=description,
                number_of_module=number_of_module,
                status=status,
            )
            project.save()
            return JsonResponse({'message': 'Project created successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Only POST requests are allowed'})


@require_GET
@jwt_auth_required
@role_required('employee')
def get_project(request):
    if request.method == 'GET':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'error': 'User not found'})
            authorizeToModule=AuthorizeToModule.objects.filter(employee_id=user).exists()
            if not authorizeToModule:
                return JsonResponse({'error': 'you are not authorized to add device'})
            project_id = request.GET.get('id')
            if not id:
                return JsonResponse({'message':'project id not found'})
            project = Project.objects.get(id=project_id)
            return JsonResponse({'project_name': project.project_name, 
                             'start_date':project.start_date,
                             'end_date':project.end_date,
                             'description':project.description,
                             'number_of_module':project.number_of_module,
                             'status':project.status
                             })
        except Project.DoesNotExist:
            return JsonResponse({'error': 'project not found'})
    else:
        return JsonResponse({'error':'only GET method is allowed for fetching the project'})
 
@require_http_methods(["PUT"])
@jwt_auth_required  
@csrf_exempt
@role_required('employee')
def update_project(request):
    if request.method == 'PUT':
        try:
            user = request.user_id
            if not user:
             return JsonResponse({'error': 'User not found'})
            authorizeToModule=AuthorizeToModule.objects.filter(employee_id=user).exists()
            if not authorizeToModule:
                return JsonResponse({'error': 'you are not authorized to add device'})
            project_id = request.GET.get('id')
            if not project_id:
                return JsonResponse({'message':'project id not found'})
            data = json.loads(request.body)
            project = Project.objects.get(id=project_id)
            project.project_name = data.get('project_name')
            project.description = data.get('description')
            project.number_of_module = data.get('number_of_module')
            project.start_date = data.get('start_date')
            project.end_date = data.get('end_date')
            project.status = data.get('status')
            project.save()
            return JsonResponse({'message': 'project updated successfully'})
        except Project.DoesNotExist:
            return JsonResponse({'error': 'project not found'})
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed for updating the project'})    
    
    
@require_http_methods(["DELETE"])
@jwt_auth_required    
@csrf_exempt  
@role_required('employee')
def delete_project(request):
    if request.method=='DELETE':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'error': 'User not found'})
            authorizeToModule=AuthorizeToModule.objects.filter(employee_id=user).exists()
            if not authorizeToModule:
                return JsonResponse({'error': 'you are not authorized to add device'})
            project_id=request.GET.get('id')  
            if not project_id:
                return JsonResponse({'message':'project not found'})
            project=Project.objects.get(id=project_id)
            project.delete()
            return JsonResponse({'message':'project deleted successfully'})
        except Project.DoesNotExist:
            return JsonResponse({'error':'project not found'})
    else:
        return JsonResponse({'error':'only DELETE method are allowed to delete the project'})
# Create your views here.




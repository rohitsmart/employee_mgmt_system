from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from module.models import Module
from users.models import User
import json
# from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes


@csrf_exempt
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_module(request):
    if request.method == 'POST':
        try:
            user = request.user
            if not user:
                return JsonResponse({'message': 'User is unauthenticated'})
            data = json.loads(request.body)
            module_name = data.get('module_name')
            project_id = data.get('project_id')
            user_id = data.get('user_id')  
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            description = data.get('description')
            assigned_hours = data.get('assigned_hours')
            actual_hours = data.get('actual_hours')
            
            # Creating the new model object here
            module = Module.objects.create(          
                module_name=module_name,
                project_id=project_id,
                user_id=user_id,
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
def delete_module(request):
    if request.method == 'DELETE':
        try:
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
def update_module(request):
    if request.method == 'PUT':
        try:
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

def get_module(request):
    if request.method == 'GET':
        try:
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
        return JsonResponse({'error':'only GET method is allowed for fetching the profile'})

# Create your views here.

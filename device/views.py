from django.shortcuts import render
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from device.models import Device
from recruit.models import AuthorizeToModule
from .decorators import jwt_auth_required,role_required

@csrf_exempt
@require_POST
@jwt_auth_required
@role_required('employee')
def add_device(request):      #here we assign the task by task id
    if request.method == 'POST':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'error': 'User not found'})
            authorizeToModule=AuthorizeToModule.objects.filter(employee_id=user).exists()
            if not authorizeToModule:
                return JsonResponse({'error': 'you are not authorized to access device'})      
            data = json.loads(request.body)
            device_name = data.get('device_name')
            device_type = data.get('device_type')
            deviceID = data.get('deviceID')  
            location = data.get('location')
                                                  
            # Creating the new model object here
            device = Device.objects.create(        
                device_name=device_name,
                device_type=device_type,
                deviceID=deviceID,
                location=location,
                user_id=user,              
            )
            device.save()
            return JsonResponse({'message': ' device added successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Only POST requests are allowed'})

@role_required('employee')
@csrf_exempt
@require_http_methods(['DELETE'])
@jwt_auth_required
def remove_device(request):
    if request.method == 'DELETE':
        try:
            user=request.user_id
            if not user:
                return JsonResponse({'message': 'user not found'})
            authorizeToModule=AuthorizeToModule.objects.filter(employee_id=user).exists()
            if not authorizeToModule:
                return JsonResponse({'error': 'you are not authorized to access device'})
            device_id=request.GET.get('id')
            if  not device_id:
                return JsonResponse({'message': 'device id not found'})
            device=Device.objects.get(id=device_id)
            device.delete()
            return JsonResponse({'message': 'device removed successfully'})
        except Device.DoesNotExist as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error':'only DELETE method is supported'}) 

@role_required('employee')
@csrf_exempt
@require_GET
@jwt_auth_required
def get_device(request):
    if request.method == 'GET':
        try:           
            user=request.user_id
            if not user:
                return JsonResponse({'message': 'user not found'})  
            authorizeToModule=AuthorizeToModule.objects.filter(employee_id=user).exists()
            if not authorizeToModule:
                return JsonResponse({'error': 'you are not authorized to access device'})          
            devices=Device.objects.all()
            if not devices:
                return JsonResponse({'message': 'device not found'})
            device_data = []
            for device in devices:
                device_data.append({
                    'device_name': device.device_name,
                    'device_type': device.device_type,
                    'deviceID': device.deviceID,
                    'location': device.location
                })
                return JsonResponse({'devices': device_data})
        except Device.DoesNotExist as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error':'only GET method is supported'})

@role_required('employee')
@csrf_exempt
@require_http_methods(['PUT'])
@jwt_auth_required
def update_device(request):          #updating the device according to the device id
    if request.method == 'PUT':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User not found'})
            authorizeToModule=AuthorizeToModule.objects.filter(employee_id=user).exists()
            if not authorizeToModule:
                return JsonResponse({'error': 'you are not authorized to access device'})
            device_id = request.GET.get('id')
            if not device_id:
                return JsonResponse({'message':'device  id not found'})
            data = json.loads(request.body)
            device = Device.objects.get(id=device_id)
            device.device_name= data.get('device_name')
            device.device_type = data.get('device_type')
            device.deviceID = data.get('deviceID')
            device.location = data.get('location')
            device.save()
            return JsonResponse({'message': 'device updated successfully'})
        except Device.DoesNotExist:
            return JsonResponse({'error': 'Device not found'})
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed for updating device'})
   
        
            
            
            
    

# Create your views here.

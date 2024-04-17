from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json
from attendance.models import Attendance
from .decorators import jwt_auth_required
@csrf_exempt
@require_POST
@jwt_auth_required
def mark_attendance(request):      
    if request.method == 'POST':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'error': 'User not found'})
        
            data = json.loads(request.body)
            date = data.get('date')
            in_time = data.get('in_time')
            out_time = data.get('out_time')  
            
            # Creating the new model object here
            attendance = Attendance.objects.create(        
                date=date,
                in_time=in_time,
                out_time=out_time,
                user_id=user,              
            )
            print(9)
            attendance.save()
            return JsonResponse({'message': ' attendance marked successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Only POST requests are allowed'})

@require_GET
@jwt_auth_required
def get_attendance(request):
    if request.method == 'GET':
        try:          
            user_id = request.GET.get('id')
            if not user_id:
                return JsonResponse({'message': 'User ID not provided'})

            attendances = Attendance.objects.filter(user_id=user_id)

            if not attendances:
                return JsonResponse({'message': 'No attendance records found for the user'})

            attendance_list = []
            for attendance in attendances:
                attendance_list.append({
                    'date': attendance.date,
                    'in_time': attendance.in_time,
                    'out_time': attendance.out_time,
                })
            return JsonResponse({'attendances': attendance_list})
        
        except Attendance.DoesNotExist as e:
            return JsonResponse({'error': str(e)})
    
    return JsonResponse({'error':'only GET method is supported'})
# Create your views here.

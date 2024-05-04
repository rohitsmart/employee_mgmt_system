from django.shortcuts import render
from leave.models import Leave
from users.models import User
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.http import require_http_methods
from .decorators import jwt_auth_required
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_POST
@jwt_auth_required
def apply_leave(request):
    if request.method == 'POST':
        try:
            user=request.user_id
            if not user:
                return JsonResponse({'message': 'user not found'})
            data=json.loads(request.body)
            leave_type=data.get('leave_type')
            start_date=data.get('start_date')
            end_date=data.get('end_date')
            reason=data.get('reason')
            status=data.get('status')
            leave=Leave.objects.create(
                                       leave_type=leave_type,
                                       start_date=start_date,
                                       end_date=end_date,
                                       reason=reason,
                                       status=status,
                                       user_id=user)
            leave.save()
            return JsonResponse({'message': 'Leave applyied successfully'})
        except Leave.DoesNotExist as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})
    
@csrf_exempt
@require_GET
@jwt_auth_required
def update_leave(request):
    if request.method=='PUT':
        try:
            user=request.user_id
            if not user:
                return JsonResponse({'message': 'user not found'})
            leave_id=request.GET.get('id')
            if not leave_id:
                return JsonResponse({'message':'leave not found'})
            leave=Leave.objects.filter(id=leave_id)
            data=json.loads(request.body)
            leave.leave_type=data.get('leave_type')
            leave.start_date=data.get('start_date')
            leave.end_date=data.get('end_date')
            leave.reason=data.get('reason')
            leave.status=data.get('status')
            leave.save()
            return JsonResponse({'message':'leave updated successfully'})
        except Leave.DoesNotExist as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'message':'only PUT method is allowed'})
    
@csrf_exempt
@require_GET
@jwt_auth_required
def get_leave(request):
    if request.method == 'GET':
        try:
            user=request.user_id
            if not user:
                return JsonResponse({'message': 'user not found'})
            user_id=request.GET.get('id')
            if not user_id:
                return JsonResponse({'message':'leave not found'})
            leaves=Leave.objects.filter(user_id=user_id)
            if not leaves:
                return JsonResponse({'message':'leave not found'})
            leave_applied=[]
            for leave in leaves:
                leave_applied.append({
                    'leave_type':leave.leave_type,
                   'start_date':leave.start_date,
                    'end_date':leave.end_date,
                   'reason':leave.reason,
                   'status':leave.status
                })           
            return JsonResponse({'leave':leave_applied})
        except Leave.DoesNotExist as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'message':'only GET method is allowed'})  
    
@csrf_exempt
@require_http_methods(['DELETE'])
@jwt_auth_required
def delete_leave(request):
    if request.method == 'DELETE':
        try:
            user=request.user_id
            if not user:
                return JsonResponse({'message': 'user not found'})
            leave_id=request.GET.get('id')
            if not leave_id:
                return JsonResponse({'message':'leave not found'})
            leave=Leave.objects.get(id=leave_id)
            leave.delete()
            return JsonResponse({'message':'leave deleted successfully'})
        except Leave.DoesNotExist as e:
            return JsonResponse({'error': str(e)})
            

# Create your views here.

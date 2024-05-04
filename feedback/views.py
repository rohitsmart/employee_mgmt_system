from django.http import JsonResponse
from django.shortcuts import render
from users.models import User
from feedback.models import Feedback
import json
from django.views.decorators.csrf import csrf_exempt
from .decorators import jwt_auth_required,role_required
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_POST
@jwt_auth_required
@role_required('employee')
def create_feedback(request):
    if request.method == 'POST':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User is unauthenticated'})
            data = json.loads(request.body)
            feedback_type = data.get('feedback_type')
            feedback_details = data.get('feedback_details')
            feedback_date = data.get('feedback_date')
            feedback_provider = data.get('feedback_provider')
            feedback_rating = data.get('feedback_rating')
            status = data.get('status')
            action_taken = data.get('action_taken')
            
            # Creating the new model object here
            feedback = Feedback.objects.create(          
                feedback_type=feedback_type,
                feedback_details=feedback_details,
                user_id=user,
                feedback_date=feedback_date,
                feedback_provider=feedback_provider,
                feedback_rating=feedback_rating,
                status=status,
                action_taken=action_taken
            )
            feedback.save()
            
            return JsonResponse({'message': 'Module created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})
    
@csrf_exempt
@jwt_auth_required
@require_http_methods(["PUT"])
@role_required('employee')
def update_feedback(request):
    if request.method=='PUT':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User is unauthenticated'})
            feedback_id = request.GET.get('id')
            if not id:
                return JsonResponse({'message':'feedback id not found'})
            data = json.loads(request.body)
            feedback = Feedback.objects.get(id=feedback_id)
            feedback.feedback_type= data.get('feedback_type')
            feedback.feedback_details = data.get('feedback_details')
            feedback.feedback_date = data.get('feedback_date')
            feedback.feedback_provider = data.get('feedback_provider')
            feedback.feedback_rating = data.get('feedback_rating')
            feedback.status = data.get('status')
            feedback.action_taken=data.get('action_taken')
            feedback.save()
            return JsonResponse({'message': 'Module updated successfully'})
        except Feedback.DoesNotExist:
            return JsonResponse({'error': 'Module not found'})
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed for updating module'})

@require_GET
@jwt_auth_required   
def get_project(request):
    if request.method == 'GET':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User is unauthenticated'})
            project_id = request.GET.get('id')
            if not id:
                return JsonResponse({'message':'project id not found'})
            project = Feedback.objects.get(id=project_id)
            return JsonResponse({'project_name': project.project_name, 
                             'start_date':project.start_date,
                             'end_date':project.end_date,
                             'description':project.description,
                             'number_of_module':project.number_of_module,
                             'status':project.status
                             })
        except Feedback.DoesNotExist:
            return JsonResponse({'error': 'project not found'})
    else:
        return JsonResponse({'error':'only GET method is allowed for fetching the project'})    

@csrf_exempt
@require_http_methods(["DELETE"])
@jwt_auth_required
@role_required('employee')
def delete_feedback(request):
    if request.method == 'DELETE':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User not found'})
            feedback_id = request.GET.get('id')
            if not id:
                return JsonResponse({'message':'feedback id not found'})
            feedback = Feedback.objects.get(id=feedback_id)
            feedback.delete()
            return JsonResponse({'message': 'feedback deleted successfully'})
        except Feedback.DoesNotExist:
         return JsonResponse({'error': 'feedback not found'})
    else:
       return JsonResponse({'error':'only DELETE method are allowed'})             
    

@csrf_exempt
@require_POST
@jwt_auth_required
@role_required('employee')
def post_feedback(request):
    try:
        user_id = request.user_id
        data = json.loads(request.body)
        if not User.objects.filter(id=user_id).exists():
            return JsonResponse({'error': 'User is not authorized or does not exist'}, status=403)

        Feedback.objects.create(
            user_id=user_id,
            feedback_details=data.get('feedback_details'),
            feedback_provider=data.get('feedback_provider'),
            feedback_rating=data.get('feedback_rating'),
            feedback_date=data.get('feedback_date'),
            publish=data.get('publish', False)
        )
        return JsonResponse({'message': 'Feedback posted successfully'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
# Create your views here.

import os
from django.core.files.storage import default_storage
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from project.decorators import jwt_auth_required
from recruit.models import AuthorizationToEmployee, AuthorizeToModule
from users.serializers import UserSerializer
from .models import User
from .models import EmpID
from .models import EmpModule
from django.db.models import Max
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.utils.timezone import now
from django.db import IntegrityError
from users.models import EmpID 
from django.contrib.auth import authenticate
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import time
from django.core.cache import cache
from django.core.mail import send_mail
from project.models import Token

from .models import User

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if 'firstName' in data and 'lastName' in data and 'role' in data and 'mobileNumber' in data:
            email = f"{data['firstName'].lower()}.{data['lastName'].lower()}@perfectkode.com"

            last_emp_id = EmpID.objects.aggregate(max_emp_id=Max('emp_id'))['max_emp_id'] or 999 #1000
            emp_id = last_emp_id + 1 #1001
            password = f"{data['firstName'][0].upper()}{data['lastName']}@{emp_id}"

            try:
                                
                emp_id_record = EmpID.objects.create(emp_id=emp_id)

                user = User.objects.create(
                    emp_id=emp_id_record,
                    firstName=data['firstName'],
                    lastName=data['lastName'],
                    email=email,
                    role=data['role'],
                    mobileNumber=data['mobileNumber'],
                    password=make_password(password),
                    active=False
                )
                response_data = {
                    'message': 'User signed up successfully',
                    'email': email,
                    'password': password
                }
                return JsonResponse(response_data, status=201)
            except IntegrityError as e:
                return JsonResponse({'error': 'Email or mobile number already exists'}, status=400)
        else:
            return JsonResponse({'error': 'First name, last name, role, and mobile number are required'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
@require_POST
def register_candidate(request):
    if request.method=='POST':
        try:
            data=json.loads(request.body)
            # userName=data.get('userName')
            fullName=data.get('fullName')
            # address=data.get('address')
            degree=data.get('degree')
            email=data.get('email')
            mobileNumber=data.get('mobileNumber')
            cv_url=data.get('cv_url')
            role='employee'
        
            candidate=User.objects.create(
            # userName=userName,
            fullName=fullName,
            # address=address,
            degree=degree,
            email=email,
            mobileNumber=mobileNumber,
            cv_url=cv_url,
            role=role
            )
            candidate.save()
            return JsonResponse({'messge':'profile submitted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})
            
        
        
        
            


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = User.objects.filter(email=email).first()
            if user:
                if (password, user.password):
                    token = jwt.encode({
                        'user_id': user.id,
                        'exp': datetime.utcnow() + timedelta(hours=1)  # Token expiry time
                    }, 'kkfwnfnfnjfknerkbeg', algorithm='HS256')
                    Token.objects.create(
                       token = token 
                    )
                    return JsonResponse({
                        'user_id': user.id,
                        'access_token': token,
                    }, status=200)
                else:
                    return JsonResponse({'error': 'Invalid credentials'}, status=400)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        else:
            return JsonResponse({'error': 'Email and password are required'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@require_POST
@jwt_auth_required
def logout(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
        
        if Token.objects.filter(token=token).exists():
            Token.objects.filter(token=token).delete()
            return JsonResponse({'message': 'Successfully logged out'}, status=200)
        else:
            return JsonResponse({'error': 'Token does not exist'}, status=400)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
@jwt_auth_required
def update_password(request):
    try:
        data = json.loads(request.body)
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        user = User.objects.filter(id=request.user_id).first()
        if not user:
            return JsonResponse({'error': 'User is not authorized or does not exist'}, status=403)
        if not check_password(current_password, user.password):
            return JsonResponse({'error': 'Current password & old password cannot be same'}, status=400)
        user.password = make_password(new_password)
        user.save()
        return JsonResponse({'message': 'Password updated successfully'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@csrf_exempt
@require_POST
def forget_password(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            return JsonResponse({'error': 'User with this email does not exist'}, status=404)

        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        cache.set(email, otp, 300)
        return JsonResponse({'otp': otp})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def update_password_with_otp(request):
    try:
        data = json.loads(request.body)
        email =data.get('email')
        otp = data.get('otp')
        new_password = data.get('new_password')
        user = User.objects.get(email=email)
        print(user)
        cached_otp = cache.get(email)

        if not cached_otp or cached_otp != otp:
            return JsonResponse({'error': 'Invalid or expired OTP'}, status=400)

        user.password = new_password
        user.save()
        cache.delete(user.email)
        return JsonResponse({'message': 'Password updated successfully'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
def upload_cv(request):
    if request.method == 'POST':
        try:
            if request.FILES.get('file'):
                file = request.FILES['file']
                timestamp = int(datetime.now().timestamp())
                filename = f'file_{timestamp}{os.path.splitext(file.name)[1]}'
                path = default_storage.save(f'public/files/{filename}', file)
                cv_url = default_storage.url(path)
                image = User(cv_url=cv_url)
                image.save()
                return JsonResponse({'success': 'Image uploaded', 'image_url': cv_url})
            else:
                return JsonResponse({'error': 'No file uploaded'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred during uploading the image'}, status=500)
    
    
@csrf_exempt
@require_POST
def create_empmodule(request):
        if request.method == 'POST':
            try:
                data=json.loads(request.body)
                moduleName=data.get('moduleName')
                moduleKey=data.get('moduleKey')   #this will be the alphanumeric filed
                empModule=EmpModule.create.objects(
                    moduleName=moduleName,
                    moduleKey=moduleKey
                )
                empModule.save()
                return JsonResponse({'message':'module created successfully'})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'error': 'Only POST requests are allowed'})
        
@csrf_exempt
@require_http_methods(['PUT'])
def update_empModule(request):
    if request.method=='PUT':
        try:
            module_id=request.get('id')
            if module_id:
                return JsonResponse({'message':'module not found'})
            data=json.loads(request.body)
            empModule=EmpModule.objects.get(id=module_id)
            empModule.moduleName=data.get('moduleName')
            empModule.moduleKey=data.get('moduleKey')
            empModule.save()
            return JsonResponse({'success':'module upated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed'})
    
@require_GET
def get_empModule(request):
    if request.method=='GET':
        try:
            module_id=request.GET.get('id')
            if module_id:
                return JsonResponse({'message':'module not found'})
            empModule=EmpModule.objects.get(id=module_id)
            return JsonResponse({'moduleName':empModule.moduleName,
                                 'moduleKey':empModule.moduleKey})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'})    
            
                    
@csrf_exempt
@require_POST
@jwt_auth_required
def authorization_to_module(request):
    if request.method=='POST':
        try:
            data=json.loads(request.body)
            employee_id=data.get('employee_id')
            module_id=data.get('module_id')
            authorizeToModule=AuthorizeToModule.objects.create(employee_id=employee_id, module_id=module_id)
            authorizeToModule.save()           
            return JsonResponse({'success': 'employee authorized successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})
    
@csrf_exempt
@require_http_methods(['PUT'])
@jwt_auth_required
def update_authorization_to_module(request):
    if request.method=='PUT':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User is unauthenticated'})
            module=request.GET.get('id')
            if not module:
                return JsonResponse({'message':'module not found'})
            data = json.loads(request.body)
            authorizeToModule= AuthorizeToModule.objects.get(id=module)
            authorizeToModule.module_id = data.get('module_id')
            authorizeToModule.employee_id=data.get('employee_id')
            authorizeToModule.save()
            return JsonResponse({'message':'authorization updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed'})    
    
@csrf_exempt
@require_POST
@jwt_auth_required
def authorize_to_employee(request):
    if request.method == 'POST':
        try:
            user=request.user_id
            if not user:
                return JsonResponse({'message': 'User is unauthenticated'})
            data=json.load(request.body)
            emp_id=data.get('emp_id')
            candidate_id=data.get('candidate_id')
            authEmployee=AuthorizationToEmployee.objects.create(emp_id=emp_id,candidate_id=candidate_id)
            authEmployee.save()
            return JsonResponse({'success':'employee is authorized to employee'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}) 
    
@csrf_exempt
@require_http_methods(['PUT'])
@jwt_auth_required
def update_authorization_to_employee(request):
    if request.method == 'PUT':
        try:
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User is unauthenticated'})
            authEmployee=request.GET.get('id')
            if not authEmployee:
                return JsonResponse({'message':'module not found'})
            data = json.loads(request.body)
            authEmployee= AuthorizationToEmployee.objects.get(id=authEmployee)
            authEmployee.module_id = data.get('module_id')
            authEmployee.employee_id=data.get('employee_id')
            authEmployee.save()
            return JsonResponse({'success': 'authorization to to candidate is updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed'})    
    
    
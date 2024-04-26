import os
from django.core.files.storage import default_storage
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from users.serializers import UserSerializer
from .models import User
from .models import EmpID
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
def create_admin(request):
    try:
        admin_exists = User.objects.filter(role='admin').exists()
        
        if not admin_exists:
            User.objects.create(
                userName='admin',
                fullName='Admin',
                email='admin@gmail.com',
                role='admin',
                mobileNumber='0123456789',
                password='password'
            )
            return JsonResponse({'Success': 'Welcome Admin'})
        else:
            return JsonResponse({'error': 'Admin exists already'}, status=409)
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
    
    
# @csrf_exempt
# @require_POST
# def create_authmodule(request):
#         if request.method == 'POST':
#             try:

import os
from django.core.files.storage import default_storage
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
# from .decorators import role_required
from users.decorators import role_required
from project.decorators import jwt_auth_required
from recruit.models import AuthorizationToEmployee, AuthorizeToModule
from users.serializers import UserSerializer
from .models import EmpID,User,EmpModule
from django.db.models import Max
import json
from django.contrib.auth.hashers import check_password
from django.db import IntegrityError
from users.models import EmpID,Token
import jwt
from datetime import datetime, timedelta
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from django.core.cache import cache
import uuid
from django.http import HttpResponse
from django.core.files.storage import default_storage
import mimetypes

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        if 'firstName' in data and 'lastName' in data and 'role' in data and 'mobileNumber' in data:
            if data['role'] == 'employee':
                try:
                    mobile_number = int(data['mobileNumber'])
                    if mobile_number < 1000000000 or mobile_number >= 10000000000:
                        return JsonResponse({'error': "Mobile number must be a 10-digit integer"}, status=400)
                except ValueError:
                    return JsonResponse({'error': "Mobile number must be an integer"}, status=400)

                email = f"{data['firstName'].lower()}.{data['lastName'].lower()}@perfectkode.com"
                last_emp_id_record = EmpID.objects.aggregate(max_emp_id=Max('emp_id'))
                last_emp_id = last_emp_id_record['max_emp_id'] if last_emp_id_record['max_emp_id'] is not None else 999  # Default value if no records found
                emp_id = last_emp_id + 1
            else:
                return JsonResponse({'error': "Role must be 'employee' to proceed"}, status=400)

            password = f"{data['firstName'][0].upper()}{data['lastName']}@{emp_id}"

            try:
                emp_id_record = EmpID.objects.create(emp_id=emp_id)
                User.objects.create(
                    emp=emp_id_record,
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
                    'password': password,
                    'emp_id':emp_id
                }
                return JsonResponse(response_data, status=201)
            except IntegrityError as e:
                return JsonResponse({'error': 'Email or mobile number already exists'}, status=400)
        else:
            return JsonResponse({'error': 'First name, last name, role, and mobile number are required'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@csrf_exempt
@require_POST
def register_candidate(request):
    try:
        if 'file' in request.FILES:
            file = request.FILES['file']
            if file and allowed_file(file.name):
                timestamp = int(datetime.now().timestamp())
                filename = f'file_{timestamp}{os.path.splitext(file.name)[1]}'
                path = default_storage.save(f'public/files/{filename}', file)
                cv_url = default_storage.url(path)

                fullName = request.POST.get('fullName')
                degree = request.POST.get('degree')
                email = request.POST.get('email')
                mobileNumber = request.POST.get('mobileNumber')

                user = User.objects.create(
                    fullName=fullName,
                    degree=degree,
                    email=email,
                    mobileNumber=mobileNumber,
                    role='candidate',
                    cv_url=filename
                )
                complete_cv_url = request.build_absolute_uri(cv_url)
                
                return JsonResponse({'success': 'Candidate registered successfully', 'cv_url': complete_cv_url})
            else:
                return JsonResponse({'error': 'Invalid file format. Allowed formats: pdf, doc, docx, jpg, jpeg, png'}, status=400)
        else:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred during registration'}, status=500)
      

@require_GET
def get_candidate_profile(request):
    if request.method == 'GET':
        try:
            candidates = User.objects.filter(role='candidate')
            if not candidates:
                return JsonResponse({'message': 'Candidates not found'})
            
            candidate_data = []
            for candidate in candidates:
              filename = candidate.cv_url
              file_path = f'public/files/{filename}'
              candidate_data.append({
                    'fullName': candidate.fullName,
                    'degree': candidate.degree,
                    'email': candidate.email,
                    'mobileNumber': candidate.mobileNumber,
                    'active': candidate.active,
                    'cv_url': file_path
                })
            
            return JsonResponse({'candidates': candidate_data})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'})
                    
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
                        'exp': datetime.utcnow() + timedelta(hours=1)
                    }, 'kkfwnfnfnjfknerkbeg', algorithm='HS256')
                    Token.objects.filter(user_id=user.id).delete()
                    Token.objects.create(
                       token=token,
                       user_id=user.id
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
        user_id = request.user_id
        if Token.objects.filter(user_id=user_id).exists():
            Token.objects.filter(user_id=user_id).delete()
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
            return JsonResponse({'error': "Current password didn't match"}, status=400)       
        if current_password == new_password:
            return JsonResponse({'error': "Current password & new password couldn't be same"}, status=400)
        
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
        if not User.objects.filter(email=email).exists():
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
        cached_otp = cache.get(email)

        if not cached_otp or cached_otp != otp:
            return JsonResponse({'error': 'Invalid or expired OTP'}, status=400)

        user.password = make_password(new_password)
        user.save()
        cache.delete(user.email)
        return JsonResponse({'message': 'Password updated successfully'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
def upload_cv(request):
    if request.method == 'POST':
        try:
            candidate_id = request.GET.get('candidate_id')

            print("Candidate ID:", candidate_id)

            if 'file' in request.FILES:
                file = request.FILES['file']
                if file and allowed_file(file.name):
                    timestamp = int(datetime.now().timestamp())
                    filename = f'file_{timestamp}{os.path.splitext(file.name)[1]}'
                    path = default_storage.save(f'public/files/{filename}', file)
                    cv_url = default_storage.url(path)
                    user = User.objects.get(id=candidate_id)
                    user.cv_url=filename
                    user.save()
                    return JsonResponse({'success': 'File uploaded', 'file_url': cv_url})
                else:
                    return JsonResponse({'error': 'Invalid file format. Allowed formats: pdf, doc, docx, jpg, jpeg, png'}, status=400)
            else:
                return JsonResponse({'error': 'No file uploaded'}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred during uploading the file'}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@require_GET
def show_cv(request, filename):
    file_path = f'public/files/{filename}'
    file = default_storage.open(file_path, 'rb')
    mime_type, _ = mimetypes.guess_type(file_path)
    response = HttpResponse(file, content_type=mime_type)
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response
    
@csrf_exempt
@require_POST
@jwt_auth_required
@role_required('admin')
def create_empmodule(request):
        if request.method == 'POST':
            try:
                data=json.loads(request.body)
                moduleName=data.get('moduleName')
                moduleKey=data.get('moduleKey')   #this will be the alphanumeric filed
                empModule=EmpModule.objects.create(
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
#@role_required('admin')
@jwt_auth_required
def update_empModule(request):
    if request.method=='PUT':
        try:
            module_id=request.GET.get('id')
            if not module_id:
                return JsonResponse({'message':'module not found'})
            data=json.loads(request.body)
            empModule=EmpModule.objects.get(id=11)
            empModule.moduleName=data.get('moduleName')
            empModule.moduleKey=data.get('moduleKey')
            empModule.save()
            return JsonResponse({'success':'module upated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed'})
    
@require_GET
@role_required('admin')
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
@role_required('admin')          #this  role_required is not working so i need to fix this  
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
@role_required('admin')
def update_authorization_to_module(request):
    if request.method=='PUT':
        try:
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
@role_required('admin')
def authorize_to_employee(request):
    if request.method == 'POST':
        try:
            data=json.loads(request.body)
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
@role_required('admin')
def update_authorization_to_employee(request):
    if request.method == 'PUT':
        try:
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
    
    
def sms_api(request):
    try:
        key = request.GET.get('key')
        to = request.GET.get('to')
        from_number = request.GET.get('from')
        body = request.GET.get('body')
        template_id = request.GET.get('templateid')
        entity_id = request.GET.get('entityid')

        if key != 'JzSSxVmq':
            raise ValueError("Invalid API key")

        messageid = str(uuid.uuid4())
        response_data = {
            "status": 100,
            "description": "Message submitted with tracking id (UID)",
            "messageid": messageid
        }
        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)                 

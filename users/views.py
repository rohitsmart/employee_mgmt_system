import os
from django.core.files.storage import default_storage
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from users.decorators import role_required
from project.decorators import jwt_auth_required
from recruit.models import AuthorizationToEmployee, AuthorizeToModule,Scheduler
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


ALLOWED_EXTENSION = {'jpg', 'jpeg', 'png'}

def allowed_image(image):
    return '.' in image and image.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

@csrf_exempt
def create_employee(request):
    if request.method == 'POST':
        img = request.FILES.get('image')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        role = request.POST.get('role')
        mobileNumber = request.POST.get('mobileNumber')
        designation = request.POST.get('designation')

        if img and allowed_image(img.name):
            timestamp = int(datetime.now().timestamp())
            imagename = f'image_{timestamp}{os.path.splitext(img.name)[1]}'
            path = default_storage.save(f'public/images/{imagename}', img)
            image_url = default_storage.url(path)

            mobile_number = int(mobileNumber)
            if mobile_number < 1000000000 or mobile_number >= 10000000000:
                return JsonResponse({'error': "Mobile number must be a 10-digit integer"}, status=400)

            email = f"{firstName.lower()}.{lastName.lower()}@perfectkode.com"
            last_emp_id_record = EmpID.objects.aggregate(max_emp_id=Max('emp_id'))
            last_emp_id = last_emp_id_record['max_emp_id'] if last_emp_id_record['max_emp_id'] is not None else 999  # Default value if no records found
            emp_id = last_emp_id + 1

            password = f"{firstName[0].upper()}{lastName}@{emp_id}"

            try:
                emp_id_record = EmpID.objects.create(emp_id=emp_id, designation=designation)
                User.objects.create(
                    emp=emp_id_record,
                    firstName=firstName,
                    lastName=lastName,
                    email=email,
                    role=role,
                    mobileNumber=mobileNumber,
                    password=make_password(password),
                    active=False,
                    img_url=imagename
                )
                response_data = {
                    'message': 'User signed up successfully',
                    'email': email,
                    'password': password,
                    'emp_id': emp_id,
                    "image_url" : image_url
                }
                return JsonResponse(response_data, status=201)
            except IntegrityError as e:
                return JsonResponse({'error': 'Email or mobile number already exists'}, status=400)
        else:
            return JsonResponse({'error': 'FirstName, lastName, Role, mobileNumber and Designation are required'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



@require_GET
def show_image(request, imagename):
    file_path = f'public/images/{imagename}'
    file = default_storage.open(file_path, 'rb')
    mime_type, _ = mimetypes.guess_type(file_path)
    response = HttpResponse(file, content_type=mime_type)
    response['Content-Disposition'] = f'inline; imagename="{imagename}"'
    return response



@csrf_exempt
def update_image(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        img = request.FILES.get('image')
      
        if not allowed_image(img.name):
            return JsonResponse({'error': 'Invalid image format'}, status=400)

        timestamp = int(datetime.now().timestamp())
        imagename = f'image_{timestamp}{os.path.splitext(img.name)[1]}'
        path = default_storage.save(f'public/images/{imagename}', img)
        image_url = default_storage.url(path)

        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        file_path = f'public/images/{user.img_url}'
        if default_storage.exists(file_path):
            default_storage.delete(file_path)

        user.img_url = imagename
        user.save()

        return JsonResponse({'message': 'Image updated successfully', 'image_url': image_url})
    else:
        return JsonResponse({'error': 'POST method required'}, status=405)


ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@csrf_exempt
@require_POST
def register_candidate(request):
    try:
        data = json.loads(request.body)
        fullName = data.get('fullName')
        degree = data.get('degree')
        email = data.get('email')
        mobileNumber = data.get('mobileNumber')
        cv_url = data.get('cv_url')
        
        user = User.objects.create(
            fullName=fullName,
            degree=degree,
            email=email,
            mobileNumber=mobileNumber,
            role='candidate',
            cv_url=cv_url
        )
        return JsonResponse({'success': 'Candidate registered successfully'})
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
              file_path = f'{filename}'
              candidate_data.append({
                    'id' : candidate.id,
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
                        'role' : user.role,
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
            #candidate_id = request.GET.get('candidate_id')

            #print("Candidate ID:", candidate_id)

            if 'file' in request.FILES:
                file = request.FILES['file']
                if file and allowed_file(file.name):
                    timestamp = int(datetime.now().timestamp())
                    filename = f'file_{timestamp}{os.path.splitext(file.name)[1]}'
                    path = default_storage.save(f'public/files/{filename}', file)
                    cv_url = default_storage.url(path)
                    #user = User.objects.get(id=candidate_id)
                    #user.cv_url=filename
                    #user.save()
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
@role_required('admin')
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
            data = json.loads(request.body)
            emp_id = data.get('emp_id')
            candidate_id = data.get('candidate_id')
            round = data.get('round')
            
            isValidScheduler = Scheduler.objects.get(round=round, candidate_id=candidate_id)
            
            if isValidScheduler.status == 'pending':
                try:
                    alreadyAuthorized = AuthorizationToEmployee.objects.get(round=round, candidate_id=candidate_id, emp_id=emp_id)
                    return JsonResponse({'error': 'The candidate is already authorized to another employee'}, status=400)
                except AuthorizationToEmployee.DoesNotExist:
                    AuthorizationToEmployee.objects.create(emp_id=emp_id, candidate_id=candidate_id, round=round)
                    return JsonResponse({'success': 'Employee is authorized for the candidate'}, status=201)
            else:
                return JsonResponse({'error': 'Candidate does not have a pending interview'}, status=400)
        except Scheduler.DoesNotExist:
            return JsonResponse({'error': 'Scheduler not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


    
    
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


@csrf_exempt
#@role_required('admin')
def get_employees(request):
    try:
        employees = EmpID.objects.all()
        employees_details = []

        for employee in employees:
            try:
                user = User.objects.get(emp_id=employee.id)
                fullname = None
                if user.firstName is None and user.lastName is None:
                    fullname = user.fullName
                else:
                    fullname = f"{user.firstName} {user.lastName}"
                print(fullname)
                #imagename=user.img_url
                #file_path = f'public/images/{imagename}'
            
                employees_details.append({
                    "emp_id": employee.emp_id,
                    "designation": employee.designation,
                    "fullname": fullname,
                    "active": user.active,
                    "image_url" : f'/public/images/{user.img_url}'

                })
            except User.DoesNotExist:
                # Handle the case where the user does not exist
                continue

        return JsonResponse({"employees_details": employees_details})
    except EmpID.DoesNotExist:
        return JsonResponse({"employees_details": []})
    
@csrf_exempt
# @role_required('admin')
def upcoming_previous_candidates(request):
    if request.method == 'GET':
        try:
            existAuthorization = AuthorizationToEmployee.objects.filter(emp_id=32)
            upcoming_candidates = []
            previous_candidates = []
            
            for authorization in existAuthorization:
                candidate_data = User.objects.get(id=authorization.candidate_id)
                isAttempted = Scheduler.objects.filter(candidate_id=authorization.candidate_id, round=authorization.round, status='pending').exists()
                
                candidate_info = {
                    'candidate_id': candidate_data.id,
                    'fullName': candidate_data.fullName,
                    'email': candidate_data.email,
                    "mobileNumber" : candidate_data.mobileNumber,
                    'cv_url': candidate_data.cv_url
                }
                
                if isAttempted:
                    upcoming_candidates.append(candidate_info)
                else:
                    previous_candidates.append(candidate_info)
                    
            return JsonResponse({'upcoming_candidates': upcoming_candidates, 'previous_candidates': previous_candidates}, status=200)
        
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except AuthorizationToEmployee.DoesNotExist:
            return JsonResponse({'error': 'AuthorizationToEmployee not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)






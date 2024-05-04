import random
import string
import json
from django.db.models import Max

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from project.decorators import jwt_auth_required
from adminauth.models import UserCredential
from users.models import User,EmpID
from django.contrib.auth.hashers import make_password



@require_POST
@csrf_exempt
@jwt_auth_required
def create_user_credential(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        if not User.objects.filter(id=request.user_id, role='admin').exists():
            return JsonResponse({'error': 'Only accessible by Admin'}, status=400)
        
        user = User.objects.filter(email=email).first()
        
        if user:
            if user.role == 'candidate':
                first_name = user.firstName
                last_name = user.lastName
                username = generate_username(first_name, last_name)
            elif user.role == 'employee':
                full_name = user.fullName
                empIDdata=user.emp
                username = generate_employee_username(full_name, empIDdata.emp_id)
            else:
                return JsonResponse({'error': 'Invalid user role'}, status=400)
            
            password = generate_password()

            if UserCredential.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            elif UserCredential.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)
            
            UserCredential.objects.create(
                username=username,
                password=password,
                email=email
            )

            return JsonResponse({
                'username': username,
                'password': password,
                'email': email
            })
        else:
            return JsonResponse({'error': 'User not found'}, status=404)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def generate_username(first_name, last_name):
    first_chars = first_name[:1].upper() + first_name[1:2].lower()
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    last_chars = last_name[:1].upper()
    return first_chars + random_chars + last_chars

def generate_employee_username(full_name, emp_id):
    first_chars = full_name[:1].upper() + '@'
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=2))
    last_chars = str(emp_id)
    return first_chars + random_chars + last_chars

def generate_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


@require_POST
@csrf_exempt
@jwt_auth_required
def change_role(request):
    try:
        if not User.objects.filter(id=request.user_id, role='admin').exists():
            return JsonResponse({'error': 'Only accessible by Admin'}, status=400)
        
        user_id = request.GET.get('user_id')
        user = User.objects.get(id=user_id)
        
        if not user:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        if user.role == 'employee':
            return JsonResponse({'message': 'User is already an employee'}, status=400)
        
        last_emp_id_record = EmpID.objects.aggregate(max_emp_id=Max('emp_id'))
        last_emp_id = last_emp_id_record['max_emp_id'] if last_emp_id_record['max_emp_id'] is not None else 999  # Default value if no records found
        emp_id = last_emp_id + 1
        emp_id_record = EmpID.objects.create(emp_id=emp_id)

        user.role = 'employee'
        user.emp = emp_id_record
        user.save()

        return JsonResponse({'message': 'User role changed to employee'}, status=200)
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def update_user(request):
    if request.method == 'PUT':
        try:
            user_id = request.GET.get('user_id')
            user = User.objects.get(id=user_id)
            data = json.loads(request.body)
            if not User.objects.filter(id=request.user_id, role='admin').exists():
             return JsonResponse({'error': 'Only accessible by Admin'}, status=400)

            user.firstName = data.get('firstName', user.firstName)
            user.lastName = data.get('lastName', user.lastName)
            user.userName = data.get('userName', user.userName)
            user.address = data.get('address', user.address)
            user.degree = data.get('degree', user.degree)
            user.email = data.get('email', user.email)
            user.role = data.get('role', user.role)
            user.mobileNumber = data.get('mobileNumber', user.mobileNumber)
            user.save()

            return JsonResponse({'message': 'User updated successfully'}, status=200)
        
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def deactivate_user(request):
    if request.method == 'PUT':
        try:
            if not User.objects.filter(id=request.user_id, role='admin').exists():
             return JsonResponse({'error': 'Only accessible by Admin'}, status=400)
            user_id = request.GET.get('user_id')
            user = User.objects.get(id=user_id)
            user.active =True
            user.save()
            return JsonResponse({'message': 'User deactivated successfully'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def delete_user(request):
    if request.method == 'DELETE':
        try:
            if not User.objects.filter(id=request.user_id, role='admin').exists():
             return JsonResponse({'error': 'Only accessible by Admin'}, status=400)
            user_id = request.GET.get('user_id')
            User.objects.get(id=user_id).delete()
            return JsonResponse({'message': 'User deleted successfully'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)    
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def reset_user_passwrod(request):
    if request.method == 'PUT':
        try:
            if not User.objects.filter(id=request.user_id, role='admin').exists():
             return JsonResponse({'error': 'Only accessible by Admin'}, status=400)
            user_id = request.GET.get('user_id')
            user = User.objects.get(id=user_id)
            new_password = 'password'
            user.password = make_password(new_password)
            user.save()
            return JsonResponse({'message': 'Password reset successfully', 'user_id': user_id, 'password': new_password}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

@csrf_exempt
def fetch_user(request):
    try:
        if not User.objects.filter(id=request.user_id, role='admin').exists():
            return JsonResponse({'error': 'Only accessible by Admin'}, status=400)
        role = request.GET.get('role')
        
        if role == 'candidate':
            users = User.objects.filter(role='candidate').exclude(role='admin').values()
        elif role == 'employee':
            users = User.objects.filter(role='employee').exclude(role='admin').values()
        elif role == 'all':
            users = User.objects.exclude(role='admin').values()
        else:
            return JsonResponse({'error': 'Invalid role'}, status=400)

        return JsonResponse({'users': list(users)}, status=200)
    
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
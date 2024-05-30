import random
import string
import json
from django.db.models import Max

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from project.decorators import jwt_auth_required
from users.models import User,EmpID
from django.contrib.auth.hashers import make_password


@require_POST
@csrf_exempt
@jwt_auth_required
def change_role(request):
    try:
        if not User.objects.filter(id=request.user_id, role='admin').exists():
            return JsonResponse({'error': 'Only accessible by Admin'}, status=400)
        
        data = json.loads(request.body)
        user_id = data.get('user_id')
        designation = data.get('designation')

        user = User.objects.filter(id=user_id).first()
        
        if not user:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        if user.role == 'employee':
            return JsonResponse({'message': 'User is already an employee'}, status=400)
        
        last_emp_id_record = EmpID.objects.aggregate(max_emp_id=Max('emp_id'))
        last_emp_id = last_emp_id_record['max_emp_id'] if last_emp_id_record['max_emp_id'] is not None else 999  # Default value if no records found
        emp_id = last_emp_id + 1
        
        emp_id_record = EmpID.objects.create(emp_id=emp_id, designation=designation)

        email = generate_email(user.fullName)
        password = generate_password(user.fullName)
        user.role = 'employee'
        user.email = email
        user.password=password
        user.emp = emp_id_record
        user.save()

        return JsonResponse({'message': 'User role changed to employee', 'email': email, 'password': password}, status=200)
    
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def generate_email(fullName):
    first_part = fullName[:3].lower()
    random_chars = ''.join(random.choices(string.ascii_lowercase, k=3))
    random_number = random.randint(100, 999)
    email = f"{first_part}{random_chars}{random_number}@perfectkode.com"
    return email


def generate_password(fullName):
    first_part = fullName[:3]
    random_number = random.randint(10000, 99999) 
    password = f"{first_part}@{random_number}"
    return password



@csrf_exempt
@jwt_auth_required
def update_user(request):
    if request.method == 'PUT':
        try:
            if not User.objects.filter(id=request.user_id, role='admin').exists():
              return JsonResponse({'error': 'Only accessible by Admin'}, status=400)
            
            user_id = request.GET.get('user_id')
            user = User.objects.get(id=user_id)
            data = json.loads(request.body)

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
@jwt_auth_required
def deactivate_employee(request):
    if request.method == 'PUT':
        try:
            if not User.objects.filter(id=request.user_id, role='admin').exists():
              return JsonResponse({'error': 'Only accessible by Admin'}, status=400)
            
            emp_id = request.GET.get('emp_id')
            id = EmpID.objects.filter(emp_id=emp_id).values_list('id', flat=True).first()
            userwithEmpId = User.objects.filter(emp=id)
            for user in userwithEmpId:     
                if user.active == False:
                   user.active = True 
                   user.save()
                   return JsonResponse({'message': 'Employee deactivated successfully'}, status=200)
                else:
                    return JsonResponse({'error': 'Employee already deactivated'}, status=400)
        except EmpID.DoesNotExist:
            return JsonResponse({'error': 'Employee ID not found'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@jwt_auth_required
def delete_employee(request):
    if request.method == 'DELETE':
        try:
            if not User.objects.filter(id=request.user_id, role='admin').exists():
               return JsonResponse({'error': 'Only accessible by Admin'}, status=400)
            emp_id = request.GET.get('emp_id')
            emp = EmpID.objects.filter(emp_id=emp_id).first() 
            if emp:
                emp.delete() 
                return JsonResponse({'message': 'Employee deleted successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Employee not found'}, status=404) 
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405) 



@csrf_exempt
@jwt_auth_required
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
@jwt_auth_required
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
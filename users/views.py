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
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = User.objects.filter(email=email).first()
            if user:
                if check_password(password, user.password):
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
            return JsonResponse({'error': 'Email and password are required'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)




# Faltu code



  # Adjust the import as per your project structure

# def login(request):
#     if request.method == 'POST':
#         data = request.POST  # Assuming email and password are sent in form data
#         email = data.get('email')
#         password = data.get('password')
#         if email and password:
#             user = User.objects.filter(email=email).first()
#             if user and check_password(password, user.password):
#                 # Generate JWT token
#                 token = jwt.encode({
#                     'user_id': user.id,
#                     'exp': datetime.utcnow() + timedelta(hours=1)  # Token expiry time
#                 }, settings.SECRET_KEY, algorithm='HS256')

#                 return JsonResponse({
#                     'user_id': user.id,
#                     'access_token': token.decode('utf-8'),
#                 }, status=200)
#             else:
#                 return JsonResponse({'error': 'Invalid credentials'}, status=400)
#         else:
#             return JsonResponse({'error': 'Email and password are required'}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)

    
    # @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
# def user_logout(request):
#     try:
#         # Log out the user
#         logout(request)

#         # Delete refresh token
#         refresh_token = request.COOKIES.get('refresh_token')
#         if refresh_token:
#             token = RefreshToken(refresh_token)
#             token.blacklist()

#         # Optionally, you can perform additional actions like updating user status
        
#         return Response({'success': 'Successfully logged out'}, status=200)
#     except Exception as e:
#         return Response({'error': 'An error occurred during logout'}, status=500)

# @csrf_exempt
# # @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# # @authentication_classes([JWTAuthentication])
# def user_logout(request):
#         if request.method == 'POST':
#             # Access the refresh token from request headers or cookies
#             try:
#                 refresh_token = request.data["refresh"]
#                 #refresh_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
#                 token = RefreshToken(refresh_token)
#                 token.blacklist()
#                 return JsonResponse({'message':'User logout successfully'})
#             except Exception as err:
#                 return JsonResponse({'message':str(err)})
#         else:
#             return JsonResponse({'error': 'Invalid request method.'})

# @csrf_exempt
# def get_empID(request):
#     if request.method == "GET":
#         last_employee_id_object = EmpID.objects.last()
#         if last_employee_id_object:
#             last_employee_id = last_employee_id_object.employeeID
#         else:
#             last_employee_id = 1000

#         new_employee_id = last_employee_id + 1
#         employeeID = EmpID.objects.create(employeeID=new_employee_id)
#         employeeID.save()
#         return JsonResponse({'employeeID': new_employee_id})
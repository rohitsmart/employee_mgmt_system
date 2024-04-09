
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import User
from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
import json
import bcrypt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import string
from users.models import EmployeeID 
from django.contrib.auth import get_user_model

@csrf_exempt
def user_signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            employeeID=data.get('employeeID')
            email = data.get('email')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            phone_number = data.get('phone_number')
            address=data.get('address')
            role =data.get('role')

            password = f"{first_name}@{employeeID}"
            # print('employee id --->',role)
            
            # if not all([email, password, first_name, last_name, phone_number, address]):
            #      return JsonResponse({'error': 'All required fields must be provided'}, status=400)
             
                
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            # Create customer
            print('1')
            user = User.objects.create(
                employeeID=employeeID,
                email=email,
                password=hashed_password.decode('utf-8'),
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                address=address,
                role=role,
            )
            print('user object',user)
            user.save()

            return JsonResponse({'message': 'User created successfully'})
        except Exception as e:
            return JsonResponse({'error from run time': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    

User = get_user_model()
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not all([email, password]):
                return JsonResponse({'error': 'Email and password are required.'}, status=400)

            user = User.objects.filter(email=email).first()

            if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                response = JsonResponse({
                    'success': 'User logged in successfully',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }, status=200)

                # Set refresh token in cookie
                response.set_cookie('refresh_token', refresh_token)
                return response
            else:
                return JsonResponse({'error': 'Authentication failed: username or password is wrong.'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


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

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def user_logout(request):
        if request.method == 'POST':
            # Access the refresh token from request headers or cookies
            try:
                refresh_token = request.data["refresh"]
                #refresh_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'message':'User logout successfully'})
            except Exception as err:
                return Response({'message':str(err)})
        else:
            return Response({'error': 'Invalid request method.'})
        
# last_employee_id = 1000  
# @csrf_exempt
# def generate_employee_id(request):
#     global last_employee_id
#     last_employee_id += 1
#     return last_employee_id

# def get_empID(request):
#     global last_employee_id
#     if request.method == "GET":
#         employee_id = generate_employee_id(request)
#         employeeID=EmployeeID.objects.create(
#             employeeID=employee_id
#         )
#         employeeID.save()
#         return JsonResponse({'employeeID': employee_id})

@csrf_exempt
def get_empID(request):
    if request.method == "GET":
        last_employee_id_object = EmployeeID.objects.last()
        if last_employee_id_object:
            last_employee_id = last_employee_id_object.employeeID
        else:
            last_employee_id = 1000

        new_employee_id = last_employee_id + 1
        employeeID = EmployeeID.objects.create(employeeID=new_employee_id)
        employeeID.save()
        return JsonResponse({'employeeID': new_employee_id})

# @csrf_exempt
# def get_empID(request):
#     if request.method == "GET":
#         return generate_employee_id(request)
        




        
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import User
from knox.models import AuthToken
# from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import json
import bcrypt
from rest_framework_simplejwt.tokens import RefreshToken
@csrf_exempt
def user_signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            phone_number = data.get('phone_number')
            address=data.get('address')
            role =data.get('role')

            if not all([email, password, first_name, last_name, phone_number, address]):
                 return JsonResponse({'error': 'All required fields must be provided'}, status=400)
                
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            # Create customer
            user = User.objects.create(
                email=email,
                password=hashed_password.decode('utf-8'),
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                address=address,
                role=role,
            )
            user.save()

            return JsonResponse({'message': 'User and customer created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if not all([email,password]):
            return JsonResponse({'error': 'Email and password are required.'}, status=400)

        user = User.objects.filter(email=email).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            access_token_expiry = timezone.now() + timedelta(minutes=15)
            refresh_token_expiry = timezone.now() + timedelta(days=1)
            
            response = JsonResponse({
                'success': 'User logged in successfully',
                'access_token': access_token,
                'expires_in':access_token_expiry
                # 'refresh_token': refresh_token
            }, status=200)
            
            response.set_cookie('refresh_token', refresh_token, expires=refresh_token_expiry)
            return response
        else:
            return JsonResponse({'error': 'Authentication failed: username or password is wrong.'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

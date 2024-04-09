
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
            
            response = JsonResponse({
                'success': 'User logged in successfully',
                'access_token': access_token,
                # 'refresh_token': refresh_token
            }, status=200)
            
            response.set_cookie('refresh_token', refresh_token)
            return response
        else:
            return JsonResponse({'error': 'Authentication failed: username or password is wrong.'}, status=401)
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
        """
        Log out all user.
        Args:
            request (HttpRequest): The client's request to the server.
        Returns:
            HttpResponseRedirect: Redirects the user to the Login page.
        """
        if request.method == 'POST':
            # Access the refresh token from request headers or cookies
            try:
                refresh_token = request.data["refresh"]
                #refresh_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'message':'User logout successfully'},status=status.HTTP_205_RESET_CONTENT)
            except Exception as err:
                return Response({'message':str(err)},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    
    
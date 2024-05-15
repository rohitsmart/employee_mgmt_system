from functools import wraps
from django.http import JsonResponse
from users.models import User
import jwt

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            try:
                #id=request.user_id
                isAdmin = User.objects.filter(role=role).exists()
                if not isAdmin:
                    return JsonResponse({'error': 'You do not have permission to access this resource.'}, status=403)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator



def jwt_auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            bearer, token = request.headers['Authorization'].split()
            if bearer != 'Bearer':
                return JsonResponse({'error': 'Invalid Authorization Header'}, status=401)

            decoded_token = jwt.decode(token, 'kkfwnfnfnjfknerkbeg', algorithms=['HS256'])
            request.user_id = decoded_token.get('user_id')
            return view_func(request, *args, **kwargs)
        except (KeyError, ValueError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return JsonResponse({'error': 'Invalid Token'}, status=401)
    return _wrapped_view
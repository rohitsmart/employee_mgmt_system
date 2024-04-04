from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
from .models import Module


def create_module(request):
    if request.method == 'POST':
        try:
            module_name = request.POST.get('module_name')
            project_id = request.POST.get('project_id')  
            user_id = request.POST.get('user_id')  
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            description = request.POST.get('description')
            assigned_hours = request.POST.get('assigned_hours')
            actual_hours = request.POST.get('actual_hours')

            # creating the new model object here
            module = Module.objects.create(          
                module_name=module_name,
                project_id=project_id,
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
                description=description,
                assigned_hours=assigned_hours,
                actual_hours=actual_hours
            )
            
            return JsonResponse({'message': 'Module created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})


def delete_module(request,id):
    if request.method == 'DELETE':
        try:
         module = Module.objects.get(id=id)
         module.delete()
         return JsonResponse({'message': 'Module deleted successfully'})
        except Module.DoesNotExist:
         return JsonResponse({'error': 'Module not found'})
    else:
       return JsonResponse({'error':'only DELETE method are allowed'}) 

def update_module(request, id):
    if request.method == 'POST':
        try:
            module = Module.objects.get(id=id)
            module.module_name = request.POST.get('module_name')
            module.start_date = request.POST.get('start_date')
            module.end_date = request.POST.get('end_date')
            module.description = request.POST.get('description')
            module.assigned_hours = request.POST.get('assigned_hours')
            module.actual_hours = request.POST.get('actual_hours')
            module.save()
            return JsonResponse({'message': 'Module updated successfully'})
        except Module.DoesNotExist:
            return JsonResponse({'error': 'Module not found'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed for updating module'})

def get_module(request, id):
    if request.method == 'GET':
        try:
            module = Module.objects.get(id=id)
            return JsonResponse({'module_name': module.module_name, 
                             'start_date':module.start_date,
                             'end_date':module.end_date,
                             'description':module.description,
                             'assigned_hours':module.assigned_hours,
                             'sctual_hours':module.actual_hours
                             })
        except Module.DoesNotExist:
            return JsonResponse({'error': 'Module not found'})
    else:
        return JsonResponse({'error':'only GET method is allowed for fetching the profile'})
    










# Create your views here.

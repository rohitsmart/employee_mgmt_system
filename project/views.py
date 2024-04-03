from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Attendance, Device

#user module 
def create_user(request):
    # Logic for create the user
    return HttpResponse("create user")

def get_user(request, id):
    # Logic for fetching the user profole
    return HttpResponse("get user")

def update_user(request, id):
    #logir for uodating the user
    return HttpResponse("update user")

def delete_user(request, id):
    #logic to delete teh user
    return HttpResponse("delete user")

#attendance module

def create_attendance(request):
    #logic for the creating the attendance
    return HttpResponse("create attendance")

def get_attendance(request, id):
    #logic for fetching the attendance
    return HttpResponse('fetch attendance')

def update_attendance(request, id):
    #logic for fetching the attendance
    return HttpResponse('update attendance')

def delete_attendance(request, id):
    #logic for fetching the attendance
    return HttpResponse('delete attendance')

#device module

def add_device(request):
    #logic for adding the device
    return HttpResponse("adding devices")

def view_device(request):
    #logic to view the device
    return HttpResponse("view device")

def update_device(request):
    #logic to update device
    return HttpResponse("update device")

def delete_device(request):
    #logic to delete the device
    return HttpResponse("delete device")





# Create your views here.

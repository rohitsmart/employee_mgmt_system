# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('user/', include('users.urls')),
# ]


from django.contrib import admin
from django.urls import path
from users.views import signup,login,update_password,forget_password,update_password_with_otp,logout
# , logout,get_empID
from project.views import create_module,delete_module, update_module, get_module,create_project,get_project
from project.views import update_project,delete_project
from task.views import create_task,update_task,delete_task,get_task
from feedback.views import create_feedback, update_feedback,post_feedback
from assign.views import assign_task,unassign_task,update_assignTask,get_assignedTask
from device.views import add_device, remove_device, get_device,update_device
from attendance.views import mark_attendance, get_attendance
from leave.views import apply_leave, update_leave, get_leave, delete_leave
from recruit.views import (
    create_stream,
    update_stream,
    get_questions,
    answer_question,
    save_result,
    delete_job,
    fetch_result,
    create_job,
    fetch_job,
    edit_job,
    fetch_job_list,
    apply_for_job,
    withdraw_job,
    fetch_notifications_by_user,
    mark_notification_as_read,
    filter_profile,
    accept_reject,
    exam_result
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/signup', signup, name='signup'),
    path('api/user/login', login, name='login'),
    path('api/user/logout', logout, name='logout'),
    # path('api/user/logout', logout, name='logout'),
    path('api/user/update_password', update_password, name='update_password'),
    path('api/user/forget_password', forget_password, name='forget_password'),
    path('api/user/update_password_with_otp', update_password_with_otp, name='update_password_with_otp'),
    path('api/project/createModule',create_module, name='create_module'),
    path('api/project/deleteModule', delete_module, name='delete_module'),
    path('api/project/updateModule', update_module, name='update_module'),
    path('api/project/getModule', get_module ,name='get_module'),
    # path('api/user/getEmpId', get_empID, name='get_empID'),
    path('api/project/createProject',create_project, name='create_project'),
    path('api/project/getProjectById', get_project, name='get_project'),
    path('api/project/updateProject', update_project, name='update_project'),
    path('api/project/deleteProject', delete_project, name='delete_project'),
    path('api/task/createTaskByModuleId',create_task, name='create_task'),
    path('api/task/updateTask', update_task, name='update_task'),
    path('api/task/getTask', get_task, name='get_task'),
    path('api/task/deleteTask', delete_task, name='delete_task'),
    path('api/feedback/post_feedback',post_feedback, name='post_feedback'),
    path('api/feedback/createFeedback',create_feedback, name='create_task'),
    path('api/feedback/updateFeedback',update_feedback, name='update_feedback'),
    path('api/assign/assignTask',assign_task, name='assign_task'),
    path('api/assign/unassignTask',unassign_task, name='unassign_task'),
    path('api/device/addDevice',add_device, name='add_device'),
    path('api/device/removeDevice',remove_device, name='remove_device'),
    path('api/device/getDevice',get_device, name='get_device'),
    path('api/device/updateDevice',update_device, name='update_device'),
    path('api/attendance/markAttendance',mark_attendance, name='mark_attendance'),
    path('api/attendance/getAttendanceRecordByID',get_attendance, name='get_attendance'), 
    path('api/assign/updateAssignedTask',update_assignTask, name='update_assignTask'),
    path('api/assign/getAssignedTask',get_assignedTask, name='get_assigned'),
    path('api/leave/applyLeave',apply_leave, name='apply_leave'),  
    path('api/leave/update_leave',update_leave, name='update_leave'),
    path('api/leave/get_leaveByUserID',get_leave, name='get_leave'), 
    path('api/leave/delete_leave',delete_leave, name='delete_leave'), 
    path('api/recruit/create_stream',create_stream,name='create_stream'), 
    path('api/recruit/update_stream',update_stream,name='update_stream'),  
    path('api/recruit/getQuestions',get_questions,name='get_questions'),    
    path('api/recruit/answerQuestion',answer_question,name='answer_question'),
    path('api/recruit/saveResult',save_result,name='save_result'),
    path('api/recruit/exam_result',exam_result,name='exam_result'),
    path('api/recruit/fetchResult',fetch_result,name='fetch_result'),
    path('api/recruit/create_job', create_job, name='create_job'),
    path('api/recruit/fetch-job', fetch_job, name='fetch_job'),
    path('api/recruit/edit-job', edit_job, name='edit_job'),
    path('api/recruit/delete-job', delete_job, name='delete_job'),
    path('api/candidate/fetch_job_list', fetch_job_list, name='fetch_job_list'),
    path('api/candidate/apply_for_job', apply_for_job, name='apply_for_job'),
    path('api/candidate/withdraw_job', withdraw_job, name='withdraw_job'),
    path('api/candidate/fetch_notifications_by_user', fetch_notifications_by_user, name='fetch_notifications_by_user'),
    path('api/candidate/mark_notification_as_read', mark_notification_as_read, name='mark_notification_as_read'),
    path('api/employee/filter/profile', filter_profile, name='filterProfile'),
    path('api/employee/candidate/accept_reject', accept_reject, name='accept_reject'),


]



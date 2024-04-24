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
from users.views import signup
from users.views import login,register_candidate
# , logout,get_empID
from project.views import create_module,delete_module, update_module, get_module,create_project,get_project
from project.views import update_project,delete_project
from task.views import create_task,update_task,delete_task,get_task
from feedback.views import create_feedback, update_feedback
from assign.views import assign_task,unassign_task,update_assignTask,get_assignedTask
from device.views import add_device, remove_device, get_device,update_device
from attendance.views import mark_attendance, get_attendance
from leave.views import apply_leave, update_leave, get_leave, delete_leave

from recruit.views import create_stream, update_stream, save_answer,submit_exam, fetch_result,candidate_scheduler
from recruit.views import update_candidate_scheduler,fetch_my_scheduler,track,get_questions, fetch_stream_with_questions,fetch_stream
#  next_question,previous_question,
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/signup', signup, name='signup'),
    path('api/user/login', login, name='login'),
    # path('api/user/logout', logout, name='logout'),
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
    # path('api/recruit/next-question',next_question,name='next_question'),  
    # path('api/recruit/previous-question',previous_question,name='previous_question'),  
    path('api/recruit/saveAnswer',save_answer,name='save_answer'),
    path('api/recruit/submitExam',submit_exam,name='submit_exam'),
    path('api/recruit/fetchResult',fetch_result,name='fetch_result'),
    path('api/recruit/scheduler/candidate-scheduler',candidate_scheduler,name='candidate_scheduler'),
    path('api/recruit/scheduler/update-candidate-schedulerBycandidateID',update_candidate_scheduler,name='update_candidate_scheduler'),
    path('api/recruit/scheduler/fetch-my-scheduler',fetch_my_scheduler,name='fetch_my_scheduler'),
    path('api/recruit/candidate/track',track,name='track'),
    path('api/recruit/candidate/questions/get-questions',get_questions,name='get_questions'),
    path('api/users/candidate/register-candidate',register_candidate,name='register_candidate'),
    path('api/recruit/get-stream-with-questions',fetch_stream_with_questions,name='fetch_stream_with_questions'),
    path('api/recruit/get-stream',fetch_stream,name='fetch_stream'),
]


#here i am pushig the code for the testing purpose




from django.contrib import admin
from django.urls import path
from users.views import authorization_to_module, authorize_to_employee, create_empmodule, signup, update_authorization_to_employee, update_authorization_to_module
from users.views import signup,register_candidate,login,upload_cv
from users.views import signup,login,update_password,forget_password,update_password_with_otp,logout,sms_api
from project.views import create_module,delete_module, update_module, get_module,create_project,get_project
from project.views import update_project,delete_project
from task.views import create_task,update_task,delete_task,get_task
from feedback.views import create_feedback, update_feedback,post_feedback
from assign.views import assign_task,unassign_task,update_assignTask,get_assignedTask
from device.views import add_device, remove_device, get_device,update_device
from attendance.views import mark_attendance, get_attendance
from leave.views import apply_leave, update_leave, get_leave, delete_leave
from recruit.views import (create_stream, update_stream, delete_job, fetch_result,
                           create_job, fetch_job, edit_job, apply_for_job,
                           withdraw_job, fetch_notifications_by_user,
                           mark_notification_as_read, filter_profile, accept_reject,
                           exam_result, get_questions, submit_exam, save_answer,
                           update_candidate_scheduler, fetch_my_scheduler, track,
                           fetch_stream_with_questions, fetch_stream,
                           candidate_scheduler, save_answer)

from adminauth.views import create_user_credential,change_role,update_user,deactivate_user,delete_user,fetch_user,reset_user_passwrod

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/admin/user/generate-credentials', create_user_credential, name='create_user'),
    path('api/admin/user/change_role', change_role, name='change_role'),
    path('api/admin/user/update_user', update_user, name='update_user'),
    path('api/admin/user/deactivate_user', deactivate_user, name='deactivate_user'),
    path('api/admin/user/delete_user', delete_user, name='delete_user'),
    path('api/admin/user/fetch_user', fetch_user, name='fetch_user'),
    path('api/admin/user/reset_user_passwrod', reset_user_passwrod, name='reset_user_passwrod'),
    path('api/user/signup', signup, name='signup'),
    path('api/user/login', login, name='login'),
    path('api/user/logout', logout, name='logout'),
    path('api/user/update_password', update_password, name='update_password'),
    path('api/user/forget_password', forget_password, name='forget_password'),
    path('api/user/update_password_with_otp', update_password_with_otp, name='update_password_with_otp'),
    path('api/project/createModule',create_module, name='create_module'),
    path('api/project/deleteModule', delete_module, name='delete_module'),
    path('api/project/updateModule', update_module, name='update_module'),
    path('api/project/getModule', get_module ,name='get_module'),
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

    #path('api/recruit/answerQuestion',answer_question,name='answer_question'),
    # path('api/recruit/saveResult',save_result,name='save_result'),
    path('api/recruit/exam_result',exam_result,name='exam_result'),
 
    path('api/recruit/saveAnswer',save_answer,name='save_answer'),
    path('api/recruit/submitExam',submit_exam,name='submit_exam'),
    path('api/recruit/fetchResult',fetch_result,name='fetch_result'),
    path('api/recruit/create_job', create_job, name='create_job'),
    path('api/recruit/fetch-job', fetch_job, name='fetch_job'),
    path('api/recruit/edit-job', edit_job, name='edit_job'),
    path('api/recruit/delete-job', delete_job, name='delete_job'),
    # path('api/candidate/fetch_job_list', fetch_job_list, name='fetch_job_list'),
    path('api/candidate/register_candidate',register_candidate,name='register_candidate'),
    path('api/candidate/apply_for_job', apply_for_job, name='apply_for_job'),
    path('api/candidate/withdraw_job', withdraw_job, name='withdraw_job'),
    path('api/candidate/fetch_notifications_by_user', fetch_notifications_by_user, name='fetch_notifications_by_user'),
    path('api/candidate/mark_notification_as_read', mark_notification_as_read, name='mark_notification_as_read'),
    path('api/employee/filter/profile', filter_profile, name='filterProfile'),
    path('api/employee/candidate/accept_reject', accept_reject, name='accept_reject'),
    path('api/recruit/candidate/update-candidate-scheduler', update_candidate_scheduler, name='update_candidate_scheduler'),
    path('api/recruit/candidate/fetch-my-scheduler', fetch_my_scheduler, name='fetch_my_scheduler'),
    path('api/recruit/candidate/track',track, name='track'),
    path('api/recruit/candidate/get-questions',get_questions, name='get_questions'),
    path('api/recruit/candidate/fetch-stream-with-questions',fetch_stream_with_questions, name='fetch_stream_with_questions'),
    path('api/recruit/candidate/fetch-stream',fetch_stream, name='fetch_stream'),
    path('api/recruit/candidate/candidate-scheduler',candidate_scheduler, name='candidate_scheduler'),
    path('api/recruit/candidate/save-answer',save_answer, name='save_answer'),
    path('api/recruit/candidate/submit-exam',submit_exam, name='submit_exam'),
    path('api/users/upload-cv',upload_cv, name='upload_cv'),
    path('api/users/create-empmodule',create_empmodule,name='create_empmodule'),
    path('api/admin/users/authorization-to-module',authorization_to_module,name='authorization_to_module'),
    path('api/admin/users/update-authorization-to-module',update_authorization_to_module,name='update_authorization_to_module'),
    path('api/admin/users/authorize-authorization-to-employee',authorize_to_employee,name='authorization_to_employee'),
    path('api/admin/users/update-authorization-to-employee',update_authorization_to_employee,name='update_authorization_to_employee'),
    path('api/users/upload-image',upload_cv, name='upload_cv'),
    path('api/sms', sms_api, name='sms_api'),
]
    





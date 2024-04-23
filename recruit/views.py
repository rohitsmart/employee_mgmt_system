from datetime import date, datetime, timezone
import os
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from project.decorators import jwt_auth_required
from recruit.models import Stream
import random
from recruit.models import Questions
from recruit.models import Exam
from recruit.models import Result,Job,ApplyJob,Notification
from users.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication



@csrf_exempt
@require_POST
# @jwt_auth_required
def create_stream(request):
    if request.method == 'POST':
        try:
            # user = request.user_id
            # if not user:
            #     return JsonResponse({'message': 'User is unauthenticated'})
            data = json.loads(request.body)
            streamName = data.get('streamName')

            stream = Stream.objects.create(          
                streamName=streamName,
            )
            stream.save()
            
            return JsonResponse({'message': 'Stream created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})

@csrf_exempt
@require_http_methods(['PUT'])
def update_stream(request):
    if request.method == 'PUT':
        try:
            stream_id=request.GET.get('id')
            if not stream_id:
                return JsonResponse({'message':'stream id not found'})
            data = json.loads(request.body)
            stream=Stream.objects.get(id=stream_id)
            stream.streamName = data.get('streamName')
            stream.save()
            return JsonResponse({'message':'stream updated successfully'})
        except Stream.DoesNotExist:
            return JsonResponse({'error': 'stream not found'})
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed for updating the stream'})


@require_GET
def get_questions(request):
    if request.method=='GET':
        try:
            json_file_path = os.path.join(settings.BASE_DIR, 'questions.json')
            with open(json_file_path, 'r') as file:
              questions_data = json.load(file)
              stream_id = request.GET.get('id') 
            total_questions = [question for question in questions_data if question.get('stream_id') == int(stream_id)]
            if len(total_questions) < 5:
              return JsonResponse({"message": "questions are less than requirement"})
    
            questions = random.sample(total_questions, 5)
            all_questions = []
            for question in questions:
                all_question = {
                    "id": question["id"],
                   "question": question["question"],
                   "option1": question["option1"],
                   "option2": question["option2"],
                   "option3": question["option3"],
                   "option4": question["option4"],
                   "type": question["type"],
                   "level": question["level"],
                   "stream_id": question["stream_id"]
                   }
                all_questions.append(all_question)
                return JsonResponse({"questions": all_questions})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed for answering the question'})



@require_POST
@csrf_exempt
def answer_question(request):
    if request.method == 'POST':
        try:
            json_file_path = os.path.join(settings.BASE_DIR, 'questions.json')
            with open(json_file_path, 'r') as file:
                json_question = json.load(file)
                data = json.loads(request.body)
                candidate_id = data.get('candidate_id')
                question_id = data.get('id')
                candidateResponse = data.get('candidateResponse') 
                Date = data.get('Date')
                                           
                question = next((question for question in json_question if question.get('id') == question_id))
                if question:
                    correctAnswer = question.get('correctAnswer')
                    question = Questions.objects.create(
                        question_id=question_id,
                        correctResponse=correctAnswer,
                    )
                    question.save()
                    exam = Exam.objects.create(
                        candidate_id=candidate_id,
                        question_id=question_id,
                        candidateResponse=candidateResponse,
                        correctResponse=correctAnswer,
                        Date=Date,                      
                    )
                    exam.save()
                    # if candidateResponse == correctAnswer:
                    #     exam.status = "correct"
                    #     exam.save()
                    #     return JsonResponse({'message': 'correct answer'})
                    # else:
                    #     exam.status = "incorrect"
                    #     exam.save()
                    #     return JsonResponse({'message': 'incorrect answer'})
                    return JsonResponse({'message': 'answer submitted successfully'})
                else:
                    return JsonResponse({'message': 'question not found'})  
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed for answering the question'})

@require_POST
@csrf_exempt
def add_result(request):               #candidate will get only 5 questions according to that result will bw calculated
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            candidate_id=data.get('candidate_id')
            date=data.get('date')
            maximum=data.get('maximum')
            needed=data.get('needed')
            
            calculate_marks=Exam.objects.filter(candidate_id=candidate_id, status='correct')
            total_marks=len(calculate_marks)*2
            
            result=Result.objects.create(
                candidate_id=candidate_id,
                date=date,
                maximum=maximum,
                needed=needed,
                obtained=total_marks,
            )
            result.save()
            # results=Exam.objects.filter(candidate_id=candidate_id)
            # result_declared=[]
            # for result_item in results:
            #     result_declared.append({
            #         'question_id':result_item.question_id,
            #        'candidateResponse':result_item.candidateResponse,
            #         'correctResponse':result_item.correctResponse,
            #        'status':result_item.status
            #     }) 
                # return JsonResponse({'result':result_declared})
            if total_marks>=needed:
                result.status="pass"
                result.save()
                return JsonResponse({'result': result_declared, 'message': 'Candidate cleared the exam'})
            else:
                result.status="fail"
                result.save()
                return JsonResponse({'message': 'candidate failed the exam'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed for calculating the results'}) 
    
require_GET
def fetch_result(request):
    if request.method=='GET':
        try:
            candidate_id=request.GET.get('candidate_id')
            results=Exam.objects.filter(candidate_id=candidate_id)
            result_declared=[]
            for result_item in results:
                result_declared.append({
                    'question_id':result_item.question_id,
                   'candidateResponse':result_item.candidateResponse,
                    'correctResponse':result_item.correctResponse,
                   'status':result_item.status
                }) 
                # return JsonResponse({'result':result_declared})
            return JsonResponse({'result': result_declared})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed for calculating the results'})       
            
            
    

@csrf_exempt
@require_POST
@jwt_auth_required
def create_job(request):
    try:
        user =request.user_id
        data = json.loads(request.body)
        is_emp_exists = User.objects.filter(id=user, role='employee').exists()
       
        if is_emp_exists:
            Job.objects.create(   
                status=data.get('status'),       
                jobName=data.get('jobName'),
                jobDescription=data.get('jobDescription'),
                jobSkills=data.get('jobSkills'),
                experience=data.get('experience'),
                expire=data.get('expire'),
                creater_id=user  
            )
            return JsonResponse({'message': 'Job created successfully'})
        else:
            return JsonResponse({'error': 'Employee with the given ID does not exist or is not an employee'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_POST
@jwt_auth_required
def fetch_job(request):
    userId = request.user_id
    query = request.GET.get('job') 

    is_emp_exists = User.objects.filter(id=userId, role='employee').exists()
    if not is_emp_exists:
        return JsonResponse({'error': 'User not authorized or does not exist'}, status=403)

    if query == 'all':
        jobs = Job.objects.all()
    elif query in ['Active', 'Expired', 'Hide', 'InActive']:
        jobs = Job.objects.filter(status=query)
    else:
        return JsonResponse({'error': 'Invalid query parameter'}, status=400)

    data = [{'id': job.id, 'status': job.status, 'jobName': job.jobName, 'jobDescription': job.jobDescription,
             'jobSkills': job.jobSkills, 'experience': job.experience, 'expire': job.expire,
             'createdDate': job.createdDate, 'creater': job.creater_id} for job in jobs]

    return JsonResponse(data, safe=False)

@csrf_exempt
@require_http_methods(["PUT"])
@jwt_auth_required
def edit_job(request):
    try:
        data = json.loads(request.body)
        jobId = request.GET.get('jobId') 
        userId =request.user_id
        is_emp_exists = User.objects.filter(id=userId, role='employee').exists()  

        if is_emp_exists:
            job = Job.objects.get(pk=jobId)
            
            job.status = data.get('status')
            job.jobName = data.get('jobName')
            job.jobDescription = data.get('jobDescription')
            job.jobSkills = data.get('jobSkills')
            job.experience = data.get('experience')
            job.expire = data.get('expire')
            job.save()
            
            return JsonResponse({'message': 'Job updated successfully'})
        else:
            return JsonResponse({'error': 'Employee with the given ID does not exist or is not an employee'}, status=400)
    except Job.DoesNotExist:
        return JsonResponse({'error': 'Job not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
@jwt_auth_required
@require_http_methods(["DELETE"])
def delete_job(request):
    try:
        userId =request.user_id
        jobId = request.GET.get('jobId')  
        is_emp_exists = User.objects.filter(id=userId, role='employee').exists()  

        if not is_emp_exists:
            return JsonResponse({'error': 'Employee with the given ID does not exist or is not an employee'}, status=400)

        job = Job.objects.get(pk=jobId)
        job.delete()
        
        return JsonResponse({'message': 'Job deleted successfully'})
    except Job.DoesNotExist:
        return JsonResponse({'error': 'Job not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_GET
@jwt_auth_required
def fetch_job_list(request):
    try:
        userId =request.user_id
        isCandidateExit = User.objects.filter(id=userId, role='candidate').exists() 
        if not isCandidateExit:
            return JsonResponse({'error': 'Candidate with the given ID does not exist or is not a candidate'}, status=400)
        
        current_date = datetime.now().date()
        jobs = Job.objects.filter(status="Active", expire__gte=current_date)
        
        data = [{'id': job.id, 'status': job.status, 'jobName': job.jobName, 'jobDescription': job.jobDescription,
                 'jobSkills': job.jobSkills, 'experience': job.experience, 'expire': job.expire,
                 'createdDate': job.createdDate, 'creater': job.creater_id} for job in jobs]
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
@require_POST
@jwt_auth_required
def apply_for_job(request):
    try:
        userId = request.user_id
        job_id = request.GET.get('jobId')
        is_candidate_exist = User.objects.filter(id=userId, role='candidate').exists()
        if not is_candidate_exist:
            return JsonResponse({'error': 'User is not authorized or does not exist'}, status=403)

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return JsonResponse({'error': 'Job does not exist'}, status=404)

        candidate = User.objects.get(id=userId)
        ApplyJob.objects.create(candidate=candidate, jobID=job_id, status='Active')

        return JsonResponse({'message': 'Job applied successfully'})

    except Exception as e:
        return JsonResponse({'error': str(e)})
    
@csrf_exempt
@require_http_methods(["PUT"])
@jwt_auth_required
def withdraw_job(request):
    try:
        candidate_id =request.user_id
        job_id = request.GET.get('jobId')
        
        is_candidate_exist = User.objects.filter(id=candidate_id, role='candidate').exists()
        if not is_candidate_exist:
            return JsonResponse({'error': 'User is not authorized or does not exist'}, status=403)

        existing_application = ApplyJob.objects.filter(candidate_id=candidate_id, jobID=job_id, status='Active').exists()
        
        if existing_application:
            ApplyJob.objects.filter(candidate_id=candidate_id, jobID=job_id, status='Active').update(status='Withdrawn')
            return JsonResponse({'message': 'Job withdrawn successfully'})
        else:
            return JsonResponse({'error': 'No active application found for this candidate and job'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@jwt_auth_required
def fetch_notifications_by_user(request):
    try:
        candidate_id =request.user_id
        is_candidate_exist = User.objects.filter(id=candidate_id, role='candidate').exists()
        if not is_candidate_exist:
            return JsonResponse({'error': 'User is not authorized or does not exist'}, status=403)

        notifications = Notification.objects.filter(user_id=candidate_id)
        notification_data = []
        for notification in notifications:
            notification_data.append({
                'user_id': notification.user_id,
                'message': notification.message,
                'date': notification.date,
                'status': notification.status,
            })
        return JsonResponse(notification_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
@require_http_methods(["PUT"])
@jwt_auth_required
def mark_notification_as_read(request):
    try:
        candidate_id =request.user_id
        notification_id = request.GET.get('notificationId')
        is_candidate_exist = User.objects.filter(id=candidate_id, role='candidate').exists()
        if not is_candidate_exist:
            return JsonResponse({'error': 'User is not authorized or does not exist'}, status=403)

        existing_notification = Notification.objects.filter(id=notification_id, user_id=candidate_id, status='unread').exists()
        
        if existing_notification:
            Notification.objects.filter(id=notification_id, user_id=candidate_id, status='unread').update(status='read')
            return JsonResponse({'message': 'Notification marked as read'})
        else:
            return JsonResponse({'error': 'No unread notification found for this user'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
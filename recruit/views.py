from datetime import date
import os
from django.conf import settings
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from project.decorators import jwt_auth_required
from recruit.models import AuthorizeToModule, Stream
from recruit.models import Questions, Scheduler
from recruit.models import Exam,Track
from recruit.models import Result,Job,ApplyJob,Notification
from users.models import User



@csrf_exempt
@require_POST
@jwt_auth_required
def create_stream(request):
    if request.method == 'POST':
        try:
            if not User.objects.filter(id=request.user.id, role='admin').exists():
              return JsonResponse({'error': 'Only admin can access it'}, status=404)
            user = request.user_id
            if not user:
                return JsonResponse({'message': 'User is unauthenticated'},status=401)
            data = json.loads(request.body)
            streamName = data.get('streamName')

            stream = Stream.objects.create(          
                streamName=streamName,
            )
            stream.save()
            
            return JsonResponse({'message': 'Stream created successfully'},status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'},status=400)


@csrf_exempt
@require_http_methods(['PUT'])
@jwt_auth_required
def update_stream(request):
    if request.method == 'PUT':
        try:
            if not User.objects.filter(id=request.user.id, role='admin').exists():
               return JsonResponse({'error': 'Only admin can access it'}, status=404)
            stream_id=request.GET.get('id')
            if not stream_id:
                return JsonResponse({'message':'stream id not found'},status=404)
            data = json.loads(request.body)
            stream=Stream.objects.get(id=stream_id)
            stream.streamName = data.get('streamName')
            stream.save()
            return JsonResponse({'message':'stream updated successfully'},status=200)
        except Stream.DoesNotExist:
            return JsonResponse({'error': 'stream not found'},status=404)
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed for updating the stream'},status=400)
  
    
@require_GET
@jwt_auth_required
@jwt_auth_required
def fetch_stream(request):
    if request.method == 'GET':
        try:
            if not User.objects.filter(id=request.user_id, role='admin').exists():
                return JsonResponse({'error': 'Only admin can access it'}, status=404)
            streams=Stream.objects.all()
            if not streams:
                return JsonResponse({'message': 'device not found'},status=404)
            stream_name = []
            for stream in streams:
                stream_name.append({
                    'streamName': stream.streamName,
                })
                return JsonResponse({'streams': stream_name})
        except Stream.DoesNotExist:
            return JsonResponse({'error':'stream not found'},status=404)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'},status=400)


@require_GET
@jwt_auth_required
def get_questions_ids(request): 
    try:
        if not User.objects.filter(id=request.user_id, role='candidate').exists():
                return JsonResponse({'error': 'Only candidate can access it'}, status=404)
        candidate_id = request.GET.get('id')
        scheduler_id = request.GET.get('scheduler_id')
        Exam.objects.filter(scheduler_id=scheduler_id, candidate_id=candidate_id).delete()
        
        is_scheduled_exam = Scheduler.objects.filter(id=scheduler_id, candidate_id=candidate_id, status='pending').exists()
        if not is_scheduled_exam:
            return JsonResponse({"error": "Exam is not scheduled yet or already attempted" , "code" :404},status=404)

        Result.objects.filter(scheduler_id=scheduler_id).delete()

        exists_questions = Exam.objects.filter(scheduler_id=scheduler_id, candidate_id=candidate_id).exists()
        refresh_questions_data = []
        questions_data = []

        if exists_questions:
            # Retrieve existing exam questions if any
            refresh_exam_questions = Exam.objects.filter(scheduler_id=scheduler_id, candidate_id=candidate_id).values_list('id', flat=True)
            for question_id in refresh_exam_questions:
                refresh_questions_data.append(question_id)
            
            if refresh_questions_data:
                refresh_questions_data = sorted(refresh_questions_data)
                return JsonResponse({"questions": refresh_questions_data})

        round_value = Scheduler.objects.filter(id=scheduler_id, candidate_id=candidate_id).values_list('round', flat=True).first()

        questions = Questions.objects.order_by('?')[:6]
        for question in questions:
            Exam.objects.create(
                candidate_id=candidate_id,
                question_id=question.id,
                candidateResponse='null',
                correctResponse=question.correctResponse,
                Date=date.today(),
                status="null",
                round=round_value,
                scheduler_id=scheduler_id
            )
        exam_questions = Exam.objects.filter(scheduler_id=scheduler_id, candidate_id=candidate_id).values_list('id', flat=True)
        for question_id in exam_questions:
                questions_data.append(question_id)

        questions_data = sorted(questions_data)
        return JsonResponse({"questions": questions_data})
    except Exception as e:
        return JsonResponse({'error': str(e)})


@require_GET
@jwt_auth_required
def get_questions(request): 
    try:
        if not User.objects.filter(id=request.user_id, role='candidate').exists():
                return JsonResponse({'error': 'Only candidate can access it'}, status=404)
        exam_id = request.GET.get('exam_id')

        examData=Exam.objects.get(id=exam_id)
        question_data=Questions.objects.get(id=examData.question_id)
        response_data = {
            "id": examData.id,
            "question": question_data.question,
            "option1": question_data.option1,
            "option2": question_data.option2,
            "option3": question_data.option3,
            "option4": question_data.option4,
            "type": question_data.type,
            "level": question_data.level,
            "stream_id": question_data.stream_id
        }
        
        return JsonResponse({"question": response_data},status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)})


@require_POST
@csrf_exempt
@jwt_auth_required
def save_answer(request):
    if request.method == 'POST':
        try:
            if not User.objects.filter(id=request.user_id, role='candidate').exists():
                return JsonResponse({'error': 'Only candidate can access it'}, status=404)
            data = json.loads(request.body)
            candidate_id = data.get('candidate_id')
            exam_id = data.get('exam_id')
            candidateResponse = data.get('candidateResponse')
            scheduler_id = data.get('scheduler_id')
            question_id = Exam.objects.filter(id=exam_id).values_list('question_id', flat=True).first()

            question = Questions.objects.get(id=question_id)
            correctAnswer = None 
            status = None 
            if question:
                correctAnswer = question.correctResponse  

                if candidateResponse == correctAnswer:
                    status = "correct"
                else:
                    status = "incorrect"

                exists = Exam.objects.filter(id=exam_id, candidate_id=candidate_id, scheduler_id=scheduler_id)
                if exists:
                    exists = exists.first()
                    exists.candidate_id = candidate_id
                    exists.question_id = question_id
                    exists.candidateResponse = candidateResponse
                    exists.correctResponse = correctAnswer
                    exists.Date = date.today()
                    exists.status = status
                    exists.round = 1
                    exists.scheduler_id = scheduler_id
                    exists.save()
                return JsonResponse({'message': 'answer submitted successfully'},status=200)
            else:
                return JsonResponse({'message': 'question not found'},status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed for answering the question'},status=400)



@require_http_methods(['PUT'])
@csrf_exempt
@jwt_auth_required
def clear_answer(request):
    if request.method == 'PUT':
        try:
            if not User.objects.filter(id=request.user_id, role='candidate').exists():
                return JsonResponse({'error': 'Only candidate can access it'}, status=404)
            candidate_id = request.GET.get('candidate_id')
            exam_id = request.GET.get('exam_id')
            exam = Exam.objects.filter(id=exam_id, candidate_id=candidate_id)
            if exam:
                exam = exam.first()
                exam.candidateResponse = 'null'
                #exam.correctResponse = 'null'
                exam.status = 'null'
                exam.save()
                return JsonResponse({'success': 'candidate response cleared successfully'},status=200)
            else:
                return JsonResponse({'error': 'Candidate response could not be cleared'}, status=400)
       
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed for answering the question'},status=400)
   

@csrf_exempt
@require_POST
@jwt_auth_required
def submit_exam(request):
    if request.method == 'POST':
        try:
            if not User.objects.filter(id=request.user_id, role='candidate').exists():
                return JsonResponse({'error': 'Only candidate can access it'}, status=404)
            data = json.loads(request.body)
            candidate_id = data.get('candidate_id')
            date = data.get('date')
            maximum = data.get('maximum')
            needed = data.get('needed')
            scheduler_id = data.get('scheduler_id')
            
            calculate_marks = Exam.objects.filter(candidate_id=candidate_id, scheduler_id=scheduler_id, status='correct')
            total_questions = Exam.objects.filter(candidate_id=candidate_id, scheduler_id=scheduler_id)
            total_marks = len(calculate_marks) * 2

            status = 'pass' if total_marks >= needed else 'fail'

            result, created = Result.objects.get_or_create(
                candidate_id=candidate_id,
                scheduler_id=scheduler_id,
                defaults={
                    'date': date,
                    'maximum': maximum,
                    'needed': needed,
                    'obtained': total_marks,
                    'round': 1,
                    'question': len(total_questions),
                    'status': status
                }
            )

            candidate = User.objects.get(id=candidate_id)
            if status == 'pass':
                Track.objects.create(
                    candidate=candidate,
                    currentStatus="Passed Exam",
                    round1="Cleared"
                )
            else:
                Track.objects.create(
                    candidate=candidate,
                    currentStatus="Failed Exam",
                    round1="Not Cleared"
                )

            updated_scheduled_exam = Scheduler.objects.get(id=scheduler_id, candidate_id=candidate_id)
            updated_scheduled_exam.status = 'attempted'
            updated_scheduled_exam.save()

            return JsonResponse({'total_marks': total_marks, 'message': 'Candidate cleared the exam' if status == 'pass' else 'Candidate failed the exam'},status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed for calculating the results'},status=400)



@csrf_exempt
@require_GET
@jwt_auth_required
def fetch_result(request):
    if request.method == 'GET':
        try:
            
            candidate_id = request.GET.get('candidate_id')
            
            results = Result.objects.filter(candidate_id=candidate_id)    
            result_final = []
            round_dict = {}

            for result_item in results:
                round_key = result_item.round
                if round_key not in round_dict:
                    round_dict[round_key] = []

                exam_details_list = []
                exam_details = Exam.objects.filter(round=result_item.round,candidate_id=candidate_id)
                for exam_detail in exam_details:
                    try:
                        questions_details = Questions.objects.get(id=exam_detail.question_id)
                        # Append the exam detail to the exam_details_list
                        if exam_detail.correctResponse == exam_detail.candidateResponse :
                         exam_details_list.append({
                            "question_id": exam_detail.question_id,
                            "question": questions_details.question,  
                            "correctResponse": exam_detail.correctResponse,
                            "yourResponse": exam_detail.candidateResponse,
                            "point": 2  
                         })
                        else:
                            exam_details_list.append({
                            "question_id": exam_detail.question_id,
                            "question": questions_details.question, 
                            "correctResponse": exam_detail.correctResponse,
                            "yourResponse": exam_detail.candidateResponse,
                            "point": 0  
                         })

                    except Questions.DoesNotExist:
                        # Handle the case where the question does not exist
                        continue

                round_dict[round_key].append({
                    'exam_id': result_item.id,
                    'total_question': result_item.question,
                    'total_marks': result_item.maximum,
                    'obtained_marks' : result_item.obtained,
                    'result': result_item.status,
                    'exam_details': exam_details_list 
                })

            # Prepare final result list
            for round_key, result_list in round_dict.items():
                result_final.append({
                    'round': round_key,
                    'result': result_list
                })

            return JsonResponse({'results': result_final})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed for fetching the results'},status=400)
 
 
@require_POST 
@csrf_exempt
@jwt_auth_required
def candidate_scheduler(request):    
    if request.method=='POST':
        try:
            user=User.objects.get(id=request.user_id)
            if user.role != 'employee' or user.emp.designation != 'hr':
              return JsonResponse({'error': 'Only HR can access it'}, status=400)

          
            data = json.loads(request.body)
            scheduledDate= data.get('scheduledDate')
            round=data.get('round')
            candidate_id=data.get('candidate_id')

            scheduler = Scheduler.objects.create(          
                scheduledDate=scheduledDate,
                round=round,
                candidate_id=candidate_id,
                status='pending'
             )
            scheduler.save()
            return JsonResponse({'message':'exam scheduled successfully'},status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'message':'only post method'},status=400)



@require_http_methods(['PUT'])             
@csrf_exempt
@jwt_auth_required
def update_candidate_scheduler(request):     
    if request.method == 'PUT':
        try:
            user=User.objects.get(id=request.user_id)
            if user.role != 'employee' or user.emp.designation != 'hr':
              return JsonResponse({'error': 'Only HR can access it'}, status=400)
            
            candidate_id=request.GET.get('id')
            if not candidate_id:
                return JsonResponse({'message':'Scheduler not found for the candidate'},status=404)
            data = json.loads(request.body)
            scheduledDate=data.get('scheduledDate')
            status=data.get('status')
            round=data.get('round')

            scheduler = Scheduler.objects.filter(candidate_id=candidate_id)
            scheduler.scheduledDate=scheduledDate
            scheduler.round=round
            scheduler.status=status
            scheduler.save()
            return JsonResponse({'message':'exam schedule updated successfully'},status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'message':'only put method allows'},status=404)
 

@require_GET
@csrf_exempt
@jwt_auth_required
def fetch_my_scheduler(request):  # This can be done by the candidate
    try:
        if not User.objects.filter(id=request.user_id, role='candidate').exists():
                return JsonResponse({'error': 'Only candidate can access it'}, status=404)
 
        schedulers = Scheduler.objects.filter(candidate_id=request.user_id)
        if not schedulers.exists():
            return JsonResponse({'message': 'No schedules found for the candidate'}, status=404)

        response_data = []
        for scheduler in schedulers:
            response_data.append({
                'schedulerId': scheduler.id,
                'scheduledDate': scheduler.scheduledDate,
                'round': scheduler.get_round_display(),
                'status': scheduler.get_status_display(),
            })

        return JsonResponse({'schedules': response_data})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
      

@require_GET
def track(request):
    if request.method=='GET':
        try:
            candidate_id=request.GET.get('id')
            if not candidate_id:
                return JsonResponse({'message':'track not found for the candidate'},status=404)
            tracks = Track.objects.filter(candidate_id=candidate_id)
            track_result=[]
            for track in tracks:
                track_result.append({
                    'currentStatus':track.currentStatus,
                   'round1':track.round1
                }) 
            return JsonResponse({'track':track_result})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'message':'only get method allows'},status=400)
    

@csrf_exempt
@require_POST
@jwt_auth_required
def create_job(request): 
    try:
        user=User.objects.get(id=request.user_id)
        if user.role != 'employee' or user.emp.designation != 'hr':
              return JsonResponse({'error': 'Only HR can access it'}, status=400)
        
        data = json.loads(request.body)

        Job.objects.create(   
                status=data.get('status'),       
                jobName=data.get('jobName'),
                jobDescription=data.get('jobDescription'),
                jobSkills=data.get('jobSkills'),
                qualification = data.get('qualification'),
                experience=data.get('experience'),
                expire=data.get('expire'),
                creater_id=request.user_id  
            )
        return JsonResponse({'message': 'Job created successfully'},status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_POST
@jwt_auth_required
def fetch_job(request):
    userId = request.user_id
    user=User.objects.get(id=userId)
    if user.role != 'employee' or user.emp.designation != 'hr':
        return JsonResponse({'error': 'Only HR can access it'}, status=400)
    
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
             'jobSkills': job.jobSkills,'qualification': job.qualification, 'experience': job.experience, 'expire': job.expire,
             'createdDate': job.createdDate, 'creater': job.creater_id} for job in jobs]

    return JsonResponse(data, safe=False)


@csrf_exempt
@require_http_methods(["PUT"])
@jwt_auth_required
def edit_job(request):
    try:
        user_id= request.user_id
        user=User.objects.get(id=user_id)
        if user.role != 'employee' or user.emp.designation != 'hr':
            return JsonResponse({'error': 'Only HR can access it'}, status=400)
        
        data = json.loads(request.body)
        jobId = request.GET.get('jobId')
        if not jobId:
            return JsonResponse({'error': 'Job ID is required'}, status=400)  
        job=Job.objects.get(id=jobId)
        job.status = data.get('status')
        job.jobName = data.get('jobName')
        job.jobDescription = data.get('jobDescription')
        job.jobSkills = data.get('jobSkills')
        job.experience = data.get('experience')
        job.expire = data.get('expire')
        job.qualification = data.get('qualification')
        job.save()
        return JsonResponse({'message': 'Job updated successfully'},status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@jwt_auth_required
@require_http_methods(["DELETE"])
def delete_job(request):
    try:
        user_id= request.user_id
        user=User.objects.get(id=user_id)
        if user.role != 'employee' or user.emp.designation != 'hr':
              return JsonResponse({'error': 'Only HR can access it'}, status=400)
        
        jobId = request.GET.get('jobId') 

        job = Job.objects.get(id=jobId)
        job.delete()
        
        return JsonResponse({'message': 'Job deleted successfully'},status=200)
    except Job.DoesNotExist:
        return JsonResponse({'error': 'Job not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_GET
def fetch_job_list(request):
    
    jobs = Job.objects.filter(status='Active',expire__gte=date.today())

    data = [
        {
            'id': job.id,
            'status': job.status,
            'jobName': job.jobName,
            'jobDescription': job.jobDescription,
            'jobSkills': job.jobSkills,
            'qualification' : job.qualification,
            'experience': job.experience,
            'expire': job.expire,
            'createdDate': job.createdDate
        }
        for job in jobs
    ]

    return JsonResponse(data, safe=False)


@csrf_exempt
@require_GET
@jwt_auth_required
def fetch_all_applied_jobs(request):
    try:
        user_id= request.user_id
        user=User.objects.get(id=user_id)
        if user.role != 'employee' or user.emp.designation != 'hr':
              return JsonResponse({'error': 'Only HR can access it'}, status=400)
        user = User.objects.get(id=user_id)

        applied_jobs = ApplyJob.objects.filter(status__in=['Applied', 'In Review'])

        applied_jobs_data = []
        for job in applied_jobs:
            try:
                job_info = Job.objects.get(id=job.job_id)
                candidate_info = User.objects.get(id=job.candidate_id)
                applied_jobs_data.append({
                    'application_id': job.id,
                    'job_id': job_info.id,
                    'job_jobName': job_info.jobName,
                    'candidate_id': candidate_info.id,
                    'candidate_name': candidate_info.fullName,
                    'qualification': job.qualification,
                    'applied_date': job.applied_date.strftime('%Y-%m-%d'),
                    'skills': job.skills,
                    'experience': job.experience,
                    'passing_year': job.passing_year,
                    'marks': job.marks,
                    'status': job.status
                })
                
                job.status = 'In Review'
                job.save()
            except Job.DoesNotExist:
                continue 
            except User.DoesNotExist:
                continue  # or handle the error as appropriate

        return JsonResponse({'applied_jobs': applied_jobs_data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@csrf_exempt
@require_POST
@jwt_auth_required
def select_candidate_for_round1(request):
    try:
        user_id = request.user_id
        user=User.objects.get(id=user_id)
        if user.role != 'employee' or user.emp.designation != 'hr':
              return JsonResponse({'error': 'Only HR can access it'}, status=400)
        

        data = json.loads(request.body)
        candidate_id = data.get('candidate_id')
        application_id = data.get('application_id')
        exam_date = data.get('exam_date')

        if not ApplyJob.objects.filter(id=application_id, candidate_id=candidate_id).exists():
            return JsonResponse({'error': 'Application does not exist.'}, status=404)

        applied_job = ApplyJob.objects.get(id=application_id, candidate_id=candidate_id)
        job_details = Job.objects.get(id=applied_job.job_id)

        if job_details.expire < date.today():
            applied_job.status = 'Rejected'
            applied_job.save()
            return JsonResponse({'error': 'Job has expired.'}, status=404)

        if applied_job.qualification not in job_details.qualification:
            applied_job.status = 'Rejected'
            applied_job.save()
            return JsonResponse({'error': 'Qualification does not match.'}, status=404)

        if Scheduler.objects.filter(job_id=applied_job.job_id, candidate_id=candidate_id).exists():
            return JsonResponse({'error': 'Exam is already scheduled.'}, status=400)
        
        scheduled = Scheduler.objects.create(
            scheduledDate=exam_date,
            status='pending',
            round=1,
            candidate_id=candidate_id,
            job_id=job_details.id
        )

        applied_job.status = 'Interviewed'
        applied_job.save()

        notification = Notification.objects.create(
                message = "Congrats!! You're eligible for the 1st round interview for the role of " + job_details.jobName,
                date = date.today(),
                status = 'unread',
                jobId = job_details.id,
                jobName = job_details.jobName,
                currentStatus = 'Round1',
                user = candidate_id
            )
        notification.save()
        Track.objects.create(
                candidate = candidate_id,
                currentStatus = 'Eligible for round1',
                round1 = 'Pending'
            )

        return JsonResponse({'success': 'Exam is scheduled.', 'scheduled': {
            'scheduledDate': scheduled.scheduledDate,
            'status': scheduled.status,
            'round': scheduled.round,
            'candidate_id': scheduled.candidate_id,
            'job_id' : scheduled.job_id
        }}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@jwt_auth_required
@require_GET
def filter_profile(request):
    try:
        user=User.objects.get(id=request.user_id)
        if user.role != 'employee' or user.emp.designation != 'hr':
              return JsonResponse({'error': 'Only HR can access it'}, status=400)

        applied_jobs = ApplyJob.objects.filter(status='Active').values()  
        
        return JsonResponse({'applied_jobs': list(applied_jobs)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@require_GET
def fetch_stream_with_questions(request):
    if request.method == 'GET':
        try:
            json_file_path = os.path.join(settings.BASE_DIR, 'questions.json')
            with open(json_file_path, 'r') as file:
                questions_data = json.load(file)
                
            stream_id = request.GET.get('id') 
            if not stream_id:
                return JsonResponse({'message': 'stream not found'},status=404)

            # Fetching the stream
            stream = Stream.objects.get(id=stream_id)
            stream_name = stream.streamName
                
            total_questions = [question for question in questions_data if question.get('stream_id') == int(stream_id)]
            all_questions = []
            
            for question in total_questions:
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
                
            if not all_questions:
                return JsonResponse({'message': 'No questions found for this stream ID'},status=404)
                
            return JsonResponse({'streamName': stream_name, 'all_questions': all_questions})
            
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed for fetching questions'},status=400)




@csrf_exempt
@require_POST
@jwt_auth_required
def apply_for_job(request):
    try:
        user_id = request.user_id

        if not User.objects.filter(id=user_id, role='candidate').exists():
            return JsonResponse({'error': 'Only candidates can apply for jobs.'}, status=403)

        data = json.loads(request.body)
        job_id = data.get('job_id')
        qualification = data.get('qualification')
        skills = data.get('skills')
        experience = data.get('experience')
        passing_year = data.get('passingYear')
        marks = data.get('marks')

        if not job_id:
            return JsonResponse({'error': 'Job ID is required.'}, status=400)

        try:
            Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return JsonResponse({'error': 'Job does not exist.'}, status=404)

        if ApplyJob.objects.filter(job_id=job_id, candidate_id=user_id).exists():
            return JsonResponse({'error': 'You have already applied for this job.'}, status=403)

        ApplyJob.objects.create(
            candidate_id=user_id,
            job_id=job_id,
            qualification=qualification,
            applied_date=date.today(),
            skills=skills,
            experience=experience,
            passing_year=passing_year,
            marks=marks,
            status='Applied'
        )

        return JsonResponse({'message': 'Job applied successfully.'}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@csrf_exempt
@require_GET
@jwt_auth_required
def fetch_applied_job_by_candidate(request):
    try:
        user_id = request.user_id

        if not User.objects.filter(id=user_id, role='candidate').exists():
            return JsonResponse({'error': 'Only candidates can fetch their applied jobs.'}, status=403)

        applied_jobs = ApplyJob.objects.filter(candidate_id=user_id)

        applied_jobs_data = []
        for job in applied_jobs:
            try:
                job_info = Job.objects.get(id=job.job_id)
                applied_jobs_data.append({
                    'job_id': job_info.id,
                    'job_jobName': job_info.jobName,
                    'qualification': job.qualification,
                    'applied_date': job.applied_date.strftime('%Y-%m-%d'),
                    'skills': job.skills,
                    'experience': job.experience,
                    'passing_year': job.passing_year,
                    'marks': job.marks,
                    'status': job.status
                })
            except Job.DoesNotExist:
                continue 

        return JsonResponse({'applied_job': applied_jobs_data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


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
                'jobName': notification.jobName,
                'currentStatus': notification.currentStatus,
                'jobId': notification.jobId
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
    
   
@require_GET
@jwt_auth_required
def exam_result(request):
    try:
        candidate_id = request.user_id 
        results = Result.objects.filter(candidate_id=candidate_id)

        serialized_results = []
        for result in results:
            serialized_result = {
                "exam": result.get_round_display(),
                "totalValue": result.maximum,
                "status": result.status,
                "totalQuestions" : 5, 
                "details": []
            }

            # Load questions from JSON file
            json_file_path = os.path.join(settings.BASE_DIR, 'questions.json')
            with open(json_file_path, 'r') as file:
                json_question = json.load(file)

            # Fetch exam results
            results = Exam.objects.filter(candidate_id=candidate_id)
            result_declared = []
            for result_item in results:
                question_id = result_item.question_id
                question_data = next((question for question in json_question if question['id'] == question_id), None)
                result_declared.append({
                    'question_id': result_item.question_id,
                    'question': question_data['question'],
                    'candidateResponse': result_item.candidateResponse,
                    'correctResponse': result_item.correctResponse,
                    'status': result_item.status
                })

            serialized_result["details"] = result_declared
            serialized_results.append(serialized_result)

        response_data = {
            "Results": serialized_results
        }

        return JsonResponse(response_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
def create_question(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = Questions.objects.create(
                question=data.get('question'),
                option1=data.get('option1'),
                option2=data.get('option2'),
                option3=data.get('option3'),
                option4=data.get('option4'),
                correctResponse=data.get('correctResponse'),
                type=data.get('type'),
                level=data.get('level'),
                stream_id=data.get('stream_id') 
            )
            return JsonResponse({'message': 'Question created successfully', 'question_id': question.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def delete_question(request):
    if request.method == 'DELETE':
        try:
            question_id = request.GET.get('question_id')
            existsQuestion = Questions.objects.get(id=question_id)
            if existsQuestion:
                existsQuestion.delete()
                return JsonResponse({'message': 'Question deleted successfully'}, status=200)
            else:
                return JsonResponse({'error': 'Question not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)  
    

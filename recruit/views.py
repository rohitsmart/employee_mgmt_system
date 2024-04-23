import os
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from recruit.models import Stream
import random
from recruit.models import Questions
from recruit.models import Exam
from recruit.models import Result
from recruit.models import Scheduler
from recruit.models import Track
from users.models import User


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
    if request.method == 'GET':
        try:
            candidate_id = request.GET.get('id')
            if not candidate_id:
                return JsonResponse({"error": "Candidate ID is required"})

            json_file_path = os.path.join(settings.BASE_DIR, 'questions.json')
            with open(json_file_path, 'r') as file:
                questions_data = json.load(file)
            stream_id = request.GET.get('id') 
            total_questions = [question for question in questions_data if question.get('stream_id') == int(stream_id)]
            if len(total_questions) < 5:
                return JsonResponse({"message": "Questions are less than requirement"})
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

            # Save questions attempted by the candidate
            for question in questions:
                Questions.objects.create(
                    candidate_id=candidate_id,
                    question_id=question["id"],
                    correctResponse=question["correctAnswer"]
                )

            return JsonResponse({"questions": all_questions})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed for fetching questions'})
@require_GET
def next_question(request):
    if request.method == 'GET':
        try:
            json_file_path = os.path.join(settings.BASE_DIR, 'questions.json')
            with open(json_file_path, 'r') as file:
                questions_data = json.load(file)
            stream_id = request.GET.get('id')

            # Fetch the last fetched questions for the current candidate from session
            last_fetched_questions = request.session.get('last_fetched_questions', [])
            
            # Filter questions by stream_id and excluding the already fetched questions
            available_questions = [question for question in questions_data
                                   if question.get('stream_id') == int(stream_id)
                                   and question not in last_fetched_questions]

            if len(available_questions) == 0:
                return JsonResponse({"message": "No more questions available"})

            # Select a random question from available questions
            next_question = random.choice(available_questions)

            # Update the last fetched questions for the current candidate in session
            last_fetched_questions.append(next_question)
            # Keep only the latest 5 questions
            if len(last_fetched_questions) > 5:
                last_fetched_questions.pop(0)

            # Update the session with the latest fetched questions
            request.session['last_fetched_questions'] = last_fetched_questions

            question_response = {
                "id": next_question["id"],
                "question": next_question["question"],
                "option1": next_question["option1"],
                "option2": next_question["option2"],
                "option3": next_question["option3"],
                "option4": next_question["option4"],
                "type": next_question["type"],
                "level": next_question["level"],
                "stream_id": next_question["stream_id"]
            }
            return JsonResponse({"question": question_response})

        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed for fetching questions'})
    
@require_GET
def previous_question(request):
    if request.method == 'GET':
        try:
            # Fetch the last fetched questions for the current candidate from session
            last_fetched_questions = request.session.get('last_fetched_questions', [])

            # Check if there are any previous questions available
            if len(last_fetched_questions) < 2:
                return JsonResponse({"message": "No previous question available"})

            # Retrieve the previous question
            previous_question = last_fetched_questions[-2]

            # Update the session to remove the current question
            request.session['last_fetched_questions'] = last_fetched_questions[:-1]

            question_response = {
                "id": previous_question["id"],
                "question": previous_question["question"],
                "option1": previous_question["option1"],
                "option2": previous_question["option2"],
                "option3": previous_question["option3"],
                "option4": previous_question["option4"],
                "type": previous_question["type"],
                "level": previous_question["level"],
                "stream_id": previous_question["stream_id"]
            }
            return JsonResponse({"question": question_response})

        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed for fetching questions'})

   

@require_POST
@csrf_exempt
def save_answer(request):           #in this we are savig the answer by the candidate
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
                scheduler_id=data.get('scheduler_id')
                                           
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
                        scheduler_id=scheduler_id                   
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
def submit_exam(request):               #candidate will get only 5 questions according to that result will bw calculated
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            candidate_id=data.get('candidate_id')
            date=data.get('date')
            maximum=data.get('maximum')
            needed=data.get('needed')
            scheduler_id=data.get('scheduler_id')
            
            calculate_marks=Exam.objects.filter(candidate_id=candidate_id, status='correct')
            total_marks=len(calculate_marks)*2
            
            result=Result.objects.create(
                candidate_id=candidate_id,
                date=date,
                maximum=maximum,
                needed=needed,
                obtained=total_marks,
                scheduler_id=scheduler_id
            )
            result.save()
            if total_marks>=needed:
                result.status="pass"
                result.save()
                candidate = User.objects.get(id=candidate_id)
                track = Track.objects.create(
                    candidate=candidate,
                    currrentStatus="Passed Exam",
                    round1="Cleared"
                )
                track.save()
                return JsonResponse({'total_marks': total_marks, 'message': 'Candidate cleared the exam'})          
            
            else:
                result.status="fail"
                result.save()
                candidate = User.objects.get(id=candidate_id)
                track = Track.objects.create(
                    candidate=candidate,
                    currrentStatus="failed the Exam",
                    round1="failed"
                )
                track.save()
                return JsonResponse({'total_marks':total_marks,'message': 'candidate failed the exam'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed for calculating the results'}) 
  
@csrf_exempt    
@require_GET
def fetch_result(request):
    if request.method=='GET':
        try:
            candidate_id=request.GET.get('candidate_id')
            json_file_path = os.path.join(settings.BASE_DIR, 'questions.json')
            with open(json_file_path, 'r') as file:
               json_question = json.load(file)

            results=Exam.objects.filter(candidate_id=candidate_id)
            result_declared=[]
            for result_item in results:
                question_id = result_item.question_id
                question_data = next((question for question in json_question if question['id'] == question_id), None)              
                result_declared.append({
                    'question_id':result_item.question_id,
                    'question': question_data['question'],
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
 

@require_POST 
@csrf_exempt
def candidate_scheduler(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            scheduledDate= data.get('scheduledDate')
            round=data.get('round')
            candidate_id=data.get('candidate_id')
            scheduler = Scheduler.objects.create(          
                scheduledDate=scheduledDate,
                round=round,
                candidate_id=candidate_id
            )
            scheduler.save()
            scheduler.status='started'
            scheduler.save()
            return JsonResponse({'message':'exam scheduled successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'message':'only post method'})

@require_http_methods(['PUT'])             
@csrf_exempt
def update_candidate_scheduler(request):     
    if request.method == 'PUT':
        # here we can update the schedule for the candidateif the candidate clear the round or if the exam has 
        # has to be reshedued 
        try:
            candidate_id=request.GET.get('id')
            if not candidate_id:
                return JsonResponse({'message':'sscheduler not found for the candidate'})
            data = json.loads(request.body)
            # candidate_id=data.get('candidate_id')
            scheduledDate=data.get('scheduledDate')
            round=data.get('round')
            scheduler = Scheduler.objects.get(id=candidate_id)
            scheduler.scheduledDate=scheduledDate
            scheduler.round=round
            scheduler.save()
            return JsonResponse({'message':'exam schedule updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'message':'only put method allows'})
 
@require_GET
@csrf_exempt
def fetch_my_scheduler(request):
    if request.method=='GET':
        try:
            candidate_id=request.GET.get('id')
            if not candidate_id:
                return JsonResponse({'message':'schedule not found for the candidate'})
            scheduler = Scheduler.objects.get(id=candidate_id)
            return JsonResponse({'scheduledDate':scheduler.scheduledDate,
                                 'round':scheduler.round})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'message':'only get method allows'})       
 

@require_GET
def track(request):
    if request.method=='GET':
        try:
            candidate_id=request.GET.get('id')
            if not candidate_id:
                return JsonResponse({'message':'track not found for the candidate'})
            tracks = Track.objects.filter(candidate_id=candidate_id)
            # leaves=Leave.objects.filter(user_id=user_id)
            # if not leaves:
            #     return JsonResponse({'message':'leave not found'})
            track_result=[]
            for track in tracks:
                track_result.append({
                    'currrentStatus':track.currrentStatus,
                   'round1':track.round1
                }) 
            return JsonResponse({'track':track_result})
            # return JsonResponse({'currrentStatus':track.currrentStatus,     
            #                      'round1':track.round1})          #here i will include the rest of the rounds according to the requirements
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'message':'only get method allows'})
 

# @csrf_exempt
# @require_GET
# def next_question(request):
#     if request.method == 'GET':
#         try:
#             json_file_path = os.path.join(settings.BASE_DIR, 'questions.json')
#             with open(json_file_path, 'r') as file:
#                 json_data = json.load(file)
#                 print(json_data)
#                 question_id = request.GET.get('id')
#                 next_question = None
#                 for idx, question in enumerate(json_data):
#                     if question.get('id') == question_id:
#                         if idx + 1 < len(json_data):
#                             next_question = json_data[idx + 1]
#                         break
#                 if next_question:
#                     return JsonResponse(next_question)
#                 else:
#                     return JsonResponse({'message': 'No next question found.'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)})
#     else:
#         return JsonResponse({'error': 'Only GET requests are allowed for fetching the next question'})

   
          
    
    

# Create your views here.

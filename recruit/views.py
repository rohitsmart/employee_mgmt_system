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
            
            
    
    

# Create your views here.

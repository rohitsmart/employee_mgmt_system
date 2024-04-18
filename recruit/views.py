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
              data=json.loads(request.body)
              question_id = data.get('id')
              your_answer = data.get('your_answer')
              
              question = next((question for question in json_question if question.get('id') == question_id))
              if question:
                  correct_answer=question.get('correctAnswer')
                  if your_answer == correct_answer:
                      return JsonResponse({'message': 'correct answer'})
                  else:
                      return JsonResponse({'message': 'incorrect answer'})
              else:
                  return JsonResponse({'message': 'question not found'})   
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed for answering the question'})

    
    

# Create your views here.

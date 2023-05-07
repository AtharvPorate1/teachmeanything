from django.shortcuts import render
import openai, os
from dotenv import load_dotenv
from django.utils import timezone
from .models import PageVisit
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import UserPageVisit

load_dotenv()
# Create your views here.

api_key = os.getenv("OPENAI_KEY",None)
openai.api_key = api_key


def sensei(request):
    sensei_response = None
    chatbot_response = None  # initialize chatbot_response with a default value

    if api_key is not None and request.method == 'POST':

        user_input = request.POST.get('user_input')
        prompt = user_input

        response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
  {"role": "user", "content": f"I want to learn everything about {prompt}, break down this topic into multiple subtopics, then teach sub-topics one by one in about 1000 words using examples and anecdotes.Ask me questions and MCQs to test my understanding, Identify my mistake and give me feedback. always remember you have to teach me each subtopic in 1000 words.and total length of the response should be 5000 words"}
]
)
        print(response)

        chatbot_response = response['choices'][0]['message']['content']
       
    return render(request,'sensei_base.html',{'response': chatbot_response})


def record_page_visit(request, page_name):
    if request.user.is_authenticated:
        # Check if there is an existing page visit record for this user and page
        try:
            page_visit = PageVisit.objects.get(user=request.user, page_name=page_name)
        except PageVisit.DoesNotExist:
            page_visit = PageVisit(user=request.user, page_name=page_name)

        # Calculate the time spent on the page
        current_time = timezone.now()
        time_spent = current_time - request.session.get('page_visited_at', current_time)
        page_visit.time_spent_seconds += time_spent.seconds

        # Save the page visit record
        page_visit.save()

        # Update the session variable to record the time the user left the page
        request.session['page_visited_at'] = current_time

    return render(request, 'sensei_base.html')

@csrf_exempt
@login_required
def save_time_spent(request):
    if request.method == "POST" and request.is_ajax():
        page_id = request.POST.get('page_id')
        time_spent = request.POST.get('time_spent')
        user = request.user
        page_visit = get_object_or_404(UserPageVisit, user=user, page_id=page_id)
        page_visit.time_spent += int(time_spent)
        page_visit.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
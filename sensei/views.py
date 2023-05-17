from django.shortcuts import render,redirect
import openai, os
from dotenv import load_dotenv
from django.utils import timezone
from .models import PageVisit
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import UserPageVisit
import json
from django.http import JsonResponse

load_dotenv()
# Create your views here.

api_key = os.getenv("OPENAI_KEY",None)
openai.api_key = api_key



def syllabus(actual_string):
    substring = actual_string

    topic_for_gpt= []
    topic_names = []


    x = substring.split('subtopic_name_start')
    for i in x:
        topic_for_gpt.append(i)
    course_size = len(topic_for_gpt)
    k = ''
    for i in range(1,course_size):
        if '''\\n''' in topic_for_gpt[i]:
            k = '\\n' 
        else:
            k = '''\n'''
    for i in range(1,course_size):
        title = topic_for_gpt[i][0:x[i].index(k)]
        topic_names.append(title)


    syllabus = {'title':topic_names,'to_gpt': topic_for_gpt}
    
    # print(syllabus)

    return syllabus


def course_generator(prompt):
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "user", "content": f"I want to learn everything about {prompt}, break down this topic into multiple subtopics, and generate a syllabus for me. I have an engineering background, so I can understand advanced concepts so include tem in the syllabus.don't use any other words other than the syllabus necessary,"}
                     ],
            temperature = 0.2
)
        #  wrap the syllabus in start_syllabus and end_syllabus tag. give result as a string

    string_this = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content": f"context is {response},now make it a string like 'subtopic_name_start1. Introduction to Data Science\\n- Definition of Data Science\\n- Importance of Data Science\\n- Applications of Data Science\\nsubtopic_name_start2. Mathematics for Data Science\\n- Linear Algebra\\n- Calculus\\n- Probability and Statistics\\nsubtopic_name_start3. Programming for Data Science\\n- Python Programming\\n- R Programming\\n- SQL\\nsubtopic_name_start4. Data Preparation\\n- Data Cleaning\\n- Data Transformation\\n- Data Integration\\nsubtopic_name_start5. Data Exploration and Visualization\\n- Exploratory Data Analysis\\n- Data Visualization Techniques\\n- Data Storytelling\\nsubtopic_name_start6. Machine Learning\\n- Supervised Learning\\n- Unsupervised Learning\\n- Reinforcement Learning\\nsubtopic_name_start7. Deep Learning\\n- Neural Networks\\n- Convolutional Neural Networks\\n- Recurrent Neural Networks\\nsubtopic_name_start8. Big Data\\n- Hadoop\\n- Spark\\n- NoSQL Databases\\nsubtopic_name_start9. Data Ethics and Privacy\\n- Ethical Considerations in Data Science\\n- Privacy Concerns in Data Science\\n- Legal and Regulatory Frameworks\\nsubtopic_name_start10. Capstone Project\\n- Applying Data Science Techniques to a Real-world Problem\\n- Project Planning and Execution\\n- Presentation and Communication Skills'"}
                     ],
            temperature = 0.1

        )
    chatbot_response = response['choices'][0]['message']['content']
    actual_string = string_this['choices'][0]['message']['content']
    
    portion = syllabus(actual_string)
    # print(portion)
    return portion





def sensei(request):
    sensei_response = None
    portion = None
    title_list = None
    prompt = None
   
    # if request.POST['action'] == 'understood':
    #     print("the user has understood")
    

    if api_key is not None and request.POST.get('form_type') == 'prompt_from_user':
        

        user_input = request.POST.get('user_input')
        prompt = user_input

        portion = course_generator(prompt)
        
        title_list = portion['title']
        gpt_list=portion['to_gpt']
        request.session['my_list'] = gpt_list
        request.session['topic_list'] = title_list
        
        
        
    if request.POST.get('form_type') == 'Start Course':
        request.session['topic'] = 1
        
        
        return redirect('/sensei/classroom/',title_list)    

        
    return render(request,'sensei_controls.html',{'response': portion,'title_list': title_list, 'prompt': prompt})


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

def doubt(question, context):
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content": f"Context is {context}, and my doubt is {question}, please explain."}
                     ],
            temperature = 0.1

        )
    return response

def my_view(request):
    response = None
    solution = None
    context_for_doubt = None


    if request.POST.get('form_type') == 'test':
        print("working properly")
    

    if api_key is not None and request.POST.get('form_type') == 'next':
            # do something to get the next page or data
            # for example, fetch the next set of items from the database
            if request.user.is_authenticated:  # Ensure the user is authenticated
                request.user.curiosity -= 1
                request.user.save()
            topic = request.session['topic']
            my_list = request.session.get('my_list', None)
            topic_list = request.session.get('topic_list', None)
            topic_name = topic_list[topic - 1]
            
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content": f"teach me on the topic {my_list[topic]},whenever there is a line break use ---br---"}
                     ],
            temperature = 0.1

        )
            
            response = response['choices'][0]['message']['content']
            list = response.split('---br---')
            text = list
            line = ''

            for i in text:
                line += (f"^1000\\n`{i}`")
                
            print(line)
            answer = []
            for i in list:
                answer.append(i)
            
            topic += 1
            request.session['context_for_doubt'] = response
            if len(my_list)<topic:
                return redirect('sensei_completed.html')
            else:
                pass
            
            
            request.session['topic'] = topic
            return render(request, 'sensei_classroom.html', {'response': response,'topic_name':topic_name,'answer':answer,'line':line})
    

    if request.POST.get('form_type') == 'doubt':
        user_doubt = request.POST.get('user_doubt')
        context_for_doubt = request.session['context_for_doubt']
        
        solution = doubt(user_doubt,context_for_doubt)
        solution = solution['choices'][0]['message']['content']
    return render(request,'sensei_classroom.html',{'response':response,'solution':solution,'context_for_doubt':context_for_doubt})
  
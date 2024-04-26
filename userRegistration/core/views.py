from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
# from .lang import helper
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from django.shortcuts import render, redirect
from .models import JobApplication
from django.views.decorators.csrf import csrf_exempt

from .utils import get_db_chain , get_qa_eval_chain


def index(request):
    return render(request , 'bot.html')

def form(request):
    return render(request , 'form.html')

def speech(request):
    return render(request , 'speech.html')

def face(request):
    return render(request , 'facial.html')

def success_page(request):
    return render(request , 'success_page.html')

@csrf_exempt
def form_submit(request):
    if request.method == 'POST':
        
        # Extract form data from the POST request
        reviewed = request.POST.get('reviewed')
        resume = request.FILES.get('resume')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        # Convert date of birth string to a Python date object
        dob_str = request.POST.get('dob_str')
        date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None

        higher_degree = request.POST.get('degree')
        skills = request.POST.get('skills')
        # Convert years of experience string to an integer
        years_of_experience = int(request.POST.get('experience')) if request.POST.get('experience') else None
        current_ctc = int(request.POST.get('currentCTC')) if request.POST.get('currentCTC') else None
        expected_ctc = int(request.POST.get('expectedCTC')) if request.POST.get('expectedCTC') else None
        notice_period = int(request.POST.get('noticePeriod')) if request.POST.get('noticePeriod') else None

        questions_json = request.POST.get('questions')
        answers_json = request.POST.get('answers')
        questions = json.loads(questions_json)
        answers = json.loads(answers_json)

        print(reviewed,resume,full_name,email,phone_number,gender,date_of_birth,higher_degree,skills,years_of_experience,current_ctc,expected_ctc,notice_period)
        print("ques",questions)
        print("answers",answers)
        score_array = []
        for q_key, question in sorted(questions.items()):
            # Get the corresponding answer
            a_key = q_key.replace('question', 'answers')
            answer = answers.get(a_key, '')
            
            # Print the question and answer together
            result= get_qa_eval_chain(questions , answers)
            print("score---",result["score"])
            score_array.append(result["score"])

        array_sum = sum(score_array)

        # Calculate the average by dividing the sum by the number of elements
        avg_score = array_sum / len(score_array)
        print("avg_score",avg_score)
            # print(question, answer)
        # res = get_qa_eval_chain(questions , answers)
        # print("rrr",res)
        # # Create a new JobApplication object and save it to the database
        # print(res["score"])
        if avg_score >4:
            job_application = JobApplication(
                review_job_description=reviewed,
                resume=resume,
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                gender=gender,
                date_of_birth=date_of_birth,
                higher_degree=higher_degree,
                skills=skills,
                years_of_experience=years_of_experience,
                current_ctc=current_ctc,
                expected_ctc=expected_ctc,
                np=notice_period,
                counter=1,  # Assuming you want to start the counter at 0
                status='Accepted'
            )
            job_application.save()
        else:
            job_application = JobApplication(
                review_job_description=reviewed,
                resume=resume,
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                gender=gender,
                date_of_birth=date_of_birth,
                higher_degree=higher_degree,
                skills=skills,
                years_of_experience=years_of_experience,
                current_ctc=current_ctc,
                expected_ctc=expected_ctc,
                np=notice_period,
                counter=1,  # Assuming you want to start the counter at 0
                status='Rejected'
            )
            job_application.save()

        return JsonResponse({'success': True})

    # Return an error response if the request method is not POST
    return JsonResponse({'success': False, 'error': 'Method not allowed'})





@csrf_exempt
def process_step1(request):
    if request.method == 'POST':
        # Retrieve data from the AJAX request
        job_description = request.POST.get('job_description')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        print(email)
        if JobApplication.objects.filter(email=email).exists():
            # Email exists in the database
            print("exist")
            data = {'exists': True}
            return JsonResponse({'success': True, 'exists': True})
       
        
    
        job_description_reviewed = request.POST.get('job_description_reviewed')
        resume_file = request.FILES.get('resume')
        # print(job_description)
        # Process the data as needed (e.g., save to the database)
        # For example, you can save the resume file to the media directory
        if resume_file:
            with open('media/' + resume_file.name, 'wb+') as destination:
                for chunk in resume_file.chunks():
                    destination.write(chunk)

        # Optionally, perform additional tasks with the data
        res=get_db_chain(job_description,'media/'+ resume_file.name)
        # print(res)

        # Return a JSON response to the frontend
        # return JsonResponse({'success': True, 'question': ["abc","cde","efg","ydd","chcg"],'exists': False})

        return JsonResponse({'success': True, 'question': res["questions"]})

    # If the request method is not POST, return an error response
    return JsonResponse({'success': False, 'message': 'Invalid request method'})





import csv
import json
import secrets
import string
import random
from django.http import HttpResponse
from django.core.serializers import serialize

from django.db import transaction

def generate_password():
    # Define character sets
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    special_chars = string.punctuation
    # Generate at least one character from each character set
    password = [
        random.choice(lowercase_letters),
        random.choice(uppercase_letters),
        random.choice(digits),
        random.choice(special_chars)
    ]
    # Fill the rest of the password with random characters
    password.extend(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(4))
    # Shuffle the password to ensure randomness
    random.shuffle(password)
    # Convert the list of characters to a string
    password_str = ''.join(password)
    return password_str

def fetch_data(request):
    # Fetch the first 10 sequential data entries
    sequential_data = JobApplication.objects.all()[:10]
    
    # Prepare CSV file content
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    # Write CSV data to the response
    writer = csv.writer(response)
    writer.writerow(['username', 'password', 'firstname', 'lastname', 'email','group1' , 'cohort1' , 'course1'])

    # Generate CSV data and delete entries
    with transaction.atomic():  # Ensure atomicity of database operations
        for entry in sequential_data:
            username = entry.email.split('@')[0] if '@' in entry.email else entry.email
            username = username.lower()
            password = generate_password()
            full_name = entry.full_name or ''
            full_name = full_name.lower()
            firstname, *lastname_parts = full_name.split(' ', 1) if ' ' in full_name else [full_name, '']
            lastname = ' '.join(lastname_parts)
            lastname = lastname.lower()
            email = entry.email.lower()
            group1 = "group"
            cohort1 = "cohort"
            course1 = "course"

            # Write CSV row
            writer.writerow([username, password, firstname, lastname, email , group1 , cohort1 , course1])

            # Delete entry from database
            # entry.delete()

    # Save JSON data to a file (optional)
    data_list = [{'full_name': entry.full_name, 'email': entry.email} for entry in sequential_data]
    json_data = json.dumps(data_list)
    with open('data.json', 'w') as f:
        f.write(json_data)

    return response
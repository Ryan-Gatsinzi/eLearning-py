from collections import UserList
from hashlib import new
from optparse import Values
from re import S
from sys import exc_info
from tokenize import Number
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from login_register.models import users, Class, chat, enroll_teachers, progress, subjects, topics, library, quiz, questions, results, attempt
from  datetime import datetime
import json
from django.core.files.base import ContentFile
import math
import time
from django.db.models import Q
def teacher(request):
    try:
        if request.session['is_loggedin'] == True:
            render(request, 'teacher_header.html', {'session': request.session['user_name']})                
            return render(request, 'teacher_dashboard.html', {'session': request.session['user_name']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def logout(request):
    del request.session['is_loggedin']
    return redirect('login')

def profile(request):
    User = users.objects.get(name = request.session['user_name'])
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        pwd = request.POST['pwd']

        if name == '' or email == '' or pwd == '':
            messages.info(request, "You can't leave fields empty")
            return redirect('/teacher_dashboard/profile')
        user = users.objects.get(id = request.session['user_id'])
        print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{user}')
        user.name = name
        user.email = email
        user.pwd = pwd
        request.session['user_name'] = name
        user.save()
        if request.POST.get('delete') == 'delete':
            user.status = 'deleted'
            user.save()
            messages.info(request, 'This account does not exist anymore')
            return redirect('login')
        return redirect('/teacher_dashboard/profile')
    render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
    return render(request, 'teacher_profile.html',{'session': request.session['user_name'], 'user':User})

def all_students(request):
    try:
        if request.session['is_loggedin'] == True:
            Users = users.objects.filter(role='student').values().exclude(status='deleted')
            render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
            return render(request, 'teacher_all-students.html', {'row': Users, 'session': request.session['user_name']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def all_subjects(request):
    try:
        if request.session['is_loggedin'] == True:
            subject = subjects.objects.filter().values().exclude(status='deleted')
            cls = Class.objects.filter().values().exclude(status='deleted')
            Users = users.objects.filter(status = 'activated', role = 'teacher').values()
            #print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{subject}')
            render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
            return render(request, 'teacher_all-subjects.html', {'subjects': subject, 'class':cls, 'teachers':Users, 'session': request.session['user_name']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def all_classes(request):
    try:
        if request.session['is_loggedin'] == True:        
            cls = Class.objects.filter().values().exclude(status='deleted')
            Users = users.objects.filter(status = 'activated', role = 'teacher').values()         
            render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
            return render(request, 'teacher_all-classes.html', {'class':cls, 'users':Users, 'session': request.session['user_name']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')


def add_topic(request):
    try:
        #print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{datetime.hour}')
        if request.session['is_loggedin'] == True:        
            subject = subjects.objects.filter(status = 'activated', teacher = request.session['user_id']).values()      
            if request.method == 'POST':   
                try:            
                    name = request.POST['topicname']
                    file = request.FILES['assignment_file']
                    sbjt = request.POST.get('subject', False)
                    desc = request.POST['description']                
                    topic = topics.objects.create(name = name, description = desc, file = file, subject = sbjt, date_assigned = datetime.today(), teacher = request.session['user_id'], status = 'activated')
                    topic.save()
                    messages.success(request, 'Success')
                    render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
                    return render(request, 'teacher_all-topic.html', {'subjects':subject, 'session': request.session['user_name']})
                except:
                    messages.info(request, 'You can not leave fields empty')
                    return redirect('/teacher_dashboard/teacher_add-topic/')
                
            render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
            return render(request, 'teacher_add-topic.html', {'subjects':subject, 'session': request.session['user_name']})

        
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def all_topics(request):
    try:
        print(datetime.today())    
        if request.session['is_loggedin'] == True:        
            cls = Class.objects.filter().values().exclude(status='deleted')
            subject = subjects.objects.filter(teacher = request.session['user_id'], status = 'activated').values()
            topic = topics.objects.filter().values().exclude(status='deleted')
            render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
            return render(request, 'teacher_all-topics.html', {'class':cls, 'subjects':subject, 'topics':topic, 'session': request.session['user_name'], 'id': request.session['user_id']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def go_to_edit(request, ids, action):    
    try:           
        if request.session['is_loggedin'] == True:
            if action == 'topic':               
                topic = topics.objects.get(id=ids)
                subject = subjects.objects.filter(status = 'activated', teacher = request.session['user_id']).values()         
                render(request, 'admin_nav.html', {'session': request.session['user_name']})
                redirect('/admin_dashboard/')                       
                return render(request, 'edit-topic.html', {'topic':topic, 'subjects':subject}) 
            elif action == 'quiz':               
                quizes = quiz.objects.get(id=ids)            
                render(request, 'admin_nav.html', {'session': request.session['user_name']})
                redirect('/admin_dashboard/')                       
                return render(request, 'edit-quiz.html', {'quiz':quizes}) 
            elif action == 'question':
                Quizes = quiz.objects.filter(status = 'activated', teacher_id = request.session['user_id']).values()          
                qn = questions.objects.get(id=ids)            
                render(request, 'admin_nav.html', {'session': request.session['user_name']})
                redirect('/admin_dashboard/')                       
                return render(request, 'edit-question.html', {'qn':qn, 'quizes':Quizes})     
            render(request, 'teacher_header.html', {'session': request.session['user_name']})
            return redirect('/teacher_dashboard/')                                   
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def edit_topic(request, id):    
    try:               
        if request.session['is_loggedin'] == True:
            if request.method == 'POST':                
                name = request.POST['topicname']                
                sbjt = request.POST.get('subject', False)
                desc = request.POST['description']                          
                topic = topics.objects.get(id=id)

                if name == '' or sbjt == 0 or desc == '':
                    messages.info(request, 'You can not leave fields empty')
                    return redirect('/teacher_dashboard/teacher_all-topics/')
                topic.name = name
                topic.subject = sbjt
                topic.description = desc
                topic.save() 
                render(request, 'teacher_header.html', {'session': request.session['user_name']})
                return redirect('/teacher_dashboard/teacher_all-topics/')                  
                                                       
            render(request, 'teacher_header.html', {'session': request.session['user_name']})
            return redirect('/teacher_dashboard/teacher_all-topics/')

    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')  

def deactivate_topic(request, topic_id):
    try:               
        if request.session['is_loggedin'] == True:
            if request.method == 'GET':
                topic = topics.objects.get(id=topic_id)
                topic.status = 'deactivated'
                topic.save()
                render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
                return redirect('/teacher_dashboard/teacher_all-topics/')                        
            return redirect('/teacher_dashboard/teacher_all-topics/')    
    except:
            messages.info(request, 'You need to log in first')
            return redirect('login')




def activate_topic(request, topic_id):
    try:               
        if request.session['is_loggedin'] == True:
            if request.method == 'GET':
                topic = topics.objects.get(id=topic_id)
                topic.status = 'activated'
                topic.save()
                render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
                return redirect('/teacher_dashboard/teacher_all-topics/')                        
            return redirect('/teacher_dashboard/teacher_all-topics/')    
    except:
            messages.info(request, 'You need to log in first')
            return redirect('login')


def Delete_topic(request, topic_id):
    try:               
        if request.session['is_loggedin'] == True:
            if request.method == 'GET':
                topic = topics.objects.get(id=topic_id)
                topic.status = 'deleted'
                topic.save()
                render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
                return redirect('/teacher_dashboard/teacher_all-topics/')                        
            return redirect('/teacher_dashboard/teacher_all-topics/')    
    except:
            messages.info(request, 'You need to log in first')
            return redirect('login')

def add_book(request):
    try:
        #print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{datetime.hour}')
        if request.session['is_loggedin'] == True:        
            subject = subjects.objects.filter(status = 'activated', teacher = request.session['user_id']).values()      
            if request.method == 'POST':   
                try:            
                    bookname = request.POST['bookname']
                    file = request.FILES['book_file']
                    bookgenre = request.POST['bookgenre']                                
                    book = library.objects.create(publisher_name = request.session['user_id'], book_name = bookname, genre = bookgenre, file = file)
                    book.save()
                    messages.success(request, 'Success')
                    render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
                    return render(request, 'teacher_add-book.html', {'session': request.session['user_name']})
                except:
                    messages.info(request, 'You can not leave fields empty')
                    return redirect('/teacher_dashboard/teacher_add-book/')
                
            render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
            return render(request, 'teacher_add-book.html', {'session': request.session['user_name']})        
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def all_books(request):
    try:
        if request.session['is_loggedin'] == True:        
            books = library.objects.filter().values().exclude(status='deleted')
            user = users.objects.filter(status = 'activated').values()            
            render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
            return render(request, 'teacher_library.html', {'books':books, 'users':user, 'session': request.session['user_name'], 'id': request.session['user_id']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def Delete_book(request, book_id):
    try:               
        if request.session['is_loggedin'] == True:
            if request.method == 'GET':
                book = library.objects.get(id=book_id)
                book.status = 'deleted'
                book.save()
                render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
                return redirect('/teacher_dashboard/teacher_library/')                        
            return redirect('/teacher_dashboard/teacher_library/')    
    except:
            messages.info(request, 'You need to log in first')
            return redirect('login')

def add_quiz(request):
    try:
        #print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{datetime.hour}')
        if request.session['is_loggedin'] == True:        
            subject = subjects.objects.filter(status = 'activated', teacher = request.session['user_id']).values()      
            if request.method == 'POST':   
                try:            
                    quizname = request.POST['quizname']
                    exam_time = request.POST['time']                                      
                    quizes = quiz.objects.create(quiz_name = quizname, exam_time = exam_time, teacher_id = request.session['user_id'])
                    quizes.save()
                    messages.success(request, 'Success')
                    render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
                    return render(request, 'teacher_add_quiz.html', {'session': request.session['user_name']})
                except:
                    messages.info(request, 'You can not leave fields empty')
                    return redirect('/teacher_dashboard/teacher_add_quiz/')
                
            render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
            return render(request, 'teacher_add_quiz.html', {'session': request.session['user_name']})        
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def add_question(request):
    # try:
        #print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{datetime.hour}')
        if request.session['is_loggedin'] == True:        
            quizes = quiz.objects.filter(status = 'activated', teacher_id = request.session['user_id']).values()   
            quizes.count()   
            if request.method == 'POST':   
                # try:            
                    quizname = request.POST.get('quizname', False)
                    qn= request.POST['questionname']
                    op1= request.POST['op1']     
                    op2= request.POST['op2']     
                    op3= request.POST['op3']     
                    op4= request.POST['op4']     
                    answer = request.POST.get('answer', False)

                    if answer == 0 or quizname == 0:
                        messages.info(request, 'You can not leave fields empty')
                        return redirect('/teacher_dashboard/teacher_add_question/')
                
                    if answer == 'Option1':
                        ans = op1
                    elif answer == 'Option2':
                        ans = op2
                    elif answer == 'Option3':
                        ans = op3
                    elif answer == 'Option4':
                        ans = op4

                    loop = 0
                    entities = questions.objects.filter(status = 'activated', teacher_id = request.session['user_id'], quiz_id = quizname).values()                                        
                    num_rows = entities.count()
                    print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{num_rows}')
                    if num_rows == 0:
                        question = questions.objects.create(question_no = 1, question = qn, opt1 = op1, opt2 = op2, opt3 = op3, opt4 = op4, answer = ans, quiz_id = quizname, teacher_id = request.session['user_id'])       
                        question.save()
                        messages.success(request, 'Success')
                        render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
                        return render(request, 'teacher_add_question.html', {'session': request.session['user_name']})
                    else:
                        loop = 1 + num_rows  
                        question = questions.objects.create(question_no = loop, question = qn, opt1 = op1, opt2 = op2, opt3 = op3, opt4 = op4, answer = ans, quiz_id = quizname, teacher_id = request.session['user_id'])       
                        question.save()
                        messages.success(request, 'Success')
                        render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
                        return render(request, 'teacher_add_question.html', {'session': request.session['user_name']})
                                            
                # except:
                #     messages.info(request, 'You can not leave fields empty')
                #     return redirect('/teacher_dashboard/teacher_add_question/')
                
            render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
            return render(request, 'teacher_add_question.html', {'quizes':quizes, 'session': request.session['user_name']})        
    # except:
    #     messages.info(request, 'You need to log in first')
    #     return redirect('login')

def all_quizes(request):
    try:   
        if request.session['is_loggedin'] == True:        
            quizes = quiz.objects.filter(teacher_id = request.session['user_id']).values().exclude(status='deleted')            
            render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
            return render(request, 'teacher_all-quizes.html', {'quizes':quizes, 'session': request.session['user_name'], 'id': request.session['user_id']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def deactivate_quiz(request, quiz_id):
    try:               
        if request.session['is_loggedin'] == True:
            if request.method == 'GET':
                quizes = quiz.objects.get(id=quiz_id)
                quizes.status = 'deactivated'
                quizes.save()
                render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
                return redirect('/teacher_dashboard/teacher_all-quizes/')                        
            return redirect('/teacher_dashboard/teacher_all-quizes/')    
    except:
            messages.info(request, 'You need to log in first')
            return redirect('login')




def activate_quiz(request, quiz_id):
    try:               
        if request.session['is_loggedin'] == True:
            if request.method == 'GET':
                quizes = quiz.objects.get(id=quiz_id)
                quizes.status = 'activated'
                quizes.save()
                render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
                return redirect('/teacher_dashboard/teacher_all-quizes/')                        
            return redirect('/teacher_dashboard/teacher_all-quizes/')    
    except:
            messages.info(request, 'You need to log in first')
            return redirect('login')


def Delete_quiz(request, quiz_id):
    try:               
        if request.session['is_loggedin'] == True:
            if request.method == 'GET':
                quizes = quiz.objects.get(id=quiz_id)
                quizes.status = 'deleted'
                quizes.save()
                render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
                return redirect('/teacher_dashboard/teacher_all-quizes/')                        
            return redirect('/teacher_dashboard/teacher_all-quizes/')    
    except:
            messages.info(request, 'You need to log in first')
            return redirect('login')

def edit_quiz(request, id):    
    try:               
        if request.session['is_loggedin'] == True:
            if request.method == 'POST':                
                quizname = request.POST['quizname']
                exam_time = request.POST['time']                          
                quizes = quiz.objects.get(id=id)

                if quizname == '' or exam_time == '':
                    messages.info(request, 'You can not leave fields empty')
                    return redirect('/teacher_dashboard/teacher_all-quizes/')
                quizes.quiz_name = quizname
                quizes.exam_time = exam_time
                quizes.save() 
                render(request, 'teacher_header.html', {'session': request.session['user_name']})
                return redirect('/teacher_dashboard/teacher_all-quizes/')                  
                                                       
            render(request, 'teacher_header.html', {'session': request.session['user_name']})
            return redirect('/teacher_dashboard/teacher_all-quizes/')

    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def all_questions(request, id):
    try:   
        if request.session['is_loggedin'] == True:        
            question = questions.objects.filter(teacher_id = request.session['user_id'], quiz_id = id).values().exclude(status='deleted')            
            render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
            return render(request, 'teacher_all-questions.html', {'questions':question, 'session': request.session['user_name'], 'id': request.session['user_id']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')
    
def Delete_question(request, id):
    try:               
        if request.session['is_loggedin'] == True:
            if request.method == 'GET':
                qn = questions.objects.get(id=id)               
                qn.status = 'deleted'                
                qn.save()                   
                render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
                return redirect('/teacher_dashboard/all_questions/')                        
            return redirect('/teacher_dashboard/all_questions/')    
    except:
            messages.info(request, 'You need to log in first')
            return redirect('login')

def edit_question(request, id):    
    try:               
        if request.session['is_loggedin'] == True:
            if request.method == 'POST':                
                quizname = request.POST.get('quizname', False)
                qn= request.POST['questionname']
                op1= request.POST['op1']     
                op2= request.POST['op2']     
                op3= request.POST['op3']     
                op4= request.POST['op4']     
                answer = request.POST.get('answer', False)
                question = questions.objects.get(id = id)
                qz = quiz.objects.get(id = question.quiz_id)
                if answer == 0 or quizname == 0:
                    messages.info(request, 'You can not leave fields empty')
                    return redirect(f'/teacher_dashboard/all_questions/{qz.id}/')
            
                if answer == 'Option1':
                    ans = op1
                elif answer == 'Option2':
                    ans = op2
                elif answer == 'Option3':
                    ans = op3
                elif answer == 'Option4':
                    ans = op4
                
                question.question = qn
                question.quiz_id = quizname
                question.opt1 = op1
                question.opt2 = op2
                question.opt3 = op3
                question.opt4 = op4
                question.answer = ans
                question.save() 
                render(request, 'teacher_header.html', {'session': request.session['user_name']})
                return redirect(f'/teacher_dashboard/all_questions/{qz.id}/')                  
                                                       
            render(request, 'teacher_header.html', {'session': request.session['user_name']})
            return redirect(f'/teacher_dashboard/all_questions/{qz.id}/')

    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def Quiz(request):
    try: 
        if request.session['is_loggedin'] == True:
            quizes = quiz.objects.filter(status = 'activated', teacher_id = request.session['user_id']).values()
            qn = questions.objects.filter(status = 'activated', teacher_id = request.session['user_id']).values()
            arr = []
            for qz in quizes:
                for qns in qn:
                    if qz['id'] == qns['quiz_id'] and qz not in arr:
                        arr.append(qz)            
            render(request, 'teacher_header.html', {'session': request.session['user_name']})                
            return render(request, 'teacher_quiz.html', {'quizes':arr, 'session': request.session['user_name']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def load_total(request):
    try: 
        if request.session['is_loggedin'] == True: 
            quizes = quiz.objects.filter(status = 'activated', teacher_id = request.session['user_id']).values() 
            qns = questions.objects.filter(status = 'activated', teacher_id = request.session['user_id']).values()  
            if request.method == 'POST':     
                qz = request.POST['quiz']
                qn = questions.objects.filter(status = 'activated', teacher_id = request.session['user_id'], quiz_id = qz).values()

                render(request, 'teacher_header.html', {'session': request.session['user_name']})                
                return HttpResponse(qn.count())
            render(request, 'teacher_header.html', {'session': request.session['user_name']})
            return render(request, 'teacher_quiz.html', {'question':qns, 'quizes':quizes, 'session': request.session['user_name']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def take_quiz(request, qn_total, quiz_id):
    try: 
        if request.session['is_loggedin'] == True:               
            qn = questions.objects.filter(status = 'activated', teacher_id = request.session['user_id'], quiz_id = quiz_id).values().order_by('id')
            check_att = attempt.objects.filter(quiz_id = quiz_id, user_id = request.session['user_id']).exists()
            if check_att != True:
                att = attempt.objects.create(quiz_id = quiz_id, user_id = request.session['user_id'])
                att.save()
            render(request, 'teacher_header.html', {'session': request.session['user_name']})                            
            return render(request, 'teacher_take_quiz.html', {'quiz_id':quiz_id, 'total':qn_total, 'questions':qn, 'session': request.session['user_name']})           
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def quiz_results(request):    
    try:               
        if request.session['is_loggedin'] == True:
            if request.method == 'POST':  
                res = request.POST.getlist('arr[]') 
                quiz_id = request.POST['quiz_id']  
                q = questions.objects.filter(quiz_id=quiz_id).values()
                qz = quiz.objects.get(id=quiz_id)                           

                correct = 0
                wrong = 0
                percentage = 0
                for i in res: 
                    j = [n for n in i]
                    j.remove(j[1])
                    b = [k for k in j]                                           
                    qn = questions.objects.get(id=b[1])                         
                    if b[0] == qn.answer:
                        correct += 1
                    else:
                        wrong+=1                                        
                percentage = (correct*100)/(correct + wrong)                
                render(request, 'teacher_header.html', {'session': request.session['user_name']})
                check_results = results.objects.filter(quiz_id = int(quiz_id), user_id = request.session['user_id'], teacher_id = qz.teacher_id, status = 'activated').exists()
                if check_results != True:
                    result = results.objects.create(quiz_id = int(quiz_id), correct_answer = correct, wrong_answer = wrong, total_question = q.count(), time = datetime.now().date(), role = request.session['user_role'], user_id = request.session['user_id'], teacher_id = qz.teacher_id, status = 'activated', percentage = round(percentage))
                    result.save()              
                return HttpResponse(f"""
                <strong style='font-size: 25px;'>
                Correct: {correct}<br>
                Wrong: {wrong}<br>                
                Percentage: {percentage} % <br>             
                </span>
            </strong>
                 """)                                                               
            render(request, 'teacher_header.html', {'session': request.session['user_name']})
            return render(request, 'teacher_results.html', {'session': request.session['user_name']})

    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def result(request):    
    try:               
        if request.session['is_loggedin'] == True:                          
            render(request, 'teacher_header.html', {'session': request.session['user_name']})
            return render(request, 'teacher_results.html', {'session': request.session['user_name']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')
    
def load_timer(request):
    try: 
        if request.session['is_loggedin'] == True: 
            quizes = quiz.objects.filter(status = 'activated', teacher_id = request.session['user_id']).values() 
            qns = questions.objects.filter(status = 'activated', teacher_id = request.session['user_id']).values()  
            if request.method == 'POST':     
                qz = request.POST['quiz']
                q = quiz.objects.get(status = 'activated', teacher_id = request.session['user_id'], id = qz)
                time_arr = []
                q_time = q.exam_time
                h = 0
                m = q_time
                s = 0                             

                if q_time >= 60:
                    h+=1 
                    if type(m) == float:
                        w = str(math.floor(q_time))                
                        z = str(m).replace(w,'0')
                        m = int(float(z)*60)
                    else:
                        m = 0                            
                if type(q_time) == float:
                    x = str(math.floor(q_time))                
                    y = str(q_time).replace(x,'0')
                    s += int(float(y)*60)
                
                T = "%02d:%02d:%02d" % (h, m, s)   
                Time = datetime.strptime(T, "%H:%M:%S").time() 
                t = (Time.minute)*60                

                while t:
                    hours = t//3600
                    mins = t//60
                    secs = t % 60
                    timer = "{:02d}:{:02d}:{:02d}".format(hours,mins,secs)
                    print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>{timer}", end='\r')                                    
                    t -= 1
                    time_arr.append(timer)
                render(request, 'teacher_header.html', {'session': request.session['user_name']})
                print(len(json.dumps(time_arr)))                
                return HttpResponse(json.dumps(time_arr))                
            render(request, 'teacher_header.html', {'session': request.session['user_name']})
            return render(request, 'teacher_quiz.html', {'question':qns, 'quizes':quizes, 'session': request.session['user_name']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def student_results(request):
    try:
        if request.session['is_loggedin'] == True:
            Users = users.objects.filter(status = 'activated').values()
            qz = quiz.objects.filter(status = 'activated').values()
            qn = questions.objects.filter(status = 'activated').values()
            res = results.objects.filter(status = 'activated').values()
            render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
            return render(request, 'teacher_all-results.html', {'results':res, 'users': Users, 'quizes':qz, 'question':qn, 'session': request.session['user_name']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def latest_results(request):
    try:
        if request.session['is_loggedin'] == True:            
            qz = quiz.objects.filter(status = 'activated').values()
            qn = questions.objects.filter(status = 'activated').values()
            res = results.objects.filter(status = 'activated').values()
            render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
            return render(request, 'teacher_latest-results.html', {'quizes':qz, 'question':qn, 'results':res, 'id': request.session['user_id'], 'session': request.session['user_name']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def people(request):
    try:
        if request.session['is_loggedin'] == True:
            ppl = users.objects.filter(status = 'activated').exclude(role = 'admin', id = request.session['user_id']).values()           
            render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
            return render(request, 'teacher_people.html', {'users':ppl, 'id': request.session['user_id'], 'session': request.session['user_name']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def teacher_livesearch(request):
    try:
        if request.session['is_loggedin'] == True:            
            name = request.POST['target']          
            person = users.objects.filter(status = 'activated', name__contains = name).values().exclude(name__contains = request.session['user_name'])               
            for user in person:
                if user['id'] != request.session['user_id'] and user['role'] != 'admin':
                    user_id = user['id']  
                    render(request, 'teacher_chat.html', {'session': request.session['user_name'], 'id':user_id})     
                    return HttpResponse(f"<h4><a href='/teacher_dashboard/teacher_chat/{user_id}/'style='color:black;'>{user['name']}</a></h4>")
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def teacher_chat(request, user_id):
    try:
        if request.session['is_loggedin'] == True:          
            person = users.objects.get(id = user_id)
            render(request, 'teacher_header.html', {'session': request.session['user_name'], 'id':user_id})     
            return render(request, 'teacher_chat.html', {'person':person, 'session': request.session['user_name']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def send_msg(request):
    try:
        if request.session['is_loggedin'] == True:          
            msg = request.POST['message']
            user_id = request.POST['id']
            sendmsg = chat.objects.create(messenger = request.session['user_id'], recipient = int(user_id), msg = msg, time = datetime.now())
            sendmsg.save()
            return render(request, 'teacher_header.html', {'session': request.session['user_name'], 'id':user_id})                 
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def display_msg(request):
    try:
        if request.session['is_loggedin'] == True:                      
            user_id = request.POST['user_id']            
            msgs = chat.objects.filter(Q(messenger = request.session['user_id'], recipient = int(user_id), status = 'activated') | Q(messenger = int(user_id), recipient = request.session['user_id'], status = 'activated')).values()            
            msg_arr = []
            for msg in msgs:
                if msg['messenger'] == request.session['user_id']:
                    #HttpResponse(f"""<div style='text-align:right;'><p style='background-color:cyan; color:black; word-warp:breack-word; display:inline-block; padding:5px; border-radius:10px; max width:70%; cursor: pointer;' id='{msg['id']}' title = 'delete' onclick = 'delete_msg(this.id);'>{msg['msg']}</p><span style='color:grey;font-size:10px;'>{msg['time']}</span></div>""")
                    Message = f"""
                    <div style='text-align:right;'>
                        <p class='rightMsg' style='color:white;word-warp:breack-word; display:inline-block; padding:5px; border-radius:10px; max width:70%; cursor: pointer;' id='{msg['id']}' title = 'delete' onclick = 'delete_msg(this.id);'>{msg['msg']}
                        </p>
                        <span style='color:grey;font-size:10px;'>{msg['time']}</span>
                    </div>
                    """
                    msg_arr.append(Message)
                else:
                    print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{msg["messenger"]}')
                    Message = f"""<div style='text-align:left;'><p class='leftMsg' style='color:white;word-warp:breack-word; display:inline-block; padding:5px; border-radius:10px; max width:70%; cursor: pointer;' id='{msg['id']}'>{msg['msg']}</p><span style='color:grey;font-size:10px;'>{msg['time']}</span></div>"""
                    msg_arr.append(Message) 
            # msgs_arr = [i.replace('\n','') for i in msg_arr ]   
            return JsonResponse({"messages":msg_arr}) 
            #return HttpResponse(json.dumps(msg_arr)) 
                    
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')
    
def delete_msg(request):
    try:
        if request.session['is_loggedin'] == True:                      
            user_id = request.POST['id']           
            deletemsg = chat.objects.get(id = int(user_id))
            deletemsg.status = 'deleted'
            deletemsg.save()
            return render(request, 'teacher_header.html', {'session': request.session['user_name'], 'id':user_id})                 
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')
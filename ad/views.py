from collections import UserList
from hashlib import new
from optparse import Values
from re import S
from sys import exc_info
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from login_register.models import users, Class, enroll_students, enroll_teachers, progress, subjects, profile, quiz, questions, results, attempt
from  datetime import datetime
import json


# from django.core.serializers.json import DjangoJSONEncoder

def admin(request):
    try:
        if request.session['is_loggedin'] == True:
            render(request, 'admin_nav.html', {'session': request.session['user_name']})                
            return render(request, 'admin_dashboard.html', {'session': request.session['user_name']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')

def logout(request):
    del request.session['is_loggedin']
    return redirect('login')

def add_student(request):
    try:
        if request.session['is_loggedin'] == True:
            if request.method == 'POST':            
                email = request.POST['email']
                name = request.POST['name']
                role = 'student'
                status = 'activated'
                pwd = request.POST['password']

                if email =='' or pwd == '' or name == '':
                    messages.info(request, 'You can not leave fields empty')
                    return redirect('/admin_dashboard/admin_add-student')

                if users.objects.filter(name = name).exists():
                    messages.info(request, 'Username exists')
                    return redirect('/admin_dashboard/admin_add-student')    

                elif users.objects.filter(email = email).exists():
                    messages.info(request, 'Email exists') 
                    return redirect('/admin_dashboard/admin_add-student')

                Users= users.objects.create(name=name, email=email, role = role, password=pwd, status = status)
                Users.save()
                messages.info(request, 'Success') 
                redirect('/admin_dashboard/admin_add-student')

               
            render(request, 'admin_nav.html', {'session': request.session['user_name']})                
            return render(request, 'admin_add-student.html', {'session': request.session['user_name']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')


def add_teacher(request):

    try:
        if request.session['is_loggedin'] == True:
            if request.method == 'POST':            
                email = request.POST['email']
                name = request.POST['name']
                role = 'teacher'
                pwd = request.POST['password']
                if email =='' or pwd == '' or name == '':
                    messages.info(request, 'You can not leave fields empty')
                    return redirect('/admin_dashboard/admin_add-teacher')

                if users.objects.filter(name = name).exists():
                    messages.info(request, 'Username exists')
                    return redirect('/admin_dashboard/admin_add-teacher')    

                elif users.objects.filter(email = email).exists():
                    messages.info(request, 'Email exists') 
                    return redirect('/admin_dashboard/admin_add-teacher')

                Users= users.objects.create(name=name, email=email, role = role, password=pwd, status = 'activated')
                Users.save()
                messages.info(request, 'Success') 
                redirect('/admin_dashboard/admin_add-teacher')

               
            render(request, 'admin_nav.html', {'session': request.session['user_name']})                
            return render(request, 'admin_add-professor.html', {'session': request.session['user_name']})
    except:
        messages.info(request, 'You need to log in first')
        return redirect('login')        



def all_students(request):
    if request.session['is_loggedin'] == True:
        Users = users.objects.filter(role='student').values().exclude(status='deleted')
        render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
        return render(request, 'admin_all-students.html', {'row': Users,
                                                            'session': request.session['user_name']})


def all_teachers(request):

    if request.session['is_loggedin'] == True:
        Users = users.objects.filter(role='teacher').values().exclude(status='deleted')
        render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
        return render(request, 'admin_all-professors.html', {'row': Users,
                                                            'session': request.session['user_name']})

def deactivate_student(request, user_id):

    if request.method == 'GET':
        Users = users.objects.get(id=user_id)
        Users.status = 'deactivated'
        Users.save()
        render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
        return redirect('/admin_dashboard/admin_all-students')                        
    return redirect('/admin_dashboard/admin_all-students')                                                    




def activate_student(request, user_id):

    if request.method == 'GET':
        Users = users.objects.get(id=user_id)
        Users.status = 'activated'
        Users.save()
        render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
        return redirect('/admin_dashboard/admin_all-students')                        
    return redirect('/admin_dashboard/admin_all-students')    



def Delete_student(request, user_id):

    if request.method == 'GET':
        Users = users.objects.get(id=user_id)
        Users.status = 'deleted'
        Users.save()
        render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
        return redirect('/admin_dashboard/admin_all-students')                        
    return redirect('/admin_dashboard/admin_all-students')
    

def progress_of_students(request, user_id):

    if request.method == 'GET':
        Users = users.objects.get(id=user_id)
        try:
            prg = progress.objects.filter(user_id = user_id).values()
            render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
            return render(request, 'progress.html', {'session': request.session['user_name'], 'users':Users, 'progress':prg})
        except:
            messages.info(request, 'No progress by this student yet')
            return redirect('/admin_dashboard/admin_all-students')
    return redirect('/admin_dashboard/admin_all-students')


def deactivate_teacher(request, user_id):

    if request.method == 'GET':
        Users = users.objects.get(id=user_id)
        Users.status = 'deactivated'
        Users.save()
        render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
        return redirect('/admin_dashboard/admin_all-teachers')                        
    return redirect('/admin_dashboard/admin_all-teachers')                                                    




def activate_teacher(request, user_id):

    if request.method == 'GET':
        Users = users.objects.get(id=user_id)
        Users.status = 'activated'
        Users.save()
        render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
        return redirect('/admin_dashboard/admin_all-teachers')                        
    return redirect('/admin_dashboard/admin_all-teachers')    



def Delete_teacher(request, user_id):

    if request.method == 'GET':
        Users = users.objects.get(id=user_id)
        Users.status = 'deleted'
        Users.save()
        render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
        return redirect('/admin_dashboard/admin_all-teachers')                        
    return redirect('/admin_dashboard/admin_all-teachers')

def go_to_edit(request, ids, action):    

    if action == 'class':               
        cls = Class.objects.get(id=ids)
        user = users.objects.filter(role='teacher').values().exclude(status = 'deleted')
        render(request, 'admin_nav.html', {'session': request.session['user_name']})
        redirect('/admin_dashboard/')                       
        return render(request, 'edit-class.html', {'user':user, 'cls':cls})
    elif action == 'subject':
        subject = subjects.objects.get(id=ids)
        cls = Class.objects.filter(status = 'activated').values()
        user = users.objects.filter(role='teacher').values().exclude(status = 'deleted')
        render(request, 'admin_nav.html', {'session': request.session['user_name']})
        redirect('/admin_dashboard/')                       
        return render(request, 'edit-subject.html', {'user':user, 'classes':cls, 'subject':subject})        
    Users = users.objects.get(id=ids)
    render(request, 'admin_nav.html', {'session': request.session['user_name']})
    redirect('/admin_dashboard/')                       
    return render(request, 'edit-user.html', {'user':Users})
    

def edit_user(request, user_id):

    try:
        if request.method == 'POST':
            Users = users.objects.get(id=user_id)
            name = request.POST['name']
            email = request.POST['email']   

            if name == '' or email == '':
                messages.info(request, 'You can not leave fields empty')
                return redirect(f'/admin_dashboard/go_to_edit/{Users.id}/user')    
            Users.name = name
            Users.email = email
            Users.save()
            redirect('/admin_dashboard/')                       
            return render(request, 'edit-user.html', {'user':Users})
        else:
            return redirect('/admin_dashboard/') 
    except:
        return redirect('/admin_dashboard/') 

def edit_class(request, class_id):
    try:
        if request.method == 'POST':
            cls = Class.objects.get(id=class_id)        
            teacher_name = request.POST.get('teacher', False)            
            Users = users.objects.get(id=teacher_name)
            user = users.objects.filter(role='teacher').values().exclude(status = 'deleted')        
            class_name = request.POST['class_name']
            val = request.POST['class_value']   

            if teacher_name == '' or class_name == '' or val == '':
                messages.info(request, 'You can not leave fields empty')
                return redirect(f'/admin_dashboard/go_to_edit/{cls.id}/class')    
            cls.name_class = class_name
            cls.homeroom_tr = Users.id
            cls.class_val = val
            cls.save()
            redirect('/admin_dashboard/')                       
            return render(request, 'edit-class.html', {'cls':cls, 'user':user})
        else:
            return redirect('/admin_dashboard/') 
    except:
        return redirect(f'/admin_dashboard/go_to_edit/{cls.id}/class')

def admin_departments(request):    

    if request.session['is_loggedin'] == True:
        if request.method == 'POST':            
            class_val = request.POST['classval']
            name = request.POST['class']
            h_tr = request.POST.get('homeroom_tr', False)

            if class_val =='' or h_tr == '' or name == '':
                messages.info(request, 'You can not leave fields empty')
                return redirect('/admin_dashboard/admin_department')

            if Class.objects.filter(name_class = name).exists():
                messages.info(request, 'Class name exists') 
                return redirect('/admin_dashboard/admin_department')    

            cls = Class.objects.create(name_class=name, class_val=class_val, homeroom_tr = h_tr , status = 'activated')
            cls.save()
            Cls = Class.objects.get(homeroom_tr=h_tr)
            en = enroll_teachers.objects.create(teacher_id = h_tr, class_id=Cls.id, status = 'activated')
            en.save()
            rows = Class.objects.all().values().exclude(status = 'deleted')
            messages.info(request, 'Success') 
            render(request, 'admin_nav.html', {'session': request.session['user_name']})                
            return render(request, 'admin_department.html', {'session': request.session['user_name'], 'rows':rows})
                
        rows = Class.objects.all().values().exclude(status = 'deleted')
        user = users.objects.filter(role='teacher').values().exclude(status = 'deleted')            
        render(request, 'admin_nav.html', {'session': request.session['user_name']})                
        return render(request, 'admin_department.html', {'session': request.session['user_name'], 'users':user, 'rows':rows})
        


def deactivate_class(request, class_id):

    if request.method == 'GET':
        cls = Class.objects.get(id=class_id)
        cls.status = 'deactivated'
        cls.save()
        render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
        return redirect('/admin_dashboard/admin_department')                        
    return redirect('/admin_dashboard/admin_department')                                                    




def activate_class(request, class_id):

    if request.method == 'GET':
        cls = Class.objects.get(id=class_id)
        cls.status = 'activated'
        cls.save()
        render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
        return redirect('/admin_dashboard/admin_department')                        
    return redirect('/admin_dashboard/admin_department')    



def Delete_class(request, class_id):

    if request.method == 'GET':
        cls = Class.objects.get(id=class_id)
        cls.status = 'deleted'
        cls.save()
        render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
        return redirect('/admin_dashboard/admin_department')                        
    return redirect('/admin_dashboard/admin_department')

def students_class(request, class_id):    

    if request.method == 'GET':
        Class_id = class_id
        en = enroll_students.objects.filter(class_id = Class_id, status = 'activated').values()
        student = users.objects.filter(role='student', status='activated').values()
        render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
        return render(request, 'admin_view_students.html', {'session': request.session['user_name'], 'enrolled':en , 'student':student})                        
    return redirect('/admin_dashboard/admin_department')


def assign_student(request):    

    enrolled = enroll_students.objects.filter(status = 'activated').values() 
    User =  users.objects.filter(role = 'student', status = 'activated').values()
    Cls = Class.objects.filter(status = 'activated').values()

    if request.method == 'POST':        
        name = request.POST.get('name', False)
        cls = request.POST.get('classroom', False)
        
        if name == 0 or cls == 0:
            messages.info(request, 'You can not leave fields empty')
            return redirect('/admin_dashboard/admin_assign_student')    
        if enroll_students.objects.filter(student_id = name).exists():
            messages.info(request, 'Student already assigned to a class')
            return redirect('/admin_dashboard/admin_assign_student')
        # print(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<{name}>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{cls} >>>>>{type(year)}') 
        year = datetime.today().year       
        enrolled = enroll_students.objects.create(student_id = name, class_id = cls, status='activated', action = 'none', year = year)        
        enrolled.save()            

        messages.info(request, 'Student succesfully assigned to a class')
        return redirect('/admin_dashboard/admin_assign_student')        
    
        # render(request, 'admin_nav.html', {'session': request.session['user_name']})
        # return render(request, 'admin_assign_student.html', {'session': request.session['user_name'], 'users':User, 'class':Cls, 'enrolled':enrolled})
    render(request, 'admin_nav.html', {'session': request.session['user_name']})
    return render(request, 'admin_assign_student.html', {'session': request.session['user_name'], 'users':User, 'class':Cls, 'enrolled':enrolled})

def edit_assign_student(request):    
    enrolled = enroll_students.objects.filter(status = 'activated').values() 
    User =  users.objects.filter(role = 'student', status = 'activated').values()
    Cls = Class.objects.filter(status = 'activated').values()

    if request.method == 'POST':        
        name = request.POST.get('name', False)
        cls = request.POST.get('classroom', False)
        
        if name == 0 or cls == 0:
            messages.info(request, 'You can not leave fields empty')
            return redirect('/admin_dashboard/admin_edit_assign_student')    
        if enroll_students.objects.filter(student_id = name).exists() == True:            
        # print(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<{name}>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{cls} >>>>>{type(year)}') 
            year = datetime.today().year       
            enrolled = enroll_students.objects.get(student_id = name)   
            enrolled.class_id = int(cls) 
            enrolled.year = year
            enrolled.save()            

            messages.info(request, 'Student succesfully assigned to a class')
            return redirect('/admin_dashboard/admin_edit_assign_student')  
        else:
            messages.info(request, 'Student already assigned to a class')
            return redirect('/admin_dashboard/admin_edit_assign_student')      
    
        # render(request, 'admin_nav.html', {'session': request.session['user_name']})
        # return render(request, 'admin_assign_student.html', {'session': request.session['user_name'], 'users':User, 'class':Cls, 'enrolled':enrolled})
    render(request, 'admin_nav.html', {'session': request.session['user_name']})
    return render(request, 'admin_edit_assign_student.html', {'session': request.session['user_name'], 'users':User, 'class':Cls, 'enrolled':enrolled})




def classses(request, actions):    

    if request.method == 'POST':
        clsid = int(request.POST['classid'])
        class_id = Class.objects.get(id = clsid).name_class
        year = datetime.today().year
        enrolled = enroll_students.objects.filter(status = 'activated', year = year).values()
        if actions == 'promote':
            cls = Class.objects.filter(status = 'activated').values()
            Users = users.objects.filter(status = 'activated', role = 'student').values()
            render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
            return render(request, 'promote.html', {'session': request.session['user_name'], 'class_id':class_id, 'users':Users, 'enrolled':enrolled, 'clsid':clsid})
        elif actions == 'demote':
            cls = Class.objects.filter(status = 'activated').values()
            Users = users.objects.filter(status = 'activated', role = 'student').values()
            render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
            return render(request, 'demote.html', {'session': request.session['user_name'], 'class_id':class_id, 'users':Users, 'enrolled':enrolled, 'clsid':clsid})
        elif actions == 'repeat':
            cls = Class.objects.filter(status = 'activated').values()
            Users = users.objects.filter(status = 'activated', role = 'student').values()
            render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
            return render(request, 'repeat.html', {'session': request.session['user_name'], 'class_id':class_id, 'users':Users, 'enrolled':enrolled, 'clsid':clsid})

        elif actions == 'records':
            cls = Class.objects.filter(status = 'activated').values()
            Users = users.objects.filter(status = 'activated', role = 'student').values()
            prg = progress.objects.values()
            og_year = 2021
            years = []
            year = datetime.today().year
            while year >= og_year:                
                years.append(og_year)
                og_year +=1         
            load_all = 'True'          
            render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
            return render(request, 'records.html', {'session': request.session['user_name'], 'class_id':class_id, 'users':Users, 'enrolled':prg, 'clsid':clsid, 'years':years, 'load_all':load_all})

    cls = Class.objects.filter(status = 'activated').values()
    render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
    return render(request, 'admin_classes.html', {'session': request.session['user_name'], 'classes':cls, 'action':actions})


def promote(request, class_id):    

    if request.method == 'POST':
        try:
            check = request.POST['check_list[]']
            for i in check:
                cls = Class.objects.get(id = class_id)
                inc = int(cls.class_val) + 1
                try:
                    new_cls = Class.objects.get(class_val = inc)
                except:
                    messages.info(request, 'That class does not exist')
                    return redirect('/admin_dashboard/admin_classes/promote/')
                
                year = datetime.today().year
                enroll = enroll_students.objects.get(status = 'activated', student_id = i)
                enroll.class_id = new_cls.id
                enroll.year = year
                enroll.action = 'promoted'
                enroll.save()
                try:
                    og_prg = progress.objects.get(user_id = i, year = year)
                    og_prg.class_id = new_cls.id
                    og_prg.year = year
                    og_prg.action = 'promoted'
                    og_prg.save() 
                except:
                    prg = progress.objects.create(user_id = i, class_id = new_cls.id, action = 'promoted', year = year)
                    prg.save()
        except:
            messages.info(request, 'No student selected')
            return redirect('/admin_dashboard/admin_classes/promote/')
        
    return redirect('/admin_dashboard/admin_classes/promote/')

def demote(request, class_id):    

    if request.method == 'POST':
        try:
            check = request.POST['check_list[]']
            for i in check:
                cls = Class.objects.get(id = class_id)
                inc = int(cls.class_val) - 1
                try:
                    new_cls = Class.objects.get(class_val = inc)
                except:
                    messages.info(request, 'That class does not exist')
                    return redirect('/admin_dashboard/admin_classes/demote/')
                
                year = datetime.today().year
                enroll = enroll_students.objects.get(status = 'activated', student_id = i)
                enroll.class_id = new_cls.id
                enroll.year = year
                enroll.action = 'demoted'
                enroll.save()
                try:
                    og_prg = progress.objects.get(user_id = i, year = year)
                    og_prg.class_id = new_cls.id
                    og_prg.year = year
                    og_prg.action = 'demoted'
                    og_prg.save() 
                except:
                    prg = progress.objects.create(user_id = i, class_id = new_cls.id, action = 'demoted', year = year)
                    prg.save()                    
        except:
            messages.info(request, 'No student selected')
            return redirect('/admin_dashboard/admin_classes/demote/')
        
    return redirect('/admin_dashboard/admin_classes/demote/')

def repeat(request, class_id):    

    if request.method == 'POST':
        try:
            check = request.POST['check_list[]']
            for i in check:
                cls = Class.objects.get(id = class_id)
                inc = int(cls.class_val)
                try:
                    new_cls = Class.objects.get(class_val = inc)
                except:
                    messages.info(request, 'That class does not exist')
                    return redirect('/admin_dashboard/admin_classes/repeat/')
                
                year = datetime.today().year
                enroll = enroll_students.objects.get(status = 'activated', student_id = i)
                enroll.class_id = new_cls.id
                enroll.year = year
                enroll.action = 'repeated'
                enroll.save()
                try:
                    og_prg = progress.objects.get(user_id = i, year = year)
                    og_prg.class_id = new_cls.id
                    og_prg.year = year
                    og_prg.action = 'repeated'
                    og_prg.save() 
                except:
                    prg = progress.objects.create(user_id = i, class_id = new_cls.id, action = 'repeated', year = year)
                    prg.save()
        except:
            messages.info(request, 'No student selected')
            return redirect('/admin_dashboard/admin_classes/repeat/')
        
    return redirect('/admin_dashboard/admin_classes/repeat/')

def Filter(request):

   if request.method == 'POST':
        try:
            status = request.POST['status']
            year = request.POST['year']
            classid = request.POST['classid']
            
            _all_students = []
            try:
                enroll = enroll_students.objects.filter(status = 'activated', class_id = classid, year = year, action =  status).values()            
                for i in enroll:
                    print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{i["student_id"]}')
                    stud_id = i["student_id"]
                    user = users.objects.filter(status = 'activated', id = stud_id)
                    for j in user:
                        all_students = {'name':j.name, 'status':i['action'], 'year':i['year']}
                        _all_students.append(all_students)
                print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{all_students}')                          
                return HttpResponse(json.dumps(_all_students)) 
            except:                               
                return HttpResponse('No students in this category')

        except:
            messages.info(request, 'Failed')
            return redirect('/admin_dashboard/admin_classes/records/')    


def waiting(request):

    if request.session['is_loggedin'] == True:
        Users = users.objects.filter(status = 'pending').values()
        render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
        return render(request, 'waiting.html', {'row': Users, 'session': request.session['user_name']})

def add_course(request):

    cls = Class.objects.filter(status = 'activated').values()
    teachers = users.objects.filter(status = 'activated', role = 'teacher').values()
    if request.method == 'POST':
        name = request.POST['subjectname']
        class_id = request.POST.get('class', False)
        teacher_id = request.POST.get('teacher', False)

        if name =='' or class_id == '0' or teacher_id == '0':
            messages.info(request, 'You can not leave fields empty')
            return redirect('/admin_dashboard/admin_course')

        if subjects.objects.filter(name = name).exists():
            messages.info(request, 'Subject already exists')
            return redirect('/admin_dashboard/admin_course')

        subject = subjects.objects.create(name = name, class_id = class_id, teacher = teacher_id, status = 'activated')
        subject.save()

    render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
    return render(request, 'admin_add-course.html', {'class': cls, 'teachers':teachers, 'session': request.session['user_name']})


def all_courses(request):

    cls = Class.objects.filter(status = 'activated').values()
    subject = subjects.objects.filter().values().exclude(status = 'deleted')
    teachers = users.objects.filter(status = 'activated', role = 'teacher').values()
    render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
    return render(request, 'admin_all-courses.html', {'class': cls, 'teachers':teachers, 'subjects':subject, 'session': request.session['user_name']})


def deactivate_subject(request, subject_id):

    if request.method == 'GET':
        subject = subjects.objects.get(id=subject_id)
        subject.status = 'deactivated'
        subject.save()
        render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
        return redirect('/admin_dashboard/admin_all-courses')                        
    return redirect('/admin_dashboard/admin_all-courses')                                                    




def activate_subject(request, subject_id):

    if request.method == 'GET':
        subject = subjects.objects.get(id=subject_id)
        subject.status = 'activated'
        subject.save()
        render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
        return redirect('/admin_dashboard/admin_all-courses')                        
    return redirect('/admin_dashboard/admin_all-courses')    



def Delete_subject(request, subject_id):

    if request.method == 'GET':
        subject = subjects.objects.get(id=subject_id)
        subject.status = 'deleted'
        subject.save()
        render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
        return redirect('/admin_dashboard/admin_all-courses')                        
    return redirect('/admin_dashboard/admin_all-courses')

def edit_subject(request, subject_id):

    try:        
        if request.method == 'POST':            
            user = users.objects.filter(role='teacher').values().exclude(status = 'deleted')
            subject = subjects.objects.get(id=subject_id)   
            name =  request.POST['subjectname']
            teacher_id = request.POST.get('teacher', False)
            class_id = request.POST.get('class', False)      
            cls = Class.objects.filter(status = 'activated').values()   

            if name =='' or class_id == 0 or teacher_id == 0:
                messages.info(request, 'You can not leave fields empty')
                return redirect('/admin_dashboard/admin_all-courses')    
            subject.name = name
            subject.class_id = class_id
            subject.teacher = teacher_id
            subject.save()
            redirect('/admin_dashboard/')                       
            return render(request, 'edit-subject.html', {'user':user, 'classes':cls, 'subject':subject})
        else:
            return redirect('/admin_dashboard/') 
    except:
        return redirect(f'/admin_dashboard/go_to_edit/{subject_id}/class')

def profile(request):
    User = users.objects.get(name = request.session['user_name'])
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        pwd = request.POST['pwd']

        if name == '' or email == '' or pwd == '':
            messages.info(request, "You can't leave fields empty")
            return redirect('/admin_dashboard/profile')
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
        return redirect('/admin_dashboard/profile')
    render(request, 'admin_nav.html', {'session': request.session['user_name']})                        
    return render(request, 'profile.html',{'session': request.session['user_name'], 'user':User})

# def student_results(request):
#     # try:
#         if request.session['is_loggedin'] == True:
#             Users = users.objects.filter(status = 'activated').values()
#             qz = quiz.objects.filter(status = 'activated').values()            
#             att = attempt.objects.filter(attempted = 'true').values()
#             arr = []
#             for i in qz:
#                 for j in att:
#                     if j['quiz_id'] == i['id']:
#                         arr.append(j)
#             print(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{arr}')
#             render(request, 'teacher_header.html', {'session': request.session['user_name']})                        
#             return render(request, 'teacher_all-results.html', {'users': Users, 'quizes':qz,'attempted':att, 'session': request.session['user_name']})
#     # except:
#     #     messages.info(request, 'You need to log in first')
#     #     return redirect('login')
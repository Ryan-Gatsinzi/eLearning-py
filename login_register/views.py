from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from login_register.models import users


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        pwd = request.POST['password']

        if email ==''or pwd == '':
            messages.info(request, 'You can not leave fields empty')
            return redirect('/') 
        try:
            User = users.objects.get(email=email, password=pwd, status='activated')
            request.session['user_id'] = User.id
            request.session['user_role'] = User.role
            request.session['user_name'] = User.name
            request.session['is_loggedin'] = True

            if  request.session['user_role'] == 'admin':
                return redirect('admin')
            elif  request.session['user_role'] == 'student':
                return redirect('student')
            elif  request.session['user_role'] == 'teacher':
                return redirect('teacher')  
        except:
            messages.info(request ,"The email or password is wrong")
            return redirect('/')
  

    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        role = request.POST['role']
        pwd = request.POST['password']  
        status = 'pending'
        if name =='' or email == '' or pwd == '' or role == '' or status == '':
            messages.info(request, 'You can not leave fields empty')
            return redirect('signup') 

        if users.objects.filter(name = name).exists():
            messages.info(request, 'Username exists')
            return redirect('signup')    

        elif users.objects.filter(email = email).exists():
            messages.info(request, 'Email exists') 
            return redirect('signup')         

        Users= users.objects.create(name=name, email=email, role = role, password=pwd, status = status)
        Users.save()
        return redirect('login')
    else:
        return render(request, 'signup.html')

from django.db import models

# Create your models here.
from enum import auto
from urllib.parse import MAX_CACHE_SIZE
from django.db import models



class users(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    status = models.CharField(max_length=255)  

class Class(models.Model):
    name_class = models.CharField(max_length=255)   
    homeroom_tr = models.IntegerField()
    class_val = models.IntegerField()    
    status = models.CharField(max_length=255)   

class enroll_students(models.Model):
    student_id = models.IntegerField()   
    class_id = models.IntegerField()        
    status = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    year = models.IntegerField()

class enroll_teachers(models.Model):
    teacher_id = models.IntegerField()   
    class_id = models.IntegerField()        
    status = models.CharField(max_length=255)  

class progress(models.Model):
    user_id = models.IntegerField()   
    class_id = models.IntegerField()        
    action = models.CharField(max_length=255) 
    year = models.IntegerField()   

class subjects(models.Model):
    name = models.CharField(max_length=255)   
    class_id = models.IntegerField()        
    teacher = models.IntegerField()
    status = models.CharField(max_length=255) 

class profile(models.Model):
    user_id = models.IntegerField()      
    image = models.ImageField(upload_to="images/", null = True, blank = True)  

class topics(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    file = models.FileField(upload_to="files/")
    subject = models.IntegerField()
    date_assigned = models.TimeField(max_length=255)
    teacher = models.IntegerField()
    status = models.CharField(max_length=255)

class library(models.Model):
    publisher_name = models.IntegerField()
    book_name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    file = models.FileField(upload_to="books/")
    status = models.CharField(max_length=255, default='activated')

class quiz(models.Model):
    quiz_name = models.CharField(max_length=255)
    exam_time = models.IntegerField()
    teacher_id = models.IntegerField()
    status = models.CharField(max_length=255, default='activated')

class questions(models.Model):
    question = models.CharField(max_length=255)
    opt1 = models.CharField(max_length=255)
    opt2 = models.CharField(max_length=255)
    opt3 = models.CharField(max_length=255)
    opt4 = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    quiz_id = models.IntegerField()
    teacher_id = models.IntegerField()
    status = models.CharField(max_length=255, default='activated')

class results(models.Model):
    quiz_id = models.IntegerField()
    total_question = models.IntegerField()
    correct_answer = models.CharField(max_length=255)
    wrong_answer = models.CharField(max_length=255)
    percentage = models.IntegerField()
    time = models.DateField()    
    role = models.CharField(max_length=255)
    user_id = models.IntegerField()  
    teacher_id = models.IntegerField()
    status = models.CharField(max_length=255, default='activated')

class attempt(models.Model):
    quiz_id = models.IntegerField()
    user_id = models.IntegerField()  
    attempted = models.CharField(max_length=255, default='true')

class chat(models.Model):
    messenger = models.IntegerField()
    recipient = models.IntegerField()  
    msg = models.CharField(max_length=255)
    time = models.DateTimeField()
    status = models.CharField(max_length=255, default='activated')
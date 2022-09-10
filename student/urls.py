from django.urls import path
from . import views

urlpatterns = [
    path('',views.student, name='student'),
    path('profile',views.profile, name='profile'),
    path('student_logout',views.logout, name='student_logout'), 
    path('student_all-students/',views.all_students, name='all_student'),
    path('student_all-courses/',views.all_subjects, name='all_subjects'), 
    path('student_class/',views.all_classes, name='all_subjects'), 
    path('student_library/',views.all_books, name='library'),   
    path('student_add-book/',views.add_book, name='add-book'),  
    path('delete_book/<int:book_id>/',views.Delete_book, name='delete_book'),
    path('quiz',views.Quiz, name='quiz'),
    path('load_total/',views.load_total, name='load_total'),
    path('take_quiz/<int:qn_total>/<int:quiz_id>/<int:teacher>/',views.take_quiz, name='take_quiz'),
    path('load_timer/',views.load_timer, name='load_timer'),
    path('quiz_results/',views.quiz_results, name='quiz_results'),
    path('results/',views.result, name='results'),
    path('latest_results',views.latest_results, name='latest_results'),
    path('people',views.people, name='people'),
    path('student_livesearch/',views.student_livesearch, name='student_livesearch'),
    path('student_chat/<int:user_id>/',views.student_chat, name='student_chat'),
    path('student_sendMessage/',views.send_msg, name='student_sendMessage'),
    path('student_displayMessage/',views.display_msg, name='student_displayMessage'),
    path('student_deleteMessage/',views.delete_msg, name='student_deleteMessage'),
    path('student_all-topics/',views.all_topics, name='all-topics'),
]
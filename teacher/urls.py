from django.urls import path
from . import views

urlpatterns = [
    path('',views.teacher, name='teacher'),
    path('profile',views.profile, name='profile'),
    path('teacher_logout',views.logout, name='teacher_logout'),
    path('teacher_all-students/',views.all_students, name='all_student'),
    path('teacher_all-courses/',views.all_subjects, name='all_subjects'),
    path('teacher_class/',views.all_classes, name='all_classes'),
    path('teacher_add-topic/',views.add_topic, name='add-topic'),
    path('teacher_all-topics/',views.all_topics, name='all-topics'),
    path('go_to_edit/<int:ids>/<str:action>/',views.go_to_edit, name='go_to_edit'),
    path('edit-topic/<int:id>/',views.edit_topic, name='edit-topic'),
    path('deactivate_topic/<int:topic_id>/',views.deactivate_topic, name='deactivate_topic'),
    path('activate_topic/<int:topic_id>/',views.activate_topic, name='activate_topic'),
    path('delete_topic/<int:topic_id>/',views.Delete_topic, name='delete_topic'),
    path('teacher_add-book/',views.add_book, name='add-book'),
    path('teacher_library/',views.all_books, name='library'),
    path('delete_book/<int:book_id>/',views.Delete_book, name='delete_book'),
    path('teacher_add_quiz/',views.add_quiz, name='add_quiz'),
    path('teacher_add_question/',views.add_question, name='add_question'),
    path('teacher_all-quizes/',views.all_quizes, name='all-quizes'),
    path('deactivate_quiz/<int:quiz_id>/',views.deactivate_quiz, name='deactivate_quiz'),
    path('activate_quiz/<int:quiz_id>/',views.activate_quiz, name='activate_quiz'),
    path('delete_quiz/<int:quiz_id>/',views.Delete_quiz, name='delete_quiz'),
    path('teacher_edit-quiz/<int:id>/',views.edit_quiz, name='edit-quiz'),
    path('all_questions/<int:id>/',views.all_questions, name='all_questions'),
    path('delete_question/<int:id>/',views.Delete_question, name='delete_question'),
    path('edit-question/<int:id>/',views.edit_question, name='edit-question'),
    path('quiz',views.Quiz, name='quiz'),
    path('load_total/',views.load_total, name='load_total'),
    path('take_quiz/<int:qn_total>/<int:quiz_id>/',views.take_quiz, name='take_quiz'),
    path('quiz_results/',views.quiz_results, name='quiz_results'),
    path('results/',views.result, name='results'),
    path('load_timer/',views.load_timer, name='load_timer'),
    path('all-results',views.student_results, name='all-results'),
    path('latest_results',views.latest_results, name='latest_results'),
    path('people',views.people, name='people'),
    path('teacher_livesearch/',views.teacher_livesearch, name='teacher_livesearch'),
    path('teacher_chat/<int:user_id>/',views.teacher_chat, name='teacher_chat'),
    path('teacher_sendMessage/',views.send_msg, name='teacher_sendMessage'),
    path('teacher_displayMessage/',views.display_msg, name='teacher_displayMessage'),
    path('teacher_deleteMessage/',views.delete_msg, name='teacher_deleteMessage'),
]
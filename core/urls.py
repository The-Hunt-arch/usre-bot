from django.urls import path

from . import views



urlpatterns = [
    path("index/", views.index, name="index"),
    path("speech/", views.speech, name="speech"),
    path("face/", views.face, name="face"),
    path("", views.form, name="form"),
    path("form-submit/", views.form_submit, name="form_submit"),
    path('success/',  views.success_page, name='success_page'),
    path('process-step1/',  views.process_step1, name='process-step1'),
    path('fetch-data/',  views.fetch_data, name='fetch_data'),
    # path('chatbot/', views.chatbot_view, name='chatbot'),
]
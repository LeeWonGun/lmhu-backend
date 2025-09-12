from django.urls import path
from .views import GPTQuestionAnswerView

urlpatterns = [
    path('ask-gpt/', GPTQuestionAnswerView.as_view(), name='ask_gpt'),
]

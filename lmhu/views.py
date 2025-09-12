import os
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from openai import OpenAI  # ✅ 최신 방식으로 불러오기

from .models import QuestionAnswer
from .serializers import QuestionAnswerSerializer

# .env 파일 로드해서 API 키 설정
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ✅ 최신 버전에서는 OpenAI client 객체 생성 필요
client = OpenAI(api_key=api_key)


class GPTQuestionAnswerView(APIView):
    def post(self, request):
        user_question = request.data.get('question')
        if not user_question:
            return Response({"error": "질문이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # GPT에게 질문 전송
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # 또는 fine-tuned 모델명으로 교체
                messages=[
                    {"role": "user", "content": user_question}
                ],
                temperature=0.7,
                max_tokens=300,
            )

            gpt_answer = response.choices[0].message.content

            # DB에 저장
            qa = QuestionAnswer.objects.create(
                question=user_question,
                answer=gpt_answer
            )
            serializer = QuestionAnswerSerializer(qa)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Choice, Question
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import json

import requests
from django.shortcuts import render

from django.http import JsonResponse
import requests

def get_nocodb_data(request):
    # URL API NocoDB (замените на ваш URL)
    url = "https://app.nocodb.com/api/v2/tables/mwkq779ax6eme5u/records"
    headers = {
        "xc-token": "C3UrQ22BaOLseRT7wVTTqy3PQ4yg4JV-RLZxnX6T",  # Замените на ваш API-ключ
    }

    # Получаем данные из NocoDB
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()  # Данные таблицы
        records = data.get('list', [])  # Извлекаем записи из ключа 'list'

        # Формируем JSON-ответ
        response_data = {
            "nocodb-data": "http://localhost:8000/nocodb-data/",  # Ссылка на таблицу
            "records": records  # Данные таблицы
        }
        return JsonResponse(response_data, status=200)
    else:
        # Если произошла ошибка, возвращаем пустой JSON
        return JsonResponse({"error": "Не удалось получить данные из NocoDB"}, status=response.status_code)

class DataViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        # URL API NocoDB
        url = "https://app.nocodb.com/api/v2/tables/mwkq779ax6eme5u/records"
        headers = {
            "xc-token": "C3UrQ22BaOLseRT7wVTTqy3PQ4yg4JV-RLZxnX6T",
        }

        # Получаем данные из NocoDB
        response = requests.get(url, headers=headers)
        print(response)

        if response.status_code == 200:
            # # Выводим содержимое ответа перед попыткой декодирования
            # print("Ответ от сервера:")
            # print(response.content.decode())  # Декодируем байты в строку для удобного чтения

            try:
                data = response.json()
                print(data)
                records = data.get('list', [])
                return Response(records)
            except json.JSONDecodeError as e:
                return Response({"error": f"Не удалось декодировать JSON: {str(e)}"})
        else:
            return Response({"error": f"Не удалось получить данные из NocoDB ({response.status_code})"}, status=response.status_code)



class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
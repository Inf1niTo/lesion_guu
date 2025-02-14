from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import JsonResponse

from .models import Choice, Question
import requests

import requests
from django.shortcuts import render

def get_nocodb_data(request):
    # URL API NocoDB (замените на ваш URL)
    url = "https://app.nocodb.com/api/v2/tables/mwkq779ax6eme5u/records"
    headers = {
        "xc-token": "C3UrQ22BaOLseRT7wVTTqy3PQ4yg4JV-RLZxnX6T",  # Замените на ваш API-ключ
    }

    # Получаем данные из NocoDB
    response = requests.get(url, headers=headers)

    # Отладочная информация
    # print(f"Статус код: {response.status_code}")
    # print(f"Ответ: {response.text}")

    if response.status_code == 200:
        data = response.json()  # Данные таблицы
        # print(data)

        # Извлекаем записи из ключа 'list'
        records = data.get('list', [])  
        print(records)

        # Если записи есть, извлекаем заголовки
        headers = records[0].keys() if records else []  
        print(headers)
    else:
        records = []  # Если произошла ошибка, передаём пустой список
        headers = []  # И заголовки тоже пустые

    # Передаём данные в шаблон
    return render(request, 'nocodb_table.html', {'headers': headers, 'records': records})

# def get_nocodb_data(request):
#     # URL API NocoDB (замените на ваш URL)
#     url = "https://app.nocodb.com/api/v2/tables/mwkq779ax6eme5u/records"
#     headers = {
#         "xc-token": "C3UrQ22BaOLseRT7wVTTqy3PQ4yg4JV-RLZxnX6T",  # Замените на ваш API-ключ
#     }
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         return JsonResponse(data, safe=False)
#     else:
#         return JsonResponse({"error": "Failed to fetch data"}, status=500)



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
    
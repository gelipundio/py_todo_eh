import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from datetime import datetime

from .models import TodoModel

error_messages = {
  "400": "Bad Request",
  "500": "Internal server error, we are working on it",
  "404": "We were unable to find that item"
}

# list todo items
def list(request):
  if not request.method == 'GET':
    return HttpResponseBadRequest(error_messages['400'])

  try:
    items = TodoModel.objects.all()
    items = json.loads(serialize('json', items))
    return JsonResponse(items, safe=False)
  except:
    return HttpResponseServerError(error_messages['500'])

# create new item
@csrf_exempt
def create(request):
  if not request.method == 'POST':
    return HttpResponseBadRequest(error_messages['400'])

  try:
    data = json.loads(request.body)
    new_item = TodoModel(**data)
    new_item.save()
    return HttpResponse('created')
  except:
    return HttpResponseServerError(error_messages['500'])

# update item
@csrf_exempt
def update(request, item_id):
  if not request.method == 'PATCH':
    return HttpResponseBadRequest(error_messages['400'])

  try:
    data = json.loads(request.body)
    todo_item = TodoModel.objects.get(pk=item_id)
    for key, value in data.items():
      setattr(todo_item, key, value)
    todo_item.save()
    return HttpResponse('done')
  except TodoModel.DoesNotExist as error:
    return HttpResponseNotFound(error_messages['404'])
  except Exception as error:
    return HttpResponseServerError(error_messages['500'])

# delete item
@csrf_exempt
def delete(request, item_id):
  if not request.method == 'DELETE':
    return HttpResponseBadRequest(error_messages['400'])
  
  try:
    todo_item = TodoModel.objects.get(pk=item_id)
    todo_item.delete()
    return HttpResponse('done')
  except TodoModel.DoesNotExist as error:
    return HttpResponseNotFound(error_messages['404'])
  except Exception as error:
    return HttpResponseServerError(error_messages['500'])
  
# complete item
@csrf_exempt
def complete(request, item_id):
  if not request.method == 'PATCH':
    return HttpResponseBadRequest(error_messages['400'])

  try:
    todo_item = TodoModel.objects.get(pk=item_id)
    todo_item.completed_date = datetime.now()
    todo_item.save()
    return HttpResponse('done')
  except TodoModel.DoesNotExist as error:
    return HttpResponseNotFound(error_messages['404'])
  except Exception as error:
    return HttpResponseServerError(error_messages['500'])


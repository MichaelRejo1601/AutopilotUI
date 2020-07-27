from django.shortcuts import render
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from .config import *
from .models import *
from .forms import *
from collections import OrderedDict
from .node import Node
# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Create your views here.
def test(request):
    assistant = Assistant.objects.latest('id')
    task = assistant.tasks.latest('id')
    test = str(client.autopilot \
                   .assistants(str(assistant)) \
                   .tasks(str(task)).task_actions().fetch().data)
    context = {'test': test}
    return render(request, "test.html", context)

def get_tasks(request, assistant_sid):
    assistant = Assistant.objects.get(sid=assistant_sid)
    tasks = client.autopilot \
        .assistants(assistant.sid) \
        .tasks.list()
    context = {'assistant':assistant, 'tasks':tasks,}
    return render(request, "tasks.html", context)
    # form = TaskForm()
    # if request.method == "POST":
    #     twilio_task = client.autopilot \
    #                    .assistants('UA1c648fa383b27e3ff0d14167b56ff57e') \
    #                    .tasks \
    #                    .create(unique_name=request.POST.get('unique_name'))
    #     sid = twilio_task.sid
    #     print(sid)
    #     unique_name = request.POST.get('unique_name')
    #     task = Task(assistant, sid, unique_name)
    #     form = TaskForm(instance=task)
    #     print('Task Posted')
    #     if form.is_valid():
    #         form.save()
    #         print('Done')
    #         form = TaskForm(initial={'assistant':assistant})
    #         context = {'form':form, 'assistant':assistant,}
    #         return render(request, "tasks.html", context)
    #     else:
    #         client.autopilot \
    #                        .assistants('UA1c648fa383b27e3ff0d14167b56ff57e') \
    #                        .tasks(sid) \
    #                        .delete()
    #         context = {'form':form, 'assistant':assistant}
    #         return render(request, "tasks.html", context)
    # else:
    #
    #     context = {'form':form, 'assistant':assistant}
    #     return render(request, "tasks.html", context)
def get_task(request, assistant_sid, task_sid):
    assistant = Assistant.objects.get(sid=assistant_sid)
    task = client.autopilot \
        .assistants(assistant.sid) \
        .tasks(task_sid).fetch()
    if request.method == "POST":
        try:
            tasks = client.autopilot \
            .assistants(assistant_sid) \
            .tasks(task_sid).update(unique_name=request.POST.get('unique_name'))
        except TwilioRestException:
            print("Yikes Dawg")
    return render(request, 'task.html', {'assistant':assistant, 'task':task})

def tree(request, assistant_sid):
    first = "Task 1"
    dict = OrderedDict()
    node = Node(first)
    assistant = Assistant.objects.get(sid=assistant_sid)
    tasks = client.autopilot \
        .assistants(assistant.sid) \
        .tasks.list()
    for task in Relationship.objects.values('parent').distinct():
        print(task)
        dict[task["parent"]] = Node(task)
        for relationship in Relationship.objects.filter(parent=task['parent']):
            print(relationship)
            dict[task['parent']].add_child(relationship.child)
    print(dict[first].children)
    context = {'assistant':assistant}
    return render(request, 'tree.html', context)

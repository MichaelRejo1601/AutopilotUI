from django.shortcuts import render
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from .config import *
from .models import *
from .forms import *
from collections import OrderedDict
from .node import Node
from .form_functions import *
import json
import traceback
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
def get_assistants(request):
    assistants = client.autopilot \
        .assistants.list()
    return render(request, 'assistants.html', {'assistants':assistants})
def get_assistant(request, assistant_sid):
    assistant = client.autopilot \
        .assistants(assistant_sid).fetch()
    if request.method == "POST":
        try:
            tasks = client.autopilot \
            .assistants(assistant_sid) \
            .update(unique_name=request.POST.get('unique_name'))
        except TwilioRestException:
            print("Yikes Dawg but for Assistant")
    return render(request, 'assistant.html', {'assistant': assistant})
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

def edit_actions(request, assistant_sid, task_sid):
    error = ''
    form_elements = ""
    counter = 0
    order = OrderedDict()
    assistant = Assistant.objects.get(sid=assistant_sid)
    task = client.autopilot \
        .assistants(assistant.sid) \
        .tasks(task_sid).fetch()
    try:
        task_actions = client.autopilot \
        .assistants(assistant_sid) \
        .tasks(task_sid).task_actions.get().fetch().data
    except TwilioRestException:
        print("Yikes Dawg")
    options = {
        "say":"<div id='say' class='inline-form'>\
    <legend>Say</legend><button id='action'>-</button>\
    <label for='speech'>Text</label>\
    <input required id='speech' type='text' name='actions[{order}][say][speech]' placeholder='Hello!'/>\
  </div>",
        "play":"<div id='play' class='inline-form'>\
    <legend>Play</legend><button id='action'>-</button>\
    <label for='loop'>Loop</label>\
    <input type='number' id='loop' name='actions[{order}][play][loop]' placeholder='3'/>\
    <label for='url'>URL</label>\
    <input required id='url' type='url' name='actions[{order}][play][url]' placeholder='https://www.mysite.com/song.mp3'/>\
  </div>",
        "listen":"<div id='listen' class='inline-form'>\
    <legend>Listen</legend><button id='action'>-</button>\
    <label for='tasks'>Tasks</label><button id='add-listen'>+</button>\
    <input type='text' id='tasks' name='actions[{order}][listen][tasks][]' placeholder='task-1'/>\
  </div>",
        "collect":"""<h1>BOLD</h1>""",
        "handoff":"<div id='handoff' class='inline-form'>\
    <legend>Handoff</legend><button id='action'>-</button>\
    <label for='chanel'>Chanel</label>\
    <select required id='chanel' name='actions[{order}][handoff][chanel]'><option>voice</option></select>\
    <label for='uri'>TwiML URI</label>\
    <input required id='uri' type='url' name='actions[{order}][handoff][uri]' placeholder='TwiML URI'/>\
    <label for='method'>Method</label>\
    <select id='method' name='actions[{order}][handoff][method]'><option>GET</option><option>POST</option></select>\
  </div>",
        "redirect":"<div id='redirect' class='inline-form'>\
    <legend>Redirect</legend><button id='action'>-</button>\
    <label for='task'>Task or URL</label>\
    <input required id='task' type='text' name='actions[{order}][redirect][uri]' placeholder='task://my-task1 OR https://www.mysite.com/my-redirect/'/>\
    <label for='method'>Method</label>\
    <select id='method' name='actions[{order}][redirect][method]'><option>GET</option><option>POST</option></select>\
  </div>",
        "show":"""<h1>BOLD</h1>""",
    }
    if request.method == 'POST':
        print(request.POST.dict())
        if('data' in request.POST.dict().keys()):
            try:
                task.task_actions.get().fetch().update(request.POST.dict()['data'])
            except TwilioRestException:
                traceback.print_exc()
                error = "Bad Form"
        if('new_array' in request.POST.dict().keys()):
            withjson = request.POST.dict()['new_array']
            pydict = json.loads(withjson)
            arr = pydict['arr']
            form_elements = ""
            for element in arr:
                order[element] = counter
                counter += 1
            for item in order:
                options[item] = options[item].format(order=order[item])
            for element in arr:
                form_elements += options[element]
            print(order)
            print(counter)
            print(arr)
            print(form_elements)
    else:
        for element in task_actions["actions"]:
            order[next(iter((element)))] = counter
            counter += 1
        for item in order:
            options[item] = options[item].format(order=order[item])
        for element in task_actions["actions"]:
            form_elements += options[next(iter((element)))]

        form_elements += ""
    return render(request, 'edit.html', {'test':test, "form_elements":form_elements, 'assistant':assistant, 'task':task, 'error':error,})

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
        dict[task["parent"]] = Node(task["parent"])
        for relationship in Relationship.objects.filter(parent=task['parent']):
            print(relationship)
            dict[task['parent']].add_child(relationship.child)
    print(list(dict.values())[0].children)
    pc_list = []
    for i in dict.keys():
        pc_list.append(dict[i])
    print(pc_list)
    print(pc_list[0].children)
    context = {'assistant':assistant, 'pc_list':pc_list}
    return render(request, 'tree.html', context)

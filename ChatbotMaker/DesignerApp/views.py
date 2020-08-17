from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
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
from django.views.decorators.csrf import csrf_exempt,csrf_protect
# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# Create your views here.
@csrf_exempt
def test(request):
    assistant = Assistant.objects.latest('id')
    task = assistant.tasks.latest('id')
    test = str(client.autopilot \
                   .assistants(str(assistant)) \
                   .tasks(str(task)).task_actions().fetch().data)
    context = {'test': test}
    return render(request, "test.html", context)
@csrf_exempt
def get_assistants(request):
    assistants = client.autopilot \
        .assistants.list()
    return render(request, 'assistants.html', {'assistants':assistants})
@csrf_exempt
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
@csrf_exempt
def get_tasks(request, assistant_sid):
    assistant = client.autopilot \
        .assistants(assistant_sid).fetch()
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
@csrf_exempt
def get_task(request, assistant_sid, task_sid):
    assistant = client.autopilot \
        .assistants(assistant_sid).fetch()
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
@csrf_exempt
def edit_actions(request, assistant_sid, task_sid):
    my_err = 'Valid Actions'
    form_elements = ""
    counter = 0
    order = OrderedDict()
    assistant = client.autopilot \
        .assistants(assistant_sid).fetch()
    task = client.autopilot \
        .assistants(assistant.sid) \
        .tasks(task_sid).fetch()
    try:
        task_actions = client.autopilot \
        .assistants(assistant_sid) \
        .tasks(task_sid).task_actions.get().fetch().data
    except TwilioRestException:
        print("Yikes Dawg")
    options1 = {
        "say":"<section id='say' class='panel'> <header class='panel-heading'> <a id='arrow-up' class='arrow'>&#8679;</a> <a id='arrow-down' class='arrow'>&#8681;</a> <strong style='font-size: 2rem;'>Say</strong> </header><div class='panel-body'><form class='form-horizontal' method='post'><div class='form-group'> <label class='col-sm-2 control-label'>Text</label><div class='col-sm-10'> <input required name='actions[0][say][speech]' type='text' class='form-control' placeholder='Hello there! How may I help you?'></div></div></form></div> </section>",
        "play":"<section id='play' class='panel'> <header class='panel-heading'> <a id='arrow-up' class='arrow'>&#8679;</a> <a id='arrow-down' class='arrow'>&#8681;</a> <strong style='font-size: 2rem;'>Play</strong> </header><div class='panel-body'><form class='form-horizontal ' method='post'><div class='form-group'> <label class='col-sm-2 control-label'>URL</label><div class='col-sm-10'> <input required name='actions[1][play][url]' type='url' class='form-control' placeholder='https://wwww.mysite.com/song.mp3'></div></div><div class='form-group'> <label class='col-sm-2 control-label'>Loop</label><div class='col-sm-10'> <input required name='actions[1][play][loop]' type='number' class='form-control' placeholder='1'></div></div></form></div> </section>",
        "listen":"<section id='listen' class='panel'> <header class='panel-heading'> <a id='arrow-up' class='arrow'>&#8679;</a> <a id='arrow-down' class='arrow'>&#8681;</a> <strong style='font-size: 2rem;'>Listen</strong> </header><div class='panel-body'><form class='form-horizontal ' method='post'><div class='form-group'> <label class='col-sm-2 control-label'>Tasks</label><div class='col-sm-10'> <input id='tasks' name='actions[2][listen][tasks][]' type='text' class='form-control' placeholder='Task-1'></div><div class='col-sm-2'></div><div class='col-sm-10'> <input id='tasks' name='actions[2][listen][tasks][]' type='text' class='form-control' placeholder='mytask-x'></div></div></form></div> </section>",

    }
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
    <label for='tasks'>Tasks</label><button id='add-listen' type='button'>+</button>\
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
                my_err = "Invalid Actions, Please Input a Valid Set of Actions"
                traceback.print_exc()
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
    else:
        for element in task_actions["actions"]:
            order[next(iter((element)))] = counter
            counter += 1
        for item in order:
            options[item] = options[item].format(order=order[item])
        for element in task_actions["actions"]:
            form_elements += options[next(iter((element)))]

        form_elements += ""
    print(order)
    print(counter)
    print(form_elements)
    return render(request, 'edit2.html', {'test':test, "form_elements":form_elements, 'assistant':assistant, 'task':task, 'my_err':my_err,})
@csrf_exempt
def tree(request, assistant_sid):
    first = "Task 1"
    dict = OrderedDict()
    node = Node(first)
    assistant = client.autopilot \
        .assistants(assistant_sid).fetch()
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
@csrf_exempt
def edit_samples(request, assistant_sid, task_sid):
    assistant = client.autopilot \
        .assistants(assistant_sid).fetch()
    task = client.autopilot \
        .assistants(assistant_sid) \
        .tasks(task_sid).fetch()
    print("sid" + task.sid)
    context = {'assistant':assistant, 'task':task}
    return render(request, 'train.html', context)
@csrf_exempt
def fields(request, assistant_sid):
    assistant = client.autopilot \
        .assistants(assistant_sid).fetch()
    context = {'assistant':assistant}
    return render(request, 'fields.html', context)
@csrf_exempt
def simulator(request, assistant_sid):
    assistant = client.autopilot \
        .assistants(assistant_sid).fetch()
    context = {'assistant':assistant}
    return render(request, 'simulator.html', context)
@csrf_exempt
def config(request, assistant_sid):
    assistant = client.autopilot \
        .assistants(assistant_sid).fetch()
    context = {'assistant':assistant}
    return render(request, 'config.html', context)
@csrf_exempt
def login(request):
    if request.method == "POST":
        return HttpResponseRedirect('/assistants/')
    return render(request, 'login.html', {})
@csrf_exempt
def create_assistant(request, unique_name):
    assistant = client.autopilot \
        .assistants.create(unique_name=unique_name)
    print('createass')
    return redirect(reverse('get_assistant', args=[assistant.sid]))
@csrf_exempt
def create_task(request, unique_name, assistant_sid):
    task = client.autopilot \
    .assistants(assistant_sid) \
    .tasks.create(unique_name=unique_name)
    print('createtask')
    return redirect(reverse('get_task', args=[assistant_sid, task.sid]))
@csrf_exempt
def delete_assistant(request, unique_name):
    assistant = client.autopilot \
        .assistants(unique_name).delete()
    print('delass')
    return redirect(reverse('get_assistants'))
@csrf_exempt
def delete_task(request, unique_name, assistant_sid):
    task = client.autopilot \
    .assistants(assistant_sid) \
    .tasks(unique_name).delete()
    print('deltask')
    return redirect(reverse('get_tasks', args=[assistant_sid]))

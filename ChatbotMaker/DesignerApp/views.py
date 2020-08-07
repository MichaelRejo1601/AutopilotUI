from django.shortcuts import render
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from .config import *
from .models import *
from .forms import *
from collections import OrderedDict
from .node import Node
from .form_functions import *
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
    test = '<h1>BOLD</h1>'
    # organized_dict = OrderedDict()
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
        "say":"""<div class='inline-form'>
        <legend>Say</legend>
        <label for='saytext'>Text</label>
        <input required type="text" name='saytext' placeholder='Hello!'/>
      </div>""",
        "play":"""<div class='inline-form'>
        <legend>Play</legend>
        <label for='play-loop'>Loop</label>
        <input required type="number" name='play-loop' placeholder='3'/>
        <label for='play-url'>URL</label>
        <input required type="url" name='play-url' placeholder='https://www.mysite.com/song.mp3'/>
      </div>""",
        "listen":"""<div class='inline-form'>
        <legend>Listen</legend>
        <label for="listen-tasks">Tasks</label>
        <input type="text" name='listen-tasks' placeholder='task-1, task-2, task-3'/>
      </div>""",
        "collect":"""<h1>BOLD</h1>""",
        "handoff":"""<div class='inline-form'>
        <legend>Handoff</legend>
        <label for="chanel">Chanel</label>
        <select name="chanel"><option>voice</option></select>
        <label for="uri">TwiML URI</label>
        <input required type="url" name='uri' placeholder='TwiML URI'/>
        <label for="method">Method</label>
        <select name="method"><option>POST</option><option>GET</option></select>
      </div>""",
        "redirect":"""<div class='inline-form'>
        <legend>Redirect</legend>
        <label for="url">URL</label>
        <input required type="url" name='url' placeholder='https://www.mysite.com/my-redirect/'/>
        <label for="method">Method</label>
        <select name="method"><option>POST</option><option>GET</option></select>
        <h3>OR</h3>
        <label for="task">Task</label>
        <input required type="text" name='task' placeholder='task://my-task1'/>
      </div>""",
        "remember":"""<div class='inline-form'>
        <legend>Remember</legend>
        <label for="url">URL</label>
        <input required type="url" name='url' placeholder='https://www.mysite.com/my-redirect/'/>
      </div>""",
        "show":"""<h1>BOLD</h1>""",
    }
    form_elements = ""
    for element in task_actions["actions"]:
        form_elements += options[next(iter((element)))]
    form_elements += "<input type='submit' value='Save'>"
    print(form_elements)
    if request.method == 'POST':
        print(request.POST)
        # say(request, task_actions)
        # for item in request.POST.keys():
        #     if item.split("-")[0] in options.keys():
        #         if item.split("-")[0] in organized_dict.keys():
        #             organized_dict[item.split("-")[0]].append(request.POST.get(item))
        #         else:
        #             organized_dict[item.split("-")[0]] = {}
        #             organized_dict[item.split("-")[0]].append(request.POST.get(item))
        # print(organized_dict)
    return render(request, 'edit.html', {'test':test, "form_elements":form_elements, 'assistant':assistant, 'task':task,})

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

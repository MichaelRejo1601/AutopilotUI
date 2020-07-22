from django.shortcuts import render
from twilio.rest import Client
from .config import *
from .models import Assistant, Task


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

def create_post(request):
    

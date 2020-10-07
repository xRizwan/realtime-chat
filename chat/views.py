from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .serializers import MessageSerializer

from .models import User, Message
import json

# Create your views here.

def index(request):
    messages = Message.objects.all()

    return render(request, 'chat/index.html', {
        'messages' : messages,
    })

def login_view(request):
    if request.method == "POST":

        # attempt to sign in the user
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication is successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "chat/login.html", {
                "message" : "Invalid username or password!"
            })
    else:
        return render(request, 'chat/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def register(request):
    # on POST
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Check if password matches confirmation password
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, 'chat/register.html', {
                'message': "Passwords Don't Match!"
            })
        
        # Attempt to create a new user

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'chat/register.html', {
                'message': "Username already taken."
            })

        login(request, user)
        print('redirecting')
        return HttpResponseRedirect(reverse("index"))

    # on GET
    else:
        return render(request, 'chat/register.html')

def send(request):
    if request.user.is_authenticated is not True:
        return JsonResponse({"message": "LoginError"}, status=400)

    if request.method == "POST":
        data = json.loads(request.body)

        message = data.get('message')
        if (message == ''):
            return JsonResponse({"error": "Message must not be empty!"}, status=400)

        else:
            newMessage = Message.objects.create(user=request.user, message=message)
            newMessage.save()

            return JsonResponse({'message': "Success!"}, status=200)
        
    else:
        return JsonResponse({"message": 'error'}, status=400)

def messages(request, key):

    if request.method == "GET":
        print(key)
        current = int(key)

        messages = Message.objects.filter(id__gt=current)
        serialized = MessageSerializer(messages, many=True)
        print(serialized.data)

        return JsonResponse({
                "message": "Success!",
                "data": serialized.data,
            }, status=200)

    else :
        return JsonResponse({
            'message': 'Error'
        })

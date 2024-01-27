from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import random

# Create your views here.
def index(request):
    return render(request, 'general/index.html')


def user_register(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        passw = request.POST.get("password")
        if User.objects.filter(username=uname).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'user/user_register.html')
        else:
            user = User.objects.create_user(
                username=uname,
                password=passw,
            )
            # Add a success message
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('user_register')
    else:
        return render(request, "user/user_register.html")
    


def user_login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')

        user = User.objects.filter(username=uname).first()
        
        if user is not None and user.check_password(passw) and user:
            login(request, user)
            return redirect('user_home')
        else:
            messages.error(request, 'Invalid login credentials.')

    return render(request, 'user/user_login.html')


def user_home(request):
    return render(request, 'user/user_home.html')



def admin_login(request):
     if request.method == "POST":
          username = request.POST['uname']
          password = request.POST['pswd']
          user = authenticate(request, username=username, password=password)
          if user is not None:
               login(request,user)
               return redirect("admins_home")
          else:
               messages.info(request,'Username or password incorrect')
               return redirect('admin_login')


     return render(request,'encadmin/admin_login.html')


def admins_home(request):
    return render(request, 'encadmin/admins_home.html')


def SignOut(request):
     logout(request)
     return redirect('admin_login')


# def text_enc(request):
#     users = User.objects.filter(is_superuser=False)
#     context = {'users':users}
#     return render(request, 'encadmin/text_enc.html', context)

def encrypt(message):
    # Convert the message to uppercase
    message = message.upper()

    # Define the DNA encoding dictionary
    encoding_dict = {'A': 'AT', 'T': 'TA', 'C': 'CG', 'G': 'GC'}

    # Encode the message using DNA encoding
    encrypted = ''
    for char in message:
        # Check if the character is in the encoding dictionary
        if char in encoding_dict:
            encrypted += encoding_dict[char]
        else:
            # If the character is not in the dictionary, add a random nucleotide pair
            nucleotides = ['A', 'T', 'C', 'G']
            random_pair = random.choice(nucleotides) + random.choice(nucleotides)
            encrypted += random_pair
    return encrypted

def text_enc(request):
    if request.method == 'POST':
        # Retrieve form data
        original_text = request.POST.get('text', '')
        key = request.POST.get('key', '')
        user_name = request.POST.get('dropdown', '')

        # Validate form data
        if not original_text or not key or not user_name:
            messages.error(request, 'Please fill in all fields.')
            return redirect('text_enc')

        # Convert the original text to uppercase
        original_text = original_text.upper()

        # Encrypt the original text using the DNA algorithm
        encrypted_text = encrypt(original_text)

        # Save the data to the database
        text_object = Text.objects.create(
            textfield=original_text,
            encrypted_text=encrypted_text,
            key=key,
            user_name=user_name
        )

        # Display confirmation
        context = {
            'original_text': original_text,
            'encrypted_text': encrypted_text,
            'key': key,
            'user_name': user_name,
        }
        return render(request, 'encadmin/text_enc.html', context)

    else:
        users = User.objects.filter(is_superuser=False)
        context = {'users': users}
        return render(request, 'encadmin/text_enc.html', context)



def manage_users(request):
    users = User.objects.filter(is_superuser=False)
    context = {'users': users}    
    return render(request, 'encadmin/manage_users.html', context)
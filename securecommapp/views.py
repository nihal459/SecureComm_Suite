from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import random
from django.contrib.auth.decorators import login_required

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


@login_required
def view_texts(request):
    current_user = request.user.username
    texts = Text.objects.filter(user_name=current_user) | Text.objects.filter(user_name="for everyone")
    context = {'texts': texts}
    return render(request, 'user/view_texts.html', context)

def view_text_msg(request, pk):
    msg = get_object_or_404(Text, pk=pk)
    password = msg.key
    if request.method == "POST":
        entered_password = request.POST.get('password')
        # Check if entered password matches the correct password
        if entered_password == password:  # Replace 'correct_password' with your actual password
            return render(request, 'user/view_text_msg.html', {'msg': msg})
        else:
            error_message = "Invalid credentials. Please try again."
            return render(request, 'user/view_text_msg.html', {'error_message': error_message})
    return render(request, 'user/view_text_msg.html')


def mark_read(request, pk):
    msg = get_object_or_404(Text, pk=pk)
    
    msg.read = not msg.read
    msg.save()
    
    return redirect('view_texts')




@login_required
def view_files(request):
    current_user = request.user.username
    texts = File.objects.filter(user_name=current_user) | File.objects.filter(user_name="for everyone")
    context = {'texts': texts}
    return render(request, 'user/view_files.html', context)



def view_file_msg(request, pk):
    msg = get_object_or_404(File, pk=pk)
    password = msg.key
    if request.method == "POST":
        entered_password = request.POST.get('password')
        # Check if entered password matches the correct password
        if entered_password == password:  # Replace 'correct_password' with your actual password
            return render(request, 'user/view_file_msg.html', {'msg': msg})
        else:
            error_message = "Invalid credentials. Please try again."
            return render(request, 'user/view_file_msg.html', {'error_message': error_message})
    return render(request, 'user/view_file_msg.html')



from django.http import HttpResponse
from django.conf import settings
import os
import mimetypes

def serve_file(request, file_path):
    # Build the absolute file path
    absolute_file_path = os.path.join(settings.MEDIA_ROOT, file_path)

    # Check if the file exists
    if os.path.exists(absolute_file_path):
        # Open the file in binary mode and read its content
        with open(absolute_file_path, 'rb') as f:
            file_content = f.read()
        
        # Determine the file's content type
        content_type, _ = mimetypes.guess_type(absolute_file_path)
        if not content_type:
            content_type = 'application/octet-stream'

        # Create the HttpResponse object with the appropriate content type
        response = HttpResponse(file_content, content_type=content_type)
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(absolute_file_path)
        return response
    else:
        # Return a 404 response if the file does not exist
        return HttpResponse('File not found', status=404)



def mark_read2(request, pk):
    msg = get_object_or_404(File, pk=pk)
    
    msg.read = not msg.read
    msg.save()
    
    return redirect('view_files')



@login_required
def view_images(request):
    current_user = request.user.username
    texts = Image.objects.filter(user_name=current_user) | Image.objects.filter(user_name="for everyone")
    context = {'texts': texts}
    return render(request, 'user/view_images.html', context)




def view_image_msg(request, pk):
    msg = get_object_or_404(Image, pk=pk)
    password = msg.key
    if request.method == "POST":
        entered_password = request.POST.get('password')
        # Check if entered password matches the correct password
        if entered_password == password:  # Replace 'correct_password' with your actual password
            return render(request, 'user/view_image_msg.html', {'msg': msg})
        else:
            error_message = "Invalid credentials. Please try again."
            return render(request, 'user/view_image_msg.html', {'error_message': error_message})
    return render(request, 'user/view_image_msg.html')



def mark_read3(request, pk):
    msg = get_object_or_404(Image, pk=pk)
    
    msg.read = not msg.read
    msg.save()
    
    return redirect('view_images')




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
     return redirect('index')



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
    texts = Text.objects.all()
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
        context = {'users': users,'texts':texts}
        return render(request, 'encadmin/text_enc.html', context)



def manage_users(request):
    users = User.objects.filter(is_superuser=False)
    context = {'users': users}    
    return render(request, 'encadmin/manage_users.html', context)


def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('manage_users')  



def verify_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.verified = not user.verified
    user.save()
    return redirect('manage_users')  


# from PyPDF2 import PdfReader
# from .models import File

# def file_enc(request):
#     files = File.objects.all()

#     if request.method == 'POST':
#         # Retrieve form data
#         uploaded_file = request.FILES.get('file')
#         key = request.POST.get('key', '')
#         user_name = request.POST.get('dropdown', '')

#         # Validate form data
#         if not uploaded_file or not key or not user_name:
#             messages.error(request, 'Please fill in all fields.')
#             return redirect('file_enc')

#         # Read content from uploaded file
#         if uploaded_file.name.endswith('.docx'):
#             messages.error(request, 'Unsupported file format. Please upload a .pdf file.')
#             return redirect('file_enc')

#         elif uploaded_file.name.endswith('.pdf'):
#             # Handle PDF document
#             with uploaded_file.open('rb') as f:
#                 pdf_reader = PdfReader(f)
#                 content = ''
#                 for page in pdf_reader.pages:
#                     content += page.extract_text()

#                 # Encrypt the content using the DNA algorithm
#                 encrypted_content = encrypt(content)

#                 # Save the data to the database
#                 file_object = File.objects.create(
#                     original_file=uploaded_file,
#                     encrypted_file=encrypted_content,
#                     key=key,
#                     user_name=user_name
#                 )

#                 # Display confirmation
#                 context = {
#                     'original_file_name': uploaded_file.name,
#                     'encrypted_file_content': encrypted_content,
#                     'key': key,
#                     'user_name': user_name,
#                 }
#                 return render(request, 'encadmin/file_enc.html', context)

#         else:
#             # Unsupported file format
#             messages.error(request, 'Unsupported file format. Please upload a .pdf file.')
#             return redirect('file_enc')

#     else:
#         users = User.objects.filter(is_superuser=False)
#         return render(request, 'encadmin/file_enc.html', {'users': users, 'files':files})





# import os
# from PyPDF2 import PdfWriter, PdfReader
# from io import BytesIO
# from reportlab.pdfgen import canvas

# def file_enc(request):
#     files = File.objects.all()

#     if request.method == 'POST':
#         # Retrieve form data
#         uploaded_file = request.FILES.get('file')
#         key = request.POST.get('key', '')
#         user_name = request.POST.get('dropdown', '')

#         # Validate form data
#         if not uploaded_file or not key or not user_name:
#             messages.error(request, 'Please fill in all fields.')
#             return redirect('file_enc')

#         # Read content from uploaded file
#         if uploaded_file.name.endswith('.docx'):
#             messages.error(request, 'Unsupported file format. Please upload a .pdf file.')
#             return redirect('file_enc')

#         elif uploaded_file.name.endswith('.pdf'):
#             # Handle PDF document
#             with uploaded_file.open('rb') as f:
#                 pdf_reader = PdfReader(f)
#                 content = ''
#                 for page in pdf_reader.pages:
#                     content += page.extract_text()

#                 # Encrypt the content using the DNA algorithm
#                 encrypted_content = encrypt(content)

#                 # Create a new PDF with the encrypted text
#                 output_pdf = BytesIO()
#                 c = canvas.Canvas(output_pdf)
#                 c.drawString(100, 800, encrypted_content)  # Adjust coordinates as needed
#                 c.save()

#                 # Create the directory if it doesn't exist
#                 output_directory = 'files/encrypted/'
#                 os.makedirs(output_directory, exist_ok=True)

#                 # Save the PDF to the files/encrypted/ folder
#                 encrypted_file_path = output_directory + uploaded_file.name  # You can modify the file name as needed
#                 with open(encrypted_file_path, 'wb') as encrypted_file:
#                     encrypted_file.write(output_pdf.getvalue())

#                 # Save the data to the database
#                 file_object = File.objects.create(
#                     original_file=uploaded_file,
#                     encrypted_file=encrypted_file_path,
#                     key=key,
#                     user_name=user_name
#                 )

#                 # Display confirmation
#                 context = {
#                     'original_file_name': uploaded_file.name,
#                     'encrypted_file_content': encrypted_content,
#                     'key': key,
#                     'user_name': user_name,
#                 }
#                 return render(request, 'encadmin/file_enc.html', context)

#         else:
#             # Unsupported file format
#             messages.error(request, 'Unsupported file format. Please upload a .pdf file.')
#             return redirect('file_enc')

#     else:
#         users = User.objects.filter(is_superuser=False)
#         return render(request, 'encadmin/file_enc.html', {'users': users, 'files': files})



# import os
# from PyPDF2 import PdfWriter, PdfReader
# from io import BytesIO
# from reportlab.pdfgen import canvas
# from django.conf import settings

# def file_enc(request):
#     files = File.objects.all()

#     if request.method == 'POST':
#         # Retrieve form data
#         uploaded_file = request.FILES.get('file')
#         key = request.POST.get('key', '')
#         user_name = request.POST.get('dropdown', '')

#         # Validate form data
#         if not uploaded_file or not key or not user_name:
#             messages.error(request, 'Please fill in all fields.')
#             return redirect('file_enc')

#         # Read content from uploaded file
#         if uploaded_file.name.endswith('.docx'):
#             messages.error(request, 'Unsupported file format. Please upload a .pdf file.')
#             return redirect('file_enc')

#         elif uploaded_file.name.endswith('.pdf'):
#             # Handle PDF document
#             with uploaded_file.open('rb') as f:
#                 pdf_reader = PdfReader(f)
#                 content = ''
#                 for page in pdf_reader.pages:
#                     content += page.extract_text()

#                 # Encrypt the content using the DNA algorithm
#                 encrypted_content = encrypt(content)

#                 # Create a new PDF with the encrypted text
#                 output_pdf = BytesIO()
#                 c = canvas.Canvas(output_pdf)
#                 c.drawString(100, 800, encrypted_content)  # Adjust coordinates as needed
#                 c.save()

#                 # Create the directory if it doesn't exist
#                 output_directory = os.path.join(settings.MEDIA_ROOT, 'files', 'encrypted')
#                 os.makedirs(output_directory, exist_ok=True)

#                 # Save the PDF to the files/encrypted/ folder
#                 encrypted_file_path = os.path.join(output_directory, uploaded_file.name)  # You can modify the file name as needed
#                 with open(encrypted_file_path, 'wb') as encrypted_file:
#                     encrypted_file.write(output_pdf.getvalue())

#                 # Save the data to the database
#                 file_object = File.objects.create(
#                     original_file=uploaded_file,
#                     encrypted_file=encrypted_file_path,
#                     key=key,
#                     user_name=user_name
#                 )

#                 # Display confirmation
#                 context = {
#                     'original_file_name': uploaded_file.name,
#                     'encrypted_file_content': encrypted_content,
#                     'key': key,
#                     'user_name': user_name,
#                 }
#                 return render(request, 'encadmin/file_enc.html', context)

#         else:
#             # Unsupported file format
#             messages.error(request, 'Unsupported file format. Please upload a .pdf file.')
#             return redirect('file_enc')

#     else:
#         users = User.objects.filter(is_superuser=False)
#         return render(request, 'encadmin/file_enc.html', {'users': users, 'files': files})



import os
from PyPDF2 import PdfWriter, PdfReader
from io import BytesIO
from reportlab.pdfgen import canvas
from django.conf import settings

def chunk_text(text, chunk_size):
    """Helper function to chunk text into lines with a maximum length."""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def file_enc(request):
    files = File.objects.all()

    if request.method == 'POST':
        # Retrieve form data
        uploaded_file = request.FILES.get('file')
        key = request.POST.get('key', '')
        user_name = request.POST.get('dropdown', '')

        # Validate form data
        if not uploaded_file or not key or not user_name:
            messages.error(request, 'Please fill in all fields.')
            return redirect('file_enc')

        # Read content from uploaded file
        if uploaded_file.name.endswith('.docx'):
            messages.error(request, 'Unsupported file format. Please upload a .pdf file.')
            return redirect('file_enc')

        elif uploaded_file.name.endswith('.pdf'):
            # Handle PDF document
            with uploaded_file.open('rb') as f:
                pdf_reader = PdfReader(f)
                content = ''
                for page in pdf_reader.pages:
                    content += page.extract_text()

                # Encrypt the content using the DNA algorithm
                encrypted_content = encrypt(content)

                # Chunk the text into lines with a maximum length of 25 characters
                lines = chunk_text(encrypted_content, 35)

                # Create a new PDF with the encrypted text
                output_pdf = BytesIO()
                c = canvas.Canvas(output_pdf)
                y_coordinate = 800  # Starting y-coordinate
                for line in lines:
                    c.drawString(100, y_coordinate, line)  # Adjust x-coordinate as needed
                    y_coordinate -= 20  # Adjust line spacing as needed
                c.save()

                # Create the directory if it doesn't exist
                output_directory = os.path.join(settings.MEDIA_ROOT, 'files', 'encrypted')
                os.makedirs(output_directory, exist_ok=True)

                # Save the PDF to the files/encrypted/ folder
                encrypted_file_path = os.path.join(output_directory, uploaded_file.name)  # You can modify the file name as needed
                with open(encrypted_file_path, 'wb') as encrypted_file:
                    encrypted_file.write(output_pdf.getvalue())

                # Save the data to the database
                file_object = File.objects.create(
                    original_file=uploaded_file,
                    encrypted_file=encrypted_file_path,
                    key=key,
                    user_name=user_name
                )

                # Display confirmation
                context = {
                    'original_file_name': uploaded_file.name,
                    'encrypted_file_content': encrypted_content,
                    'key': key,
                    'user_name': user_name,
                }
                return redirect('file_enc')

        else:
            # Unsupported file format
            messages.error(request, 'Unsupported file format. Please upload a .pdf file.')
            return redirect('file_enc')

    else:
        users = User.objects.filter(is_superuser=False)
        return render(request, 'encadmin/file_enc.html', {'users': users, 'files': files})



# delete_file
from django.shortcuts import render, redirect
from django.conf import settings
from stegano import lsb
import os

def image_enc(request):
    users = User.objects.filter(is_superuser=False)
    images = Image.objects.all()
    if request.method == 'POST':
        # Get form data
        uploaded_file = request.FILES['file']
        key = request.POST.get('key')
        message = request.POST.get('message')
        user_name = request.POST.get('dropdown')

        # Perform validation for PNG file
        if not uploaded_file.name.endswith('.png'):
            return render(request, 'encadmin/image_enc.html', {'error': 'Please upload a PNG file', 'users': users})

        # Construct file paths
        original_image_path = os.path.join(settings.MEDIA_ROOT, 'Original_Image', uploaded_file.name)
        encrypted_image_path = os.path.join(settings.MEDIA_ROOT, 'Steganographed_Image', uploaded_file.name)

        # Save original image to the specified folder
        with open(original_image_path, 'wb') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # Perform steganography
        secret = lsb.hide(original_image_path, message)
        secret.save(encrypted_image_path)

        # Save original and encrypted images to the database
        # original_image = Image.objects.create(original_file='Original_Image/' + uploaded_file.name, message=message, key=key, user_name=user_name)
        encrypted_image = Image.objects.create(original_file='Original_Image/' + uploaded_file.name, encrypted_file='Steganographed_Image/' + uploaded_file.name, message=message, key=key, user_name=user_name)

        return redirect('image_enc')  # Redirect to the same page after successful encryption

    return render(request, 'encadmin/image_enc.html', {'users': users, 'images':images})



def delete_file(request, pk):
    # Retrieve the file object from the database
    file_obj = get_object_or_404(File, pk=pk)

    # Delete associated files from the file system
    original_file_path = file_obj.original_file.path
    encrypted_file_path = file_obj.encrypted_file.path

    if os.path.exists(original_file_path):
        os.remove(original_file_path)
    if os.path.exists(encrypted_file_path):
        os.remove(encrypted_file_path)

    # Delete the file object from the database
    file_obj.delete()

    # Redirect to a success page
    return redirect('file_enc')



def delete_image(request, pk):
    # Retrieve the image object from the database
    image_obj = get_object_or_404(Image, pk=pk)

    # Delete image files from the file system
    if image_obj.original_file:
        if os.path.exists(image_obj.original_file.path):
            os.remove(image_obj.original_file.path)
    if image_obj.encrypted_file:
        if os.path.exists(image_obj.encrypted_file.path):
            os.remove(image_obj.encrypted_file.path)

    # Delete the image object from the database
    image_obj.delete()

    # Redirect to a success page
    return redirect('image_enc') 


def delete_text(request, pk):
    # Retrieve the text object from the database
    text_obj = get_object_or_404(Text, pk=pk)

    # Delete the text object from the database
    text_obj.delete()

    # Redirect to a success page
    return redirect('text_enc')
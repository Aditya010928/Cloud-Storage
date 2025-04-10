
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from .models import EncryptedFile
from .crypto_utils import get_fernet
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

@login_required
def dashboard(request):
    files = EncryptedFile.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'files': files})

@login_required

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            password = form.cleaned_data['password']

            # Encrypt the file
            fernet = get_fernet(password)
            encrypted_data = fernet.encrypt(file.read())

            # Create model entry with empty file
            new_file = EncryptedFile.objects.create(
                user=request.user,
                file=None,
                filename=file.name
            )

            # Define upload path safely
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)  # ✅ Ensure folder exists

            path = os.path.join(upload_dir, f"{new_file.id}_{file.name}")
            with open(path, 'wb') as f:
                f.write(encrypted_data)

            # Update file field with relative path
            new_file.file.name = f'uploads/{new_file.id}_{file.name}'
            new_file.save()

            return redirect('dashboard')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

@login_required
def decrypt_file(request, file_id):
    if request.method == 'POST':
        password = request.POST['password']
        f_obj = EncryptedFile.objects.get(id=file_id, user=request.user)
        fernet = get_fernet(password)
        with open(f_obj.file.path, 'rb') as f:
            encrypted_data = f.read()
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
        except Exception:
            return HttpResponse("Wrong password")
        response = HttpResponse(decrypted_data, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{f_obj.filename}"'
        return response
    return render(request, 'decrypt.html', {'file_id': file_id})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

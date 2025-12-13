from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# ------------------ LOGIN ------------------
def logindj(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('producto')

            return redirect('menu')

        else:
            return render(request, 'login.html', {
                'error': 'Usuario y/o clave incorrecto'
            })

    return render(request, 'login.html')



def registerdj(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'register.html', {'error': 'Las contraseñas no coinciden'})
        if User.objects.filter(username=email).exists():
            return render(request, 'register.html', {'error': 'Este usuario ya existe'})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Ya se registró un usuario con este correo'})

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        login(request, user)
        return redirect('menu')

    return render(request, 'register.html')

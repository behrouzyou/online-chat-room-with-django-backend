from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from chat.models import Room,Message
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
    else:
        form =UserCreationForm()
    return render(request,'chat/register.html',{'form':form})


def login_view(request):
    if request.method =='POST':
        username =request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request,'chat/login.html',{'error':'نام کاربری یا رمز عبور اشتباه است'})
    return render(request,'chat/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    if request.method == "POST":
        room_name =request.POST.get('room_name').strip()
        if room_name:
            Room.objects.get_or_create(name=room_name)
            return redirect('home')
    rooms =Room.objects.all()
    return render(request,'chat/home.html',{'rooms':rooms})
@login_required
def room_view(request,room_name):
    room, created = Room.objects.get_or_create(name=room_name)

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                room=room,
                user=request.user,
                content=content
            )
        return redirect('room', room_name=room_name)

    messages = Message.objects.filter(room=room).select_related('user').order_by('created_at')
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages,
    })
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Task, Bid

def home(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/home.html', {'tasks': tasks})

def generate_ai_risks(title, description):
    text = (title + " " + description).lower()
    if 'python' in text or 'django' in text or 'backend' in text or 'code' in text:
        return "1. Risk of database performance bottlenecks and scalability issues.\n2. Potential security vulnerabilities in backend data handling."
    elif 'design' in text or 'ui' in text or 'frontend' in text or 'landing' in text:
        return "1. Risk of browser compatibility issues across different devices.\n2. Potential delays due to multiple revisions in UI/UX requirements."
    else:
        return "1. Risk of scope creep and unclear project requirements.\n2. Potential timeline delays due to external dependencies."

@login_required
def post_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        budget = request.POST.get('budget')
        description = request.POST.get('description')
        
        # توليد تقييم المخاطر تلقائياً بناءً على العنوان والوصف
        risks = generate_ai_risks(title, description)
        
        Task.objects.create(
            title=title,
            category=category,
            budget=budget,
            description=description,
            created_by=request.user,
            risk_assessment=risks
        )
        return redirect('home')
    return render(request, 'tasks/post_task.html')

def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST' and request.user.is_authenticated:
        amount = request.POST.get('amount')
        message = request.POST.get('message')
        
        Bid.objects.create(
            task=task,
            freelancer=request.user,
            amount=amount,
            message=message
        )
        return redirect('task_detail', task_id=task.id)
        
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # التأكد أن المستخدم الحالي هو صاحب المهمة فقط قبل الحذف
    if request.user == task.created_by:
        task.delete()
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    my_tasks = Task.objects.filter(created_by=request.user)
    my_bids = Bid.objects.filter(freelancer=request.user)
    return render(request, 'tasks/profile.html', {
        'my_tasks': my_tasks,
        'my_bids': my_bids
    })

@login_required
def accept_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)
    task = bid.task
    
    if request.user == task.created_by:
        task.status = 'Assigned'
        task.save()
        
    return redirect('task_detail', task_id=task.id)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from django.utils import timezone

def home(request):
    projects = Project.objects
    return render(request, 'projects/home.html', {'projects': projects})

@login_required(login_url="/accounts/signup")
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            project = Project()
            project.title = request.POST['title']
            project.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                project.url = request.POST['url']
            else:
                project.url = 'http://'+ request.POST['url']
            project.icon = request.FILES['icon']
            project.image = request.FILES['image']
            project.pub_date = timezone.datetime.now()
            project.votes_total = 0
            project.stormer = request.user
            project.save()
            return redirect('/projects/' + str(project.id))
        else:
            return render(request, 'projects/create.html', {'error': 'All fields are required.'})

    else:
        return render(request, 'projects/create.html')

def detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'projects/detail.html', {'project':project})

@login_required(login_url="/accounts/signup")
def upvote(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=project_id)
        project.votes_total += 1
        project.save()
        return redirect('/projects/' + str(project.id))

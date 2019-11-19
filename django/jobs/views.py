import logging
import os

from django.contrib.auth.models import Group, User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_safe
from django.views.generic import ListView, DetailView, DeleteView
from rest_framework import viewsets

from jobs.models import JobModel
from jobs.serializers import (
    GroupSerializer, JobSerializer, UserSerializer
)
from jobs.scheduler.jobs import Jobs
from mysite.settings import BASE_DIR
from jobs.util.file_util import FileUtil

REPO_URL = 'https://github.com/mkoertgen/hello.django-jobs'
LOGGER = logging.getLogger(__name__)


@require_safe
def index(request):
    context = {
        'app': {
            'git': REPO_URL,
            'wiki': 'https://github.com/mkoertgen/hello.django-jobs/wiki'
        }
    }
    return render(request, 'jobs/index.html', context)


@require_safe
def about(request):
    context = {
        'git': {
            'commit': os.environ.get('OPENSHIFT_BUILD_COMMIT', 'master'),
            'repository': {
                'source': os.environ.get('OPENSHIFT_BUILD_SOURCE', REPO_URL),
                'commits': f"{REPO_URL}/commits"
            }
        }
    }
    return render(request, 'jobs/about.html', context)


@cache_control(public=True, max_age=60 * 60)
@require_safe
def docs(request):
    file_path = request.path.replace('/jobs/docs', '').strip(' /')
    if not file_path:
        return redirect('/jobs/docs/index.md')
    file_path = f"{BASE_DIR}/docs/{file_path}"
    is_markdown = file_path.endswith('.md')
    if not is_markdown:
        return HttpResponse(FileUtil.read_bytes(file_path))
    context = {
        'content': FileUtil.read_text(file_path)
    }
    return render(request, 'jobs/docs.html', context)


class JobList(ListView):
    def get(self, request):
        context = {
            'jobs': Jobs.all(),
            'executions': JobModel.objects.all().order_by('-updated_at')
        }
        return render(request, 'jobs/jobs.html', context)

    def post(self, request):
        job_class_name = request.POST['job_class']
        LOGGER.info("Scheduling '%s'...", job_class_name)
        job = Jobs.create(job_class_name)
        job.perform_later()
        return HttpResponseRedirect(job.job_model.get_absolute_url())


class JobDetail(DetailView):
    model = JobModel
    context_object_name = 'job'


class JobDelete(DeleteView):
    model = JobModel
    success_url = reverse_lazy('jobs')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = JobModel.objects.all().order_by('-updated_at')
    serializer_class = JobSerializer

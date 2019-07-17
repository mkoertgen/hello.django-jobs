from django.contrib.auth.models import User, Group
from rest_framework import serializers
from jobs.models import JobModel


class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Group
    fields = ('url', 'name')


class JobSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = JobModel
    fields = ('url', 'created_at', 'updated_at', 'job_class',
              'status', 'started', 'finished', 'duration', 'logs')

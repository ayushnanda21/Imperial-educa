from rest_framework import generics
from rest_framework import response
from ..models import Subject
from .serializers import SubjectSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Course


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class CourseEnrollView(APIView):
    def post(self,request, pk ,format= None):
        course =  get_object_or_404(Course, pk= pk)
        course.students.add(request.user)
        return response({'enrolled': True})
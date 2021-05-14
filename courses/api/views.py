from rest_framework import generics
from rest_framework import response
from ..models import Subject
from .serializers import SubjectSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Course
from rest_framework.decorators import detail_route
from .permissions import IsEnrolled
from .serializers import CourseWithContentsSerializer

#to handle authentication for API
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

#routers
from rest_framework import viewsets
from .serializers import CourseSerializer


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

    authentication_classes = (BasicAuthentication,)

    permission_classes = (IsAuthenticated,)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset =  Course.objects.all()
    serializer_class= CourseSerializer

    @detail_route(methods=['post'],
    authentication_classes=[BasicAuthentication],
    permission_classes=[IsAuthenticated])


    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response({'enrolled': True})

    @detail_route(methods=['get'],
    serializer_class=CourseWithContentsSerializer,
    authentication_classes=[BasicAuthentication],
    permission_classes=[IsAuthenticated,IsEnrolled])
    
    def contents(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


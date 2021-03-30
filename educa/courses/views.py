from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from .models import Course

# Create your views here.
class ManagerCourseListView(ListView):
    model= Course
    template_name = 'courses/manage/course/list.html'


    def get_queryset(self):
        qs = super(ManagerCourseListView, self).get_queryset()
        return qs.filter(owner =self.request.user)

class OwnerMixin(object):
    def def get_queryset(self):
        qs =super(OwnerMixin,self).get_queryset()
        return qs.filter(owner = self.request.user)
        
    

class OwnerEditMixin(Object):
    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin ,self).form_valid(form)

class OwnerCourseMixin(OwnerMixin):
    model = Course

class OwnerCourseEditMixin(OwnerCourseMixin ,OwnerEditMixin):
    fields = ['subject' , 'title' , 'slug' , 'overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/form.html'

class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name ='courses/manage/course/list.html'

class CourseCreateView(OwnerCourseEditMixin , CreateView):
    pass

class CourseUpdateView(OwnerCourseEditMixin , UpdateView):
    pass

class CourseDeleteView(OwnerCourseMixin ,DeleteView):
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')


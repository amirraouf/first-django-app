from django.shortcuts import render, redirect
from courses.models import *
from courses.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response , get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
import json
from django.core import serializers


def home(request):

    return render(request, 'categories/home.html', {})


def categories(request):
    it = Category.objects.filter(name__contains='IT')
    business = Category.objects.filter(name__contains='Business')
    hr = Category.objects.filter(name__contains='HR')
    lang = Category.objects.filter(name__contains='Languages')
    art = Category.objects.filter(name__contains='Art and design')
    academic = Category.objects.filter(name__contains='Academic')

    context = {
        "it": it,
        "business": business,
        "hr": hr,
        "lang": lang,
        "art": art,
        "academic": academic,
    }
    return render(request, 'categories/categories.html', context)


def categories_pages(request, category_name):
    spec = Specialization.objects.filter(
        id_S__name__icontains=category_name
    ).order_by('name')

    context = {
        "spec": spec,
        "category": category_name
    }
    return render(request, 'categories/categories-page.html', context)



def specs_categories_pages(request, category_name, spec_name):
    category = Category.objects.filter(name__contains=category_name)
    courses = Course_dir.objects.filter(
        availability=True,
        id_CO__id_S__name=category_name
    ).order_by('date')

    courses_spec = Course_dir.objects.filter(
        availability=True,
        id_CO__name=spec_name
    ).order_by('date')

    spec = Specialization.objects.filter(
        id_S__name__icontains=category_name
    ).order_by('name')

    context = {
        "courses": courses,
        "spec": spec,
        "courses_spec": courses_spec,
        "category": category_name
    }

    return render(request, 'categories/specialization-page.html',context)


def profiler(request, slug):
    person = Person.objects.get(username=slug)

    context = {'user': person,
               }
    return render(request, 'profiler/profile_user.html', context)


def courses_detail(request, course_name):
    course=get_object_or_404(Course_dir, name=course_name)

    spec = course.id_CO.name
    category = course.id_CO.id_S.name
    date = course.date
    x = "{:%B %d, %Y, %H}".format(date)
    # y = "{:%Y-%m-%d %H:%M}".format(date)
    month = x.split(",",1)[0]
    hours = x.split(",",1)[1].split(",",1)[1]
    choice = ['a.m','p.m']

    if int(hours)>12:
        AorP = choice[1]
    else:
        AorP = choice[0]
    hours = (int(hours)-10)%12

    context = {'spec':spec,
               'course':course,
               'category':category,
               'month':month,
               'hours':hours,
               'AorP':AorP,
               }
    return render(request, 'categories/courses.html',context)


@csrf_protect
def register(request):
    if request.method == 'POST':

        form = RegistrationForm(request.POST)
        if form.is_valid():

            return HttpResponseRedirect('registration/choose_your_type.html',)
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})

    return render_to_response('registration/registration_form.html', variables)

@csrf_protect
def choose_your_type(request):
    c = request.POST['choice']
    person = Person.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    email=request.POST['email'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],)
    if request.method == 'POST':
        uform = User_profile(request.POST)
        iform = Instructor_profile(request.POST)
        tform = Training_center_profile(request.POST)
        if c == 'User':

            #Go_User.objects.create(person=person)
            if uform.is_valid():
                user = Go_User.objects.create(person=person,
                                              age=uform.cleaned_data['age'],
                                              mobile=uform.cleaned_data['mobile'],
                                              img=uform.cleaned_data['image'])
                user.save()
                return HttpResponse('registration/user_registration_form.html', {'uform': uform})

        elif c == 'Instructor':

            #Training_Center.objects.create(Person=Person)
            return render(request,'registration/instructor_registration_form.html', {'iform': iform})

        else:

            #Instructor.objects.create(Person=Person)
            return render(request,'registration/training_center_registration_form.html', {'tform': tform})
    else:
        uform = RegistrationForm()
    return render_to_response('registration/registration_form.html', context_instance = RequestContext(request))



def register_success(request):
    Person.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    email=request.POST['email'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],)
    return render_to_response('registration/registration_complete.html', {})


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

#
# @login_required
# def home(request):
#     return render_to_response('categories/home.html', {'user': request.user})

@csrf_protect
def c_login(request):
    username = request.POST.get('username',False)
    password = request.POST.get('password','')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render_to_response('categories/home.html', {'user': request.user})
        else:
            return render_to_response(register)

    else:
        pass


def course_create(request):
    form = courses
    return render_to_response('categories/nothing.html', {'form':form})
#
# def like(request, course_id):
#     new_like, created = Like.objects.get_or_create(user=request.user, course=course_id)
#     if not created:
#         pass
#     else:
#         pass

# def upload_pic(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             m = Users.objects.get(pk=Users.id_US)
#             m.pro_picture = form.cleaned_data['image']
#             m.save()
#             return HttpResponse('image upload success')

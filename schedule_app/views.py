from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login as login_view, logout as logout_view
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime

from .models import AvailableTimes, Profile, Role

def login(request):
    context = {}
    return render(request, 'login.html', context)


@login_required
def index(request):
    profile = Profile.objects.get(user = request.user)
    role = profile.role.role_name
    if role == 'HR':
        bln_role = True
    else:
        bln_role = False
    context = {'bln_role':bln_role,'add_user':False}
    return render(request, 'index.html', context)


class LoginUserView(View):

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login_view(request, user)
            return redirect('index') 
        else:
            return JsonResponse({'status': 'failed','message':'Username or Password Mismatch'})

def logout_user(request):
    logout_view(request)
    return redirect('login')

@login_required
def add_users(request):
    profile = Profile.objects.get(user = request.user)
    role = profile.role.role_name
    if role == 'HR':
        bln_role = True
    else:
        bln_role = False
    roles = Role.objects.values()
    users = Profile.objects.values('id','role__role_name','unique_id','user__first_name','user__last_name','user__email','user__username')
    context = {'bln_role':bln_role,'add_user':True, 'roles':roles,'users':users}
    return render(request, 'add_user.html', context)


class SaveUserView(View):

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        username = request.POST.get('username')
        password = request.POST.get('password')
        id = request.POST.get('id')
        try:
            already_exist = User.objects.filter(username = username)
            if already_exist:
                return JsonResponse({'status': 'failed','message':'Username already exist'})
            else:
                user = User.objects.create_user(username, email, password) 
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                profile = Profile.objects.create(user = user, role = Role.objects.get(id = role), unique_id = id)
                return JsonResponse({'status': 'success','message':'Added Successfully'})
        except Exception as e:
            return JsonResponse({'status': 'failed','message':str(e)})

class SaveAvailableTimeView(View):

    def post(self, request):
        available_time_from = request.POST.get('available_time_from')
        available_time_to = request.POST.get('available_time_to')
        available_time_from = available_time_from[:-2]+'00'
        available_time_to = available_time_to[:-2]+'00'
        user = Profile.objects.get(user = request.user)
        try:
            already_exist = AvailableTimes.objects.filter(user = user, available_time_from = available_time_from, available_time_to = available_time_to)
            if already_exist:
                return JsonResponse({'status': 'failed','message':'Already exist'})
            else:
                AvailableTimes.objects.create(user = user, available_time_from = available_time_from, available_time_to = available_time_to)
                return JsonResponse({'status': 'success','message':'Added Successfully'})
        except Exception as e:
            return JsonResponse({'status': 'failed','message':str(e)})

class SearchAvailableTimesView(View):

    def post(self, request):
        try:
            candidate_id = request.POST.get('candidate_id')
            interviewer_id = request.POST.get('interviewer_id')
            if candidate_id.upper() == interviewer_id.upper():
                return JsonResponse({'status': 'failed','message':'Same Id given for both'})
            try:
                candidate = Profile.objects.get(unique_id__iexact = candidate_id)
            except:
                return JsonResponse({'status': 'failed','message':'Candidate Id Note Found'})
            try:
                interviewer = Profile.objects.get(unique_id__iexact = interviewer_id)
            except:
                return JsonResponse({'status': 'failed','message':'Interviewer Id Note Found'})
            available_times_of_interviewer = AvailableTimes.objects.filter(user = interviewer).values('available_time_from','available_time_to')
            lst_times = []
            for item in available_times_of_interviewer:
                available_times_of_candidate = AvailableTimes.objects.filter(user = candidate).values('available_time_from','available_time_to')
                for value in available_times_of_candidate:
                    times = []
                    if item['available_time_from'] < value['available_time_from']:
                        from_time = value['available_time_from']
                    else:
                        from_time = item['available_time_from']
                    if item['available_time_to'] < value['available_time_to']:
                        to_time = item['available_time_to']
                    else:
                        to_time = value['available_time_to']
                    max_time = from_time.hour
                    while max_time < to_time.hour:
                        if max_time < 12 or max_time == 24:
                            f_time = str(max_time) + ' AM'
                        elif max_time == 12:
                            f_time = str(max_time) + ' PM'
                        else:
                            f_time = str(max_time-12)+' PM'
                        if max_time+1 < 12 or max_time+1 == 24:
                            t_time = str(max_time+1) + ' AM'
                        elif max_time+1 == 12:
                            t_time = str(max_time+1) + ' PM'
                        else:
                            t_time = str(max_time+1-12) + ' PM'
                        times.append((f_time,t_time))
                        max_time += 1
                    lst_times.append({'date':datetime.strftime(from_time,'%d-%m-%Y'),'times':times})
            return JsonResponse({'status': 'success','lst_times':lst_times})
        except Exception as e:
            return JsonResponse({'status': 'failed','message':str(e)})
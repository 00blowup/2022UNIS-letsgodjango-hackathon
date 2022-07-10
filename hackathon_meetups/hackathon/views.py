from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ApplicationForm
from .models import Application
from django.db.models import ObjectDoesNotExist

# Create your views here.


# 첫 페이지
def index(request):
    context = {}
    return render(request, 'pages/index.html', context)


# 로그인 페이지
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=email, password=password)
            if user:    # if user is not None과 같은 말임.
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.warning(request, '계정 혹은 비밀번호를 확인해주세요.')
    else:
        form = LoginForm()  # 화면에 빈 폼을 그려주는 것

    context = {
        'form': form
    }
    return render(request, 'pages/login.html', context)


# 회원가입 페이지
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)       # form 객체 가져오기
        if form.is_valid():
            email = form.cleaned_data['email']  # 가져온 form 객체에서 이메일 데이터 가져오기
            password = form.cleaned_data['password']    # 가져온 form 객체에서 비밀번호 데이터 가져오기
            User.objects.create_user(email, email, password)      # username, email, password를 인자로 받는 User 생성 함수
            return HttpResponseRedirect('/')    # 회원가입 완료 후 첫 페이지로 돌아가도록
    else:   # POST가 아닐 경우
        form = RegisterForm()   # 아무 데이터도 입력되지 않은 RegisterForm

    context = {
        'form': form
    }
    return render(request, 'pages/register.html', context)


# 로그아웃 페이지
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


# 참가 정보 수정
def update_application(request):
    if not request.user.is_authenticated:   # 로그인되어있지 않다면 첫 페이지로 돌려보내기
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user

            try:
                original = Application.objects.get(user=request.user)
                application.id = original.id
            except ObjectDoesNotExist:
                pass
            finally:
                application.save()

            return HttpResponseRedirect('/application/update/')

    else:
        try:
            original = Application.objects.get(user=request.user)
            form = ApplicationForm(instance=original)
            cancelable = True
        except ObjectDoesNotExist:
            form = ApplicationForm()
            cancelable = False

    context = {
        'form': form,
        'cancelable': cancelable
    }
    return render(request, 'pages/update_application.html', context)


# 전체 참가자 목록 페이지
def view_applications(request):
    applications = Application.objects.all()

    context = {
        'applications': applications
    }
    return render(request, 'pages/view_applications.html', context)


# 참가 취소 페이지
def cancel_application(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')

    try:
        original = Application.objects.get(user=request.user)
        original.delete()
    except ObjectDoesNotExist:
        pass

    return HttpResponseRedirect('/')
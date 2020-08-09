from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from accounts.forms import UserLoginForm, UserRegistrationForm, UserRUCF1Form,UserRUMForm, UserRUCF2Form, UserRUCA1Form, CreateStudentForm, RegistrationForm, PersonalDetailForm#, StudentProfileForm, StudentProfileAttributeForm
from accounts.models import UserRegistration,UserRUCF1,UserRUM,UserRUCF2,UserRUCA1
# Create your views here.

def user_login(request):

    template_name = 'Ouarth/login.html'
    if request.user.is_authenticated:

        return redirect('/user/')
    if request.method == 'POST':

        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # str_relace = str.replace(username, '/', f'')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'login was successful')
            return redirect('/user/')
        else:
            messages.warning(
                request, f'login Error !!!! Provide Correct Username And Password')
            return redirect('/user/')
    else:
        form = UserLoginForm()


    return render(request, template_name, {'form': form})


def user_register(request):

    template_name = 'Ouarth/register.html'
    return render(request, template_name, {})

@login_required(login_url='/user/login/')
def user_account_profile(request):
    context = {}
    try:
        user_profile = UserRegistration.objects.get(user = request.user.userregistration.user)
        context['user_profile'] = user_profile
        try:
            rucf1_profile = UserRegistration.objects.get(user = request.user.userrucf1.user)
        except UserRUCF1.DoesNotExist:
            messages.warning(request, f'Please Fill The RUC F1 Form.')
            return redirect('/user/create/')
        try:
            rum_profile = UserRegistration.objects.get(user = request.user.userrum.user)
        except UserRUM.DoesNotExist:
            messages.warning(request, f'Please Fill The RUM Form.')
            return redirect('/user/create/')
        
        try:
            rucf2_profile = UserRegistration.objects.get(user = request.user.userrucf2.user)
        except UserRUCF2.DoesNotExist:
            messages.warning(request, f'Please Fill The RUC F2 Form.')
            return redirect('/user/create/')
        try:
            ruca1_profile = UserRegistration.objects.get(user = request.user.userruca1.user)
        except UserRUCA1.DoesNotExist:
            messages.warning(request, f'Please Fill The RUC A1 Form.')
            return redirect('/user/create/')

        template_name = 'user/profile.html'

        return render(request, template_name, context)
    except UserRegistration.DoesNotExist:
        messages.warning(request, f'Please Contant Administration It Seems That Your Datails Is Not Captured Correctly.')
        return redirect('/user/logout/')

@login_required(login_url='/user/login/')
def student_personal_info(request):
    # try:
    template_name = 'pages/student_personal_details.html'
    profile = UserRegistration.objects.get(user = request.user.userregistration.user)
    context = {'profile':profile}
    if request.method == 'POST':
        form = PersonalDetailForm(request.POST or None, instance=profile)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user_id = request.user_id
            obj.save()
            messages.success(request, f'Your Personal details have beeen updated successfuly')
            return redirect('/user/create')
        messages.warning(request, f'Update Failed, Fill All The fields')
        return redirect('/user/student_personal_info/')
    form = PersonalDetailForm()
    context = {'form':form}
    return render(request, template_name, context)
    # except:
    #     messages.warning(request, f'Please Contant Administration It Seems That Your Datails Is Not Captured Correctly.')
    #     return redirect('/user/logout/')
    


@login_required(login_url='/user/login/')
def user_create_profile(request):
    context = {}
    
    try:
        template_name = 'user/create_profile.html'
        user_profile = UserRegistration.objects.get(user = request.user.userregistration.user)
        context['user_profile'] = user_profile
        if request.method == 'POST':
            personalInfo = PersonalDetailForm(request.POST or None, instance=user_profile)
            form = UserRegistrationForm(request.POST, request.FILES, instance = user_profile)
            userRUCF1Form = UserRUCF1Form(request.POST, request.FILES)
            userRUMForm = UserRUMForm(request.POST, request.FILES)
            userRUCF2Form = UserRUCF2Form(request.POST, request.FILES)
            userRUCA1Form = UserRUCA1Form(request.POST, request.FILES)
            
            # TODO: implement UserRUCF1Form reg
            if userRUCF1Form.is_valid():
                obj = userRUCF1Form.save(commit=False)
                obj.user_id = request.user.id
                obj.save()
                messages.success(request, f'RUCF1 Form Upload was successful')
                return redirect('/user/create/')
            elif userRUCA1Form.is_valid():
                obj = userRUCA1Form.save(commit=False)
                obj.user_id = request.user.id
                obj.save()
                messages.success(request, f'RUC A1 Form Upload was successful')
                return redirect('/user/create/')
            elif userRUCF2Form.is_valid():
                obj = userRUCF2Form.save(commit=False)
                obj.user_id = request.user.id
                obj.save()
                messages.success(request, f'RUCF2 Form Upload was successful')
                return redirect('/user/create/')
            elif form.is_valid():
                form.save() 
                messages.success(request, f'Update was successful')
                return redirect('/user/create/')
            elif personalInfo.is_valid():
                personalInfo.save() 
                messages.success(request, f'Persona Info Update was successful')
                return redirect('/user/create/')
            elif userRUMForm.is_valid():
                obj = userRUMForm.save(commit=False)
                obj.user_id = request.user.id
                obj.save()
                messages.success(request, f'RU M Form Upload was successful')
                return redirect('/user/create/')
            else:
                messages.warning(request, f'Update Failed, Fill All The fields')
                return redirect('/user/create/')
        else:
            form = UserRegistrationForm()
            userRUCF1Form = UserRUCF1Form()
            userRUMForm = UserRUMForm()
            userRUCF2Form = UserRUCF2Form()
            userRUCA1Form = UserRUCA1Form()

            context['userRUCA1Form'] = userRUCA1Form
            context['userRUCF2Form'] = userRUCF2Form
            context['userRUMForm'] = userRUMForm
            context['form'] = form
            context['userRUCF1Form'] = userRUCF1Form


        return render(request, template_name, context)
    except UserRegistration.DoesNotExist:
        messages.warning(request, f'Please Contant Administration It Seems That Your Datails Is Not Captured Correctly.')
        return redirect('/user/logout/')

@login_required(login_url='/user/login/')
def user_dashboard(request):
    context = {}
    try:
        try:
            rucf1_profile = UserRUCF1.objects.get(user = request.user.userrucf1.user)
        except UserRUCF1.DoesNotExist:
            messages.warning(request, f'Please Fill The RUC F1 Form.')
            return redirect('/user/create/')
        try:
            rum_profile = UserRUM.objects.get(user = request.user.userrum.user)
        except UserRUM.DoesNotExist:
            messages.warning(request, f'Please Fill The RUM Form.')
            return redirect('/user/create/')
        try:
            rucf2_profile = UserRUCF2.objects.get(user = request.user.userrucf2.user)
        except UserRUCF2.DoesNotExist:
            messages.warning(request, f'Please Fill The RUC F2 Form.')
            return redirect('/user/create/')
        try:
            ruca1_profile = UserRUCA1.objects.get(user = request.user.userruca1.user)
        except UserRUCA1.DoesNotExist:
            messages.warning(request, f'Please Fill The RUC A1 Form.')
            return redirect('/user/create/')

        template_name = 'user/dashboard.html'
        return render(request, template_name, {})
    except UserRegistration.DoesNotExist:
        messages.warning(request, f'Please Contant Administration It Seems That Your Datails Is Not Captured Correctly.')
        return redirect('/user/logout/')

def create_and_auth_then_redirect(request):
    template_name = 'Ouarth/create_and_auth_then_redirect.html'
    try:
        if request.method == 'POST':
            form = CreateStudentForm(request.POST)

            adm_number = request.POST.get('adm_number')

            email_to_save = f'{adm_number}@rongovarsity.co.ke'

            User.objects.create_user(
                username = adm_number,
                email= email_to_save,
                password = adm_number,
            )
        
            # Authenticate the created student with the profile
            user = authenticate(username=adm_number,password=adm_number)
            login(request, user) 
            return redirect('/user/student/profile/')
    except IntegrityError:
        messages.warning(request, f'That Student { request.user.username }has been created Creat Another')
        return redirect('/user/student/')
    else:
        form = CreateStudentForm()
    
    return render(request, template_name, {'form' : form})

def create_prof_then_redirect_to_another_then_log_out(request):
    template_name = 'Ouarth/create_prof_then_redirect_to_another_then_log_out.html'
    form = RegistrationForm(request.POST)
    if form.is_valid():
        obj = form.save(commit=False) 
        obj.user_id = request.user.id
        obj.adm_no = request.user.username
        obj.save()
        messages.success(request, f'Profile Created successful')
        logout(request)

        return redirect('/user/student/')
    else:
        form = RegistrationForm()
    return render(request, template_name, {'form' : form})
    # messages.warning(request, f'You Have logout !!!')
    # return redirect('/user/login/')

def user_logout(request):
    logout(request)
    messages.warning(request, f'You Have logout !!!')
    return redirect('/user/login/')


def error_404(request, exception):
    template_name = 'user/err/404.html'
    return render(request, template_name, {}, status=404)

def error_500(request):
    template_name = 'user/err/500.html'
    return render(request, template_name, {})
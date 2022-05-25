from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .forms import CodeForm
from users.models import CustomUser
from django.shortcuts import get_object_or_404
from .utils import send_sms
from users.forms import RegisterUserForm
from .models import Code

import logging

logging.basicConfig(level=logging.DEBUG)


class HomeView(LoginRequiredMixin, View):
    """
    Accessing the view requires logging in.
    If the user is not logged in then redirect to the logging page.
    After successful logging in, redirect back to the requested url.
    """

    def get(self, request):
        return render(request,
                      'home.html',
                      context={'registered': request.session.pop('registered', False),
                               'logged_in': request.session.pop('logged_in', False)})


class FirstFactorAuthenticationView(View):

    def get(self, request):
        """
        Show the 1st factor authentication form to the user.
        """
        form = AuthenticationForm()
        return render(request,
                      template_name='codes/auth.html',
                      context={'form': form,
                               'error_message': request.session.pop('error_message', False)})

    def post(self, request):
        """
        Check user credentials against 1st factor of authentication.
        """
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            # if user passed the first factor authentication - save the pk that identifies the user in the session
            request.session['pk'] = form.get_user().pk
            return redirect(reverse('codes:login_second'))
        else:
            # if user failed the first factor authentication - redirect back to the authentication form with error message
            request.session['error_message'] = "Invalid username or password, try again."
            return redirect(request.path)


class SecondFactorAuthenticationView(View):
    """
    Second authentication factor.
    """

    def get(self, request):
        """
        Show the 2nd factor authentication form to the user.
        """
        pk = request.session.get('pk', False)
        if pk:
            # if pk in session then user must have already passed the 1st factor of authentication - show 2nd factor form
            form = CodeForm()
            user = get_object_or_404(CustomUser, pk=pk)

            user.code.save()  # 're-saving' the code instance generates a new verification code number

            # print the newly generated verification code to the console
            logging.debug(f"Verification code: {user.code.number}")

            # send SMS with verification code to the user's phone
            send_sms(user_code=user.code.number, phone_number=user.phone_number)

            return render(request,
                          template_name='codes/auth_second.html',
                          context={'form': form,
                                   'error_message': request.session.pop('error_message', False)})
        else:
            # if pk not in session then user hasn't successfully passed the 1st factor of authentication yet - redirect to 1st factor view
            return redirect(reverse("codes:login_first"))

    def post(self, request):
        """
        Check user credentials against 2nd factor of authentication.
        """
        form = CodeForm(data=request.POST)
        if form.is_valid():
            user = get_object_or_404(CustomUser, pk=request.session['pk'])
            valid_code = user.code.number

            # if user passed the second factor of authentication - log in the user into the session
            if valid_code == form.cleaned_data['number']:
                login(request, user)
                request.session.pop('pk')
                request.session['logged_in'] = True
                return redirect(reverse('codes:home'))

        request.session['error_message'] = "Invalid verification code, try again."
        return redirect(request.path)


class RegistrationView(View):
    """
    Register new user.
    """

    def get(self, request):
        """
        Show user the blank registration form.
        """
        form = RegisterUserForm()
        return render(request, template_name='codes/register.html', context={'form': form})

    def post(self, request):
        """
        Process the registration form submitted by the user.
        """
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            request.session['user_data'] = form.cleaned_data
            return redirect(reverse('codes:register-verify'))
        else:
            # of registration form is invalid - redirect back to registration form view with form validation errors
            return render(request, template_name='codes/register.html', context={'form': form})


class RegisterVerifyView(View):
    """
    Verify user's phone number (so that the user cannot register
     under a phone number he does not have access to).
    """

    def get(self, request):
        """
        Show the verification code form to the user.
        """
        user_data = request.session.get('user_data', False)
        if user_data:

            code_form = CodeForm()
            # manually generate verification code (without binding it to the user - he doesn't exist yet)
            valid_code = next(Code.gen_code)
            request.session['valid_code'] = valid_code

            # print the newly generated verification code to the console
            logging.debug(f"Verification code: {valid_code}")

            # send SMS with verification code to the user's phone
            send_sms(user_code=valid_code, phone_number=user_data.get('phone_number'))

            return render(request,
                          template_name='codes/auth_second.html',
                          context={'form': code_form,
                                   'error_message': request.session.pop('error_message', False)})
        else:
            # if user_data not in session then user hasn't successfully submitted the registration form - redirect to registration view
            return redirect(reverse("codes:register"))

    def post(self, request):
        """
        Verify user's phone number using the verification code.
        """
        code_form = CodeForm(data=request.POST)
        user_data = request.session.get('user_data', False)
        if code_form.is_valid() and user_data:

            valid_code = request.session.pop('valid_code', False)

            if valid_code == code_form.cleaned_data['number']:
                # if user verified his phone number - register him and log him into the current session
                reg_form = RegisterUserForm(user_data)
                if reg_form.is_valid():
                    user = reg_form.save(commit=True)
                    login(request, user)
                    request.session['registered'] = True
                    request.session.pop('user_data')
                    return redirect(reverse('codes:home'))

        # if the verification code submitted by the user is not valid - redirect back to verification code form with error message
        request.session['error_message'] = "Invalid verification code, try again."
        return redirect(request.path)

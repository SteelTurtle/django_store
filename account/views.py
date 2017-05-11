from django.conf import settings
from django.contrib.auth import get_user, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.messages import error, success
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import DetailView, View

# we import an artifact UpdateView from the "core" app, because the names of our update forms
# do not conform with the common "template_suffix_name" of the django GCBV views
from core.utils import UpdateView
from .decorators import class_login_required
from .forms import ResendActivationEmailForm, UserCreationForm
from .models import Profile
from .utils import MailContextViewMixin, ProfileGetObjectMixin


class ActivateAccount(View):
    success_url = reverse_lazy('dj-auth:login')
    template_name = 'user/account_activate.html'

    # The goal of get() is to use the uidb64 and token arguments to activate an account.
    # We use the uidb64 to identify the user according to primary key, and we then check
    # to see if the token is valid (check that we created it). If the token was successfully created,
    # we activate the account and redirect to the login page.
    # NOTICE that we DO NOT cache the url, because this url must expire the same moment it is
    # used to activate an account
    @method_decorator(never_cache)
    def get(self, request, uidb64, token):
        # To get the code to work inside of get(), we need the model that represents the user
        # (currently Django’s User model class) and a way to turn the base-64 uidb64 number into a
        # base-10 number for us to use with the model. (basically the reversed process we did for the
        # user activation URL creation in the CreateUser view + Mixin)

        User = get_user_model()  # let's get the auth.User model first...
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            # now, let's retrieve the user we want to activate by its id
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # if we actually get a user AND the token we got from the url is valid...
        if (user is not None and token_generator.check_token(user, token)):
            # ..then activate the user and save it
            user.is_active = True
            user.save()
            success(request, 'Your user has been activated! You may now login ')
            return redirect(self.success_url)
        # else,redirect the user to a page where we ask him/her to get a new activation link
        else:
            return TemplateResponse(request, self.template_name)


class CreateAccount(MailContextViewMixin, View):
    # we use our customized UserCreationForm as form_class
    form_class = UserCreationForm
    success_url = reverse_lazy('dj-auth:create_done')
    template_name = 'account/account_create.html'

    @method_decorator(csrf_protect)
    def get(self, request):
        return TemplateResponse(request, self.template_name, {'form': self.form_class})

    # the post method use the @sensitive_post_parameter decorator marking specific form data
    # as sensitive. In this case, we want the password data to NOT be displayed
    #  to the developers or users in case there is some error during the registration process
    @method_decorator(csrf_protect)
    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            # we do not want to cache the returned user
            bound_form.save(**self.get_save_kwargs(request))
            # if the value of mail_sent is True (this value is set as the result of execution of the send_mail()
            # method inside the UserCreationForm), we redirect the user to the success_url
            if bound_form.mail_sent:
                return redirect(self.success_url)
            else:
                # let's record the errors and show it to the user
                errs = bound_form.non_field_errors()
                for err in errs:
                    error(request, err)
                return TemplateResponse(request, self.template_name, {'form': bound_form})

        # else, if the form posted has some errors, we just redisplay it to the user
        return TemplateResponse(request, self.template_name, {'form': bound_form})


class DisableAccount(View):
    success_url = settings.LOGIN_REDIRECT_URL
    template_url = 'account/account_confirm_delete.html'

    @method_decorator(login_required)
    @method_decorator(csrf_protect)
    def get(self, request):
        disabled_user = get_user(request)
        disabled_user.set_unusable_password()
        disabled_user.is_active = False
        disabled_user.save()
        logout(request)
        return redirect(self.success_url)


# We use the decorator "class_login_required" to be sure that only the authenticated user who
# owns his/her profile can actually access and modify this page.
# Notice also that we use the generic class DetailView to spare a lot of code for the representation
# of the data...
@class_login_required
class ProfileDetail(ProfileGetObjectMixin, DetailView):
    model = Profile


# on the other hand, a read only version of the profile is available to anybody
class PublicProfileDetail(DetailView):
    model = Profile


@class_login_required
class ProfileUpdate(ProfileGetObjectMixin, UpdateView):
    fields = ('about',)
    model = Profile


class ResendActivationEmail(MailContextViewMixin, View):
    form_class = ResendActivationEmailForm
    success_url = reverse_lazy('dj-auth:login')
    template_name = 'account/resend_activation.html'

    @method_decorator(csrf_protect)
    def get(self, request):
        return TemplateResponse(
            request,
            self.template_name,
            {'form': self.form_class()})

    @method_decorator(csrf_protect)
    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            user = bound_form.save(**self.get_save_kwargs(request))
            if (user is not None
                and not bound_form.mail_sent):
                errs = (
                    bound_form.non_field_errors())
                for err in errs:
                    error(request, err)
                if errs:
                    bound_form.errors.pop(
                        '__all__')
                return TemplateResponse(
                    request,
                    self.template_name,
                    {'form': bound_form})
        success(
            request,
            'Activation Email Sent!')
        return redirect(self.success_url)

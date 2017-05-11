import logging

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import Profile
from .utils import ActivationMailFormMixin

# Get the logger defined in the ActivationMailFormMixin, inherited by the
# ResendActivationEmailForm down here...
logger = logging.getLogger(__name__)


class ResendActivationEmailForm(ActivationMailFormMixin, forms.Form):
    email = forms.EmailField()
    mail_validation_error = 'We are experiencing problems in sending you' \
                            ' the activation email. Please try again.'

    def save(self, **kwargs):
        User = get_user_model()
        try:
            # always try to get CLEANED data from the form, not raw ones...
            user = User.objects.get(
                email=self.cleaned_data['email'])
        except:
            logger.warning(
                'Resend Activation: No user with '
                'email: {} .'.format(self.cleaned_data['email']))
            return None
        self.send_mail(user=user, **kwargs)
        return user


# We want to use some of the features of the predefined UserCreationForm in django.auth
# this is why we import it in the class, together with our Activation Mail Mixin facility
class UserCreationForm(ActivationMailFormMixin, BaseUserCreationForm):
    # the mail_validation_error overwrites the default value of '' inherited from the ActivationMailFormMixin
    mail_validation_error = 'The User has ben created; however, we could not send the activation email ' \
                            'to the specified email address. Please try again later...'

    # since we will access user profiles with urls like "/account/<username>", we must be sure
    # that this namespace will not collide with all the existing "account/some-name" already
    # defined in the account.urls file. Such is the purpose of the "clean_username" method
    def clean_username(self):
        username = self.cleaned_data['username']
        not_allowed = {
            'activate',
            'create',
            'disable',
            'login',
            'logout',
            'password',
            'profile',
        }
        # we trick the user telling him/her that this username already exists, not that these are
        # reserved words
        if username in not_allowed:
            raise ValidationError("Sorry, a user account with that username already exist.")
        # otherwise...
        return username

    # this save() method will trigger the registration of the user on the DB. THIS METHOD IS
    # CALLED BY THE "CreateAccount" VIEW. We first overwrite the original save() method of the ModelForm,
    # specifying that we still do not want to commit the change to the DB. Actually,
    # we first want the user to complete the activation mail process :)
    def save(self, **kwargs):
        user = super().save(commit=False)
        # If user already has a primary key, then the data is already in the database,
        # and we don’t need to send an account activation email.
        if not user.pk:
            user.is_active = False
            send_mail = True
        else:
            send_mail = False
        # after we understand if we have to send or not the activation email, we finally save the user
        # and all its the associated DB relations (with the save_m2m() method inherited from the ModelForm
        user.save()
        self.save_m2m()
        # Once the user is activated and saved in the DB, we also create its user profile
        # notice that we double-check that the user's slug do contain only alphanumeric characters
        # through the "slugify" method
        Profile.objects.update_or_create(user=user, defaults={'slug': slugify(user.get_username())})

        if send_mail:
            self.send_mail(user=user, **kwargs)
        return user

    # By manipulating the Meta class, we change the beahviour of the parent BaseUserCreationForm
    # overriding its ModelForm behavior: We override the model with get user model() and add
    # the email form to the field
    class Meta(BaseUserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')

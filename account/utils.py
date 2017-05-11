import logging
import traceback
from logging import CRITICAL, ERROR
from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth import get_user
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import BadHeaderError, send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

logger = logging.getLogger(__name__)


class ActivationMailFormMixin:
    mail_validation_error = ''

    # The LOGGER, ladies and gentlemen!!
    def log_mail_error(self, **kwargs):
        msg_list = [
            'Activation email did not send.\n',
            'from_email: {from_email}\n'
            'subject: {subject}\n'
            'message: {message}\n',
        ]
        recipient_list = kwargs.get('recipient_list', [])
        for recipient in recipient_list:
            msg_list.insert(1, 'recipient: {r}\n'.format(r=recipient))
        if 'error' in kwargs:
            level = ERROR
            error_msg = (
                'error: {0.__class__.__name__}\n'
                'args: {0.args}\n')
            error_info = error_msg.format(
                kwargs['error'])
            msg_list.insert(1, error_info)
        else:
            level = CRITICAL
        msg = ''.join(msg_list).format(**kwargs)
        logger.log(level, msg)

    @property
    def mail_sent(self):
        if hasattr(self, '_mail_sent'):
            return self._mail_sent
        return False

    @mail_sent.setter
    def set_mail_sent(self, value):
        raise TypeError(
            'Cannot set mail_sent attribute.')

    # get the activation message to be sent to the user
    def get_message(self, **kwargs):
        email_template_name = kwargs.get('email_template_name')
        context = kwargs.get('context')
        return render_to_string(email_template_name, context)

    # get the mail subject of the message sent to the user
    def get_subject(self, **kwargs):
        subject_template_name = kwargs.get('subject_template_name')
        context = kwargs.get('context')
        subject = render_to_string(subject_template_name, context)
        # subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        return subject

    # if context is null, let's create a new one filled with the relevant keys/values for the activation
    def get_context_data(self, request, user, context=None):
        if context is None:
            context = dict()
        # get the current site, and check if user is connecting through  http or https
        current_site = get_current_site(request)
        if request.is_secure():
            protocol = 'https'
        else:
            protocol = 'http'
        # then, let's create a cryptographic token to be used with the authentication url
        token = token_generator.make_token(user)
        # turn into bytes and encode the 'user' primary key in base64, to be included in the url
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # finally, we assemble the 'context' dictionary and return it to the caller
        context.update({
            'domain': current_site.domain,
            'protocol': protocol,
            'site_name': current_site.name,
            'token': token,
            'uid': uid,
            'user': user,
        })
        return context

    # define an "utility" function that will handle the main job of sending the activation email to the user,
    # given a proper HttpRequest AND a user passed to the function.
    # Notice that the contexts contents, the mail message and the mail subject will be retrieved by
    # the three methods we defined up here
    def _send_mail(self, request, user, **kwargs):
        kwargs['context'] = self.get_context_data(request, user)
        mail_kwargs = {
            "subject": self.get_subject(**kwargs),
            "message": self.get_message(**kwargs),
            "from_email": settings.DEFAULT_FROM_EMAIL,
            "recipient_list": [user.email],
        }
        try:
            # number_sent value will be 0 or 1. Notice what happens here: the send_mail
            # method is from the django.mail package and it has NOTHING to do with the
            # send_mail methods we define in this class. Also, notice how the mail_kwargs
            # dictionary is expanded to cover all the arguments expected by the function
            number_sent = send_mail(**mail_kwargs)
        except Exception as error:
            self.log_mail_error(error=error, **mail_kwargs)
            if isinstance(error, BadHeaderError):
                err_code = 'badheader'
            elif isinstance(error, SMTPException):
                err_code = 'smtperror'
            else:
                err_code = 'unexpectederror'
            return (False, err_code)
        else:
            # else, if the activation email has actually been sent
            if number_sent > 0:
                return (True, None)
        # in any other case, we are facing and unknown error and we must log it
        self.log_mail_error(**mail_kwargs)
        return (False, 'unknownerror')

    # This is the actual send_mail method that we will call from the UserRegistrationForm. The flow of
    # the complete actions is then: send_mail from the UserCreationForm, which call the _send_mail ("static") method
    # of this class, which in turn call the send_mail method of the django.mail package..
    def send_mail(self, user, **kwargs):
        # Extract the http request dictionary element from the UserCreationForm, or assign it the value None
        # in case request is empty (In this case, an empty dictionary will trigger some error
        request = kwargs.pop('request', None)
        if request is None:
            tb = traceback.format_stack()
            tb = ['  ' + line for line in tb]
            logger.warning('send_mail called without '
                           'request.\nTraceback:\n{}'.format(''.join(tb)))
            self._mail_sent = False
            return self.mail_sent
        # otherwise we pass the request to the inner _send_mail method and
        # we return to the caller the mail_sent boolean value and an eventual error message
        (self._mail_sent, error) = self._send_mail(request, user, **kwargs)
        # if the value of mail_sent returned by _send_mail is false, we log the error
        if not self.mail_sent:
            self.add_error(None, ValidationError(self.mail_validation_error, code=error))
        return self.mail_sent


# Just a mixin for the laziness: the send_mail method of the ActivationMailFormMixin expects that we
# pass a dictionary with specific keys/values. We do not want to fix these names in memory, so we delegate
# this business to the mixin below
class MailContextViewMixin:
    email_template_name = 'account/email_create.txt'
    subject_template_name = 'account/subject_create.txt'

    def get_save_kwargs(self, request):
        return {
            'request': request,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name
        }


# To display the profile of the current user, we retrieve the authenticated User from the HttpRequest object
# and return the associated user Profile. Note the use of the "get_object()" as name of the method
# This naming convention is commonly used in the GCBV generic classes, and we will actually
# overwrite the get_object() method of the UpdateView GCBV class inherited by the ProfileUpdate view...
class ProfileGetObjectMixin:
    def get_object(self):
        current_user = get_user(self.request)
        return current_user.profile

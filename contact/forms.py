from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import BadHeaderError, mail_managers


class ContactForm(forms.Form):
    email = forms.EmailField(initial='user@yourdomain.org')
    # force a CharField to be visualized as TextArea on th eHTML page
    text = forms.CharField(widget=forms.Textarea)

    FEEDBACK = 'F'
    CORRECTION = 'C'
    SUPPORT = 'S'
    CHOICE_SELECTED = (
        (FEEDBACK, 'Feedback'),
        (CORRECTION, 'Correction'),
        (SUPPORT, 'Support'),
    )
    contact_reason_selector = forms.ChoiceField(
        choices=CHOICE_SELECTED, initial=FEEDBACK
    )

    def send_email(self):
        # Get the (guaranteed) cleaned content of the selector
        contact_reason = self.cleaned_data.get('contact_reason_selector')
        # make a dictionary from the CHOICE_SELECTED enumerator
        contact_reason_dictionary = dict(self.CHOICE_SELECTED)
        # Get the full information from the selector (not simply the initials 'F', 'C' or 'S')
        cleaned_selection = contact_reason_dictionary.get(contact_reason)
        email = self.cleaned_data.get('email')
        text = self.cleaned_data.get('text')
        message_body = 'Message from: {}\n\n{}'.format(email, text)

        try:
            mail_managers(cleaned_selection, message_body)
        except BadHeaderError:
            self.add_error(None, ValidationError('Could not send the email.\n'
                                                 'Extra Headers are not allowed'
                                                 'in the message body.'))
            return False
        else:
            return True

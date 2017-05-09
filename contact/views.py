from django.contrib.messages import success
from django.shortcuts import redirect, render
from django.views.generic import View

from .forms import ContactForm


class ContactView(View):
    form_class = ContactForm
    template_name = 'contact/contact_form.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            mail_sent_to_user = bound_form.send_email()
            if mail_sent_to_user:
                # show a message on the contact form template
                success(request, 'Your email has been successfully sent'
                                 'to the Administrators')
                return redirect('blog_post_list')
        # else...
        return render(request, self.template_name, {'form': bound_form})

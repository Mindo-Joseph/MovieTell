from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .token_generator import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse


def register(request):
    
    if request.method == "POST":
        # Instantiate form with the data to be posted
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active() = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate your account'
            message = render_to_string ('users/activate_account.html', {
                'user':user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_text(user.pk)).decode(),
                'token': account_activation_token.make_token(user),


            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject,message, to=[to_email])
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')

            
            """
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}!')
            return redirect('home')
            """

            
    else:
        # Instantiate new empty form
        form = UserRegisterForm()



    return render(request, 'users/register.html', {'form':form})

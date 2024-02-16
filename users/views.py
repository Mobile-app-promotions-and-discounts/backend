import requests


from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse, get_script_prefix
from django.http import HttpResponse, QueryDict, HttpRequest

from users.forms import CustomPasswordForm


def reset_password(request, uid, token):
    form = CustomPasswordForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        requests.post('http://cherry_app:8000/auth/users/reset_password_confirm/', data=data)
        # return redirect('/auth/users/reset_password_confirm/')
        return HttpResponse(f'данные формы - {data}')
    init_data = {'uid': uid, 'token': token}
    form = CustomPasswordForm(initial=init_data)
    return render(
        request=request,
        template_name='create_password.html',
        context={'form': form},
    )

from django.shortcuts import render

from users.forms import CustomPasswordForm


def reset_password(request, uid, token):
    """Отправить подтверждение сброса пароля."""
    init_data = {'uid': uid, 'token': token}
    form = CustomPasswordForm(initial=init_data)
    return render(
        request=request,
        template_name='create_password.html',
        context={'form': form},
    )

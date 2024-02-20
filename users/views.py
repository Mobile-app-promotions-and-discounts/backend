from django.shortcuts import render

from users.forms import CustomPasswordForm


def reset_password(request, uid, token):
    """Отправить подтверждение сброса пароля."""
    form = CustomPasswordForm()
    return render(
        request=request,
        template_name='create_password.html',
        context={
            'form': form,
            'uid': uid,
            'token': token,
        },
    )

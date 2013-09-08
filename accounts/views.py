from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render


@login_required
def change_password(request):

    if request.method == "POST":
        form = PasswordChangeForm(
            request.user,
            request.POST,
        )
        if form.is_valid():
            form.save()
        else:
            print form.errors
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/password_change.html', {
        "form": form
    })

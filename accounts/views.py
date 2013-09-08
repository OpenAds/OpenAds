from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib import messages


@login_required
def change_password(request):

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit'))

    if request.method == "POST":
        form = PasswordChangeForm(
            request.user,
            request.POST,
        )
        if form.is_valid():
            messages.success(request, "Your password has been changed!")
            form.save()
        else:
            print form.errors
    else:
        form = PasswordChangeForm(user=request.user)

    form.helper = helper
    return render(request, 'accounts/password_change.html', {
        "form": form
    })

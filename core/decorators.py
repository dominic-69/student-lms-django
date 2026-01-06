from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
#only for admin..student cantta accesssssss 
def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return redirect('dashboard')
    return wrapper

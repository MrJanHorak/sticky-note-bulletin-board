from .models import Profile

def background(request):
  is_authenticated = request.user.is_authenticated
  context = {}
  print(request.user)
  if is_authenticated:
    background = Profile.objects.get(user=request.user).background
    context = {'background': background}
  return context
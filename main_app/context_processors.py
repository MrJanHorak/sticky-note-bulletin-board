from .models import Profile

def background(request):
  user = request.user.is_authenticated
  context = {}
  if user:
    background = Profile.objects.get(user=request.user).background
    context = {'background': background}
  return context
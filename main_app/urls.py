from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('accounts/login/', views.Login.as_view(), name='login'),
  path('accounts/signup/', views.signup, name='signup'),
  path('notes/', views.notes_index, name='notes_index'),
  path('notes/<int:note_id>/', views.notes_detail, name='notes_detail'),
  path('notes/type-selection/', views.note_type_selection, name='note_type_selection'),
  path('notes/create/', views.NoteCreate.as_view(), name='notes_create'),
  path('notes/<int:pk>/update/', views.NoteUpdate.as_view(), name='notes_update'),
  path('notes/<int:pk>/delete/', views.NoteDelete.as_view(), name='notes_delete'),
  path('notes/<int:note_id>/add_photo/', views.add_photo, name='add_photo'),
  path('profile/', views.profile, name='profile'),
  path('profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update'),
]
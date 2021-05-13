from django.urls import path
from .views import ActivitiesView, UserRegister, UserLogin, CourseView, CourseRegistrationView, ActivityFilterView

urlpatterns = [
    path('accounts/', UserRegister.as_view()),
    path('login/', UserLogin.as_view()),
    path('courses/', CourseView.as_view()),
    path('courses/registrations/', CourseRegistrationView.as_view()),
    path('activities/', ActivitiesView.as_view()),
    path('activities/<int:user_id>/', ActivityFilterView.as_view())
]
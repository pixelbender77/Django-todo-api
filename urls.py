from django.urls import path,include
#from django.conf.urls import url
from .views import ( 
    TodoListApiView,TodoDetailApiView
)
urlpatterns = [
    path('api',TodoListApiView.as_view()),
    path('api/<int:pk>',TodoDetailApiView.as_view()), #notice we are adding the .as_view() because the url is accessing a class based view..
]                                                           #in contrast, function based views will as addressed simply eg. views.get_detail()
#
#I think the best way to get rid of this my neigbor is to tell him the truth tomorrow  morning. The 
# more i keep silent the more they will think that i am joking or that it is a joking matter

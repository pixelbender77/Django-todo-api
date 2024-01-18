from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Todo
from .serializers import TodoSerializer
from rest_framework import decorators
from rest_framework import generics
from rest_framework import mixins

'''                          ===== CONCISE GENERIC CLASS BASED API VIEW =====
class TodoListApiView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs ):
        return self.create(request, *args, **kwargs)

class TodoDetailApiView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Todo.objects.get()
    serializer_class = TodoSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)'''


#'''                 ===== EXTREMELY CONCISE GENERIC CLASS BASED API VIEW  =====
class TodoListApiView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    
    def perform_create(self, serializer): #specifying an action during creation of a todo list
        serializer.save(owner=self.request.user)

class TodoDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
#'''

'''                 ===== BROAD | NATIVE | PRECISE CLASS BASED API VIEW =====
class TodoListApiView (APIView):
    permission_classes = [permissions.IsAuthenticated] #This typically replaces decorators in normal django
    #actually listing all the permission needed to access the view. In this case, user needs to be authenticated
    
    #collecting all the todos of a particular user
    def get(self, request, format=None, *args, **kwargs):
        todos = Todo.objects.filter(user = request.user.id ) # requesting all the todo objects of a particular user
        serializer = TodoSerializer(todos, many=True) # serializing the object. Note that by default many is False
        return Response(serializer.data, status= status.HTTP_200_OK) #returning the serialized data and a positive HTTP response
    
    #@csrf_exempt CAN BE ADDED FOR CLIENTS THAT DIDN'T INCLUDE THIS IN THIER FORMS
    #posting or creating a todo for a particular user
    def post(self, request , format=None,*args, **kwargs ):
        data = { #collecting data from the request sent
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'),
            'user': request.user.id
        }
        serializer = TodoSerializer(data=data)
        if serializer.is_valid(): #checking if the data gotten is correct and matches the business logic mmm.. kinda
            serializer.save() #Saving
            return Response(serializer.data, status=status.HTTP_201_CREATED) #returning the serialized object(.json file) and a created status
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)# if the serializer is not valid then we return a negative response

class TodoDetailApiView(APIView):
    
    permission_classes=[ permissions.IsAuthenticated]

    def get_object(self,todo_id, user_id): #helper method which seeks for and return a particular object or None of the object is not found
        try:
            return Todo.objects.get(id=todo_id , user = user_id)
        except Todo.DoesNotExist:
            return None
    
    #GETTING A TODO WITH GIVEN ID & USER
    def get(self, request, todo_id, format=None, *args, **kwargs):
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res":"The object with todo_id does not exist"},
                status= status.HTTP_400_BAD_REQUEST
            )

        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    #UPDATE
    def put(self, request, todo_id, format=None, *args, **kwargs):

        todo_instance = self.get_object(todo_id, request.user.id) #getting the object to be updated
        if not todo_instance:
            return Response(
                {"res":"The object with todo_id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = { #collecting the data to be put in the object( This data is gotten from the client request)
            "task": request.data.get('task'),
            "completed": request.data.get('completed'),
            "user": request.user.id
        }
        serializer  = TodoSerializer( instance=todo_instance , data=data , partial = True) #inserting into/ updating the data of the gotten object(to be updated), with the data sent by client.
                                                                                          #The partial parameter is to say the we might not be updating everything() (compulsory fields included)
        if serializer.is_valid(): #if the updated serializer is valid then we save and return the serialized data and an OK HTTP RESPONSE along with it
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #if the serializer is not correct we return a bad request instead
    
    def delete(self,request , todo_id , *args, **kwargs):
        todo_instance = self.get_object(todo_id, request.user.id)

        if not todo_instance :
            return Response(
                {"res":"The object with this todo_it doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res":"Ojbect deleted!"},
            status=status.HTTP_200_OK
        )
'''
            #Notice that the Response Class takes in elements just like a tupple(parameters) mmm.. kinda
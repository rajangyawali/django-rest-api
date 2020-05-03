from django.shortcuts import render, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework import filters
from rest_framework import generics
from rest_framework.decorators import api_view
from . serializers import UserProfileSerializer
from . models import UserProfile
from . import permissions


### API Views ##########################################################################################################

class ListUsers(APIView):
    """
    View to list all users in the system with API View.
    """
    filter_backends = [filters.SearchFilter]
    search_fields = ['email','name']

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        emails = [user.email for user in UserProfile.objects.all()]
        return Response({'Emails':emails})

    def post(self, request, format=None):
        """
        Creates a new user
        """

        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.data.get('email')            
            return Response({'email':email}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsersDetail(APIView):
    """
    Retrieve, update or delete an User instance with API View.
    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.UpdateOwnProfile, ]

    def get_object(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        Gets a detailed information of particular user
        """
        user_object = self.get_object(pk)
        serializer = UserProfileSerializer(user_object)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Updates an existing user
        """
        user_object = self.get_object(pk)
        serializer = UserProfileSerializer(user_object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        """
        Updates certain field of an existing user
        """
        user_object = self.get_object(pk)
        serializer = UserProfileSerializer(user_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        Deletes an existing user
        """
        user_object = self.get_object(pk)
        user_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

### End of API Views ##########################################################################################################

### Generic API Views ##########################################################################################################
class ListUserProfile(generics.ListCreateAPIView):
    """
    View to list all users in the system with Generic API View.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    # You can add the functionality by overriding get and post methods

class DetailUserProfile(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an User instance with Generic API View
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.UpdateOwnProfile, ]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    

    # You can add the functionality by overriding put, patch and delete methods

### End of Generic API Views ##########################################################################################################

### Function based API View ##########################################################################################################
@api_view(['GET', 'POST'])
def hello_api(request):
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world!"})

@api_view(['GET', 'POST'])
def profiles_list(request):
    """
    View to list all users in the system with Function based API View.
    """
    if request.method == 'GET':
        data = UserProfile.objects.all()

        serializer = UserProfileSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def profiles_detail(request, pk):
    """
    Retrieve, update or delete an User instance with Function based API View.
    """
    try:
        user = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserProfileSerializer(user, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

### End of Function based API View ##########################################################################################################



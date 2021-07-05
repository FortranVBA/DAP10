"""Project OC DAP 10 - Account views file."""

from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# Create your views here.


class SignUpView(APIView):
    """Sign up view."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Registration with post request."""
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RadiusAuthSerializer


class RadiusAuthView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RadiusAuthSerializer

    def post(self, request, format=None):
        print(request.data)
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

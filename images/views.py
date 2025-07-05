from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageSerializer
from .services import ImageService


class ImageUploadView(APIView):

    def post(self, request):

        image = request.FILES.get('image')
        if not image:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            service = ImageService(user=request.user)
            uploaded_image = service.upload_image(
                image_file=image, user=request.user)
            serializer = ImageSerializer(uploaded_image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

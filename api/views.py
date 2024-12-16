from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from api.models import product
from rest_framework import status
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated 

@api_view()
# @permission_classes((IsAuthenticated,))
def getData(request):
    return Response({"message":"Hello World"})

@permission_classes((IsAuthenticated,))
class ProductList(APIView):
    def get(self,request):
        products = product.objects.all()
        serializer = ProductSerializer(products,many=True) #converted to json
        return Response(serializer.data)
    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
@permission_classes((IsAuthenticated,))
class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return product.objects.get(pk=pk)
        except product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
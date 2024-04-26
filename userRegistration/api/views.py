from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import viewsets
from core.models import JobApplication  # Replace 'yourapp' with the actual name of your app
from .serializers import JobApplicationSerializer

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        total_objects = queryset.count()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'total_objects': total_objects,
                'results': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'total_objects': total_objects,
            'results': serializer.data
        })

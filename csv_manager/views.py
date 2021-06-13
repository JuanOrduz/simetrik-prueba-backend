import pandas as pd

from rest_framework import generics, status
from rest_framework.response import Response

from csv_manager import models, serializers


class CSVFilesListCreate(generics.ListCreateAPIView):
    queryset = models.CSVFiles.objects.all()
    serializer_class = serializers.CSVFilesSerializer
    ordering_fields = ("name", "created_at")
    filterset_fields = {"name": ["exact"], "is_store": ["exact", "isnull"]}

    def create(self, request, *args, **kwargs):
        csv_file = request.FILES["file"]
        df_csv = pd.read_csv(csv_file, sep=",")
        serializer = self.get_serializer(
            data={
                "name": csv_file.name,
                "column_set_string": ",".join(df_csv.columns),
                "file": csv_file,
            }
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

        # Store in external database
        # return Response("Ok", status=status.HTTP_201_CREATED)


class CSVFilesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CSVFiles.objects.all()
    serializer_class = serializers.CSVFilesSerializer
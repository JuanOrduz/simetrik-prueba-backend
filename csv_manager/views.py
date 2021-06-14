import copy
import pandas as pd

from rest_framework import generics, status
from rest_framework.response import Response

from csv_manager import models, serializers
from csv_manager.csv_data_db import utils


class CSVFilesListCreate(generics.ListCreateAPIView):
    queryset = models.CSVFiles.objects.all()
    serializer_class = serializers.CSVFilesSerializer
    ordering_fields = ("name", "created_at")
    filterset_fields = {"name": ["exact"], "is_store": ["exact", "isnull"]}

    def create(self, request, *args, **kwargs):
        csv_file = request.FILES["file"]
        df_csv = pd.read_csv(csv_file, sep=",")
        df_csv.index.name, _ = csv_file.name.split(".")
        serializer = self.get_serializer(
            data={
                "name": csv_file.name.split(".")[0],
                "column_set_string": ",".join(df_csv.columns),
                "file": csv_file,
            }
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        utils.create_table(df_csv)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class CSVFilesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CSVFiles.objects.all()
    serializer_class = serializers.CSVFilesSerializer


class CSVDataListView(generics.ListAPIView):
    def get_filtered_queryset(self):
        table_name = self.kwargs["pk"]
        ordering = "id"
        query_params = copy.deepcopy(self.request.query_params)

        if "limit" in query_params:
            del query_params["limit"]
        if "offset" in query_params:
            del query_params["offset"]
        if "ordering" in query_params:
            ordering = query_params["ordering"]
            del query_params["ordering"]
        return utils.retrieve_data(
            table_name=table_name, order_by=ordering, filters=query_params
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_filtered_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(page)

        return Response(queryset)

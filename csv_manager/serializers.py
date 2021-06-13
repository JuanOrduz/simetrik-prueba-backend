from rest_framework import serializers
from csv_manager import models


class CSVFilesSerializer(serializers.ModelSerializer):
    column_set = serializers.SerializerMethodField()

    class Meta:
        model = models.CSVFiles
        fields = ("id", "name", "column_set_string", "file", "is_store", "created_at", "column_set")
        read_only_field = ("id", "column_set")
        extra_kwargs = {"column_set_string": {"write_only": True}}
    
    def get_column_set(self, obj):
        return obj.column_set_string.split(",")

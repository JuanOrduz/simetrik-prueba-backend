from unittest import mock, TestCase

from csv_manager.models import CSVFiles
from csv_manager.serializers import CSVFilesSerializer


@mock.patch("django.db.models.base.Model.save")
class TestCSVFilesSerializer(TestCase):
    def test_serialized_json(self, mock_save):
        csv_file = CSVFiles(
            id=1,
            name="Inventary",
            column_set_string="id,name,quantity,price",
            file="/csv_files/Inventary.csv",
        )
        csv_file.save()
        serialized_json = CSVFilesSerializer(csv_file).data

        mock_save.assert_called()
        assert serialized_json["id"] == csv_file.id
        assert serialized_json["name"] == csv_file.name
        assert serialized_json["file"].startswith(
            "https://simetrik-backend-test.s3.amazonaws.com/csv_files"
        )
        assert serialized_json["column_set"] == ["id", "name", "quantity", "price"]

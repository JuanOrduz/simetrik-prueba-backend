from unittest import mock, TestCase

from csv_manager.models import CSVFiles


class TestCSVFilesModel(TestCase):
    @mock.patch("django.db.models.base.Model.save")
    def test_create_model(self, mock_save):
        csv_file = CSVFiles(
            name="Inventary",
            column_set_string="id-name-quantity-price",
            file="/csv_files/Inventary.csv",
        )
        csv_file.save()

        mock_save.assert_called()
        assert isinstance(csv_file, CSVFiles)

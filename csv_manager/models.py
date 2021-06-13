"""
Models improvements based on https://sunscrapers.com/blog/6-expert-tips-for-building-better-django-models/
"""
from django.db import models
from django.utils import timezone


class SoftDeletableQS(models.QuerySet):
    def delete(self, **kwargs):
        self.update(deleted_at=timezone.now(), **kwargs)

    def hard_delete(self, **kwargs):
        super().delete(**kwargs)


class SoftDeletableManager(models.Manager):
    def get_queryset(self):
        return SoftDeletableQS(
            model=self.model, using=self._db, hints=self._hints
        ).filter(deleted_at__isnull=True)


class SoftDeletableModel(models.Model):
    objects = SoftDeletableManager()
    archive_objects = models.Manager()
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()


class CSVFiles(SoftDeletableModel):
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        unique=True,
        db_index=True,
        help_text="Please, Write an unique name for CSV file",
    )
    column_set_string = models.TextField(
        null=False,
        blank=False,
    )
    file = models.FileField(upload_to="csv_files/")
    is_store = models.BooleanField(null=False, blank=False, default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

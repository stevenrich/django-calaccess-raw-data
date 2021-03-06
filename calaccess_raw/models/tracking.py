#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from hurry.filesize import size as sizeformat
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class RawDataVersion(models.Model):
    """
    A version of CAL-ACCESS raw source data, typically released every day
    """
    release_datetime = models.DateTimeField(
        unique=True,
        null=False,
        verbose_name='date and time of release',
        help_text='Date and time the version of the CAL-ACCESS database was released '
                  '(value of last-modified field in HTTP response header)'
    )
    size = models.IntegerField(
        null=False,
        verbose_name='size of raw data version in bytes',
        help_text='Size of the .ZIP file for this version of the CAL-ACCESS raw source data '
                  '(value of content-length field in HTTP response header)'
    )

    class Meta:
        app_label = 'calaccess_raw'
        verbose_name = 'CAL-ACCESS raw data version'
        ordering = ('-release_datetime',)

    def __str__(self):
        return str(self.release_datetime)

    def pretty_size(self):
        return sizeformat(self.size)
    pretty_size.short_description = 'size'
    pretty_size.admin_order_field = 'size'


@python_2_unicode_compatible
class RawDataFile(models.Model):
    """
    A data file included in a version of the CAL-ACCESS raw source data
    """
    version = models.ForeignKey(
        'RawDataVersion',
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='raw data version',
        help_text='Foreign key referencing the version of the raw '
                  'source data in which the file was included'
    )
    file_name = models.CharField(
        max_length=100,
        verbose_name='raw data file name',
        help_text='Name of the raw source data file without extension',
    )
    download_records_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='download records count',
        help_text='Count of records in the original file downloaded from CAL-ACCESS'
    )
    clean_records_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='clean records count',
        help_text='Count of records in the cleaned file generated by calaccess_raw'
    )
    load_records_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='load records count',
        help_text="Count of records in the loaded from cleaned file into "
                  "calaccess_raw's data model"
    )
    download_columns_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='download columns count',
        help_text='Count of columns in the original file downloaded from CAL-ACCESS'
    )
    clean_columns_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='clean columns count',
        help_text='Count of columns in the cleaned file generated by calaccess_raw'
    )
    load_columns_count = models.IntegerField(
        null=False,
        default=0,
        verbose_name='load columns count',
        help_text='Count of columns on the loaded calaccess_raw data model'
    )

    class Meta:
        app_label = 'calaccess_raw'
        unique_together = (('version', 'file_name'),)
        verbose_name = 'CAL-ACCESS raw data file'
        ordering = ('-version_id', 'file_name',)

    def __str__(self):
        return self.file_name


@python_2_unicode_compatible
class RawDataCommand(models.Model):
    """
    A call of a command from this application with start and finish times
    """
    version = models.ForeignKey(
        'RawDataVersion',
        on_delete=models.CASCADE,
        related_name='command_logs',
        verbose_name='raw data version',
        help_text='Foreign key referencing the version of the raw '
                  'source data on which the command was performed'
    )
    command = models.CharField(
        max_length=50,
        verbose_name='command name',
        help_text='Name of the command performed on the given version of the raw source data'
    )
    called_by = models.ForeignKey(
        'self',
        related_name="called",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='called by',
        help_text='Foreign key refencing log of the CalAccessCommand that '
                  'called this command. Null represents call from command line'
    )
    file_name = models.CharField(
        max_length=100,
        verbose_name='raw data file name',
        help_text='Name of the raw source data file without extension',
    )
    start_datetime = models.DateTimeField(
        auto_now_add=True,
        null=False,
        verbose_name='date and time command started',
        help_text='Date and time when the given command started on the '
                  'given version of the raw source data'
    )
    finish_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time command finished',
        help_text='Date and time when the given command finished on '
                  'the given version of the raw source data'
    )

    class Meta:
        app_label = 'calaccess_raw'
        verbose_name = 'CAL-ACCESS raw data command'
        ordering = ('-id',)

    def __str__(self):
        return self.command

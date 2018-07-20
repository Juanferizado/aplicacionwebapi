# -*- coding: utf-8 -*-
"""
Basic building blocks for generic class based views.

We don't bind behaviour to http method handlers yet,
which allows mixin classes to be composed in interesting ways.
"""
from __future__ import unicode_literals
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings


class CreateModelMixin(object):
    """Create a model instance."""

    def create(self, request, *args, **kwargs):
        """."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """."""
        serializer.save()

    def get_success_headers(self, data):
        """."""
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}


class ListModelMixin(object):
    """List a queryset."""

    def list(self, request, *args, **kwargs):
        """."""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RetrieveModelMixin(object):
    """Retrieve a model instance."""

    def retrieve(self, request, *args, **kwargs):
        """."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UpdateModelMixin(object):
    """Update a model instance."""

    def update(self, request, *args, **kwargs):
        """."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        """."""
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        """."""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin(object):
    """Destroy a model instance."""

    def destroy(self, request, *args, **kwargs):
        """."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        """."""
        instance.delete()


class CancelModelMixin(object):
    """Mixin para ejecutar acción de anular alguna transacción.

    Se necesita implementar el metodo perform_cancel

    def perform_cancel(self, instance):
        pass
    """

    def cancel(self, request, *args, **kwargs):
        """."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.perform_cancel(instance)
        return Response(serializer.data)


class ChangeStatusModelMixin(object):
    """Mixin para ejecutar acción de cambiar estatus de alguna transacción.

    Se necesita implementar el metodo perform_change_status

    def perform_change_status(self, instance, estatus):
        pass
    """

    def change_status(self, request, *args, **kwargs):
        """."""
        instance = self.get_object()
        estatus = self.request.data.get('estatus', instance.estatus)
        estatus = estatus.upper()
        serializer = self.get_serializer(instance)
        self.perform_change_status(instance, estatus)
        return Response(serializer.data)


class ProcessStatusModelMixin(object):
    """Mixin para ejecutar acción de cambiar estatus de alguna transacción.

    Se necesita implementar el metodo perform_process_status
    Este metodo se debdfe de utilizar si modelo no tiene campo estatus

    def perform_process_status(self, instance, estatus):
        pass
    """

    def process_status(self, request, *args, **kwargs):
        """."""
        instance = self.get_object()
        process = self.request.data.get('process', None)
        serializer = self.get_serializer(instance)
        self.perform_process_status(instance, process)
        return Response(serializer.data)

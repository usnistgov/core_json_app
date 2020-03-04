""" REST views for the data API
"""

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core_json_app.components.data import api as data_api
from core_json_app.rest.data.serializers import DataSerializer
from core_main_app.commons import exceptions
from core_main_app.utils.file import get_file_http_response


class DataList(APIView):
    """ List all user Data, or create a new one.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """ Create a Data

        Parameters:

            {
                "title": "document_title",
                "template": "template_id",
                "dict_content": "document_content"
            }

        Args:

            request: HTTP request

        Returns:

            - code: 201
              content: Created data
            - code: 400
              content: Validation error
            - code: 404
              content: Template was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Build serializer
            data_serializer = DataSerializer(data=request.data)
            # Validate data
            data_serializer.is_valid(True)
            # Save data
            data_serializer.save(user=request.user)

            # Return the serialized data
            return Response(data_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.DoesNotExist:
            content = {'message': 'Template not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DataDownload(APIView):
    """ Download JSON file in data
    """

    def get_object(self, request, pk):
        """ Get Data from db

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            Data
        """
        try:
            return data_api.get_by_id(pk, request.user)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """ Download the JSON file from a data

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 200
              content: JSON file
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            data_object = self.get_object(request, pk)

            return get_file_http_response(data_object.dict_content, data_object.title, 'application/json', 'json')
        except Http404:
            content = {'message': 'Data not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
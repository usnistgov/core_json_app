""" REST abstract views for the template version manager API
"""
from abc import ABCMeta, abstractmethod


from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView


from core_main_app.commons.exceptions import NotUniqueError, XSDError
from core_json_app.rest.template_version_manager.serializers import TemplateVersionManagerSerializer, \
    CreateTemplateSerializer


class AbstractTemplateList(APIView, metaclass=ABCMeta):
    """ Create a template
    """

    def post(self, request):
        """ Create a template

        Parameters:

            {
                "title": "title",
                "filename": "filename",
                "content": "<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'><xs:element name='root'/></xs:schema>"
            }

        Note:

            "dependencies_dict": json.dumps({"schemaLocation1": "id1" ,"schemaLocation2":"id2"})

        Args:

            request: HTTP request

        Returns:

            - code: 201
              content: Created template
            - code: 400
              content: Validation error / not unique / XSD error
            - code: 500
              content: Internal server error
        """
        try:
            # Build serializers
            template_serializer = CreateTemplateSerializer(data=request.data)
            template_version_manager_serializer = TemplateVersionManagerSerializer(data=request.data)

            # Validate data
            template_serializer.is_valid(True)
            template_version_manager_serializer.is_valid(True)

            # Save data
            template_version_manager_object = template_version_manager_serializer.save(user=self.get_user())
            template_serializer.save(template_version_manager=template_version_manager_object)

            return Response(template_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = {'message': validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except NotUniqueError:
            content = {'message': "A template with the same title already exists."}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except XSDError as xsd_error:
            content = {'message': "XSD Error: " + str(xsd_error)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as api_exception:
            content = {'message': str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @abstractmethod
    def get_user(self):
        """ Retrieve a user
        """
        raise NotImplementedError("get_user method is not implemented.")

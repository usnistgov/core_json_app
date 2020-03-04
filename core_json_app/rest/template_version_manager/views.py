""" REST views for the template version manager API
"""
from rest_framework.permissions import IsAuthenticated

from core_json_app.rest.template_version_manager.abstract_views import AbstractTemplateList


class UserTemplateList(AbstractTemplateList):
    """ Create a Template (linked to the user)
    """

    permission_classes = (IsAuthenticated, )

    def post(self, request):
        """ Create a Template (linked to the user)

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
              content: Created Template
            - code: 400
              content: Validation error / not unique / XSD error
            - code: 500
              content: Internal server error
        """
        return super(UserTemplateList, self).post(request)

    def get_user(self):
        """ Retrieve the user from the request

        Returns:

            User ID
        """
        return str(self.request.user.id)



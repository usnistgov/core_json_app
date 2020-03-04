"""Serializers used throughout the Rest API
"""
from rest_framework_mongoengine.serializers import DocumentSerializer


from core_main_app.components.template.models import Template
from core_json_app.components.template_version_manager import api as template_version_manager_api
from core_main_app.components.template_version_manager.models import TemplateVersionManager
from core_json_app.rest.template.serializers import TemplateSerializer

class TemplateVersionManagerSerializer(DocumentSerializer):
    """
        Template Version Manager serializer
    """
    class Meta(object):
        model = TemplateVersionManager
        fields = "__all__"
        read_only_fields = ['id',
                            'user',
                            'versions',
                            'current',
                            'is_disabled',
                            'disabled_versions']

    def create(self, validated_data):
        """ Create.

        Args:
            validated_data:

        Returns:

        """
        return TemplateVersionManager(**validated_data)


class CreateTemplateSerializer(TemplateSerializer):
    """
        Template Version Manager serializer
    """
    def create(self, validated_data):
        """
        Create and return a new `Template` instance, given the validated data.
        """
        template_object = Template(filename=validated_data['filename'],
                                   content=validated_data['content'])
        template_version_manager_object = validated_data['template_version_manager']

        # Create the template and its template version manager
        template_version_manager_api.insert(template_version_manager_object, template_object)

        return template_object

    def update(self, instance, validated_data):
        raise NotImplementedError("Template Version Manager should only be updated using specialized APIs.")

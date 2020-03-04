"""
Template API
"""
import hashlib
import logging
import json


from jsonschema import Draft7Validator


logger = logging.getLogger(__name__)


def upsert(template):
    """Save or Updates the template.

    Args:
        template:

    Returns:

    """
    # Check if schema is valid
    Draft7Validator.check_schema(json.loads(template.content))
    # Get hash for the template
    template.hash = hashlib.md5(template.content.encode("utf-8")).hexdigest()
    # Save template
    return template.save()


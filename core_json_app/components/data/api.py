""" Data API
"""
import datetime
import pytz
import json
import core_main_app.access_control.api
import core_main_app.components.workspace.access_control
from core_main_app.access_control.decorators import access_control
from core_main_app.commons import exceptions as exceptions
from jsonschema import validate

@access_control(core_main_app.access_control.api.can_write)
def upsert(data, user):
    """ Save or update the data.

    Args:
        data:
        user:

    Returns:

    """
    if data.dict_content is None:
        raise exceptions.ApiError("Unable to save data: dict_content field is not set.")

    data.last_modification_date = datetime.datetime.now(pytz.utc)
    check_dict_file_is_valid(data)
    return data.save()


def check_dict_file_is_valid(data):
    template = data.template
    try:
        validate(data.dict_content,json.loads(template.content))
    except Exception as valid_err:
        print("Validation KO: {}".format(valid_err))
        raise valid_err
    else:
        print("JSON validé")
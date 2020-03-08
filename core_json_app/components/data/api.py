""" Data API
"""
import datetime
import pytz
import json
import core_main_app.access_control.api
import core_main_app.components.workspace.access_control
from core_main_app.access_control.decorators import access_control
from core_main_app.commons import exceptions as exceptions
from core_main_app.components.data.models import Data
from jsonschema import validate
from core_main_app.settings import DATA_SORTING_FIELDS


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


def get_all_by_user(user, order_by_field=DATA_SORTING_FIELDS):
    """ Return all data owned by a user.

        Parameters:
            user:
            order_by_field: Order by field.

        Returns: data collection
    """
    return Data.get_all_by_user_id(str(user.id), order_by_field)


def get_by_id(data_id, user):
    """ Return data object with the given id.

        Parameters:
            data_id:
            user:

        Returns: data object
    """
    return Data.get_by_id(data_id)
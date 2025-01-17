import typing

from flask import current_app
from marshmallow.exceptions import ValidationError
from marshmallow.validate import Validator

_T = typing.TypeVar("_T")


class ExperimentsValidator(Validator):
    def __call__(self, value: _T) -> _T:
        current_app.logger.debug(f"Validating {value}")

        raise ValidationError(
            {
                "experiments": {
                    "layer": ["foobar"]
                }
            }
        )
        # return value

#!/usr/bin/env python

"""A mixin for validating form submissions"""

import re
import logging

class ValidationMixin(object):

    MSG_DEFAULT = u"is not valid"
    MSG_REQUIRED = u"is required"
    MSG_MUST_MATCH = u" doesn't match"

    ALPHA = r"^\D+$"
    NUMERIC = r"^\d+$"
    EMAIL = r"^[a-zA-Z0-9._%-+]+\@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,}$"
    USERNAME = r"^[a-z0-9._]{3,}$"

    def _help(self, specified, name, type):
        if specified is not None:
            self.errors[name] = specified
        else:
            self.errors[name] = name + " " + type

    def valid(self, arg_name, validator=None, help=None, name=None, required=True, force_type=None):
        """
        Tornado mixin for validating POST arguments
        Alternative to self.get_argument, but validates first
        Returns the argument after validating it
        Any validation errors will be in self.errors as a dict in the form:
            { field_name: help_message }

        Parameters:
        @arg_name: name of the argument to check
        @required: validate for filled-in first (default is True)
        @help: help message to display if argument doesn't validate
        @name: argument title, default is replacing _ with " " and capitalizing the arg name.
               this is how the field name appears in generated error messages
        @validator: can be either:
            - not specified
            - a validation function returning True or False
            - a string containing another argument name: the two must match
            - a string containing a regular expression: must match (case-insensitive)
            - a python type (int, float, bool)
        """
        value = self.get_argument(arg_name, None)
        value2 = self.get_argument(validator, None)

        if not hasattr(self, "errors"):
            self.errors = {}
        if not required and not validator:
            # nothing to validate
            return value
        if arg_name in self.errors:
            # already validated
            return value
        if not name:
            name = arg_name.replace("_", " ").capitalize()
        # not filled in ?
        if required and (value is None or len(value) == 0):
            self._help(help, name, ValidationMixin.MSG_REQUIRED)
        # doesn't match type ?
        elif force_type is not None:
            if force_type == bool:
                if value.lower() not in [ "1", "true", "yes", "on" ]:
                    self._help(help, name, ValidationMixin.MSG_DEFAULT)
            else:
                try:
                    force_type(value)
                except ValueError:
                    self._help(help, name, ValidationMixin.MSG_DEFAULT)
        # doesn't match custom function ?
        elif type(validator) == type(self.valid):
            if not validator(value):
                self._help(help, name, ValidationMixin.MSG_DEFAULT)
        # doesn't match another argument ?
        elif value2 is not None:
            if value != value2:
                self._help(help, name, ValidationMixin.MSG_MUST_MATCH)
        # doesn't match regex format ?
        elif type(validator) == str:
            if re.match(validator, value, re.IGNORECASE) is None:
                self._help(help, name, ValidationMixin.MSG_DEFAULT)
        return value


class RangeValidator(object):
    def __init__(self, max, min):
        self.max = max
        self.min = min

    def validate(value):
        return (self.min <= value <= self.max)
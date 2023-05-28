from pydantic import BaseModel as PydanticBaseModel, validate_model
from pydantic import Extra


class BaseModel(PydanticBaseModel):
    """
    Base model to be inherited
    """

    def __hash__(self):  # make hashable BaseModel subclass
        return hash((type(self),) + tuple(self.__dict__.values()))

    def check(self):
        """
        Used to manually run validations

        :return: None
        """
        *_, validation_error = validate_model(self.__class__, self.__dict__)
        if validation_error:
            raise validation_error

    class Config:
        """
        The configuration class for the base model
        """

        arbitrary_types_allowed = True
        validate_assignment = True
        anystr_strip_whitespace = True
        extra = Extra.ignore
        # use_enum_values = True

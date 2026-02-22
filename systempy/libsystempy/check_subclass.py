from .constants import lifecycle_disallowed_attrs
from .register import lifecycle_disallowed_method_exempt


def check_on_subclassing(cls: type) -> None:
    clsdict = vars(cls)
    for check_attribute, description in lifecycle_disallowed_attrs:
        if check_attribute in clsdict:
            attr_val = clsdict[check_attribute]
            if attr_val in lifecycle_disallowed_method_exempt:
                continue

            message = f"Attribute {check_attribute} is not allowed"

            if description:
                message = f"{message}. {description}"

            raise ValueError(message, cls)

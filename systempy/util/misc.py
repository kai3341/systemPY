def create_dict_registerer(target_dict):
    def outer(name_or_target):
        passed_name = isinstance(name_or_target, str)

        if passed_name:
            name = name_or_target
        else:
            name = name_or_target.__name__

        def registerer(target):
            target_dict[name] = target
            return target

        if passed_name:
            return registerer
        else:
            return registerer(name_or_target)

    return outer


def get_key_or_create(the_dict, key, default_factory=dict):
    """
    Like DefaultDict
    """
    if key in the_dict:
        return the_dict[key]
    else:
        value = default_factory()
        the_dict[key] = value
        return value

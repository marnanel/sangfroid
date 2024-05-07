def normalise_synfig_layer_type_name(s):
    """
    Changes a value of the "name" attribuyte on a <layer> tag
    into its normal form.

    Args:
        s (str): the name

    Returns:
        str
    """
    return s.lower().replace('_', '')

def type_and_value_to_str(t, v):
    if v is None:
        return None
    elif issubclass(t, bool):
        return str(bool(v)).lower()
    else:
        return str(v)

def type_and_str_to_value(t, s):
    if v is None:
        return None
    elif issubclass(t, bool):
        return v.lower()=='true'
    else:
        return t(v)

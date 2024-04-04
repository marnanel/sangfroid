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

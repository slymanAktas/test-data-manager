import tckn


def generate_tckn():
    tckn_data = tckn.generate()
    is_tckn_valid = tckn.validate(tckn_data)
    return {
        'tckn': tckn_data,
        'isValid': is_tckn_valid
    }

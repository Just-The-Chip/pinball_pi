def build_component_message(target_id, option_value=1):
    message = (target_id << 8) | option_value

    return message.to_bytes(2, "big") + b'\n'


def build_light_message(group_id, pattern_id, variant_id=0, option_value=0):
    message = (group_id << 24) | (pattern_id << 16) | (
        variant_id << 8) | option_value
    return message.to_bytes(4, "big") + b'\n'

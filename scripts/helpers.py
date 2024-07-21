def specified_color(is_syn, check_arg, default_colors, index, session):
    span_start = '<span style="color: '
    span_end = ';">'
    if not is_syn:
        if check_arg:
            return span_start + default_colors[str(index)] + span_end
        else:
            return span_start + session["color" + str(str(index + 1))] + span_end
    else:
        if check_arg:
            return span_start + default_colors[str(index)] + span_end
        else:
            return span_start + session["color" + str(index + 1)] + span_end
def parse_text(html: str):
    return html\
        .replace('<', '&#60;') \
        .replace('>', '&#62;') \
        .replace('=', '&#61')

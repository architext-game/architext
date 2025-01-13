# import architext.chatbot.util
# locale = architext.chatbot.util.get_config()['locale']

import gettext as _gettext

gnu_translations = _gettext.translation(
    domain='architext',
    localedir='architext/chatbot/locale/',
    languages=['en_US']
)

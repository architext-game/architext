# set up internationalization
import architext.util
locale = architext.util.get_config()['locale']

import gettext as _gettext

gnu_translations = _gettext.translation(
    domain='architext',
    localedir='architext/locale/',
    languages=[locale]
)
gnu_translations.install()  # Magically make the _ function globally available

import architext.session
import architext.entities
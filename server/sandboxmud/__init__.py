# set up internationalization
import sandboxmud.util
locale = sandboxmud.util.get_config()['locale']

import gettext as _gettext

gnu_translations = _gettext.translation(
    domain='sandboxmud',
    localedir='sandboxmud/locale/',
    languages=[locale]
)
gnu_translations.install()  # Magically make the _ function globally available

import sandboxmud.session
import sandboxmud.entities
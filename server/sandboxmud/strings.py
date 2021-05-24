many_found         = _("There is more than one thing with a similar name. Be more specific.")
not_found          = _("You can't find that here.")
cancelled          = _("Action cancelled")
cancel_prompt      = _('❌ You can send "/" anytime to cancel.')
is_empty           = _("It can't be empty.")
wrong_format       = _("The name cannot end with # followed by a number. Try another one.")
room_name_clash    = _("There is already an item or exit with that name in this room. Try another one.")
takable_name_clash = _("There is a takable item with that name in this world. Takable items need a unique name, so try with another one.")


def format(title, body, cancel=False):
    subtitle_bar = '─'*len(title)
    cancel = cancel_prompt + '\n\n' if cancel else ''
    return f'{title}\n{subtitle_bar}\n{cancel}{body}'
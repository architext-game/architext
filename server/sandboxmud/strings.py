many_found        = _("There is more than one thing with a similar name. Be more specific.")
not_found         = _("You can't find that here.")
cancelled         = _("Action cancelled")
cancel_prompt     = _('❌ You can send "/" anytime to cancel.')
is_empty         = _("It can't be empty.")


def format(title, body, cancel=False):
    subtitle_bar = '─'*len(title)
    cancel = cancel_prompt + '\n\n' if cancel else ''
    return f'{title}\n{subtitle_bar}\n{cancel}{body}'
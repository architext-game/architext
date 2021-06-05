many_found         = _("There is more than one thing with a similar name. Be more specific.")
not_found          = _("You can't find that here.")
cancelled          = _("Action cancelled")
cancel_prompt      = _('❌ You can send "/" anytime to cancel.')
is_empty           = _("It can't be empty.")
wrong_format       = _("The name cannot end with # followed by a number. Try another one.")
room_name_clash    = _("There is already an item or exit with that name in this room. Try another one.")
takable_name_clash = _("There is a takable item with that name in this world. Takable items need a unique name, so try with another one.")
room_not_found     = _("There is not a room with that room number. Try another one.")
not_a_number       = _("Please enter a number.")
wrong_value        = _("Please enter the value of one of the options.")
has_line_breaks    = _("It can't contain line breaks.")

default_description = _("It's nothing special.")

# item edition and creation
visibility_list    = _(
    '  (l) "listed"  ─ the item will be automatically listed in the room description.\n'
    '  (v) "visible" ─ it won\'t be listed in room description.\n'
    '  (h) "hidden"  ─ it won\'t even be listed by the "items" verb.\n'
    '  (t) "takable" ─ players will be able to take the item into their inventory. It will be a listed item. Its name will need to be unique in the world.'
)
visible_input_options = [_('visible'), _('v'), _('vi')]
listed_input_options  = [_('listed'), _('l'), _('li')]
hidden_input_options  = [_('hidden'), _('h'), _('hi')]
takable_input_options = [_('takable'), _('t'), _('ta')]
yes_input_options = [_('yes'), _('y')]
no_input_options = [_('no'), _('n')]

# world edition
public  = _('public')
private = _('private')

user_name_placeholder = _('.user')

def format(title, body, cancel=False):
    subtitle_bar = '─'*len(title)
    cancel = cancel_prompt + '\n\n' if cancel else ''
    return f'{title}\n{subtitle_bar}\n{cancel}{body}'

def box(string):
   return (
        '┏━━━━{fillin}━━━━┓\n'
        '┃    {string}    ┃\n'
        '┗━━━━{fillin}━━━━┛\n'
    ).format(
        string=string,
        fillin='━'*len(string),
    )
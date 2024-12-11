from .verb import Verb, NOBOT
import rolldice

class RollDice(Verb):
    """Rolls dice. Dice are specified using CritDice notation."""

    command = _('roll ')
    permissions = NOBOT

    def process(self, message):
        command_length = len(self.command)
        dice_str = message[command_length:]
        try:
            result, explanation = rolldice.roll_dice(dice_str)
        except rolldice.rolldice.DiceGroupException:
            self.session.send_to_client(_("That is not a valid dice expression. You can see valid expresions here: https://github.com/Fiona1729/py-rolldice#dice-syntax"))
        else:
            self.session.send_to_room(_(
                '{user_name} rolls {dice_str} and gets a {result} ({explanation})'
            ).format(
                user_name=self.session.user.name,
                dice_str=dice_str,
                result=result,
                explanation=explanation
            ))
        self.finish_interaction()
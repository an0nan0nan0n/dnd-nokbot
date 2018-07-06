"""
Rolls dice using the following command syntax:

/roll 1d6 where 1 is the number of dice, d6 is the sides of each dice.
Output in Discord chat: *User* rolled 1d6: *result*

Can do other rolls such as 1d20, 1d100, etc.

Also supports "bonuses" for rolls such as "1d6+50" where "+50" is the bonus
Can also do negative "penalties" the same way.
"""

import random
import re
from discord.ext import commands
from helpers import ROLLER_MESSAGES


class DiceRoller(object):
    """Handles the dice rolls."""
    def parse_roll(roll_arg, roll_bonus: bool):
        """Return a parsed regex object for doing a valid dice roll."""
        if roll_bonus:
            roll_string = re.search(
                r'^[\d*]{1,3}d[\d*]{1,3}[\+-][\d*]{1,3}$', roll_arg)
        else:
            roll_string = re.search(r'^[(\d*)]{1,3}d[\d*]{1,3}$', roll_arg)
        return roll_string

    def roll_dice(dice_count, dice_sides, bonus):
        """Roll a dice for a random outcome.

        number_of_dice is an int representing how many dice to roll.
        dice_sides is an int representing how many sides on each die rolled.
        bonus is an int representing how much to add/subtract from the roll.
        """
        roll_stats = {
            'roll_results': [],
            'total': 0,
            'bonus': 0,
        }
        for dice in range(0, dice_count):
            dice = random.randint(1, dice_sides)
            roll_stats['roll_results'].append(dice)
        roll_stats['total'] = int(sum(
            roll_stats['roll_results']) + bonus)
        roll_stats['bonus'] = bonus
        return roll_stats


@commands.command(case_insensitive=True, pass_context=True)
async def roll(ctx, arg):
    """Roll dice."""
    # Setup, fail message if invalid.
    updated_arg = arg.lower()
    roll_bonus = '-' in updated_arg or '+' in updated_arg
    roll_string = DiceRoller.parse_roll(updated_arg, roll_bonus)
    try:
        valid_roll = roll_string.string
        if '-' in valid_roll:
            splitter = '-'
        elif '+' in valid_roll:
            splitter = '+'
        dice_count = int(valid_roll.split('d')[0])
        if roll_bonus:
            dice_sides = int(valid_roll.split('d')[1].split(splitter)[0])
            dice_bonus = int(valid_roll.split('d')[1].split(splitter)[1])
        else:
            dice_sides = int(valid_roll.split('d')[1])
            dice_bonus = 0
        rolled_dice = DiceRoller.roll_dice(dice_count, dice_sides, dice_bonus)
        await ctx.send(
            ROLLER_MESSAGES['success_result'].format(
                rolled_dice['roll_results'], rolled_dice['bonus'],
                rolled_dice['total']))
    except AttributeError:  # Fail if valid_roll isn't created
        await ctx.send(ROLLER_MESSAGES['invalid_roll'].format(arg))
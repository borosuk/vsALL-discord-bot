import discord
import random

# Need some values or it fails: discord.errors.HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body
    # In data.components.0.components.0.options: Must be between 1 and 25 in length.
OPTIONS = [ # the list of options from which users can choose, a required field
    discord.SelectOption(
        label="placeholder",
        description="placeholder, ignore"
    )
]

RPSChoices = {
    'rock': {
        'description': 'sedimentary, igneous, or perhaps even metamorphic',
        'emoji': '🪨',
        'responses': {
            'virus': 'outwaits',
            'computer': 'smashes',
            'scissors': 'crushes'
        }
    },
    'cowboy': {
        'description': 'yeehaw~',
        'emoji': '🤠',
        'responses': {
            'scissors': 'puts away',
            'wumpus': 'lassos',
            'rock': 'steel-toe kicks'
        }
    },
    'scissors': {
        'description': 'careful ! sharp ! edges !!',
        'emoji': '✂️',
        'responses': {
            'paper': 'cuts',
            'computer': 'cuts cord of',
            'virus': 'cuts DNA of'
        }
    },
    'virus': {
        'description': 'genetic mutation, malware, or something inbetween',
        'emoji': '☣️',
        'responses': {
            'cowboy': 'infects',
            'computer': 'corrupts',
            'wumpus': 'infects'
        }
    },
    'computer': {
        'description': 'beep boop beep bzzrrhggggg',
        'emoji': '🖥️',
        'responses': {
            'cowboy': 'overwhelms',
            'paper': 'uninstalls firmware for',
            'wumpus': 'deletes assets for'
        }
    },
    'wumpus': {
        'description': 'the purple Discord fella',
        'emoji': '🧸',
        'responses': {
            'paper': 'draws picture on',
            'rock': 'paints cute face on',
            'scissors': 'admires own reflection in'
        }
    },
    'paper': {
        'description': 'versatile and iconic',
        'emoji': '📄',
        'responses': {
            'virus': 'ignores',
            'cowboy': 'gives papercut to',
            'rock': 'covers'
        }
    }
}

def formatOption(label, value, description, emoji=None, default=False):
    return discord.SelectOption(
        label = label,
        value = value,
        description = description,
        emoji = emoji,
        default = default
    )

class CRPSAcceptChallenge(discord.ui.View):

    @discord.ui.button(label="Accept", row=0, style=discord.ButtonStyle.success)
    async def accept_button_callback(self, button, interaction):
        await interaction.response.send_message(f"Crazy Rock papers scissors challenge from {interaction.user.mention}", view=CRPSChooseChallenge())


class CRPSChooseChallenge(discord.ui.View):

    def __init__(self):
        OPTIONS.clear()
        for choice in RPSChoices:
            OPTIONS.append(
                formatOption(choice, choice, RPSChoices[choice]['description'], RPSChoices[choice]['emoji'])
            )
        random.shuffle(OPTIONS)
        super().__init__()

    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "What is your object of choice?", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = OPTIONS
    )
    async def select_challenge_callback(self, select, interaction): # the function called when the user is done selecting options
        await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")
import discord
import random

CRPSChoices = {
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

def getSelection():

    CRPSSelection = discord.Option(
            str,
            name = "selection",
            description = "Pick your object!",
            choices = getChoices(),
            required = True,
            min_values = 1,
            max_values = 1
        )
    
    return CRPSSelection


def getOptions():
    OPTIONS = []

    for choice in CRPSChoices:
        OPTIONS.append(
            formatOption(choice, choice, CRPSChoices[choice]['description'], CRPSChoices[choice]['emoji'])
        )

    random.shuffle(OPTIONS)

    return OPTIONS


def getChoices():
    CHOICES = []

    for choice in CRPSChoices:
        CHOICES.append(
            formatChoice(choice, choice)
        )

    random.shuffle(CHOICES)

    return CHOICES


def formatChoice(name, value):
    return discord.OptionChoice(
        name = name.capitalize(),
        value = value.lower()
    )


def formatOption(label, value, description, emoji=None, default=False):
    return discord.SelectOption(
        label = label.capitalize(),
        value = value.lower(),
        description = description,
        emoji = emoji,
        default = default
    )


class CRPSAcceptChallenge(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # timeout of the view must be set to None

    @discord.ui.button(label="Accept", custom_id = "crps-accept-button", row=0, style=discord.ButtonStyle.success)
    async def accept_button_callback(self, button, interaction):
        await interaction.response.send_message(f"Crazy Rock papers scissors challenge from {interaction.user.mention}", view=CRPSChooseChallenge(), ephemeral = True)


class CRPSChooseChallenge(discord.ui.View):

    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose your object!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = getOptions()
    )
    async def select_challenge_callback(self, select, interaction): # the function called when the user is done selecting options
        await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")
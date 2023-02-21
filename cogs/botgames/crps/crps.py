import discord
import random
import vsalldb

CRPSChoices = {
    'rock': {
        'description': 'sedimentary, igneous, or perhaps even metamorphic',
        'emoji': '🪨',
        'versus': {
            'virus': 'outwaits',
            'computer': 'smashes',
            'scissors': 'crushes'
        }
    },
    'cowboy': {
        'description': 'yeehaw~',
        'emoji': '🤠',
        'versus': {
            'scissors': 'puts away',
            'wumpus': 'lassos',
            'rock': 'steel-toe kicks'
        }
    },
    'scissors': {
        'description': 'careful ! sharp ! edges !!',
        'emoji': '✂️',
        'versus': {
            'paper': 'cuts',
            'computer': 'cuts cord of',
            'virus': 'cuts DNA of'
        }
    },
    'virus': {
        'description': 'genetic mutation, malware, or something inbetween',
        'emoji': '☣️',
        'versus': {
            'cowboy': 'infects',
            'computer': 'corrupts',
            'wumpus': 'infects'
        }
    },
    'computer': {
        'description': 'beep boop beep bzzrrhggggg',
        'emoji': '🖥️',
        'versus': {
            'cowboy': 'overwhelms',
            'paper': 'uninstalls firmware for',
            'wumpus': 'deletes assets for'
        }
    },
    'wumpus': {
        'description': 'the purple Discord fella',
        'emoji': '🧸',
        'versus': {
            'paper': 'draws picture on',
            'rock': 'paints cute face on',
            'scissors': 'admires own reflection in'
        }
    },
    'paper': {
        'description': 'versatile and iconic',
        'emoji': '📄',
        'versus': {
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
    OPTIONS = [formatOption(choice, choice, CRPSChoices[choice]['description'], CRPSChoices[choice]['emoji']) for choice in CRPSChoices]
    random.shuffle(OPTIONS)

    return OPTIONS


def getChoices():
    CHOICES = [formatChoice(choice, choice) for choice in CRPSChoices]
    random.shuffle(CHOICES)

    return CHOICES


def getResult(player1, player2):
    gameResult = None

    if player2.objectName in CRPSChoices[player1.objectName]['versus']:
        # player1 wins
        gameResult = {
            'win': player1,
            'lose': player2,
            'verb': CRPSChoices[player1.objectName]['versus'][player2.objectName]
        }
    elif player1.objectName in CRPSChoices[player2.objectName]['versus']:
        # player2 wins
        gameResult = {
            'win': player2,
            'lose': player1,
            'verb': CRPSChoices[player2.objectName]['versus'][player1.objectName]
        }
    else:
        # tie -- win/lose don't
        gameResult = {
            'win': player1,
            'lose': player2,
            'verb': 'tie'
        }

    return formatResult(gameResult)
    

def formatResult(gameResult):
    win = gameResult['win']
    lose = gameResult['lose']
    verb = gameResult['verb']
    res = ""

    if gameResult['verb'] == 'tie':
        res = f"<@{win.id}> and <@{lose.id}> draw with **{win.objectName}**"
    else:
        res = f"<@{win.id}>'s **{win.objectName}** {verb} <@{lose.id}>'s **{lose.objectName}**"

    return res


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

class CRPSPlayer():
    def __init__(self, id, objectName):
        self.id = id
        self.objectName = objectName


class CRPSAcceptChallenge(discord.ui.View):
    def __init__(self, selection):
        self.selection = selection
        self.conn = vsalldb.get_connection()
        self.curs = self.conn.cursor()
        super().__init__(timeout = None) # timeout of the view must be set to None

    @discord.ui.button(label="Accept", custom_id = "crps-accept-button", row=0, style=discord.ButtonStyle.success)
    async def accept_button_callback(self, button, interaction):
        player1 = CRPSPlayer(interaction.user.id, self.selection)
        insertstm = f"INSERT INTO GAMES_CRPS (PLAYER1, PLAYER1_CHOICE) VALUES ({interaction.user.id}, '{self.selection}')"
        self.curs.execute(insertstm)
        insertedid = self.curs.lastrowid

        await interaction.response.send_message(f"Crazy Rock Paper Scissors challenge from {interaction.user.mention}", view=CRPSChooseChallenge(interaction.message.id, player1, insertedid), ephemeral = True, delete_after = 10)


class CRPSChooseChallenge(discord.ui.View):
    def __init__(self, msg_to_del, player1, insertedid):
        self.msg_to_del = msg_to_del
        self.player1 = player1
        self.insertedid = insertedid
        self.conn = vsalldb.get_connection()
        self.curs = self.conn.cursor()
        super().__init__()

    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose your object!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = getOptions()
    )
    async def select_challenge_callback(self, select, interaction): # the function called when the user is done selecting options
        # select.disabled = True # can't use the same response to edit_message(view=self), as we can't send a response after. TODO: fix this.
        player2 = CRPSPlayer(interaction.user.id, select.values[0])

        msg = await interaction.channel.fetch_message(self.msg_to_del)
        await msg.delete()

        result = getResult(self.player1, player2)
        updatestm = f'UPDATE GAMES_CRPS SET PLAYER2 = {interaction.user.id}, PLAYER2_CHOICE = "{select.values[0]}", RESULT = "{result}" WHERE ID = {self.insertedid}'
        self.curs.execute(updatestm)

        await interaction.response.send_message(f"{result}")
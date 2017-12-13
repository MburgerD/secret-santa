from utils import encode


class Santa:
    def __init__(self, name):
        self.name = name
        self.gifts = []  # list of Gift objects the santa will be giving

    def is_recipient(self, recipient):
        return recipient in [g.recipient for g in self.gifts]

    def add_gift(self, gift):
        self.gifts.append(gift)

    def see_now(self):
        for g in self.gifts:
            print('>>>>>>>>  {} with ${} budget'.format(g.recipient.name, g.budget))

    def see_code(self):
        message = ("merry christmas {} !!! \nyour santas are ...\n"
                   "{}".format(
                       self.name,
                       ', '.join(['{} (${})'.format(g.recipient.name, g.budget) for g in self.gifts]))
                   )
        return encode(message)


class Gift:
    def __init__(self, recipient, budget):
        self.recipient = recipient
        self.budget = budget


class Round:
    def __init__(self, budget):
        self.budget = budget


class SecretSanta:
    def __init__(self):
        self.santas = []
        self.rounds = []
        self.unique_recipients = True

    def add_santa(self, name):
        self.santas.append(Santa(name=name))

    def add_round(self, budget):
        self.rounds.append(Round(budget=budget))

    def all_names(self):
        return [santa.name for santa in self.santas]

    def number_rounds(self):
        return len(self.rounds)

    def get_santa(self, name):
        return [s for s in self.santas if s.name == name][0]

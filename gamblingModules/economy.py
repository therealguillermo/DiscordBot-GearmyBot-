import json

CREDITINC = 10

class Economy(object):
    def __init__(self):
        self.econ = json.loads(open('gamblingModules/econ.json').read())

    def create(self, user):
        key = str(user)
        if key not in self.econ.keys():
            self.econ[key] = 0
            return True
        else:
            return False
    
    def pump(self, users):
        for user in users:
            try:
                self.econ[str(user)] += CREDITINC
            except:
                self.create(user)
        self.save()

    def save(self):
        with open('gamblingModules/econ.json', 'w') as file:
            json.dump(self.econ, file)

    def setCoins(self, user, coins):
        self.econ[user] = coins

    def addCoins(self, user, coins):
        self.econ[user] += coins

    def subCoins(self, user, coins):
        self.econ[user] -= coins

    def get(self, user):
        return self.econ[user]
    
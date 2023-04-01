
class APIKEY():
    
    @staticmethod
    def getKey(key):
        with open("api_keys.txt", "r") as file:
            for line in file:
                data = line.split('=')
                if data[0] == key:
                    return data[1].strip()


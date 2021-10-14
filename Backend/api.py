import requests

# API Key from Riot Developer Portal
apiKey = "RGAPI-db3e3f9c-ea33-434b-bd60-35361a7a7587"

class riotAPI(object):
    def reqData(sName):
        # This functions requests data from your Summoner Name
        URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + sName + "?api_key=" + apiKey
        response = requests.get(URL)

        # Return raw json with relevant information
        return response.json()

    def reqRankData(id):
        # This functions requests data based on Summoner ID
        # Summoner ID is extracted from Summoner Name and used to create the following link.
        URL = "https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/" + id +"?api_key=" + apiKey
        response = requests.get(URL)

        # Return raw json with relevant information
        return response.json()

    def main ():
        # This functions asks for user input, then prints relevant information
        # Asks the user for their Summoner Name
        sName = (str)(input('Input Summoner Name: '))

        # Send user inuputted information to function reqData
        responseJSON = riotAPI.reqData(sName)

        # Assigning variables to the information that we want
        id = responseJSON['id']
        accountId = responseJSON['accountId']
        puuid = responseJSON['puuid']

        responseJSON2 = riotAPI.reqRankData(id)

        rTier = responseJSON2[0]['tier']
        rRank = responseJSON2[0]['rank']

        # This fails if player does not have a rank in TFT, make something to check that 
        # print(sName + ' is ' + rTier + ' ' + rRank + ' in Teamfight Tactics')
        # print("Summoner ID: " + id + "\nAccount ID: " + accountId + "\npuuid: " + puuid)

        return sName, rTier, rRank

    

if __name__ == "__main__":
    riotAPI.main()
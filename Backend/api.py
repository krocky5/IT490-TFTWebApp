import requests

# API Key from Riot Developer Portal
apiKey = "RGAPI-2555a7ee-300e-4ae5-b94a-812ace697f2a"

class riotAPI(object):
    def reqData(sumName):
        # This functions requests data from your Summoner Name
        URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + sumName + "?api_key=" + apiKey
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

    def reqMatchID(puuid):
        # This functions requests data based on Summoner puuid
        # Summoner puuid is extracted from Summoner Name and used to create the following link.
        URL = "https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/" + puuid + "/ids?count=20&api_key=" + apiKey
        response = requests.get(URL)

        # Return raw json with relevant information
        return response.json()

    def main ():
        # This functions asks for user input, then prints relevant information
        # Asks the user for their Summoner Name
        sumName = (str)(input('Input Summoner Name: '))

        # Send user inputted information 'sumName' to riotAPI's function reqData
        sumPlayerData = riotAPI.reqData(sumName)

        # Assigning variables to the information that we want
        id = sumPlayerData['id']
        accountId = sumPlayerData['accountId']
        puuid = sumPlayerData['puuid']

        # Sending 'id' to riotAPI's function reqRankData
        sumTFTRankData = riotAPI.reqRankData(id)

        # Sending 'puuid' to riotAPI's function reqMatchID
        sumTFTMatchID = riotAPI.reqMatchID(puuid)

        sumTier = sumTFTRankData[0]['tier']
        sumRank = sumTFTRankData[0]['rank']
        sumMatchID = sumTFTMatchID[0]
        print(sumName, sumTier, sumRank)
        return sumName, sumTier, sumRank

    
if __name__ == "__main__":
    riotAPI.main()
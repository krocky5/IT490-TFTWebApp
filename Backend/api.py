import json
import requests, sys, os, inflect

# API Key from Riot Developer Portal
apiKey = "RGAPI-5680df8a-8b8c-463b-b624-214f3627435c"

# inflect is used to create ordinal numbers
ordinalNumbers = inflect.engine()

# Response Errors (HTTP STATUS CODES)
errorCodes = [400, 401, 403, 404, 405, 415, 429, 500, 502, 503, 504]

class riotAPI(object):
    def reqData(sumName):
        # This functions requests data from your Summoner Name
        URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + sumName + "?api_key=" + apiKey
        response = requests.get(URL)

        # Return raw json with relevant information
        return response.json()

    def summonerIcon(iconNum):
        iconNum_as_str = str(iconNum)
        URL = "https://ddragon.leagueoflegends.com/cdn/11.21.1/img/profileicon/" + iconNum_as_str + ".png"
        return URL

    def reqRankData(sumId):
        # This functions requests data based on Summoner ID
        # Summoner ID is extracted from Summoner Name and used to create the following link.
        URL = "https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/" + sumId +"?api_key=" + apiKey
        response = requests.get(URL)

        # Return raw json with relevant information
        return response.json()

    def summonerName(playerPuuid):
        # This functions requests summoner named based on puuid

        URL = "https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/" + playerPuuid + "?api_key=" + apiKey
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

    def latestMatchIDStats(matchID):
        # This functions requests data based on latest match id.
        # Match id is extracted from reqMatchID and used to create the following link.
        URL = "https://americas.api.riotgames.com/tft/match/v1/matches/" + matchID + "?api_key=" + apiKey
        response = requests.get(URL)
        
        # Return raw json with relevant information
        return response.json()

    def main (sumName):
        # main function

        # Send user inputted information 'sumName' to riotAPI's function reqData
        sumPlayerData = riotAPI.reqData(sumName)

        # Error Checking
        try:
            # Checks if "name" in the JSON exists. When user does not exist, this field does not show up.
            sumPlayerData["name"] == True
            # Program will continue on.
        except Exception:
            # Check the HTTP Status Code
            if sumPlayerData['status']['status_code'] in errorCodes:
                eCode = sumPlayerData['status']['status_code']
                eCode_as_string = str(eCode)
                return "Summoner Name: " + sumName + " does not exist. Error Code: " + eCode_as_string
        
        # Assigning variables to the information we are passing to the above functions.
        sumId = sumPlayerData['id']
        accountId = sumPlayerData['accountId']
        puuid = sumPlayerData['puuid']
        playerIcon = sumPlayerData['profileIconId']

        # Sending 'id' to riotAPI's function reqRankData
        sumTFTRankData = riotAPI.reqRankData(sumId)

        # Check to see if the user has a TFT rank. 
        if sumTFTRankData == []:
            return sumName + " does not have a TFT rank."

        # Sending 'puuid' to riotAPI's function reqMatchID
        sumTFTMatchID = riotAPI.reqMatchID(puuid)

        # Sending 'playerIcon' to riotAPI's function summonerIcon
        sumIcon = riotAPI.summonerIcon(playerIcon)

        sumTier = sumTFTRankData[0]['tier']
        sumRank = sumTFTRankData[0]['rank']
        
        # Latest Match
        sumMatchID = sumTFTMatchID[0]

        # Latest Match Stats
        sumMatchIDStats = riotAPI.latestMatchIDStats(sumMatchID)
        

        # for loop that gets the name of each player in your game and their respective placement
        nameList =[]

        for i in range(0, 8):
            playerPuuid = sumMatchIDStats['info']['participants'][i]['puuid']
            playerPlacement = sumMatchIDStats['info']['participants'][i]['placement']
            playerLevel = sumMatchIDStats['info']['participants'][i]['level']
            addingOrdinal = ordinalNumbers.ordinal(playerPlacement)
            playerPlacement_as_string = str(addingOrdinal)
            playerLevel_as_string = str(playerLevel)
            playerStats = riotAPI.summonerName(playerPuuid)
            playerName = playerStats['name']
            nameList.append(playerName + " - Level: " + playerLevel_as_string + " - Finished " + playerPlacement_as_string)

        # string with information about Summoner + Tier + Rank
        sumString = sumName, sumTier, sumRank
        jsumString = ', '.join(sumString)

        # string of the player's in your last match w/ their level and placement
        nameListAsString = nameList
        jnameListAsString = '\n'.join(nameListAsString)
        
        finalResults = jsumString + "\nStats from Last Game:\n" + jnameListAsString
        return finalResults + '\n' + sumIcon


if __name__ == '__main__':
    try:
        riotAPI.main()
    except KeyboardInterrupt:
        print('\nProgram Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
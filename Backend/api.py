import requests, sys, os, inflect

# API Key from Riot Developer Portal
API_KEY = "RGAPI-db20d80a-37e0-4a44-b5fb-429858187bbb"

# Response Errors (HTTP STATUS CODES)
ERROR_CODES = [400, 401, 403, 404, 405, 415, 429, 500, 502, 503, 504]

# inflect module is used to create ordinal numbers
ordinal_numbers = inflect.engine()

class RiotAPI(object):
    def req_data(sum_name):
        # This function requests data from your Summoner Name
        URL = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{sum_name}?api_key={API_KEY}"
        response = requests.get(URL)

        # Return raw json with relevant information
        return response.json()

    def summoner_icon(icon_number):
        icon_number_as_string = str(icon_number)
        URL = f"https://ddragon.leagueoflegends.com/cdn/11.21.1/img/profileicon/{icon_number_as_string}.png"
        return URL

    def req_rank_data(sum_id):
        # This function requests data based on Summoner ID
        # Summoner ID is extracted from Summoner Name and used to create the following link.
        URL = f"https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/{sum_id}?api_key={API_KEY}"
        response = requests.get(URL)

        # Return raw json with relevant information
        return response.json()

    def summoner_name(player_puuid):
        # This function requests summoner named based on puuid

        URL = f"https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{player_puuid}?api_key={API_KEY}"
        response = requests.get(URL)

        # Return raw json with relevant information
        return response.json()

    def req_match_id(puuid):
        # This function requests data based on Summoner puuid
        # Summoner puuid is extracted from Summoner Name and used to create the following link.
        URL = f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count=20&api_key={API_KEY}"
        response = requests.get(URL)

        # Return raw json with relevant information
        return response.json()

    def latest_match_id_stats(match_id):
        # This function requests data based on latest match id.
        # Match id is extracted from req_match_id and used to create the following link.
        URL = f"https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}?api_key={API_KEY}"
        response = requests.get(URL)
        
        # Return raw json with relevant information
        return response.json()

    def main(sum_name):
        # main function
        # Send user inputted information 'sum_name' to RiotAPI's function req_data
        sum_player_data = RiotAPI.req_data(sum_name)

        # Error Checking
        try:
            # Checks if "name" in the JSON exists. When a user does not exist, this field does not show up.
            sum_player_data["name"] == True
            # Program will continue on.
        except Exception:
            # Check the HTTP Status Code
            if sum_player_data['status']['status_code'] in ERROR_CODES:
                e_code = sum_player_data['status']['status_code']
                e_code_as_string = str(e_code)
                return f"Summoner Name: {sum_name} does not exist.\nError Code: {e_code_as_string}"
        
        # Assigning variables to the information we are passing to the above functions.
        sum_id = sum_player_data['id']
        puuid = sum_player_data['puuid']
        player_icon = sum_player_data['profileIconId']

        # Sending 'id' to RiotAPI's function req_rank_data
        sum_TFT_rank_data = RiotAPI.req_rank_data(sum_id)

        # Check to see if the user has a TFT rank. 
        if (sum_TFT_rank_data == []): return f"{sum_name} does not have a TFT rank."
            
        # Sending 'puuid' to RiotAPI's function req_match_id
        sum_TFT_match_id = RiotAPI.req_match_id(puuid)

        # Sending 'player_icon' to RiotAPI's function summoner_icon
        sum_icon = RiotAPI.summoner_icon(player_icon)

        sum_tier = sum_TFT_rank_data[0]['tier']
        sum_rank = sum_TFT_rank_data[0]['rank']
    
        # Latest Match
        sum_match_id = sum_TFT_match_id[0]
        
        # Latest Match Stats
        sum_match_id_stats = RiotAPI.latest_match_id_stats(sum_match_id)
        
        # for loop that gets the name of each player in your game and their respective placement
        name_list = []
        for i in range(0, 8):
            player_puuid = sum_match_id_stats['info']['participants'][i]['puuid']
            player_placement = sum_match_id_stats['info']['participants'][i]['placement']
            player_level = sum_match_id_stats['info']['participants'][i]['level']
            adding_ordinal = ordinal_numbers.ordinal(player_placement)
            player_placement_as_string = str(adding_ordinal)
            player_level_as_string = str(player_level)
            player_stats = RiotAPI.summoner_name(player_puuid)
            player_name = player_stats['name']
            name_list.append(f"{player_name} - Level: {player_level_as_string} - Finished {player_placement_as_string}")

        # simple message that states your placement from your last game lmfao
        player_placement_list=[]
        for i in range(0,8):
            if puuid == sum_match_id_stats['info']['participants'][i]['puuid']:
                player_placement = sum_match_id_stats['info']['participants'][i]['placement']
                adding_ordinal = ordinal_numbers.ordinal(player_placement)
                player_placement_as_string = str(adding_ordinal)
                player_placement_list.append(player_placement_as_string)
        player_placement_list_as_string = ''.join(player_placement_list)
        ur_the_best = f"You placed {player_placement_list_as_string} in your last game!"

        # avg placement / wr over last 20 games
        total_number_of_matches = len(sum_TFT_match_id)
        first_place_counter = 0
        for i in range(total_number_of_matches):
            sum_match_id = sum_TFT_match_id[i]
            sum_match_id_stats = RiotAPI.latest_match_id_stats(sum_match_id)
            for i in range(0,8):
                if puuid == sum_match_id_stats['info']['participants'][i]['puuid']:
                    player_placement = sum_match_id_stats['info']['participants'][i]['placement']
                    if player_placement == 1:
                        first_place_counter += 1
        
        win_rate = (first_place_counter/total_number_of_matches) * 100
        winner = f"You have a {win_rate} % win rate over the last {total_number_of_matches} games!"

        # converting the tuple 'sum_string' into a string
        sum_string = sum_name, sum_tier, sum_rank
        join_sum_string = ', '.join(sum_string)

        # converting name_list into a string
        join_name_list = '\n'.join(name_list)
        
        # final results
        final_results = f"{join_sum_string}\nStats from Last Game:\n{join_name_list}"
        return f"{final_results}\n{sum_icon}\n{ur_the_best}\n{winner}"


if __name__ == '__main__':
    try:
        RiotAPI.main()
    except KeyboardInterrupt:
        print('\nProgram Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
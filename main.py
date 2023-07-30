import requests

def get_steam_id(api_key, vanity_url):
    base_url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
    params = {
        "key": api_key,
        "vanityurl": vanity_url
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        success = data.get("response", {}).get("success", 0)
        if success == 1:
            steam_id = data.get("response", {}).get("steamid", None)
            return steam_id
        else:
            print("Failed to resolve vanity URL.")
            return None
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None


def get_player_summaries(api_key, steam_id):
    base_url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    params = {
        "key": api_key,
        "steamids": steam_id
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

def main():
    api_key = "APIKEYHERE"  # Replace this with your own Steam API key

    print("Choose an option:")
    print("1. Enter Steam ID")
    print("2. Enter Vanity URL")
    option = input("Option (1/2): ")

    if option == "1":
        steam_id = input("Enter the Steam ID: ")
    elif option == "2":
        vanity_url = input("Enter the Vanity URL: ").strip()
        if not vanity_url:
            print("Vanity URL cannot be empty.")
            return
        steam_id = get_steam_id(api_key, vanity_url)
    else:
        print("Invalid option. Please choose 1 or 2.")
        return

    if steam_id:
        print(f"Resolved Steam ID: {steam_id}")

        output_type = input("(RAW/PRETTY/SIMPLE) Pick an output type: ").strip().lower()

        while output_type not in ["raw", "pretty", "simple"]:
            print("Invalid output type. Please enter 'raw', 'pretty', or 'simple'.")
            output_type = input("(RAW/PRETTY/SIMPLE) Pick an output type: ").strip().lower()

        data = get_player_summaries(api_key, steam_id)

        if data:
            print(f"Player Summaries (Output Type: {output_type}):")
            if output_type == "pretty":
                import json
                print(json.dumps(data, indent=2))
            elif output_type == "simple":
                player_info = data.get("response", {}).get("players", [{}])[0]
                avatar = player_info.get("avatar", "")
                profileurl = player_info.get("profileurl", "")
                personaname = player_info.get("personaname", "")
                country = player_info.get("loccountrycode", "")
                print(f"Avatar: {avatar}")
                print(f"Profile URL: {profileurl}")
                print(f"Personaname: {personaname}")
                print(f"Base Location: {country}")
            else:
                print(data)
        else:
            print("Data retrieval failed.")
    else:
        print("Steam ID retrieval failed.")

if __name__ == "__main__":
    main()

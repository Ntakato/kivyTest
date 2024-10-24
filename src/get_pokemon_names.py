import asyncio

import aiohttp
from kivy.app import App
from kivy.lang.builder import Builder

kv = '''
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        ToggleButton:
            id: btn1
            group: 'a'
            text: 'Japanese'
            on_press: app.button_pressed('ja-Hrkt')
        ToggleButton:
            id: btn2
            group: 'a'
            text: 'English'
            on_press: app.button_pressed('en')
        ToggleButton:
            id: btn3
            group: 'a'
            text: 'Korean'
            on_press: app.button_pressed('ko')
        Button:
            id: btn4
            group: 'a'
            text: 'Chinese'
            on_press: app.button_pressed('zh-Hans')
    Label:
        id: label
        status: 'Reading'
        text: 'Press Button!'
'''


BASE_URL = "https://pokeapi.co/api/v2/"


class PokemonApp(App):

    def build(self):
        self.loop = asyncio.get_running_loop()
        return Builder.load_string(kv)

    async def get_pokemon_name(self, session, url, language):
        async with session.get(url) as resp:
            print(f"request start: {url}")
            pokemon = await resp.json()
            name_info = next((item for item in pokemon['names'] if item['language']['name'] == language), None)
            if (name_info):
                print(name_info['name'])
                return name_info['name']
            return 'not found'

    async def get_pokemon_names(self, language):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for number in range(1, 151):
                url = f'{BASE_URL}/pokemon-species/{number}'
                tasks.append(asyncio.create_task(self.get_pokemon_name(session, url, language)))
            original_pokemon = await asyncio.gather(*tasks)
            print("=================")
            for pokemon in original_pokemon:
                print(pokemon)

    def button_pressed(self, language):
        asyncio.create_task(self.get_pokemon_names(language))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(PokemonApp().async_run())
    print('close')
    loop.close()

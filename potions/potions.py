import json

with open('potions.json', 'r') as fp:
	config = json.load(fp)


class Potion:
	def __init__(self, config: dict) -> None:
		self.name = config['name']
		self.extend = bool(config.get('extend'))
		self.enhance = bool(config.get('enhance'))
		self.duration = config.get('duration', '')
		self.recipe = '\n'.join( f'{k+1}. {i}' for k, i in enumerate(['Nether Wart'] + config['recipe']) )
		self.modifiers = ''
		if self.extend or self.enhance:
			modifiers = '/'.join((['§c+§r'] if self.extend else []) + (['§6II§r'] if self.enhance else []))
			modlen = len('/'.join((['+'] if self.extend else []) + (['II'] if self.enhance else [])))
			self.modifiers = f"{' ' * (23 - modlen - len(self.name))}[{modifiers}]"

		if self.extend:
			self.recipe += f'\n§c+. Redstone§r'

		if self.enhance:
			self.recipe += f'\n§6II. Glowstone§r'

		if self.duration:
			duration = f'Duration: {self.duration}'

			extend = {
				'180': 480,
				'90': 240,
				'45': 90,
				'20': 40,
			}

			enhance = {
				'180': 90,
				'45': 22,
				'20': 20,
			}

			if self.extend:
				duration += f' §c{extend[str(self.duration)]}§r'

			if self.enhance:
				duration += f' §6{enhance[str(self.duration)]}§r'

			self.duration = duration

		self.page_text = f"""
			§3{self.name}§r{self.modifiers}
			--------------------

			{self.recipe}

			{self.duration}
		""".replace('\t', '').strip()


with open('out.txt', 'w') as fp:
	fp.write('\n\n'.join([Potion(i).page_text for i in config['potions']]) )

"Data for Augh!chievements"

class Meta:
	def __init__(self, name, section):
		self.name = name
		self.section = section
		
		self.achievements = {}
		self.order = []
		self.progress = []
	
	def add_achievements(self, *achievements):
		for a_name, a_id, a_icon in achievements:
			self.achievements[a_name] = (a_id, a_icon)
			self.order.append(a_name)
	
	def add_progress(self, a_name, p_name, p_text):
		self.progress.append((a_name, p_name, p_text))
	
	def check_achievements(self, data):
		results = []
		
		for a_name in self.order:
			r = data.get(a_name, None)
			if r is not None:
				results.append(r[:10])
			else:
				found = False
				pro = [p for p in self.progress if p[0] == a_name]
				for p in pro:
					r = data.get(p[1], None)
					if r is not None:
						found = p[2]
						break
				
				results.append(found)
		
		return results

# ---------------------------------------------------------------------------

def get_data():
	metas = []
	
	# 10 man Malygos/Naxxramas/Sartharion
	m = Meta('Glory of the Raider', 4)
	m.add_achievements(
		('The Dedicated Few', 578, 'spell_shadow_raisedead'),
		('Arachnophobia', 1858, 'achievement_halloween_spider_01'),
		('Make Quick Werk Of Him', 1856, 'spell_shadow_abominationexplosion'),
		('The Safety Dance', 1996, 'ability_rogue_quickrecovery'),
		('Momma Said Knock You Out', 1997, 'spell_shadow_curseofmannoroth'),
		('Shocking!', 2178, 'spell_chargepositive'),
		('Subtraction', 2180, 'spell_chargenegative'),
		("The Spellweaver's Downfall", 622, 'achievement_dungeon_nexusraid'),
		("You Don't Have An Eternity", 1874, 'achievement_dungeon_nexusraid'),
		('A Poke In The Eye', 1869, 'achievement_dungeon_nexusraid_heroic'),
		('Gonna Go When the Volcano Blows', 2047, 'spell_shaman_lavaflow'),
		('The Twilight Zone', 2051, 'achievement_dungeon_coablackdragonflight_normal'),
		('The Hundred Club', 2146, 'inv_misc_head_dragon_blue'),
		('And They Would All Go Down Together', 2176, 'spell_deathknight_summondeathcharger'),
		("Denyin' the Scion", 2148, 'inv_elemental_mote_shadow01'),
		('The Undying', 2187, 'spell_holy_sealofvengeance'),
		("Just Can't Get Enough", 2184, 'spell_deathknight_plaguestrike'),
	)
	m.add_progress('The Twilight Zone', 'Twilight Duo', '+2')
	m.add_progress('The Twilight Zone', 'Twilight Assist', '+1')
	metas.append(m)
	
	# 25 man Malygos/Naxxramas/Sartharion
	m = Meta('Heroic: Glory of the Raider', 5)
	m.add_achievements(
		('Heroic: The Dedicated Few', 579, 'spell_shadow_raisedead'),
		('Heroic: Arachnophobia', 1859, 'achievement_halloween_spider_01'),
		('Heroic: Make Quick Werk Of Him', 1857, 'spell_shadow_plaguecloud'),
		('Heroic: The Safety Dance', 2139, 'ability_rogue_quickrecovery'),
		('Heroic: Momma Said Knock You Out', 2140, 'spell_shadow_curseofmannoroth'),
		('The Immortal', 2186, 'spell_holy_weaponmastery'),
		('Heroic: Shocking!', 2179, 'spell_chargepositive'),
		('Heroic: And They Would All Go Down Together', 2177, 'spell_deathknight_summondeathcharger'),
		('Heroic: Subtraction', 2181, 'spell_chargenegative'),
		("Heroic: The Spellweaver's Downfall", 623, 'achievement_dungeon_nexusraid_10man'),
		("Heroic: You Don't Have An Eternity", 1875, 'achievement_dungeon_nexusraid'),
		('Heroic: A Poke In The Eye', 1870, 'achievement_dungeon_nexusraid_25man'),
		('Heroic: Gonna Go When the Volcano Blows', 2048, 'spell_shaman_lavaflow'),
		("Heroic: Denyin' the Scion", 2149, 'inv_elemental_mote_shadow01'),
		('Heroic: The Twilight Zone', 2054, 'achievement_dungeon_coablackdragonflight_normal'),
		('Heroic: The Hundred Club', 2147, 'inv_misc_head_dragon_blue'),
		("Heroic: Just Can't Get Enough", 2185, 'spell_deathknight_plaguestrike'),
	)
	m.add_progress('Heroic: The Twilight Zone', 'Heroic: Twilight Duo', '+2')
	m.add_progress('Heroic: The Twilight Zone', 'Heroic: Twilight Assist', '+1')
	metas.append(m)
	
	# 10 man Ulduar
	m = Meta('Glory of the Ulduar Raider', 6)
	m.add_achievements(
		('Orbit-uary', 3056, 'inv_misc_shadowegg'),
		("Stokin' the Furnace", 2930, 'achievement_boss_ignis_01'),
		('Iron Dwarf, Medium Rare', 2923, 'achievement_dungeon_ulduarraid_irondwarf_01'),
		('Heartbreaker', 3058, 'inv_valentinescardtornleft'),
		('I Choose You, Steelbreaker', 2941, 'achievement_boss_theironcouncil_01'),
		('Disarmed', 2953, 'ability_warrior_disarm'),
		('Crazy Cat Lady', 3006, 'achievement_boss_auriaya_01'),
		('I Could Say That This Cache Was Rare', 3182, 'inv_box_04'),
		('Lose Your Illusion', 3176, 'achievement_boss_thorim'),
		('Knock, Knock, Knock on Wood', 3179, 'achievement_boss_warpsplinter'),
		('Firefighter', 3180, 'inv_misc_bomb_04'),
		('I Love the Smell of Saronite in the Morning', 3181, 'achievement_boss_generalvezax_01'),
		('One Light in the Darkness', 3158, 'spell_shadow_shadesofdarkness'),
	)
	m.add_progress('Orbit-uary', 'Nuked from Orbit', '+3')
	m.add_progress('Orbit-uary', 'Orbital Devastation', '+2')
	m.add_progress('Orbit-uary', 'Orbital Bombardment', '+1')
	m.add_progress('Knock, Knock, Knock on Wood', 'Knock, Knock on Wood', '+2')
	m.add_progress('Knock, Knock, Knock on Wood', 'Knock on Wood', '+1')
	m.add_progress('One Light in the Darkness', 'Two Lights in the Darkness', '-2')
	m.add_progress('One Light in the Darkness', 'Three Lights in the Darkness', '-1')
	metas.append(m)
	
	# 25 man Ulduar
	m = Meta('Heroic: Glory of the Ulduar Raider', 7)
	m.add_achievements(
		('Heroic: Orbit-uary', 3057, 'inv_misc_shadowegg'),
		("Heroic: Stokin' the Furnace", 2929, 'achievement_boss_ignis_01'),
		('Heroic: Iron Dwarf, Medium Rare', 2924, 'achievement_dungeon_ulduarraid_irondwarf_01'),
		('Heroic: Heartbreaker', 3059, 'inv_valentinescardtornleft'),
		('Heroic: I Choose You, Steelbreaker', 2944, 'achievement_boss_theironcouncil_01'),
		('Heroic: Disarmed', 2954, 'ability_warrior_disarm'),
		('Heroic: Crazy Cat Lady', 3007, 'achievement_boss_auriaya_01'),
		('Heroic: I Could Say That This Cache Was Rare', 3184, 'inv_box_04'),
		('Heroic: Lose Your Illusion', 3183, 'achievement_boss_thorim'),
		('Heroic: Knock, Knock, Knock on Wood', 3187, 'achievement_boss_warpsplinter'),
		('Heroic: Firefighter', 3189, 'inv_misc_bomb_04'),
		('Heroic: I Love the Smell of Saronite in the Morning', 3188, 'achievement_boss_generalvezax_01'),
		('Heroic: One Light in the Darkness', 3163, 'spell_shadow_shadesofdarkness'),
	)
	m.add_progress('Heroic: Orbit-uary', 'Heroic: Nuked from Orbit', '+3')
	m.add_progress('Heroic: Orbit-uary', 'Heroic: Orbital Devastation', '+2')
	m.add_progress('Heroic: Orbit-uary', 'Heroic: Orbital Bombardment', '+1')
	m.add_progress('Heroic: Knock, Knock, Knock on Wood', 'Heroic: Knock, Knock on Wood', '+2')
	m.add_progress('Heroic: Knock, Knock, Knock on Wood', 'Heroic: Knock on Wood', '+1')
	m.add_progress('Heroic: One Light in the Darkness', 'Heroic: Two Lights in the Darkness', '-2')
	m.add_progress('Heroic: One Light in the Darkness', 'Heroic: Three Lights in the Darkness', '-1')
	metas.append(m)
	
	return metas

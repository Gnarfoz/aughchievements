"Data for Augh!chievements"

class Meta:
	def __init__(self, name, section, cutoff=None):
		self.name = name
		self.section = section
		self.cutoff = cutoff
		
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
	
	def check_meta_cutoff(self, data):
		'Check the cutoff date for the meta'
		
		dates = [d for d in data if d is not False and len(d) == 10]
		dates.sort()
		
		if len(dates) == 0:
			return (None, False)
		
		if len(dates) < len(data):
			return (False, False)
		
		if self.cutoff is None or dates[-1] < self.cutoff:
			return (True, True)
		else:
			return (True, False)

# ---------------------------------------------------------------------------

def get_data():
	metas = []
	
	# 10 man Malygos/Naxxramas/Sartharion
	m = Meta('Glory of the Raider (10 player)', 4, cutoff='2009-04-14')
	m.add_achievements(
		('The Dedicated Few (10 player)', 578, 'spell_shadow_raisedead'),
		('Arachnophobia (10 player)', 1858, 'achievement_halloween_spider_01'),
		('Make Quick Werk Of Him (10 player)', 1856, 'spell_shadow_abominationexplosion'),
		('The Safety Dance (10 player)', 1996, 'ability_rogue_quickrecovery'),
		('Momma Said Knock You Out (10 player)', 1997, 'spell_shadow_curseofmannoroth'),
		('Shocking! (10 player)', 2178, 'spell_chargepositive'),
		('Subtraction (10 player)', 2180, 'spell_chargenegative'),
		("The Spellweaver's Downfall (10 player)", 622, 'achievement_dungeon_nexusraid'),
		("You Don't Have An Eternity (10 player)", 1874, 'achievement_dungeon_nexusraid'),
		('A Poke In The Eye (10 player)', 1869, 'achievement_dungeon_nexusraid_heroic'),
		('Gonna Go When the Volcano Blows (10 player)', 2047, 'spell_shaman_lavaflow'),
		('The Twilight Zone (10 player)', 2051, 'achievement_dungeon_coablackdragonflight_normal'),
		('The Hundred Club (10 player)', 2146, 'inv_misc_head_dragon_blue'),
		('And They Would All Go Down Together (10 player)', 2176, 'spell_deathknight_summondeathcharger'),
		("Denyin' the Scion (10 player)", 2148, 'inv_elemental_mote_shadow01'),
		('The Undying', 2187, 'spell_holy_sealofvengeance'),
		("Just Can't Get Enough (10 player)", 2184, 'spell_deathknight_plaguestrike'),
	)
	m.add_progress('The Twilight Zone (10 player)', 'Twilight Duo (10 player)', '+2')
	m.add_progress('The Twilight Zone (10 player)', 'Twilight Assist (10 player)', '+1')
	metas.append(m)
	
	# 25 man Malygos/Naxxramas/Sartharion
	m = Meta('Glory of the Raider (25 player)', 5, cutoff='2009-04-14')
	m.add_achievements(
		('The Dedicated Few (25 player)', 579, 'spell_shadow_raisedead'),
		('Arachnophobia (25 player)', 1859, 'achievement_halloween_spider_01'),
		('Make Quick Werk Of Him (25 player)', 1857, 'spell_shadow_plaguecloud'),
		('The Safety Dance (25 player)', 2139, 'ability_rogue_quickrecovery'),
		('Momma Said Knock You Out (25 player)', 2140, 'spell_shadow_curseofmannoroth'),
		('The Immortal', 2186, 'spell_holy_weaponmastery'),
		('Shocking! (25 player)', 2179, 'spell_chargepositive'),
		('And They Would All Go Down Together (25 player)', 2177, 'spell_deathknight_summondeathcharger'),
		('Subtraction (25 player)', 2181, 'spell_chargenegative'),
		("The Spellweaver's Downfall (25 player)", 623, 'achievement_dungeon_nexusraid_10man'),
		("You Don't Have An Eternity (25 player)", 1875, 'achievement_dungeon_nexusraid'),
		('A Poke In The Eye (25 player)', 1870, 'achievement_dungeon_nexusraid_25man'),
		('Gonna Go When the Volcano Blows (25 player)', 2048, 'spell_shaman_lavaflow'),
		("Denyin' the Scion (25 player)", 2149, 'inv_elemental_mote_shadow01'),
		('The Twilight Zone (25 player)', 2054, 'achievement_dungeon_coablackdragonflight_normal'),
		('The Hundred Club (25 player)', 2147, 'inv_misc_head_dragon_blue'),
		("Just Can't Get Enough (25 player)", 2185, 'spell_deathknight_plaguestrike'),
	)
	m.add_progress('The Twilight Zone (25 player)', 'Twilight Duo (25 player)', '+2')
	m.add_progress('The Twilight Zone (25 player)', 'Twilight Assist (25 player)', '+1')
	metas.append(m)
	
	# 10 man Ulduar
	m = Meta('Glory of the Ulduar Raider (10 player)', 6)
	m.add_achievements(
		('Orbit-uary (10 player)', 3056, 'inv_misc_shadowegg'),
		("Stokin' the Furnace (10 player)", 2930, 'achievement_boss_ignis_01'),
		('Iron Dwarf, Medium Rare (10 player)', 2923, 'achievement_dungeon_ulduarraid_irondwarf_01'),
		('Heartbreaker (10 player)', 3058, 'inv_valentinescardtornleft'),
		('I Choose You, Steelbreaker (10 player)', 2941, 'achievement_boss_theironcouncil_01'),
		('Disarmed (10 player)', 2953, 'ability_warrior_disarm'),
		('Crazy Cat Lady (10 player)', 3006, 'achievement_boss_auriaya_01'),
		('I Could Say That This Cache Was Rare (10 player)', 3182, 'inv_box_04'),
		('Lose Your Illusion (10 player)', 3176, 'achievement_boss_thorim'),
		('Knock, Knock, Knock on Wood (10 player)', 3179, 'achievement_boss_warpsplinter'),
		('Firefighter (10 player)', 3180, 'inv_misc_bomb_04'),
		('I Love the Smell of Saronite in the Morning (10 player)', 3181, 'achievement_boss_generalvezax_01'),
		('One Light in the Darkness (10 player)', 3158, 'spell_shadow_shadesofdarkness'),
	)
	m.add_progress('Orbit-uary (10 player)', 'Nuked from Orbit (10 player)', '+3')
	m.add_progress('Orbit-uary (10 player)', 'Orbital Devastation (10 player)', '+2')
	m.add_progress('Orbit-uary (10 player)', 'Orbital Bombardment (10 player)', '+1')
	m.add_progress('Knock, Knock, Knock on Wood (10 player)', 'Knock, Knock on Wood (10 player)', '+2')
	m.add_progress('Knock, Knock, Knock on Wood (10 player)', 'Knock on Wood (10 player)', '+1')
	m.add_progress('One Light in the Darkness (10 player)', 'Two Lights in the Darkness (10 player)', '-2')
	m.add_progress('One Light in the Darkness (10 player)', 'Three Lights in the Darkness (10 player)', '-1')
	metas.append(m)
	
	# 25 man Ulduar
	m = Meta('Glory of the Ulduar Raider (25 player)', 7)
	m.add_achievements(
		('Orbit-uary (25 player)', 3057, 'inv_misc_shadowegg'),
		("Stokin' the Furnace (25 player)", 2929, 'achievement_boss_ignis_01'),
		('Iron Dwarf, Medium Rare (25 player)', 2924, 'achievement_dungeon_ulduarraid_irondwarf_01'),
		('Heartbreaker (25 player)', 3059, 'inv_valentinescardtornleft'),
		('I Choose You, Steelbreaker (25 player)', 2944, 'achievement_boss_theironcouncil_01'),
		('Disarmed (25 player)', 2954, 'ability_warrior_disarm'),
		('Crazy Cat Lady (25 player)', 3007, 'achievement_boss_auriaya_01'),
		('I Could Say That This Cache Was Rare (25 player)', 3184, 'inv_box_04'),
		('Lose Your Illusion (25 player)', 3183, 'achievement_boss_thorim'),
		('Knock, Knock, Knock on Wood (25 player)', 3187, 'achievement_boss_warpsplinter'),
		('Firefighter (25 player)', 3189, 'inv_misc_bomb_04'),
		('I Love the Smell of Saronite in the Morning (25 player)', 3188, 'achievement_boss_generalvezax_01'),
		('One Light in the Darkness (25 player)', 3163, 'spell_shadow_shadesofdarkness'),
	)
	m.add_progress('Orbit-uary (25 player)', 'Nuked from Orbit (25 player)', '+3')
	m.add_progress('Orbit-uary (25 player)', 'Orbital Devastation (25 player)', '+2')
	m.add_progress('Orbit-uary (25 player)', 'Orbital Bombardment (25 player)', '+1')
	m.add_progress('Knock, Knock, Knock on Wood (25 player)', 'Knock, Knock on Wood (25 player)', '+2')
	m.add_progress('Knock, Knock, Knock on Wood (25 player)', 'Knock on Wood (25 player)', '+1')
	m.add_progress('One Light in the Darkness (25 player)', 'Two Lights in the Darkness (25 player)', '-2')
	m.add_progress('One Light in the Darkness (25 player)', 'Three Lights in the Darkness (25 player)', '-1')
	metas.append(m)

	# 10 man Call of the Crusade
	m = Meta('Call of the Crusade (10 player)', 8)
	m.add_achievements(
		('Call of the Crusade (10 player)', 3917, 'achievement_reputation_argentchampion'),
		('Call of the Grand Crusade (10 player)', 3918, 'achievement_reputation_argentchampion'),
		('Upper Back Pain (10 player)', 3797, 'inv_ammo_snowball'),
		('Not One, But Two Jormungars (10 player)', 3936, 'ability_hunter_pet_worm'),
		('Three Sixty Pain Spike (10 player)', 3996, 'spell_shadow_shadowmend'),
		('Resilience Will Fix It (10 player)', 3798, 'achievement_arena_5v5_3'),
		('Salt and Pepper (10 player)', 3799, 'achievement_boss_svalasorrowgrave'),
		('The Traitor King (10 player)', 3800, 'achievement_boss_anubarak'),
		('A Tribute to Insanity (10 player)', 3819, 'inv_crown_13'),
	)
	m.add_progress('A Tribute to Insanity (10 player)', 'A Tribute to Mad Skill (10 player)', '45')
	m.add_progress('A Tribute to Insanity (10 player)', 'A Tribute to Skill (10 player)', '25')
	metas.append(m)
	
	# 25 man Call of the Crusade
	m = Meta('Call of the Crusade (25 player)', 9)
	m.add_achievements(
		('Call of the Crusade (25 player)', 3916, 'achievement_reputation_argentchampion'),
		('Call of the Grand Crusade (25 player)', 3812, 'achievement_reputation_argentchampion'),
		('Upper Back Pain (25 player)', 3813, 'inv_ammo_snowball'),
		('Not One, But Two Jormungars (25 player)', 3937, 'ability_hunter_pet_worm'),
		('Three Sixty Pain Spike (25 player)', 3997, 'spell_shadow_shadowmend'),
		('Resilience Will Fix It (25 player)', 3814, 'achievement_arena_5v5_3'),
		('Salt and Pepper (25 player)', 3815, 'achievement_boss_svalasorrowgrave'),
		('The Traitor King (25 player)', 3816, 'achievement_boss_anubarak'),
		('A Tribute to Insanity (25 player)', 3819, 'inv_crown_13'),
	)
	m.add_progress('A Tribute to Insanity (25 player)', 'A Tribute to Mad Skill (25 player)', '45')
	m.add_progress('A Tribute to Insanity (25 player)', 'A Tribute to Skill (25 player)', '25')
	metas.append(m)	
	
	return metas

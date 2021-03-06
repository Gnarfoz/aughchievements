"Data for Augh!chievements"

class Meta:
	def __init__(self, name, short_name, section, cutoff=None):
		self.name = name
		self.short_name = short_name
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
			return (True, dates[-1])
		else:
			return (True, False)

# ---------------------------------------------------------------------------

def get_data():
	metas = []
	
	# 10 man Malygos/Naxxramas/Sartharion
	m = Meta('Glory of the Raider (10 player)', 'naxx10', 3, cutoff='2009-04-14')
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
	m = Meta('Glory of the Raider (25 player)', 'naxx25', 3, cutoff='2009-04-14')
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
	m = Meta('Glory of the Ulduar Raider (10 player)', 'uld10', 3)
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
	m = Meta('Glory of the Ulduar Raider (25 player)', 'uld25', 3)
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
	m = Meta('Call of the Crusade (10 player)', 'toc10', 3)
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
	m = Meta('Call of the Crusade (25 player)', 'toc25', 3)
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
	
	# 10 man Icecrown Citadel
	m = Meta('Glory of the Icecrown Raider (10 player)', 'icc10', 3)
	m.add_achievements(
        ('Heroic: Storming the Citadel (10 player)', 4628, 'achievement_dungeon_icecrown_icecrownentrance'),
        ('Heroic: The Plagueworks (10 player)', 4629, 'achievement_dungeon_plaguewing'),
        ('Heroic: The Crimson Hall (10 player)', 4630, 'achievement_dungeon_crimsonhall'),
        ('Heroic: The Frostwing Halls (10 player)', 4631, 'achievement_dungeon_icecrown_frostwinghalls'),
        ('Boned (10 player)', 4534, 'achievement_boss_lordmarrowgar'),
        ('Full House (10 player)', 4535, 'achievement_boss_ladydeathwhisper'),
        ("I'm on a Boat (10 player)", 4536, 'achievement_dungeon_hordeairship'),
        ("I've Gone and Made a Mess (10 player)", 4537, 'achievement_boss_saurfang'),
        ('Dances with Oozes (10 player)', 4538, 'spell_nature_acid_01'),
        ('Flu Shot Shortage (10 player)', 4577, 'achievement_boss_festergutrotface'),
        ('Nausea, Heartburn, Indigestion... (10 player)', 4578, 'achievement_boss_profputricide'),
        ('The Orb Whisperer (10 player)', 4582, 'achievement_boss_princetaldaram'),
        ('Once Bitten, Twice Shy (10 player)', 4539, 'achievement_boss_lanathel'),
        ('Portal Jockey (10 player)', 4579, 'achievement_boss_shadeoferanikus'),
        ('All You Can Eat (10 player)', 4580, 'achievement_boss_sindragosa'),
        ('Been Waiting a Long Time for This (10 player)', 4601, 'spell_deathknight_bloodplague'),
	)
	metas.append(m)
	
	# 25 man Icecrown Citadel
	m = Meta('Glory of the Icecrown Raider (25 player)', 'icc25', 3)
	m.add_achievements(
        ('Heroic: Storming the Citadel (25 player)', 4632, 'achievement_dungeon_icecrown_icecrownentrance'),
        ('Heroic: The Plagueworks (25 player)', 4633, 'achievement_dungeon_plaguewing'),
        ('Heroic: The Crimson Hall (25 player)', 4634, 'achievement_dungeon_crimsonhall'),
        ('Heroic: The Frostwing Halls (25 player)', 4635, 'achievement_dungeon_icecrown_frostwinghalls'),
        ('Boned (25 player)', 4610, 'achievement_boss_lordmarrowgar'),
        ('Full House (25 player)', 4611, 'achievement_boss_ladydeathwhisper'),
        ("I'm on a Boat (25 player)", 4612, 'achievement_dungeon_hordeairship'),
        ("I've Gone and Made a Mess (25 player)", 4613, 'achievement_boss_saurfang'),
        ('Dances with Oozes (25 player)', 4614, 'spell_nature_acid_01'),
        ('Flu Shot Shortage (25 player)', 4615, 'achievement_boss_festergutrotface'),
        ('Nausea, Heartburn, Indigestion... (25 player)', 4616, 'achievement_boss_profputricide'),
        ('The Orb Whisperer (25 player)', 4617, 'achievement_boss_princetaldaram'),
        ('Once Bitten, Twice Shy (25 player)', 4618, 'achievement_boss_lanathel'),
        ('Portal Jockey (25 player)', 4619, 'achievement_boss_shadeoferanikus'),
        ('All You Can Eat (25 player)', 4620, 'achievement_boss_sindragosa'),
        ('Been Waiting a Long Time for This (25 player)', 4621, 'spell_deathknight_bloodplague'),
		('Neck-Deep in Vile (25 player)', 4622, 'spell_shadow_devouringplague'),
	)
	metas.append(m)
	
	# Glory of the Cataclysm Hero
	m = Meta('Glory of the Cataclysm Hero', 'gotch', 4)
	m.add_achievements(
		('Crushing Bones and Cracking Skulls', 5281, 'achievement_dungeon_blackrockcaverns_romoggbonecrusher'),
		('Arrested Development', 5282, 'achievement_dungeon_blackrockcaverns_corlaheraldoftwilight'),
		('Too Hot to Handle', 5283, 'achievement_dungeon_blackrockcaverns_karshsteelbender'),
		('Ascendant Descending', 5284, 'achievement_dungeon_blackrockcaverns_ascendantlordobsidius'),
		('Old Faithful', 5285, 'achievement_boss_ladyvashj'),
		('Prince of Tides', 5286, 'achievement_dungeon_throneofthetides_ozumat'),
		('Rotten to the Core', 5287, 'ability_warlock_moltencore'),
		('No Static at All', 5288, 'achievement_dungeon_thevortexpinnacle_asaad'),
		('Extra Credit Bonus Stage', 5289, 'spell_frost_windwalkon'),
		('Umbrage for Umbriss', 5297, 'achievement_dungeon_grimbatol_generalumbriss'),
		("Don't Need to Break Eggs to Make an Omelet", 5298, 'achievement_halloween_rottenegg_01'),
		('I Hate That Song', 5293, 'spell_holy_divinehymn'),
		("Straw That Broke the Camel's Back", 5294, 'ability_mount_camel_tan'),
		('Faster Than the Speed of Light', 5296, 'inv_misc_pocketwatch_01'),
		('Sun of a....', 5295, 'achievement_dungeon_hallsoforigination_rajh'),
		('Kill It With Fire!', 5290, 'inv_misc_firedancer_01'),
		('Acrocalypse Now', 5291, 'ability_hunter_pet_crocolisk'),
		('Headed South', 5292, 'ability_mage_netherwindpresence'),
		('Ready for Raiding', 5366, 'spell_fire_burnout'),
		('Rat Pack', 5367, 'inv_misc_food_100_hardcheese'),
		('Prototype Prodigy', 5368, 'inv_gizmo_goblingtonkcontroller'),
		("It's Frost Damage", 5369, 'spell_deathknight_pathoffrost'),
		("I'm on a Diet", 5370, 'inv_misc_food_115_condorsoup'),
		('Vigorous VanCleef Vindicator', 5371, 'achievement_boss_edwinvancleef'),
		('Pardon Denied', 5503, 'ability_rogue_stayofexecution'),
		('To the Ground!', 5504, 'spell_holy_sealofblood'),
		('Bullet Time', 5505, 'inv_misc_ammo_bullet_05'),
	)
	metas.append(m)
	
	# Glory of the Cataclysm Raider
	m = Meta('Glory of the Cataclysm Raider', 'gotcr', 5)
	m.add_achievements(
		('Heroic: Magmaw', 5094, 'ability_hunter_pet_worm'),
		('Heroic: Omnotron Defense System', 5107, 'achievement_dungeon_blackwingdescent_darkironcouncil'),
		('Heroic: Maloriak', 5108, 'achievement_dungeon_blackwingdescent_raid_maloriak'),
		('Heroic: Atramedes', 5109, 'achievement_dungeon_blackwingdescent_raid_atramedes'),
		('Heroic: Chimaeron', 5115, 'achievement_dungeon_blackwingdescent_raid_chimaron'),
		('Heroic: Nefarian', 5116, 'achievement_dungeon_blackwingdescent_raid_nefarian'),
		('Heroic: Halfus Wyrmbreaker', 5118, 'achievement_dungeon_bastionoftwilight_halfuswyrmbreaker'),
		('Heroic: Valiona and Theralion', 5117, 'achievement_dungeon_bastionoftwilight_valionatheralion'),
		('Heroic: Ascendant Council', 5119, 'achievement_dungeon_bastionoftwilight_twilightascendantcouncil'),
		("Heroic: Cho'gall", 5120, 'achievement_dungeon_bastionoftwilight_chogallboss'),
		('Heroic: Sinestra', 5121, 'achievement_dungeon_bastionoftwilight_ladysinestra'),
		('Heroic: Conclave of Wind', 5122, 'ability_druid_galewinds'),
		("Heroic: Al'Akir", 5123, 'achievement_boss_murmur'),
		('Parasite Evening', 5306, 'ability_hunter_pet_worm'),
		('Achieve-a-tron', 5307, 'achievement_dungeon_blackwingdescent_darkironcouncil'),
		('Silence is Golden', 5308, 'inv_misc_bell_01'),
		('Full of Sound and Fury', 5309, 'warrior_talent_icon_furyintheblood'),
		('Aberrant Behavior', 5310, 'ability_racial_aberration'),
		('Keeping it in the Family', 4849, 'achievement_boss_onyxia'),
		('The Only Escape', 5300, 'inv_misc_crop_01'),
		('Double Dragon', 4852, 'achievement_dungeon_bastionoftwilight_valionatheralion'),
		('Elementary', 5311, 'achievement_dungeon_bastionoftwilight_twilightascendantcouncil'),
		('The Abyss Will Gaze Back Into You', 5312, 'spell_shadow_mindflay'),
		("I Can't Hear You Over the Sound of How Awesome I Am", 5313, 'achievement_dungeon_bastionoftwilight_ladysinestra'),
		('Stay Chill', 5304, 'spell_deathknight_frostfever'),
		('Four Play', 5305, 'spell_shaman_staticshock')
	)
	metas.append(m)
	
	return metas

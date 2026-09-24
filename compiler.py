# sorry for the terribly messy code

import os, glob
from itertools import chain

outindex = "list.html"
outdir = "./gfiles/"
html5gamesin = "html5/"
rarchgamesin = "rarch/"
romdir = "roms/*"
flashgamesin = "flash/"
pregba = [".gba", ".gb", ".gbc"]
pregen = [".mdx", ".md", ".smd", ".gen", ".sms", ".gg", ".sg"]
prenes = [".nes", ".fds", ".unf", ".unif"]
pren64 = [".n64", ".v64", ".z64", ".ndd"]
presnes = [".smc", ".sfc", ".swc", ".fig"]
index = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Games &middot; Nebula</title>
<link rel="stylesheet" href="./css/style.css">
</head>
<body class="games">
<div class="aurora" aria-hidden="true"><span class="blob blob-1"></span><span class="blob blob-2"></span><span class="blob blob-3"></span></div>
<nav class="topnav">
<a class="brand" href="/"><span class="brand-mark">\u2726</span><span class="brand-name">Nebula</span></a>
<div class="links"><a href="/">Proxy</a><a class="active" href="/games">Games</a></div>
</nav>
<header class="games-header">
<h1 class="games-title">Games Library</h1>
<p class="games-sub">%d games ready to play &mdash; HTML5, Flash and retro consoles.</p>
<input type="text" id="gsearchbar" oninput="gfilter(this.value)" autocomplete="off" spellcheck="false" placeholder="Search games\u2026" />
<p id="gnoresults" class="no-results" hidden>No games match your search.</p>
</header>
<main class="games-main">
%s
</main>
<script>
function gfilter(q){
	q = q.toUpperCase().replace(/ /g, "");
	var total = 0;
	document.querySelectorAll(".cat").forEach(function (cat) {
		var any = false;
		cat.querySelectorAll(".game-card").forEach(function (c) {
			var show = c.dataset.name.indexOf(q) !== -1;
			c.style.display = show ? "" : "none";
			if (show) { any = true; total++; }
		});
		cat.style.display = any ? "" : "none";
	});
	document.getElementById("gnoresults").hidden = total !== 0;
}
</script>
</body>
</html>'''
import hashlib, html


def _disk_path(served):
	# served paths look like "./gfiles/..."; map to a path relative to cwd
	return served[2:] if served.startswith("./") else served


def _gradient(name):
	h = int(hashlib.md5(name.encode("utf-8")).hexdigest(), 16)
	h1 = h % 360
	h2 = (h1 + 45) % 360
	return h1, h2


def card(href, label, thumb=None, emoji=None):
	"""Build one game card. Uses a thumbnail image when available, otherwise an
	emoji tile or a gradient tile bearing the game's initial."""
	key = label.upper().replace(" ", "")
	safe = html.escape(label)
	if thumb and os.path.exists(_disk_path(thumb)):
		inner = '<span class="thumb"><img src="%s" loading="lazy" alt="" /></span>' % thumb
	elif emoji:
		inner = '<span class="thumb emoji">%s</span>' % emoji
	else:
		h1, h2 = _gradient(label)
		initial = html.escape((label[:1].upper() or "?"))
		inner = '<span class="thumb ph" style="--h1:%d;--h2:%d">%s</span>' % (h1, h2, initial)
	return '<a class="game-card" href="%s" data-name="%s">%s<span class="title">%s</span></a>' % (
		href, html.escape(key), inner, safe)


def section(title, cards):
	return '<section class="cat">\n<h2>%s</h2>\n<div class="grid">\n%s\n</div>\n</section>' % (
		html.escape(title), "\n".join(cards))
html5names = {"adarkroom": "A Dark Room", "asciispace": "ASCII Space", "blackholesquare": "Black Hole Square", "bounceback": "Bounce Back", "captaincallisto": "Captain Callisto", "chromaincident": "Chroma Incident", "chromedino": "Chrome Dino", "connect3": "Connect 3", "cookieclicker": "Cookie Clicker", "edgenotfound": "Edge not Found", "evilglitch": "Evil Glitch", "factoryballsforever": "Factory Balls Forever", "flappybird": "Flappy Bird", "geometrydash": "Geometry Dash", "ninjavsevilcorp": "Ninja vs Evilcorp", "pacman": "Pac-Man", "particleclicker": "Particle Clicker", "pushback": "Push Back", "radiusraid": "Radius Raid", "roadblocks": "Road Blocks", "run3": "Run 3", "sleepingbeauty": "Sleeping Beauty", "spacecompany": "Space Company", "spacegarden": "Space Garden", "spacehuggers": "Space Huggers", "themazeofspacegoblins": "The Maze of Space Goblins", "xx142-b2exe": "xx142-b2.exe"}

# Make HTML5 lists
html5_1 = sorted(next(os.walk(outdir + html5gamesin))[1])
html5_cards = [card(outdir + rarchgamesin, "webretro", thumb="./gfiles/thumbnails/rarch.jpg")]

# Generate cards for HTML5 list
for name in html5_1:
	label = html5names.get(name) if (name in html5names) else name.capitalize()
	html5_cards.append(card(
		outdir + html5gamesin + name + "/",
		label,
		thumb="./gfiles/thumbnails/html5/" + name + ".jpg",
	))
html5_2 = section("HTML5 Games", html5_cards)

# Make GBA lists
gba_1 = list(chain.from_iterable([[os.path.basename(x) for x in glob.glob(outdir + rarchgamesin + romdir + y)] for y in pregba]))
gba_cards = [card(outdir + rarchgamesin + "?core=mgba", "Upload ROM", emoji="\U0001F579\uFE0F")]

# Generate cards for GBA list
for rom in gba_1:
	gba_cards.append(card(outdir + rarchgamesin + "?core=mgba&rom=" + rom, os.path.splitext(rom)[0].capitalize()))
gba_2 = section("Gameboy Advance", gba_cards)

# Make Genesis lists
gen_1 = list(chain.from_iterable([[os.path.basename(x) for x in glob.glob(outdir + rarchgamesin + romdir + y)] for y in pregen]))
gen_cards = [card(outdir + rarchgamesin + "?core=genesis_plus_gx", "Upload ROM", emoji="\U0001F579\uFE0F")]

# Generate cards for Genesis list
for rom in gen_1:
	gen_cards.append(card(outdir + rarchgamesin + "?core=genesis_plus_gx&rom=" + rom, os.path.splitext(rom)[0].capitalize()))
gen_2 = section("Genesis / Master System", gen_cards)

# Make N64 lists
n64_1 = list(chain.from_iterable([[os.path.basename(x) for x in glob.glob(outdir + rarchgamesin + romdir + y)] for y in pren64]))
n64_cards = [card(outdir + rarchgamesin + "?core=mupen64plus_next", "Upload ROM", emoji="\U0001F579\uFE0F")]

# Generate cards for N64 list
for rom in n64_1:
	n64_cards.append(card(outdir + rarchgamesin + "?core=mupen64plus_next&rom=" + rom, os.path.splitext(rom)[0].capitalize()))
n64_2 = section("Nintendo 64", n64_cards)

# Make NES lists
nes_1 = list(chain.from_iterable([[os.path.basename(x) for x in glob.glob(outdir + rarchgamesin + romdir + y)] for y in prenes]))
nes_cards = [card(outdir + rarchgamesin + "?core=nestopia", "Upload ROM", emoji="\U0001F579\uFE0F")]

# Generate cards for NES list
for rom in nes_1:
	nes_cards.append(card(outdir + rarchgamesin + "?core=nestopia&rom=" + rom, os.path.splitext(rom)[0].capitalize()))
nes_2 = section("NES", nes_cards)

# Make SNES lists
snes_1 = list(chain.from_iterable([[os.path.basename(x) for x in glob.glob(outdir + rarchgamesin + romdir + y)] for y in presnes]))
snes_cards = [card(outdir + rarchgamesin + "?core=snes9x", "Upload ROM", emoji="\U0001F579\uFE0F")]

# Generate cards for SNES list
for rom in snes_1:
	snes_cards.append(card(outdir + rarchgamesin + "?core=snes9x&rom=" + rom, os.path.splitext(rom)[0].capitalize()))
snes_2 = section("Super Nintendo", snes_cards)

# Make flash lists
# Just a premade list for now
flash_1 = ['1on1soccer.swf', '3dtanks.swf', 'abobosbigadventure.swf', 'achievementunlocked.swf', 'achievementunlocked2.swf', 'achievementunlocked3.swf', 'actionturnip.swf', 'adaran.swf', 'adrenaline.swf', 'americanracing1.swf', 'americanracing2.swf', 'arkandianrevenant.swf', 'armyofages.swf', 'awesomecars.swf', 'awesomeplanes.swf', 'battlepanic.swf', 'bloonsplayerpack2.swf', 'bloonsplayerpack3.swf', 'bloonsplayerpack4.swf', 'bloonsplayerpack5.swf', 'bloonstd1.swf', 'bloonstd3.swf', 'bloonstd4.swf', 'bloonstd5.swf', 'bobtherobber.swf', 'boombot2.swf', 'boxhead2play.swf', 'bubbletanks2.swf', 'bulletbill.swf', 'bullettimefighting.swf', 'burritobison.swf', 'burritobisonrevenge.swf', 'cactusmccoy.swf', 'cactusmccoy2.swf', 'cannonbasketball2.swf', 'cargobridge.swf', 'causality.swf', 'chibiknight.swf', 'clickerheroes.swf', 'computerbashing.swf', 'crushthecastle.swf', 'crushthecastle2.swf', 'cubefield.swf', 'cyclomaniacs2.swf', 'diggy.swf', 'donkeykong.swf', 'dontshootthepuppy.swf', 'doodledefender.swf', 'doom.swf', 'dragracing.swf', 'ducklife.swf', 'ducklife2.swf', 'ducklife3.swf', 'ducklife4.swf', 'earntodie.swf', 'earntodie2.swf', 'earntodiesuperwheel.swf', 'electricman2.swf', 'elephantquest.swf', 'epicbattlefantasy3.swf', 'epiccomboredux.swf', 'exitpath.swf', 'factoryballs.swf', 'factoryballs2.swf', 'factoryballs3.swf', 'factoryballs4.swf', 'fancypantsadventure.swf', 'fancypantsadventure2.swf', 'fancypantsadventure3.swf', 'flashflightsimulator.swf', 'flight.swf', 'fracuum.swf', 'freerider2.swf', 'getontop.swf', 'giveuprobot.swf', 'giveuprobot2.swf', 'hanger.swf', 'hanger2.swf', 'happywheels.swf', 'hobo.swf', 'hobo2.swf', 'hobo3.swf', 'hobo4.swf', 'hobo5.swf', 'hobo6.swf', 'hobo7.swf', 'houseofwolves.swf', 'interactivebuddy.swf', 'jacksmith.swf', 'jellytruck.swf', 'johnnyupgrade.swf', 'jumpix2.swf', 'knightmaretower.swf', 'learn2fly.swf', 'learn2fly2.swf', 'learn2fly3.swf', 'magnetface.swf', 'mariocombat.swf', 'marioracingtournament.swf', 'meatboy.swf', 'megamanprojectx.swf', 'metroidelements.swf', 'mineblocks.swf', 'minesweeper.swf', 'mirrorsedge.swf', 'moneymovers.swf', 'moneymovers3.swf', 'motherload.swf', 'motox3m.swf', 'multitask.swf', 'mutilateadoll2.swf', 'myangel.swf', 'nanotube.swf', 'newgroundsrumble.swf', 'ngame.swf', 'nitromemustdie.swf', 'nucleus.swf', 'nv2.swf', 'nyancatlostinspace.swf', 'offroaders.swf', 'onemanarmy2.swf', 'outofthisworld.swf', 'pacman.swf', 'pandemic.swf', 'pandemic2.swf', 'papalouie.swf', 'papalouie2.swf', 'papalouie3.swf', 'picosschool.swf', 'picosschool2.swf', 'pirates.swf', 'polarjump.swf', 'portal.swf', 'portal2d.swf', 'quadrobarreldefence.swf', 'qubeythecube.swf', 'qwop.swf', 'raftwars.swf', 'raftwars2.swf', 'raze.swf', 'redball.swf', 'redball2.swf', 'redball4.swf', 'redball4v2.swf', 'redball4v3.swf', 'redshift.swf', 'revenant2.swf', 'riddleschool1.swf', 'riddleschool2.swf', 'riddleschool3.swf', 'riddleschool4.swf', 'riddleschool5.swf', 'riddletransfer.swf', 'riddletransfer2.swf', 'run2.swf', 'run3.swf', 'saszombieassault3.swf', 'sentryknight.swf', 'shoppingcarthero3.swf', 'siftheads.swf', 'siftheads2.swf', 'siftheads3.swf', 'siftheads4.swf', 'siftheads5.swf', 'sniperassassin4.swf', 'sportsheadsfootball.swf', 'sportsheadsracing.swf', 'sportsheadstennis.swf', 'stickrpg.swf', 'stickrun2.swf', 'stickwar.swf', 'strikeforceheroes2.swf', 'strikeforcekittylaststand.swf', 'sugarsugar.swf', 'sugarsugar2.swf', 'sugarsugar3.swf', 'superd.swf', 'superfighters.swf', 'supermario63.swf', 'supermarioflash.swf', 'supermarioflash2.swf', 'supersmashflash.swf', 'swordsandsandals2.swf', 'tacticalassassin.swf', 'tanks.swf', 'tanktrouble.swf', 'tetris.swf', 'thebindingofisaac.swf', 'thegame.swf', 'theimpossiblequiz.swf', 'theimpossiblequiz2.swf', 'theworldshardestgame2.swf', 'thingthingarena.swf', 'thisistheonlylevel.swf', 'tosstheturtle.swf', 'truckloader4.swf', 'ultimateflashsonic.swf', 'ultimatetactics.swf', 'unrealflash.swf', 'vex.swf', 'vex2.swf', 'vex3.swf', 'warfare1917.swf', 'warfare1944.swf', 'warp.swf', 'xenos.swf', 'xtremecliffdiving.swf', 'yearofthesnake.swf', 'yuriusshouseofspooks.swf', 'zombiealienparasites.swf']
flash_cards = [card(outdir + flashgamesin, "Upload SWF", emoji="\u26A1")]

# Generate cards for flash list
for swf in flash_1:
	flash_cards.append(card(outdir + flashgamesin + "?swf=" + swf, os.path.splitext(swf)[0].capitalize()))
flash_2 = section("Flash Games", flash_cards)


# Write to list file
sections = [html5_2, gba_2, gen_2, n64_2, nes_2, snes_2, flash_2]

# Count total playable cards (every card minus the utility upload tiles)
all_cards = html5_cards + gba_cards + gen_cards + n64_cards + nes_cards + snes_cards + flash_cards
game_count = sum(1 for c in all_cards if 'Upload ROM' not in c and 'Upload SWF' not in c)

final_list = index % (game_count, "\n".join(sections))

with open(outindex, "w") as file:
	file.write(final_list)

print("Wrote %s with %d games across %d sections." % (outindex, game_count, len(sections)))
print("Done!")

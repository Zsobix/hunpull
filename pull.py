################################################################
#					Hungarian M3U8 playlist puller
#				by: Zsobix (https://github.com/Zsobix)
#		
#						WARNING!!!!:		
#			you will need to self host because the 
#			idiotic mediaklikk streams are ip specific
#
#					i fucking hate mediaklikk
#why does the stream need to be fucking encrypted on one stream
#					but not on the other????
#also the other stream can be only accessed in an iframe???????
################################################################


from requests import get
import re as regex

BASE_URL = "https://player.mediaklikk.hu/playernew/player.php?noflash=yes&video="

m3u = []
m3u.append('#EXTM3U x-tvg-url="https://zsobix.xyz/epg_ripper_HU1.xml"')

urls=["mtv1live","mtv2live","mtv4live","mtv4plus","mtv5live","dunalive","hirtv"]

for url in urls:
	if url == "hirtv":
		request = get("https://onlinestream.live/hir-tv/videoplayer/4740-1").text.split('"')
		# mmm yes H%C3ADr_TV
		m3u.append('#EXTINF:-1 tvg-shift="+1" tvg-id="HIR.TV.hu" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/4/44/H%C3%ADr_TV.png",HirTV')
		for line in request:
			if "play.m3u8" in line:
				# the line will start with a // or smth so i need to add the origin url
				m3u.append(get(f"https://onlinestream.live{line}").text.replace("#EXTM3U", "").replace("\n", ""))
	#custom logic for m4 sport (i hate you mediaklikk)
	elif url == "mtv4live":
		headers = {
			'Host': 'player.mediaklikk.hu',
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate, br, zstd',
			'DNT': '1',
			'Connection': 'keep-alive',
			'Referer': 'https://m4sport.hu/',
			'Cookie': 'SERVERID=playercookieA',
			'Upgrade-Insecure-Requests': '1',
			'Sec-Fetch-Dest': 'iframe',
			'Sec-Fetch-Mode': 'navigate',
			'Sec-Fetch-Site': 'cross-site',
			'Priority': 'u=4',
			'Pragma': 'no-cache',
			'Cache-Control': 'no-cache'
		}
		# ?????
		# why does it need this?
		request = get(f'{BASE_URL}{url}', timeout=15, headers=headers, cookies={"SERVERID":"playercookieA"}).text
		lines = request.split('"')
		for line in lines:
			if "index.m3u8" in line:
				m3u.append('#EXTINF:-1 tvg-id="m4.hu" tvg-logo="https://upload.wikimedia.org/wikipedia/hu/f/fd/M4_logo.png",M4 Sport')
				# add some info
				line = regex.sub(r'\\', "", line)
				# https://stackoverflow.com/questions/11475885/python-replace-regex thank you stackoverflow
				m3u.append(regex.sub(r'\?v=5iip:((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$', "", line))
	else:
		request = get(f'{BASE_URL}{url}', timeout=15).text
		lines = request.split('"')
		for line in lines:
			if "index.m3u8" in line:
				match url:
					# i finally added a switch statment
					case "mtv1live":
						m3u.append('#EXTINF:-1 tvg-id="m1.HD.hu" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/f/f1/M1_2020.png",M1')
					case "mtv2live":
						m3u.append('#EXTINF:-1 tvg-id="m2.HD.hu" tvg-logo="https://upload.wikimedia.org/wikipedia/hu/b/b5/M2_gyerekcsatorna_log%C3%B3ja.png",M2')
					case "mtv4plus":
						m3u.append('#EXTINF:-1 tvg-id="m4sport+.hu" tvg-logo="https://upload.wikimedia.org/wikipedia/hu/b/bd/Duna_world_log%C3%B3.png",Duna World/M4 Sport+')
					case "mtv5live":
						m3u.append('#EXTINF:-1 tvg-id="m5.hu" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/b/b4/M5logo.png",M5')
					case "dunalive":
						m3u.append('#EXTINF:-1 tvg-id="Duna.TV.hu" tvg-logo="https://upload.wikimedia.org/wikipedia/hu/d/d3/Dunatv_logo.png",Duna')
				line = regex.sub(r'\\', "", line)
				m3u.append(regex.sub(r'\?v=5iip:((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$', "", line))
# my euronews feed from youtube
m3u.append('#EXTINF:-1 tvg-id="Euronews.hu" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Euronews_2022.svg/1280px-Euronews_2022.svg.png",Euronews')
m3u.append("https://raw.githubusercontent.com/Zsobix/YouTube_to_m3u/refs/heads/main/youtube.m3u8")
with open("hungary.m3u", "a") as playlist:
	for lines in m3u:
			playlist.write(f"{lines}\n")

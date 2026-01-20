import requests
import re

def get_list():
    # هەردوو سەرچاوەکە لێرە دادەنێین
    sources = [
        "http://oktvtv.atwebpages.com/load.js",   # ئەمە ١١٥ کەناڵە گشتییەکەیە
        "http://oktvtv.atwebpages.com/loadb.js"  # ئەمە کەناڵە تایبەت و نوێیەکانە
    ]
    
    all_unique_links = []
    
    for url in sources:
        try:
            response = requests.get(url, timeout=15)
            content = response.text
            # دۆزینەوەی هەموو ئەو لینکەانەی لە ناو " " یان ' ' دان
            found_links = re.findall(r'"(https?://.*?)"', content)
            all_unique_links.extend(found_links)
        except:
            print(f"نەتوانرا داتا لە {url} بهێنرێت")

    # لادانی دووبارەکان
    final_links = list(dict.fromkeys(all_unique_links))
    
    m3u_content = "#EXTM3U\n"
    for i, link in enumerate(final_links):
        # تەنها ئەو لینکەانە وەردەگرین کە فۆرماتی ڤیدیۆن
        if ".m3u8" in link or ".mpd" in link or "/play/" in link:
            # لێرەدا دەتوانیت ناوەکان دیاری بکەیت، بۆ ئێستا بە ژمارە دایان دەنێین
            m3u_content += f"#EXTINF:-1, OK-TV Channel {i+1}\n{link}\n\n"

    with open("oktv_list.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    
    print(f"✅ تەواو! کۆی گشتی {len(final_links)} لینک کۆکرایەوە.")

if __name__ == "__main__":
    get_list()

import requests
import re

def get_list():
    source_url = "http://oktvtv.atwebpages.com/loadb.js"
    try:
        response = requests.get(source_url, timeout=10)
        content = response.text
        
        # ئەمجارە دەگەڕێین بەدوای هەموو جۆرە لینکەکان (هەم MPD و هەم M3U8)
        # کە لە ناو فایلی JS بەم شێوانە نووسراون
        patterns = [
            r'streamUrl\s*=\s*"(.*?)"',
            r'url\s*:\s*"(.*?)"',
            r'source\s*:\s*"(.*?)"'
        ]
        
        all_links = []
        for pattern in patterns:
            found = re.findall(pattern, content)
            all_links.extend(found)
        
        # لادانی ئەو لینکەانەی کە دووبارەن
        unique_links = list(dict.fromkeys(all_links))
        
        m3u = "#EXTM3U\n"
        for i, url in enumerate(unique_links):
            # فلتەرکردنی ئەو لینکەانەی کە بەتاڵن یان تەنها کۆدێکی کورتن
            if len(url) > 10 and (url.startswith('http') or url.startswith('https')):
                m3u += f"#EXTINF:-1, OK-TV Channel {i+1}\n{url}\n\n"
            
        with open("oktv_list.m3u", "w", encoding="utf-8") as f:
            f.write(m3u)
        print(f"✅ سەرکەوتوو بوو! {len(unique_links)} لینک دۆزرایەوە.")
        
    except Exception as e:
        print(f"❌ هەڵە: {e}")

if __name__ == "__main__":
    get_list()

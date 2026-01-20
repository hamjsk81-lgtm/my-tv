import requests
import re

def clean_name(url):
    # دەرهێنانی ناو لە ناو لینکەکە
    name = url.split('/')[-2] if '/' in url else "Unknown"
    if "index.m3u8" in url or "playlist.m3u8" in url:
        # هەوڵدان بۆ دۆزینەوەی ناوی پاکتر لە ناو بەشەکانی لینکەکە
        parts = url.split('/')
        for part in reversed(parts):
            if part and not part.endswith('.m3u8') and not part.endswith('.smil'):
                name = part
                break
    
    # جوانکردنی ناوەکان (لادانی _ و - و گۆڕینی بۆ پیتی گەورە)
    name = name.replace('_', ' ').replace('-', ' ').replace('HD', '').replace('live', '').strip()
    return name.title()

def get_list():
    sources = [
        "http://oktvtv.atwebpages.com/load.js",
        "http://oktvtv.atwebpages.com/loadb.js"
    ]
    
    m3u_content = "#EXTM3U\n"
    seen_links = set()

    for url in sources:
        try:
            response = requests.get(url, timeout=15)
            content = response.text
            # دۆزینەوەی هەموو لینکەکان لە ناو کوتەیشنەکاندا
            links = re.findall(r'"(https?://[^"]+)"', content)
            
            for link in links:
                if link not in seen_links:
                    if ".m3u8" in link or ".mpd" in link or ":8000/play/" in link:
                        name = clean_name(link)
                        # لۆگۆی گشتی بۆ ئەوەی لیستەکە جوانتر بێت
                        logo = f"https://ui-avatars.com/api/?name={name}&background=random&color=fff"
                        
                        # چاککردنی هەندێک ناوی تایبەت بە دەستی
                        if "channel8" in link.lower(): name = "Channel 8"
                        elif "rudaw" in link.lower(): name = "Rudaw TV"
                        elif "kurdsat" in link.lower(): name = "Kurdsat"
                        
                        m3u_content += f'#EXTINF:-1 tvg-logo="{logo}", {name}\n{link}\n\n'
                        seen_links.add(link)
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    with open("oktv_list.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print(f"✅ تەواو! {len(seen_links)} کەناڵ بە ناوەوە ئامادەکران.")

if __name__ == "__main__":
    get_list()

import requests
import re

def get_list():
    # سەرچاوەی سەرەکی کە لینکەکان دەگۆڕێت
    source_url = "http://oktvtv.atwebpages.com/loadb.js"
    try:
        response = requests.get(source_url, timeout=10)
        content = response.text
        
        # دەرهێنانی هەموو ئەو لینکە MPDیانەی کە تۆکنیان پێوەیە
        streams = re.findall(r'streamUrl\s*=\s*"(.*?)"', content)
        
        m3u = "#EXTM3U\n"
        for i, url in enumerate(streams):
            # لێرەدا دەتوانیت ناوەکان بگۆڕیت، بۆ نموونە بەپێی ڕیزبەندی
            m3u += f"#EXTINF:-1, OK-TV Channel {i+1}\n{url}\n\n"
            
        # پاشەکەوتکردنی وەک فایلێکی M3U جیاواز
        with open("oktv_list.m3u", "w", encoding="utf-8") as f:
            f.write(m3u)
        print("✅ لیستەکە بە سەرکەوتووی دروست کرا.")
    except Exception as e:
        print(f"❌ هەڵە ڕوویدا: {e}")

if __name__ == "__main__":
    get_list()

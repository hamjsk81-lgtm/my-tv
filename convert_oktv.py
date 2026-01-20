import requests
import re

def get_list():
    # لینکی لاپەڕەی سەرەکی بۆ ناوەکان و لینکی load.js بۆ ستریمەکان
    home_url = "http://oktvtv.atwebpages.com/"
    js_url = "http://oktvtv.atwebpages.com/load.js"
    
    try:
        # 1. وەرگرتنی لینکەکان لە فایلی JS
        js_res = requests.get(js_url)
        streams = re.findall(r'"(https?://[^"]+)"', js_res.text)
        
        # 2. وەرگرتنی ناوی کەناڵەکان لە لاپەڕەی سەرەکی (Index)
        home_res = requests.get(home_url)
        # ئەم بەشە بەدوای ناوەکاندا دەگەڕێت کە لەناو تاقەکانی HTML داندراون
        names = re.findall(r"showChannelName\('([^']+)'\)", home_res.text)
        
        # ئەگەر ناوەکان نەدۆزرانەوە، ناوێکی کاتی دادەنێین
        if not names:
            names = [f"Channel {i+1}" for i in range(len(streams))]

        m3u_content = "#EXTM3U\n"
        
        # 3. تێکەڵکردنی ناو و لینکەکان
        for i in range(len(streams)):
            name = names[i] if i < len(names) else f"Channel {i+1}"
            link = streams[i]
            
            # دروستکردنی لۆگۆیەکی سادە بەپێی ناوی کەناڵەکە
            logo = f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=random"
            
            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}", {name}\n{link}\n\n'

        # 4. خەزنکردنی فایلەکە
        with open("oktv_list.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
            
        print(f"✅ سەرکەوتوو بوو! {len(streams)} کەناڵ بە ناوی خۆیانەوە زیادکران.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_list()

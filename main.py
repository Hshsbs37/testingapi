from flask import Flask, jsonify, request
import os 
import re

from yt_dlp import YoutubeDL

app = Flask(__name__)

def g_link(url):

    out = []

    out.clear()

    try:

        c = 1

        with YoutubeDL({'quiet': True, "geo-bypass": True}) as ydl:

            info_dict = ydl.extract_info(url, download=False)

            title = info_dict['title']

            thumb = info_dict['thumbnail']

            regex = r'(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|playlist\?|watch\?v=|watch\?.+(?:&|&#38;);v=))([a-zA-Z0-9\-_]{11})?(?:(?:\?|&|&#38;)index=((?:\d){1,3}))?(?:(?:\?|&|&#38;)?list=([a-zA-Z\-_0-9]{34}))?(?:\S+)?'

            if re.match(regex,url):

                for format in info_dict["formats"]:

                    if format["format_id"] in ["18", "22"]:

                        videos = {"format": format["height"], "url": format["url"]}

                        out.append(videos)

                l = out

            else:

                for format in info_dict['formats']:

                    

                    if format.get("height"):

                        

                        m = 180

                        if format.get("manifest_url"):

                            u = format.get("manifest_url")

                        else:

                            u = format.get("url")

                        if not '.mpd' in u:

                            if not 'i.ytimg.com' in u:

                                if not '.jpg' in u:

                                    m*= c

                                    videos = {"format": m, "url": u}

                                    out.append(videos)

                                    c+=1

                l = out

            u = (list(filter(lambda l: l['format'] == 360 , l)))[0]['url']

            return 1,{'title':title,'thumb':thumb,'url':u}

    except Exception as e:

        return 0,0

@app.route('/')

def hello_world():

 

     t = {

     'status':False , 

     "usage":'please use in proper format \n/api/v1/yt-dlp?id=your link'

     }

     

     return jsonify(t)

@app.route('/api/v1/yt-dlp')

def api_hello():

    

    try:

     id = request.args['id']

    except:

     t = {

     'status':False , 

     "usage":'please use in proper format \n/api/v1/yt-dlp?id=your link'

     }

     

     return jsonify(t)

     

    x,y=g_link(id)

    

    if x ==1:

     t = {'status':True,'title':y.get('title'),'thumb': y.get('thumb'),'url':y.get('url')}

    else:

     t = {'status':False,'url':None}

    return jsonify(t)

if __name__ == '__main__':  

    app.run(debug=True,port=os.getenv("PORT", default=5000))


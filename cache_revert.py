import json
import os
import requests

home_dir = os.environ['HOME']
cache_dir = home_dir + '/Library/Containers/com.tencent.QQMusicMac/Data/Library/Application Support/QQMusicMac/iTemp/playing'
out_dir = home_dir +'/music/autodownload'


def get_music_info(filename):

    def get_music_url(filename):
        if filename.find('-') < 0:
            print("error filename: "+ filename)
            exit(0)
        id = filename.split('-')[1]
        return 'https://y.qq.com/n/yqq/song/{0}_num.html'.format(id)

    music_url = get_music_url(filename)

    resp = requests.get(music_url)
    text = resp.text
    flag_start = 'g_SongData = '

    start = text.index(flag_start) + len(flag_start)
    end = text.index("</script>",start) - 3
    js = text[start:end]
    info = json.loads(js)
    return info['songname'], info['singer'][0]['name']

def copy_cache():
    ld = os.listdir(cache_dir)
    for file in ld:
        song, singer = get_music_info(file)
        size = os.path.getsize(cache_dir + '/' + file) / 1024 / 1024
        filename = singer + ' - ' + song + '.m4a'
        cmd = 'cp "{0}/{1}" "{2}/cache/{3}"'.format(cache_dir, file, out_dir, filename)
        os.system(cmd)
        print("%s, %.2fMB" % (filename, size))

def m4a2mp3():
    m4a_dir = out_dir + '/cache/'
    ld = os.listdir(m4a_dir)
    for file in ld:
        out_file = os.path.splitext(file)[0] + '.mp3'
        cmd = 'ffmpeg -i "{0}" "{1}/{2}"'.format(m4a_dir+file, out_dir, out_file)
        os.system(cmd)
        print(cmd)


if __name__ == '__main__':
    copy_cache()



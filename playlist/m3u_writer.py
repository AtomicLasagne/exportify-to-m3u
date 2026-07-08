def write_m3u(path,tracks):
    with open(path,'w',encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        for t in tracks:
            f.write(t+'\n')

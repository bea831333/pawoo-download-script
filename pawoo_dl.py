import os, sys, urllib.request

if __name__ == "__main__":
    artistname = sys.argv[1]
    downloadfolder = "downloads"
    urlbase = "https://pawoo.net/@" + artistname + "/media?page="
    pagenum = 1
    flag = True
    while flag:
        flag = False
        url = urlbase + str(pagenum)
        page = urllib.request.urlopen(url).read().decode("utf-8")
        lines = page.split('\n')
        for line in lines:
            if line.startswith("<a href=\"https://img.pawoo.net/media_attachments/files"):
                if not os.path.exists(downloadfolder + artistname):
                    os.makedirs(downloadfolder)
                    os.makedirs(downloadfolder + artistname)
                
                download = line.split('"')[1]
                filename = download.split('/')[9]
                urllib.request.urlretrieve(download, os.path.join(artistname, filename))
                print("Downloaded " + filename)
            elif "Show more" in line:
                pagenum += 1
                flag = True
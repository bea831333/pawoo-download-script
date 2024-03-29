import os, sys, urllib.request

def increment_file_name(filename, multiple):
    filenameparts = filename.split('.')
    return ('.'.join(filenameparts[:-1]) + " - " + str(multiple) + "." + filenameparts[1])

if __name__ == "__main__":
    artistname = sys.argv[1]
    downloadfolder = "downloads"
    urlbase = "https://pawoo.net/@" + artistname + "/media"
    pagecomponent = ""
    flag = True
    end = False
    while flag and not end:
        flag = False
        if pagecomponent != "":
            url = urlbase + "?" + pagecomponent
        else:
            url = urlbase
        page = urllib.request.urlopen(url).read().decode("utf-8")
        lines = page.split('\n')
        for line in lines:
            if line.startswith("<a href=\"https://img.pawoo.net/media_attachments/files"):
                if not os.path.exists(downloadfolder):
                    os.makedirs(downloadfolder)
                if not os.path.exists(os.path.join(downloadfolder, artistname)):
                    os.makedirs(os.path.join(downloadfolder, artistname))
                
                download = line.split('"')[1]
                filename = download.split('/')[9]
                
                if os.path.exists(os.path.join(downloadfolder, artistname, filename)):
                    end = True
                    multiple = 1
                    newfilename = increment_file_name(filename, multiple)
                    while os.path.exists(os.path.join(downloadfolder, artistname, newfilename)):
                        multiple += 1
                        newfilename = increment_file_name(filename, multiple)
                    urllib.request.urlretrieve(download, os.path.join(downloadfolder, artistname, newfilename))
                    print("Downloaded '" + filename + "' as '" + newfilename + "'")
                else:
                    urllib.request.urlretrieve(download, os.path.join(downloadfolder, artistname, filename))
                    print("Downloaded '" + filename + "'")
            elif "Show more" in line:
                pagecomponent = line.split('?')[1].split('"')[0]
                flag = True
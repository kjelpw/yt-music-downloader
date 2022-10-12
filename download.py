playliststart = 1
playlistend = 24
download_link = ''

def guess_name():
    artist = ''
    title = ''
    if file[:-16].find(' - ') != -1:
        #if splittable
        artist = file[:-16].split(' - ')[0]
        title = file[:-16].split(' - ')[1]
        print(f'Artist: {artist} \nTitle: {title}')
        answer = input('Is this correct? (y/n)')
    else:
        title = file[:-16]
        print(f'Title: {title}')
        answer = input('Is this correct? (y/n)')
    return eval_answer(answer, artist, title)

def eval_answer(answer, artist, title):
    print(f'answer: {answer}')
    if answer == 'n':
        print(f'Filename: {file}')
        artist = input('Artist: ')
        title = input('Title: ')
    elif answer == 'y' and artist == '':
        print(f'Filename: {file}')
        artist = input('Artist: ')
    elif answer == 'y' and artist != '':
        print('You said title and artist are correct')
    else:
        print('answer must be y/n')
        guess_name()

    return artist, title


if __name__ == '__main__':
    import os
    if not os.path.exists('music'):
        os.mkdir('music')
    os.chdir('music')
    # download mp3
    import youtube_dl

    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'playliststart': playliststart,
        'playlistend': playlistend,
        'skip_download': False,
        'progress_hooks': [my_hook],
        'writethumbnail': True,
        'ignoreerrors': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([''])

    # add the thumbnails
    import eyed3
    import glob

    print('\n\n\nmp3 editing')

    # for every file
    for file in glob.glob("*.mp3"):
        print(file)
        # load mp3
        audiofile = eyed3.load(file)
        if (audiofile.tag == None):
            audiofile.initTag()

        print('thumbnail')

        # if .webp format exists, must convert
        if os.path.exists(file[:-4] + '.webp'):
            image_name = file[:-4] + '.webp'
            #convert thumbnails to jpeg
            from PIL import Image
            im = Image.open(image_name).convert('RGB')
            im.save(image_name[:-5] + '.jpg', 'jpeg')
        # save jpg to mp3
        if os.path.exists(file[:-4] + '.jpg'):
            image_file = open(file[:-4] + '.jpg', 'rb').read()
            audiofile.tag.images.set(3, image_file, 'image/jpeg')
        else:
            print(f'\n\n\n\n\n\n\nNO THUMBNAIL for {file}')

        #generate artist title
        artist, title = guess_name()
        audiofile.tag.title = title
        audiofile.tag.artist = artist

        audiofile.tag.save()
        print('\n\n\n')

    print('\n\n\n\n\nStarting Cleanup')

    for item in os.listdir('.'):
        if item.endswith(".jpg") or item.endswith(".webp"):
            print(f'Deleting: {item}')
            os.remove(item)
    os.chdir('..')

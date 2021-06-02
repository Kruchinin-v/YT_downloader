from pytube import YouTube
from environments.envdef.get_config import get_config

class Download:
    def __init__(self, url: str, path: str, progressive: bool, adaptive: bool, extension: str):
        self.url = url
        self.path = path
        self.progressive = progressive
        self.adaptive = adaptive
        self.extension = extension

        self.streams = None
        self.resolution = None

    def ask_resolution(self):
        resolutions = set()
        for i in self.streams:
            resolutions.add(int(i.resolution[:-1]))

        # print(resolutions)

        resolutions = list(resolutions)
        resolutions.sort()
        resolutions.reverse()

        for i in range(len(resolutions)):
            print(f"[{i}] {resolutions[i]}")

        result = ''
        response = ''
        while result != 'OK':
            try:
                response = input(
                    "Выбирите качество: ").lower()
            except KeyboardInterrupt:
                result = 'OK'
                print("")
                exit()

            try:
                response = int(response)
                if response > len(resolutions):
                    print("Число не в диапазоне")
                    continue
            except ValueError:
                print("Некорректный ввод")
                exit()

            result = 'OK'
        self.resolution = resolutions[response]
        return f"{self.resolution}p"

    def download():


        yt = YouTube(url)
        title = yt.title
        resolution = ""

        print(f"Название видео: {title}")

        streams = yt.streams.filter(file_extension=extension).order_by('resolution').desc()
        streams = streams.filter(progressive=progressive, adaptive=adaptive)

        if resolution == "":
            resolution = ask_resolution(streams)

        streams = streams.filter(resolution=resolution)

        if len(streams.filter(progressive=True)) > 0:
            print("Downloading...")
            streams.filter(progressive=True).first().download(output_path=path)
            return 0

        print("прогрессивного нет(")

        for i in streams:
            print(i)

    # print(streams.first().resolution)

    # yt.streams.filter(file_extension='mp4').order_by('resolution').desc().first().download(path)
    # yt.streams.filter(only_audio=True).first().download(PATH_TO_DOWNLOAD)

    # yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
    # for i in yt.streams.filter(resolution="1080p", file_extension='mp4'):
    # for i in yt.streams.filter(progressive=progressive, adaptive=adaptive).order_by('resolution').desc():

    # for i in yt.streams.order_by('resolution').desc():
    # for i in yt.streams:
    # for i in yt.streams.filter(only_audio=True):


def concat():
    import ffmpeg

    input_video = ffmpeg.input(r'z:\home\vkruchinin\projects\youtube_downloader\download\YouTube_video.mp4')

    input_audio = ffmpeg.input(r'z:\home\vkruchinin\projects\youtube_downloader\download\YouTube_audio.mp4')

    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(r'z:\home\vkruchinin\projects\youtube_downloader\download\YouTube_concat.mp4').run()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    config = get_config()['result']

    url_youtube = config['URL_YOUTUBE']
    is_progressive = config['PROGRESSIVE']
    is_adaptive = config['ADAPTIVE']
    file_extension = config['FILE_EXTENSION']
    base_dir = config['BASE_DIR']

    path_to_download = config['PATH_TO_DOWNLOAD']

    app = Download(url_youtube, path_to_download, is_progressive, is_adaptive, file_extension)
    app.download()

    # concat()

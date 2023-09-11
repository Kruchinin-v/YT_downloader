import os
import time
from pytube import YouTube
from environments.envdef.get_config import get_config
# from google.auth import credentials, compute_engine, exceptions
# from google.auth.transport.requests import Request
# from google.oauth2 import service_account


class Download:
    def __init__(self, url: str, path: str, progressive: bool, adaptive: bool, extension: str):
        self.url: str = url
        self.path = path
        self.progressive = progressive
        self.adaptive = adaptive
        self.extension = extension

        self.temp_dir = os.path.join(self.path, 'tmp')
        self.streams = None
        self.resolution = None
        self.title_video = None
        self.title_audio = None
        self.yt = None
        self.title = None
        self.path_input_video = None
        self.path_input_audio = None
        self.path_out = None
        self.begin_time = None
        self.end_time = None

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
                response = input("Выберите качество: ").lower()
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

    def ask_url(self) -> str:
        try:
            response: str = input("Enter url: ").strip()
        except KeyboardInterrupt:
            result = 'OK'
            print("")
            exit()
        return response

    def create_temp_dir(self):

        try:
            os.mkdir(self.temp_dir)
        except FileExistsError:
            pass
        except:
            raise

    def delete_tmp_files(self):
        os.remove(self.path_input_video)
        os.remove(self.path_input_audio)

    def concat(self):
        import subprocess

        path_out = os.path.join(self.path, f"{self.title}.mp4")
        self.path_out = path_out
        # path_out = os.path.join(self.temp_dir, f"out.mp4")

        try:
            command = f"ffmpeg -y -i {self.path_input_video} -i {self.path_input_audio} -c:v copy \"{path_out}\""
            print(command)
            answer = subprocess.run(command, shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, encoding='UTF-8')

            # print(answer.stdout)
            # print(answer.returncode)
            if answer.returncode != 0:
                print(answer.stderr)

            # print(input_audio)
            # print(input_video)

        except:
            raise

    def download_parts(self):
        import time
        time = int(time.time() * 1000)

        self.create_temp_dir()

        # time = "1622807133952"

        self.title_video = f"yt_{time}_video.mp4"
        self.title_audio = f"yt_{time}_audio.mp4"

        self.streams.first().download(output_path=self.temp_dir, filename=self.title_video)
        stream = self.yt.streams.filter(file_extension="mp4", only_audio=True)

        stream.first().download(output_path=self.temp_dir, filename=self.title_audio)

        path_input_video = os.path.join(self.temp_dir, self.title_video)
        path_input_audio = os.path.join(self.temp_dir, self.title_audio)

        self.path_input_video = path_input_video
        self.path_input_audio = path_input_audio

    def the_end(self):
        self.end_time = time.monotonic()
        result_time = int((self.end_time - self.begin_time) * 1000) / 1000
        print(f"Время работы: {result_time} sec")

    def download(self):
        import re
        if self.url == "":
            self.url = self.ask_url()
        # Авторизация может не сработать, надо поменять в коде библиотеки
        # в файле innertube.py на 223 строчке ANDROID_MUSIC на ANDROID
        yt = YouTube(self.url, use_oauth=True, allow_oauth_cache=True)
        self.yt = yt
        self.title = yt.title
        resolution = ""

        print(f"Название видео: {self.title}")

        self.title = re.sub('(\\|/|\*|:|#|\|)', '', self.title)
        # print(self.title)

        streams = yt.streams.filter(file_extension=self.extension).order_by('resolution').desc()
        streams = streams.filter(progressive=self.progressive, adaptive=self.adaptive)

        if resolution == "":
            self.streams = streams
            resolution = self.ask_resolution()

        streams = streams.filter(resolution=resolution)

        self.begin_time = time.monotonic()

        print("Downloading...")

        if len(streams.filter(progressive=True)) > 0:
            # streams.filter(progressive=True).first().download(output_path=self.path, skip_existing=False)
            streams.filter(progressive=True).first().download(output_path=self.path)
            self.the_end()
            return 0

        print("прогрессивного нет(")
        self.streams = streams
        self.download_parts()
        self.concat()
        self.delete_tmp_files()
        self.the_end()


        # for i in yt.streams.filter(only_audio=True, file_extension="mp4"):
        #     print(i)


def main():
    result = get_config()
    if result['status'] == 'Fail':
        print(result['result'])
        print(result['detail'])
        exit(1)

    config = result['result']

    url_youtube = config['URL_YOUTUBE']
    is_progressive = config['PROGRESSIVE']
    is_adaptive = config['ADAPTIVE']
    file_extension = config['FILE_EXTENSION']
    base_dir = config['BASE_DIR']

    path_to_download = config['PATH_TO_DOWNLOAD']

    app = Download(url_youtube, path_to_download, is_progressive, is_adaptive, file_extension)
    app.download()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Abort\n")
        exit()

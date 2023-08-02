####################################################################################################
# Project: Facebook Video Downloader
# Author: Jose Rey
# Date Created: 2023-08-02
# Description: A simple Facebook Video Downloader
####################################################################################################
# Github : https://github.com/joserey-alfante
####################################################################################################

import json
import os
import webbrowser
import subprocess
import sys
import re
import youtube_dl
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QFileDialog
from PyQt5.uic import loadUi


class FacebookDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.mode = 'day'
        try:
            loadUi("./assets/ui/facebookdownloader.ui", self)
            self.setWindowTitle("Facebook Downloader")
            self.setWindowIcon(QIcon("./assets/images/icon_logo.png"))

            # create a tray icon
            self.tray_icon = QSystemTrayIcon(self)
            self.tray_icon.setIcon(QIcon("./assets/images/icon_logo.png"))  # Load your custom image here
            self.tray_icon.setToolTip('YouTube Downloader')
            self.tray_icon.activated.connect(self.on_tray_icon_activated)

            self.tray_icon.show()

            # hide components
            self.errorMessage.setVisible(False)
            self.imgThumbnail.setVisible(False)
            self.btnDownload.setVisible(False)
            self.lblNote_2.setVisible(False)

            # connect signals
            self.btnDownload.clicked.connect(self.download_facebook_video)
            self.btnSearch.clicked.connect(self.search_video)
            self.btnFacebook.clicked.connect(self.open_facebook)
            self.btnGithub.clicked.connect(self.open_github)
            self.btnYoutube.clicked.connect(self.open_youtube)
            self.btnMode.clicked.connect(self.change_mode)

        except Exception as e:
            print("Error:", e)

    # get styles
    def get_content_by_name(self, target_name):
        try:
            file_path = "./assets/ui/styles/mode.json"
            with open(file_path, 'r') as file:
                data = json.load(file)
                for item in data:
                    if item.get('name') == target_name:
                        return item.get('content')
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Change Mode
    def change_mode(self):

        if self.mode == 'day':
            self.mode = 'night'
            self.btnMode.setIcon(QIcon("./assets/images/icon_day_mode.png"))
            pixmap = QPixmap("./assets/images/imgTh.png")
            self.imgThumbnail.setPixmap(pixmap)
            containerStyle = self.get_content_by_name('container-dark')
            titleStyle = self.get_content_by_name('lblTitle-dark')
            noteStyle = self.get_content_by_name('lblNote-dark')
            inputLinkStyle = self.get_content_by_name('inputLink-dark')
            lblNote2Style = self.get_content_by_name('lblNote_2-dark')
            self.container.setStyleSheet(str(containerStyle))
            self.lblTitle.setStyleSheet(str(titleStyle))
            self.lblNote.setStyleSheet(str(noteStyle))
            self.inputLink.setStyleSheet(str(inputLinkStyle))
            self.lblNote_2.setStyleSheet(str(lblNote2Style))

        else:
            self.mode = 'day'
            self.btnMode.setIcon(QIcon("./assets/images/icon_night_mode.png"))
            pixmap = QPixmap("./assets/images/imgThd.png")
            self.imgThumbnail.setPixmap(pixmap)
            containerStyle = self.get_content_by_name('container-light')
            titleStyle = self.get_content_by_name('lblTitle-light')
            noteStyle = self.get_content_by_name('lblNote-light')
            inputLinkStyle = self.get_content_by_name('inputLink-light')
            lblNote2Style = self.get_content_by_name('lblNote_2-light')
            self.container.setStyleSheet(str(containerStyle))
            self.lblTitle.setStyleSheet(str(titleStyle))
            self.lblNote.setStyleSheet(str(noteStyle))
            self.inputLink.setStyleSheet(str(inputLinkStyle))
            self.lblNote_2.setStyleSheet(str(lblNote2Style))

    # Open Github
    def open_github(self):
        # go to link github repository
        webbrowser.open('https://github.com/joserey-alfante/Facebook-Video-Downloader', new=2)

    # Open Youtube
    def open_youtube(self):
        # go to link youtube channel
        webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ', new=2)

    # Open Facebook
    def open_facebook(self):
        # go to link facebook page
        webbrowser.open('https://www.facebook.com/prgmr.joserey/', new=2)

    # Unshow Items
    def unshow_items(self):
        self.imgThumbnail.setVisible(False)
        self.btnDownload.setVisible(False)
        self.lblNote_2.setVisible(False)

    # Search Video
    def search_video(self):
        video_url = self.inputLink.text()
        if video_url == "":
            self.errorMessage.setText("Please enter link in the box.")
            self.errorMessage.setVisible(True)
            self.unshow_items()
            return
        self.errorMessage.setVisible(False)
        try:
            ydl_opts = {
                'quiet': True,
                'simulate': True,
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                try:
                    info_dict = ydl.extract_info(video_url, download=False)
                    if info_dict.get('entries'):
                        self.errorMessage.setVisible(False)
                        self.imgThumbnail.setVisible(True)
                        self.btnDownload.setVisible(True)
                        self.lblNote_2.setVisible(True)
                    else:
                        self.errorMessage.setText("Please enter a valid URL.")
                        self.errorMessage.setVisible(True)
                        self.unshow_items()
                except Exception as e:
                    self.errorMessage.setText("Please enter a valid URL.")
                    self.errorMessage.setVisible(True)
                    self.unshow_items()

        except Exception as e:
            print("Error:", e)

    # Download Video
    def download_facebook_video(self):
        video_url = self.inputLink.text()
        if video_url == "":
            self.errorMessage.setText("Please enter link in the box.")
            self.errorMessage.setVisible(True)
            self.unshow_items()
            return
        self.errorMessage.setVisible(False)
        try:
            ydl_opts = {
                'quiet': True,
                'simulate': True,
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                try:
                    info_dict = ydl.extract_info(video_url, download=False)
                    # get video id
                    video_id = info_dict.get('id', None)
                    match = re.search(r'facebook\.com/([^/]+)', video_url)
                    name = match.group(1)
                    if 'watch' in name:
                        name = 'facebookvideo'

                    if info_dict.get('entries'):

                        save_location, _ = QFileDialog.getSaveFileName(self, 'Save Audio', name + video_id,
                                                                       'Audio Files (*.mp4)')
                        if save_location:
                            self.download_start_message()
                            self.remove_temp_files()
                            ydl_opts1 = {
                                'format': 'bestvideo/best',
                                'outtmpl': './assets/temp/video_temp.mp4',
                            }

                            with youtube_dl.YoutubeDL(ydl_opts1) as ydl:
                                try:
                                    info_dict = ydl.extract_info(video_url, download=False)
                                    video_title = info_dict.get('title', 'video')
                                    uploader = info_dict.get('uploader', 'unknown')
                                    print(f"Downloading video: {video_title} by {uploader}")
                                    ydl.download([video_url])
                                except Exception as e:
                                    print("Error:", e)

                            ydl_opts2 = {
                                'format': 'bestaudio/best',
                                'outtmpl': './assets/temp/audio_temp.mp3',
                            }
                            with youtube_dl.YoutubeDL(ydl_opts2) as ydl1:
                                try:
                                    ydl1.download([video_url])
                                except Exception as e:
                                    print("Error:", e)

                            video_path = "./assets/temp/video_temp.mp4"
                            audio_path = "./assets/temp/audio_temp.mp3"

                            ffmpeg_path = "./assets/tools/ffmpeg.exe"
                            ffmpeg_cmd = f'"{ffmpeg_path}" -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac "{save_location}"'
                            self.tray_icon.showMessage('Facebook Video Downloader',
                                                       'Processing your Video Please Wait....',
                                                       QSystemTrayIcon.Information, 1000)
                            print("Merging audio and video files...")
                            subprocess.run(ffmpeg_cmd, shell=True)
                            self.remove_temp_files()
                            self.download_complete_message()
                    else:
                        self.errorMessage.setText("Please enter a valid URL.")
                        self.errorMessage.setVisible(True)
                        self.unshow_items()
                except Exception as e:
                    self.errorMessage.setVisible(True)
                    self.errorMessage.setText("Please enter a valid URL.")
                    self.unshow_items()

        except Exception as e:
            self.errorMessage.setVisible(True)
            self.errorMessage.setText("Please enter a valid URL.")

    # remove temp files
    def remove_temp_files(self):
        if os.path.exists("./assets/temp/video_temp.mp4"):
            os.remove("./assets/temp/video_temp.mp4")
        if os.path.exists("./assets/temp/audio_temp.mp3"):
            os.remove("./assets/temp/audio_temp.mp3")

    # Tray Icon Messages if Download Started
    def download_start_message(self):
        self.tray_icon.showMessage('Facebook Video Downloader', 'Download Started....',
                                   QSystemTrayIcon.Information, 1000)

    # Tray Icon Messages if Download Completed
    def download_complete_message(self):
        self.tray_icon.showMessage('Facebook Video Downloader', f'The facebook video downloaded successfully.',
                                   QSystemTrayIcon.Information, 5000)

    # Tray Icon Double-Click Event
    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggle_window()

    # Tray Icon Toggle Window
    def toggle_window(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FacebookDownloader()
    window.show()
    sys.exit(app.exec_())

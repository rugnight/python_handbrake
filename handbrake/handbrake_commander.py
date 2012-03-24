# -*- coding: utf-8 -*-

import sys
import commands
import handbrake_media as HB_MEDIA
import handbrake_setting as HB_SETTING

class HandBrakeCommander:
    def __init__(self):
        self.command_list = []

    def set(self, media, setting, output_dir):
        for title in media.titles:
            # 設定された有効時間を超える映像か
            if title.hour < setting.title_duration_available_hour or title.minute < setting.title_duration_available_minute or title.second < setting.title_duration_available_second:
                print "[no conv] title %d duration less than setting" % title.no
                continue
            
            # チャプター分割設定を読み込み
            chapter_splits = []
            chapter_num = len(title.chapters)
            if chapter_num < setting.chapter_split:
                print "[no conv] title %d chapter num less than chpater split setting" % title.no
                continue

            # 実際のチャプター数に収まる回数チャプター分割する
            begin = 1
            end   = begin + setting.chapter_split - 1
            while ( end < chapter_num ):
                chapter_splits.append([begin, end])
                begin = end + 1
                end   = begin + setting.chapter_split - 1
            
            # 実際に叩くコマンドを生成
            for i, chapter_split in enumerate(chapter_splits):
                TARGET_NAME      = media.name
                OUTPUT_EXT       = "m4v"
                TITLE_NO         = title.no
                PRESET_NAME      = setting.profile
                CHAPTER_BEGIN    = chapter_split[0]
                CHAPTER_END      = chapter_split[1]
                AUDIO_TRACK      = title.audios[0].no
                OUTPUT_FULL_NAME = "%s/%s_%02d_%02d.%s" % (output_dir, \
                                                            TARGET_NAME, \
                                                            TITLE_NO, \
                                                            i, \
                                                            OUTPUT_EXT )
                OUTPUT_FULL_NAME = OUTPUT_FULL_NAME.replace("//", "/")

                HB_CONVERT_COMMAND= "HandBrakeCLI -i %s -t %d -c %d-%d -a %d -o %s --preset \"%s\"" %(TARGET_NAME, \
                                                                                                        TITLE_NO, \
                                                                                                        CHAPTER_BEGIN, \
                                                                                                        CHAPTER_END, \
                                                                                                        AUDIO_TRACK, \
                                                                                                        OUTPUT_FULL_NAME, \
                                                                                                        PRESET_NAME)
                self.command_list.append(HB_CONVERT_COMMAND)

        if len(self.command_list) < 1:
            return False
        return True

    def dump(self):
        for command in self.command_list:
            print command 


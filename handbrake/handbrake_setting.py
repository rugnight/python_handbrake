# -*- coding: utf-8 -*-

import re

# ==================================================
class HandBrakeSetting:
# ==================================================

    # --------------------------------
    def __init__(self):
        self.title_duration_available_hour   = 0
        self.title_duration_available_minute = 0
        self.title_duration_available_second = 0

        self.chapter_split = 0
        self.profile       = ""
        self.output_ext    = ""

    # --------------------------------
    def set(self, setting_file):
        f = open(setting_file, "r")

        for line in f:
            # タイトル時間設定
            match = re.match(r"^TITLE_DURATION_AVAILABLE\s+?\d\d:\d\d:\d\d", line)
            if match != None:
                search = re.search(r"\d\d:\d\d:\d\d", line)
                duration = search.group().split(":")

                self.title_duration_available_hour   = int(duration[0])
                self.title_duration_available_minute = int(duration[1])
                self.title_duration_available_second = int(duration[2])
                continue

            # チャプター分割設定
            match = re.match(r"^CHAPTER_SPLIT\s+?\d", line)
            if match != None:
                self.chapter_split = int(match.group().split()[1])
                continue

            # 映像品質設定
            match = re.match(r"^PROFILE\s+?\"[\s\w\d_-]+\"", line)
            if match != None:
                self.profile = re.search(r"\"[\s\w\d_-]+\"", line).group()

            # 出力形式を設定
            match = re.match(r"^OUTPUT_EXT\s+?\"[\w\d]+\"", line)
            if match != None:
                self.output_ext = re.search(r"\"[\w\d]+\"", line).group()

        f.close()
        return self.is_valid()

    # --------------------------------
    def is_valid(self):
        if self.title_duration_available_hour == 0 and self.title_duration_available_minute == 0 and self.title_duration_available_second == 0:
            return False
        if self.chapter_split == 0:
            return False
        if self.profile == "":
            return False
        if self.output_ext == "":
            return False

        return True

    # --------------------------------
    def dump(self):
        if self.is_valid() == False:
            print "invalid setting\n"
            return 

        print "TITLE_DURATION_AVAILABLE %02d:%02d:%02d" % (self.title_duration_available_hour, self.title_duration_available_minute, self.title_duration_available_second)
        print "CHAPTER_SPLIT %d" % self.chapter_split
        print "PROFILE %s" % self.profile

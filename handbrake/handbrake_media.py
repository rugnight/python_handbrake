# -*- coding: utf-8 -*-

import re
import sys
import string

# ==================================================
class HandBrakeChapter:
# ==================================================
    # ------------------------------
    def __init__(self):
        self.no              = 0
        self.cells_begin     = 0
        self.cells_end       = 0
        self.blocks          = 0
        self.duration_hour   = 0
        self.duration_minute = 0
        self.duration_second = 0
    # ------------------------------
    def set(self, hb_chapter_line):
        if re.match(r"^\s{4,4}\+\s(\d+?): cells", hb_chapter_line) == None:
            return False

        # + と : と , を削除
        hb_chapter_line = hb_chapter_line.translate(string.maketrans("", ""), "+,")
        hb_chapter_line = hb_chapter_line.replace(":", " ")
        hb_chapter_line = hb_chapter_line.replace("->", " ")
        # 先頭と末尾の空白を除去
        hb_chapter_line = hb_chapter_line.strip()

        # 情報を抽出
        list = hb_chapter_line.split(" ")
        self.no              = int(list[0])
        self.cells_begin     = int(list[3])
        self.cells_end       = int(list[4])
        self.blocks          = int(list[5])
        self.duration_hour   = int(list[8])
        self.duration_minute = int(list[9])
        self.duration_second = int(list[10])
        return True
    # ------------------------------
    def dump(self):
        print "    %d: cells %d->%d, %d blocks, duration %02d:%02d:%02d" % (self.no, self.cells_begin, self.cells_end, self.blocks, self.duration_hour, self.duration_minute, self.duration_second)

# ==================================================
class HandBrakeAudioTrack:
# ==================================================
    # ------------------------------
    def __init__(self):
        self.no     = 0
        self.locale = ""
    # ------------------------------
    def set(self, line):
        if re.match(r"^\s{4,4}\+\s(\d+?),\s(Japanese|English)\s(\(AC3\)|\(DTS\))", line) == None:
            return False
        # 先頭と末尾の空白を除去
        list = line.translate(string.maketrans("", ""), "+,()").strip().split()
        self.no     = int(list[0])
        self.locale = list[1]
        return True
    # ------------------------------
    def dump(self):
        print "    %d, %s" % (self.no, self.locale)

# ==================================================
class HandBrakeSubtitleTrack:
# ==================================================
    # ------------------------------
    def __init__(self):
        self.no     = 0
        self.locale = ""
    # ------------------------------
    def set(self, line):
        if re.match(r"^\s{4,4}\+\s(\d+?),\s(Japanese|English)", line) == None:
            return False
        # 先頭と末尾の空白を除去
        list = line.translate(string.maketrans("", ""), "+,()").strip().split()
        self.no     = int(list[0])
        self.locale = list[1]
        return True
    # ------------------------------
    def dump(self):
        print "    %d, %s" % (self.no, self.locale)

# ==================================================
class HandBrakeTitle:
# ==================================================
    # ------------------------------
    def __init__(self):
        self.no                   = 0
        self.duration_hour        = 0
        self.duration_minute      = 0
        self.duration_second      = 0

        self.chapter_list        = []
        self.audio_track_list    = []
        self.subtitle_track_list = []
    # ------------------------------
    def set_title_line(self, line):
        line = line.replace(":", "")
        list = line.split(" ")
        self.no = int(list[2])
    # ------------------------------
    def set_duration(self, line):
        match = re.search(r"\d\d:\d\d:\d\d", line)
        if match != None:
            list = match.group().split(":")
            self.duration_hour        = int(list[0])
            self.duration_minute      = int(list[1])
            self.duration_second      = int(list[2])
    # ------------------------------
    def add_chapter(self, chapter):
        self.chapter_list.append(chapter)
    # ------------------------------
    def add_audio_track(self, audio_track):
        self.audio_track_list.append(audio_track)
    # ------------------------------
    def add_subtitle_track(self, subtitle_track):
        self.subtitle_track_list.append(subtitle_track)
    # ------------------------------
    def set(self, line):
        chapter        = HandBrakeChapter()
        audio_track    = HandBrakeAudioTrack()
        subtitle_track = HandBrakeSubtitleTrack()

        if re.match(r"^\+\stitle", line) != None:
            self.set_title_line(line)
        elif re.match(r"^\s{2,2}\+\s(duration)", line) != None:
            self.set_duration(line)
        elif chapter.set(line) == True:
            self.add_chapter(chapter) # 各チャプター情報の行マッチ
        elif audio_track.set(line) == True:
            self.add_audio_track(audio_track)
        elif subtitle_track.set(line) == True:
            self.add_subtitle_track(subtitle_track)

    # ------------------------------
    def dump(self):
        print "title %d" % self.no
        print "  duration %02d:%02d:%02d" % (self.duration_hour, self.duration_minute, self.duration_second)
        self.dump_chapters()
        self.dump_audio_tracks()
        self.dump_subtitle_tracks()
    # ------------------------------
    def dump_chapters(self):
        if len(self.chapter_list) == 0:
            return
        print "  chapters %d" % len(self.chapter_list)
        for chapter in self.chapter_list:
            chapter.dump()
    # ------------------------------
    def dump_audio_tracks(self):
        if len(self.audio_track_list) == 0:
            return
        print "  audio_tracks"
        for track in self.audio_track_list:
            track.dump()
    # ------------------------------
    def dump_subtitle_tracks(self):
        if len(self.subtitle_track_list) == 0:
            return
        print "  subtitle_tracks"
        for track in self.subtitle_track_list:
            track.dump()

# ==================================================
class HandBrakeMedia:
# ==================================================
    # ------------------------------
    def __init__(self):
        self.titles = []
    # ------------------------------
    def set(self, lines):
        title = None
        for line in lines:
            if re.match(r"^\+", line) != None:
                if title != None:
                    self.titles.append(title)
                title = HandBrakeTitle()
                title.set(line)
            elif re.match(r"^\s{1,4}\+\s", line) != None:
                title.set(line)
        title.dump()

        for title in self.titles:
            title.dump()

argvs = sys.argv  # コマンドライン引数を格納したリストの取得
argc = len(argvs) # 引数の個数

f = open("dvdinfo", "r")
media = HandBrakeMedia()
media.set(f)
f.close()

# -*- coding: utf-8 -*-

import re
import string

# ==========================================================================================================
# チャプター情報を保持する
# こういう文字列を入れると各数値を保持してくれる-> "    + 1: cells 0->0, 314920 blocks, duration 00:10:21"
# ==========================================================================================================
class HandBrakeChapter:
    def __init__(self):
        self.no              = 0
        self.cells_begin     = 0
        self.cells_end       = 0
        self.blocks          = 0
        self.duration_hour   = 0
        self.duration_minute = 0
        self.duration_second = 0

    def set(self, hb_chapter_line):
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

    def dump(self):
        print "    %d: cells %d->%d, %d blocks, duration %02d:%02d:%02d" % (self.no, self.cells_begin, self.cells_end, self.blocks, self.duration_hour, self.duration_minute, self.duration_second)

class HandBrakeAudioTrack:
    def __init__(self):
        self.no     = 0
        self.locale = ""

    def set(self, line):
        # 先頭と末尾の空白を除去
        list = line.translate(string.maketrans("", ""), "+,()").strip().split()
        self.no     = int(list[0])
        self.locale = list[1]

    def dump(self):
        print "    %d, %s" % (self.no, self.locale)

class HandBrakeSubtitleTrack:
    def __init__(self):
        self.no     = 0
        self.locale = ""

    def set(self, line):
        # 先頭と末尾の空白を除去
        list = line.translate(string.maketrans("", ""), "+,()").strip().split()
        self.no     = int(list[0])
        self.locale = list[1]

    def dump(self):
        print "    %d, %s" % (self.no, self.locale)

# ==========================================================================================================
# タイトル以下の情報を保持する
# ==========================================================================================================
class HandBrakeTitle:
    def __init__(self):
        self.no                   = 0
        self.cells_begin          = 0
        self.cells_end            = 0
        self.blocks               = 0
        self.duration_hour        = 0
        self.duration_minute      = 0
        self.duration_second      = 0

        self.chapter_list        = []
        self.audio_track_list    = []
        self.subtitle_track_list = []

    def set_title_line(self, line):
        line = line.replace(":", "")
        list = line.split(" ")
        self.no = int(list[2])

    def set_duration(self, line):
        match = re.search(r"\d\d:\d\d:\d\d", line)
        if match != None:
            list = match.group().split(":")
            self.duration_hour        = int(list[0])
            self.duration_minute      = int(list[1])
            self.duration_second      = int(list[2])

    def add_chapter(self, line):
        chapter = HandBrakeChapter()
        chapter.set(line)
        self.chapter_list.append(chapter)

    def add_audio_track(self, line):
        audio_track = HandBrakeAudioTrack()
        audio_track.set(line)
        self.audio_track_list.append(audio_track)

    def add_subtitle_track(self, line):
        subtitle_track = HandBrakeSubtitleTrack()
        subtitle_track.set(line)
        self.subtitle_track_list.append(subtitle_track)

    def set(self, hb_title_lines):
        for line in hb_title_lines:
            if re.match(r"^\+\stitle", line) != None:
                self.set_title_line(line)
            #elif re.match(r"^\s{2,2}\+\s(vts)", line) != None:
            elif re.match(r"^\s{2,2}\+\s(duration)", line) != None:
                self.set_duration(line)
            #elif line.startswith("vts") == True: 
            #elif line.startswith("size") == True: 
            #elif line.startswith("autocrop") == True: 
            #elif line.startswith("audio tracks") == True: 
            #elif line.startswith("subtitle tracks") == True: 
            #elif re.match(r"^\s{4,4}\+\s(\d+?): cells", line) != None:
            #elif re.match(r"^\s{2,2}\+\s(chapters:)", line) != None:
            elif re.match(r"^\s{4,4}\+\s(\d+?): cells", line) != None:
                self.add_chapter(line) # 各チャプター情報の行マッチ
            elif re.match(r"^\s{4,4}\+\s(\d+?),\s(Japanese|English)\s(\(AC3\)|\(DTS\))", line) != None:
                self.add_audio_track(line)
            elif re.match(r"^\s{4,4}\+\s(\d+?),\s(Japanese|English)", line) != None:
                self.add_subtitle_track(line)

    def dump(self):
        print "title %d" % self.no
        print "duration %02d:%02d:%02d" % (self.duration_hour, self.duration_minute, self.duration_second)
        print "chapters %d" % len(self.chapter_list)
        self.dump_chapters()
        print "audio_tracks"
        self.dump_audio_tracks()
        print "subtitle_tracks"
        self.dump_subtitle_tracks()

    def dump_chapters(self):
        for chapter in self.chapter_list:
            chapter.dump()

    def dump_audio_tracks(self):
        for track in self.audio_track_list:
            track.dump()

    def dump_subtitle_tracks(self):
        for track in self.subtitle_track_list:
            track.dump()

title_lines = [ "+ title 1:", "  + vts 1, ttn 1, cells 0->15 (2798727 blocks)", "  + duration: 01:30:50", "  + size: 720x480, aspect: 1.78, 23.976 fps", "  + autocrop: 54/58/0/0", "  + chapters:", "    + 1: cells 0->0, 314920 blocks, duration 00:10:21", "    + 2: cells 1->2, 333687 blocks, duration 00:10:46", "    + 3: cells 3->4, 319852 blocks, duration 00:10:24", "    + 4: cells 5->5, 275321 blocks, duration 00:08:52", "    + 5: cells 6->6, 219914 blocks, duration 00:07:06", "    + 6: cells 7->8, 136708 blocks, duration 00:04:25", "    + 7: cells 9->9, 177895 blocks, duration 00:05:48", "    + 8: cells 10->10, 199956 blocks, duration 00:06:28", "    + 9: cells 11->11, 145376 blocks, duration 00:04:47", "    + 10: cells 12->12, 269923 blocks, duration 00:08:41", "    + 11: cells 13->13, 160433 blocks, duration 00:04:57", "    + 12: cells 14->15, 244742 blocks, duration 00:08:17", "  + audio tracks:", "    + 1, English (AC3) (Dolby Surround), 48000Hz, 192000bps", "    + 2, English (DTS) (5.1 ch), 48000Hz, 1536000bps", "    + 3, Japanese (AC3) (5.1 ch), 48000Hz, 384000bps", "    + 4, Japanese (AC3) (5.1 ch), 48000Hz, 384000bps", "  + subtitle tracks:", "    + 1, English (iso639-2: eng)", "    + 2, Japanese (iso639-2: jpn)"]

title = HandBrakeTitle()
title.set(title_lines)
title.dump()

#!/usr/bin/env python3.6

"""
For all MOV and MKV files, MD5 sidecar files are created for both the video and audio streams.
e.g.
* 10SecondTest.mkv.videomd5
* 10SecondTest.mov.videomd5
* 10SecondTest.mkv.audiomd5
* 10SecondTest.mov.audiomd5

We need to check that the contents of 10SecondTest.mkv.videomd5 & 10SecondTest.mov.videomd5 match.

Likewise, 10SecondTest.mkv.audiomd5 & 10SecondTest.mov.audiomd5 should match.
Note that the audio stream isn't reencoded in BAVC's workflow - so there really should be no difference there!
"""

import filecmp
import os
import re
import sys


AUDIO = 'audio'
VIDEO = 'video'
MATCHES = 'matches'
MISMATCHES = 'mismatches'


def retrieve_base_filename(filename):
    # 10SecondTest.mkv.videomd5 → 10SecondTest
    return re.match('(.+?)\.mkv\.videomd5', filename).group(1)


def audio_match(base_filename):
    return file_contents_match(base_filename, AUDIO)


def video_match(base_filename):
    return file_contents_match(base_filename, VIDEO)


def file_contents_match(base_filename, stream_type):
    return filecmp.cmp(f'{base_filename}.mkv.{stream_type}md5', f'{base_filename}.mov.{stream_type}md5')


def report_on_files(filenames, path):
    stats = {
        AUDIO: {
            MATCHES: [],
            MISMATCHES: []
        },
        VIDEO: {
            MATCHES: [],
            MISMATCHES: [],
        }
    }

    for f in filenames:
        file_path = os.path.join(path, f)

        if audio_match(file_path):
            stats[AUDIO][MATCHES].append(f)
        else:
            stats[AUDIO][MISMATCHES].append(f)

        if video_match(file_path):
            stats[VIDEO][MATCHES].append(f)
        else:
            stats[VIDEO][MISMATCHES].append(f)

    return stats


def print_stats(base_filenames, stats):
    print(f"""
    -----------------------------------------------
    {len(base_filenames)} files were checked.

    🎵    🎵    🎵    🎵    🎵    🎵    🎵    🎵    🎵    🎵
    Audio stream checksum mismatches: {len(stats[AUDIO][MISMATCHES])}
    {files_affected_summary(stats, AUDIO)}

    📼    📼    📼    📼    📼    📼    📼    📼    📼    📼
    Video stream checksum mismatches: {len(stats[VIDEO][MISMATCHES])}
    {files_affected_summary(stats, VIDEO)}
    -----------------------------------------------
    """)


def files_affected_summary(stats, stream_type):
    mismatches = stats[stream_type][MISMATCHES]

    if len(mismatches) > 0:
        return f"The following files were affected: {(', '.join(mismatches))}"
    else:
        return 'No worries!'


def set_md5_directory():
    if len(sys.argv) == 1:
        print('No directory supplied! Will attempt to run script on contents of current directory')
        return '.'

    path = sys.argv[1]

    if os.path.exists(path):
        return path
    else:
        print('Not a valid directory! Will attempt to run script on contents of current directory')
        return '.'


def main():
    path = set_md5_directory()
    filenames = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    mov_md5_filenames = [f for f in filenames if re.search('.mkv.videomd5', f)]
    base_filenames = [retrieve_base_filename(f) for f in mov_md5_filenames]

    if len(base_filenames) == 0:
        print('No relevant files detected!')
        return

    stats = report_on_files(base_filenames, path)
    print_stats(base_filenames, stats)


main()

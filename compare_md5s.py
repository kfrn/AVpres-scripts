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


def report_on_files(filenames):
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
        if audio_match(f):
            stats[AUDIO][MATCHES].append(f)
        else:
            stats[AUDIO][MISMATCHES].append(f)

        if video_match(f):
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


def main():
    # Will look at files in the current directory (of the script)
    filenames = [f for f in os.listdir('.') if os.path.isfile(f)]
    mov_md5_filenames = [f for f in filenames if re.search('.mkv.videomd5', f)]
    base_filenames = [retrieve_base_filename(f) for f in mov_md5_filenames]

    stats = report_on_files(base_filenames)
    print_stats(base_filenames, stats)


main()

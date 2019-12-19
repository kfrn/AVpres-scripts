# AVpres-scripts

A repo for AVpres-related odds & ends.

Requirements:
* Python `3.6`

## `compare_md5s.py`

At BAVC, they're [converting ffv1/MKV files to v210/MOV](https://bavc.org/blog/converting-ffv1mkv-v210mov).  
For each file, they create checksums for the video and audio streams before and after transcode, and then compare the two in order to check the content integrity.

Morgan Morel writes,
> From here it’s just a matter of comparing the MD5 of the MKV and MOV streams. At this point there was no bash scripting or application to help, we simply opened up the MD5 sidecar files in TextEdit and made the comparison manually. [...]
>
> If anybody has any good suggestions on how to use diff or a similar tool to do this comparison quickly, please let us know! Automation would certainly be useful on a batch of hundreds of files, but for 27 files we were fine to do it manually.

This script addresses that use case.

To run:
```bash
python3 compare_md5s.py
# Or:
python3 compare_md5s.py '/path/to/md5_directory'
```

Note that the path supplied is relative to the directory from which you call the script.

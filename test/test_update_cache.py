"""
Test pyficache.main.update_cache
"""

import os
import shutil
import tempfile

# Important note. Access to file_cache must come via
# pyfycache.main qualification and can't be "from" imported
# since that can cache the information.
import pyficache
from pyficache.main import update_cache


def test_update_cache():
    # Get the path of the current script
    current_file = __file__

    orig_lines = open(current_file).readlines()
    cached_filename = update_cache(current_file, {"use_linecache_lines": True})

    # Note that we access file_cache via pyfycache.main!
    assert pyficache.main.file_cache[cached_filename].lines["plain"] == orig_lines

    try:
        # Create a NamedTemporaryFile
        # delete=False ensures the file remains on disk after we close the context
        with tempfile.NamedTemporaryFile(
            delete=False, prefix="test_update_cache", suffix=".py"
        ) as tmp:
            tmp_path = tmp.name

        # Copy current file to the temporary file path
        shutil.copy2(current_file, tmp_path)
        print(f"Temporary file created at: {tmp_path}")

        cached_filename2 = update_cache(tmp_path, {"use_linecache_lines": True})
        assert pyficache.main.file_cache[cached_filename2].lines["plain"] == orig_lines

        # Modify a character in the temporary file
        # We open it in r+ mode (read/write)
        with open(tmp_path, "r+") as f:
            content = f.read()
            if content:
                # For example, replace the first character with an 'X'
                modified_content = "X" + content[1:]

                f.seek(0)  # Go back to start
                f.write(modified_content)
                f.truncate()  # Ensure no old data remains if the new content is shorter

        cached_filename3 = update_cache(tmp_path, {"use_linecache_lines": True})
        assert pyficache.main.file_cache[cached_filename3].lines["plain"] != orig_lines
    finally:
        # Delete temporary file used in test.
        os.remove(tmp_path)

    return


if __name__ == "__main__":
    test_update_cache()

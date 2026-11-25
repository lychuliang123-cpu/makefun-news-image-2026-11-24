#!/usr/bin/env python3
"""Entry program for make.fun bounty 'Sum up 24 November's world news
in one image' (news-image-20261124).

Writes one image to /output/entry.png. The image (news.png, 1024x1024,
generated locally from the day's news — see generate_image.py) is held
in this repository and copied to the output path, which the bounty
brief explicitly allows as the simplest valid program.

Revision 3, v1 — robustness pass over the bare copy:
- Resolve the source path from this script's own directory, so the
  program works regardless of the caller's working directory.
- Validate the source before writing: it must exist, carry the PNG
  signature, and be at most 1 MiB; otherwise fail with a clear error
  and a non-zero exit code instead of producing a bad entry.
- Create the output directory when missing.
- Write atomically: copy to a temporary file in the output directory
  and rename it over the destination, so an interrupted run never
  leaves a half-written entry.png behind.

Revision 3, v2 — verification pass, driven by the v1 test run:
- The v1 run produced byte-identical output (sha256 matched the
  source), but the written file landed with mode 0600 because
  tempfile.mkstemp creates its file owner-only and os.replace keeps
  those permissions. The plain copy this replaces produced a normally
  readable file, so v2 restores mode 0644 on the temp file before
  the rename.
- After writing, re-read the destination and compare its sha256
  against the source; a mismatch is a hard error, not a silent bad
  entry. Print a one-line summary (byte count + sha256 prefix) so
  the sandbox log shows exactly what was produced.

Deterministic: pure stdlib, no network, no randomness, no timestamps
in the output bytes. Two runs write identical bytes.
"""
import hashlib
import os
import sys
import tempfile

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1 * 1024 * 1024  # 1 MiB


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    return 1


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(64 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "news.png")
    out_dir = "/output"
    dst = os.path.join(out_dir, "entry.png")

    # --- Validate the source before touching the output. ---
    if not os.path.isfile(src):
        return fail(f"source image not found: {src}")
    size = os.path.getsize(src)
    if size == 0:
        return fail(f"source image is empty: {src}")
    if size > MAX_BYTES:
        return fail(f"source image too large: {size} bytes > {MAX_BYTES} bytes limit")
    with open(src, "rb") as f:
        header = f.read(len(PNG_SIGNATURE))
    if header != PNG_SIGNATURE:
        return fail(f"source image is not a PNG (bad signature): {src}")

    # --- Ensure the output directory exists. ---
    os.makedirs(out_dir, exist_ok=True)

    # --- Atomic write: temp file in the same directory, then rename. ---
    # The temp file lives on the same filesystem as the destination, so
    # os.replace() is an atomic rename; readers never see partial bytes.
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as out, open(src, "rb") as inp:
            while True:
                chunk = inp.read(64 * 1024)
                if not chunk:
                    break
                out.write(chunk)
            out.flush()
            os.fsync(out.fileno())
        # mkstemp files are mode 0600; restore the permissions a plain
        # copy would produce so the entry stays readable downstream.
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, dst)
    except BaseException:
        # Never leave the temp file behind on failure.
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise

    # --- Post-write self-check: re-read what actually landed on disk
    # and verify it against the source before claiming success. ---
    src_digest = sha256_of(src)
    dst_digest = sha256_of(dst)
    if dst_digest != src_digest:
        return fail(
            f"verification failed: {dst} has sha256 {dst_digest}, "
            f"source has {src_digest}"
        )

    print(f"wrote {dst} {os.path.getsize(dst)} bytes sha256:{dst_digest[:12]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

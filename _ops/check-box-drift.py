#!/usr/bin/env python3
"""
check-box-drift.py — is anything live on the ZimaOS box missing from GitHub?

WHY THIS EXISTS
    On 2026-08-19 an audit found 3,452 files / 1,160 MB that existed only on
    zima:/DATA/AppData/acedigitalservicesco/work and in no repo. 915 MB of it was
    lebanon-borough-v2/docs, 1,969 scraped borough PDFs that the live site links to.

    Cause: the deploy tooling writes to the box and never commits. lebanon_sync.py
    scp'd PDFs straight there (fixed 2026-08-19). Five more scripts under
    ~/.openclaw/workspace-leo/scripts (deploy_demo, batch-demos, factory_tick,
    gallery_backfill, gallery_backfill_cached) rsync to the box with zero git refs.

    Patching all five was judged riskier than leaving them: they are the working
    demo factory. So instead of five preventions, one detector. Run this and the
    drift cannot rot silently again.

WHAT IT CHECKS
    Every file under the box's work/ against what is committed on the REMOTE
    (origin/main) of both repos that feed it:
      - acedigitalservicesco   (the repo the box is a checkout of, deploys by webhook)
      - ace-demos              (holds the cold demos + lebanon + gallery, no webhook)

    Committed-on-remote is the bar, not "exists on my Mac". A file in a working
    tree is not backed up.

USAGE
    check-box-drift.py                 # report
    check-box-drift.py --quiet         # only print if drift found (for cron)
    check-box-drift.py --json          # machine readable

EXIT CODES
    0 = no drift          1 = drift found          2 = could not complete the check
"""
import argparse, json, os, subprocess, sys

BOX_HOST = "zima"
BOX_WORK = "/DATA/AppData/acedigitalservicesco/work"
REPOS = {
    "acedigitalservicesco": os.path.expanduser("~/ace-sites-v3/acedigitalservicesco-clone"),
    "ace-demos":            os.path.expanduser("~/ace-sites-v3/digital"),
}
# Genuine non-artifacts: scratch backups and generated caches. Anything ignored here
# is a deliberate decision, not an oversight. Keep this list SHORT and justified.
IGNORE_PREFIXES = (
    "gallery-under-main.bak-",   # dated scratch backups of an already-tracked dir
)
IGNORE_SUFFIXES = (".DS_Store",)


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def box_files():
    """Every regular file under the box's work/, relative to work/."""
    r = sh(["ssh", "-o", "ConnectTimeout=15", "-o", "BatchMode=yes", BOX_HOST,
            f"cd {BOX_WORK} && find . -type f 2>/dev/null | sed 's|^\\./||'"])
    if r.returncode != 0:
        sys.exit(f"could not list the box over ssh ({BOX_HOST}): {r.stderr.strip()[:200]}")
    return {l for l in r.stdout.splitlines() if l}


def committed_files():
    """Union of files committed on origin/main under work/, across both repos."""
    out = set()
    for name, path in REPOS.items():
        if not os.path.isdir(path):
            print(f"  ! repo not found locally, skipping: {name} ({path})", file=sys.stderr)
            continue
        f = sh(["git", "-C", path, "fetch", "-q", "origin"])
        if f.returncode != 0:
            sys.exit(f"git fetch failed for {name}: {f.stderr.strip()[:200]}")
        r = sh(["git", "-C", path, "ls-tree", "-r", "--name-only", "origin/main", "work/"])
        if r.returncode != 0:
            sys.exit(f"git ls-tree failed for {name}: {r.stderr.strip()[:200]}")
        for line in r.stdout.splitlines():
            if line.startswith("work/"):
                out.add(line[len("work/"):])
        # ace-demos also keeps quarantined demos at the repo root, and the box
        # holds them under work/_quarantine/. Same content, different path.
        r2 = sh(["git", "-C", path, "ls-tree", "-r", "--name-only", "origin/main", "_quarantine/"])
        for line in r2.stdout.splitlines():
            if line.startswith("_quarantine/"):
                out.add("work/" + line)
                out.add(line)
    return out


def ignored(rel):
    return rel.endswith(IGNORE_SUFFIXES) or any(rel.startswith(p) for p in IGNORE_PREFIXES)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true", help="print nothing when clean")
    ap.add_argument("--json", action="store_true", help="machine readable output")
    a = ap.parse_args()

    box = box_files()
    committed = committed_files()
    missing = sorted(f for f in box - committed if not ignored(f))

    by_dir = {}
    for f in missing:
        by_dir.setdefault(f.split("/")[0], []).append(f)

    if a.json:
        print(json.dumps({"box_files": len(box), "committed_files": len(committed),
                          "missing_count": len(missing),
                          "missing_dirs": {k: len(v) for k, v in sorted(by_dir.items())},
                          "missing": missing}, indent=2))
        return 1 if missing else 0

    if not missing:
        if not a.quiet:
            print(f"clean — all {len(box)} files on the box are committed on origin/main")
        return 0

    print(f"DRIFT: {len(missing)} file(s) live on the box are NOT committed on origin/main")
    print(f"       (box has {len(box)} files; {len(committed)} paths committed across "
          f"{', '.join(REPOS)})\n")
    for d, fs in sorted(by_dir.items(), key=lambda kv: -len(kv[1])):
        print(f"  {d}  ({len(fs)} file(s))")
        for f in fs[:4]:
            print(f"      {f}")
        if len(fs) > 4:
            print(f"      ... and {len(fs) - 4} more")
    print("\nTo fix, pull them into the repo that owns the directory and push, e.g.:")
    print("  cd ~/ace-sites-v3/digital/work && \\")
    print(f"    rsync -a {BOX_HOST}:{BOX_WORK}/<slug> . && \\")
    print("    cd .. && git add work/<slug> && git commit -m 'Recover box-only files' && git push")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(2)

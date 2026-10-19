#!/usr/bin/env python3
"""Compile generated Jetpack Compose / Compose Multiplatform files without the user's project.

  compile_kotlin.py <file.kt or folder> [...] [--no-android] [--offline]

Copies the files into a throwaway Kotlin Multiplatform project (scripts/kotlin-check: Kotlin
2.2.21, Compose Multiplatform 1.9.0, JVM + Android targets) and compiles them:
  - files that import Android-only APIs (android.*, androidx.activity, androidx.core, Google Fonts,
    LocalContext, androidx.compose.ui.res) go to androidMain;
  - everything else, and anything under shared/ or commonMain/, goes to commonMain and must
    compile for both targets, so Android-only APIs in shared CMP code fail as in a real module;
  - Compose resources the code references (Res.font.x, Res.drawable.x, Res.string.x) are
    stubbed, so a missing asset file is reported as a note, not a compile error.

Exit 0: compiles. Exit 1: errors (printed as file:line: message, with your paths).
Exit 3: can't run here (no JDK 17+, no Gradle, or dependencies unavailable offline):
say "Kotlin not compiled" in the report; don't claim a pass.

The first run downloads the Gradle plugins and Compose libraries it doesn't find in
~/.gradle (tens to a few hundred MB). Later runs reuse the cache and a warm project in
~/.cache/app-ui-slopless/kotlin-check. This checks your code against the libraries above,
not against the user's real dependencies: if their project has a Gradle build, compile
there instead.

Standard library only; works on Python 3.9.
"""
from __future__ import annotations

import argparse
import fcntl
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent / "kotlin-check"
WORK = Path.home() / ".cache" / "app-ui-slopless" / "kotlin-check"
GRADLE_VERSION = "8.14.5"
ANDROID_ONLY = re.compile(r"^\s*import\s+(android\.|androidx\.activity\.|androidx\.core\.|com\.google\.android\.|androidx\.compose\.ui\.text\.googlefonts\.|androidx\.compose\.ui\.platform\.LocalContext|androidx\.compose\.ui\.res\.)", re.M)
RES_IMPORT = re.compile(r"^\s*import\s+([\w.]+)\.generated\.resources\.", re.M)
RES_REF = re.compile(r"\bRes\.(font|drawable|string|plurals|array)\.(\w+)")
R_IMPORT = re.compile(r"^\s*import\s+([\w.]+)\.R\s*$", re.M)
R_REF = re.compile(r"(?<![\w.])R\.(font|drawable|string|color|dimen|array|raw)\.(\w+)")
ERROR = re.compile(r"^e: (?:file://)?(\S+?\.kt):(\d+):(\d+)\s+(.*)$")


def find_jdk() -> str | None:
    for env in ("JAVA_HOME",):
        home = os.environ.get(env)
        if home and (Path(home) / "bin" / "java").exists() and java_major(home) >= 17:
            return home
    if Path("/usr/libexec/java_home").exists():
        for v in ("17", "21", "25"):
            r = subprocess.run(["/usr/libexec/java_home", "-v", v], capture_output=True, text=True)
            if r.returncode == 0 and r.stdout.strip():
                return r.stdout.strip()
    return None


def java_major(home: str) -> int:
    r = subprocess.run([str(Path(home) / "bin" / "java"), "-version"], capture_output=True, text=True)
    m = re.search(r'version "(\d+)', r.stderr)
    return int(m.group(1)) if m else 0


def find_android_sdk() -> str | None:
    for env in ("ANDROID_HOME", "ANDROID_SDK_ROOT"):
        p = os.environ.get(env)
        if p and (Path(p) / "platforms").exists():
            return p
    p = Path.home() / "Library" / "Android" / "sdk"
    return str(p) if (p / "platforms").exists() else None


def ensure_project(jdk: str) -> bool:
    WORK.mkdir(parents=True, exist_ok=True)
    for f in TEMPLATE.iterdir():
        if f.is_file():
            shutil.copy(f, WORK / f.name)
    if (WORK / "gradlew").exists():
        return True
    gradle = shutil.which("gradle")
    cached = sorted((Path.home() / ".gradle" / "wrapper" / "dists").glob(f"gradle-{GRADLE_VERSION}-bin/*/gradle-{GRADLE_VERSION}/bin/gradle"))
    tool = str(cached[0]) if cached else gradle
    if not tool:
        return False
    r = subprocess.run([tool, "wrapper", "--gradle-version", GRADLE_VERSION, "-q"], cwd=WORK,
                       env={**os.environ, "JAVA_HOME": jdk}, capture_output=True, text=True)
    return r.returncode == 0 and (WORK / "gradlew").exists()


def place_sources(files: list[Path]) -> tuple[dict[str, Path], list[str], str | None, str | None]:
    # Fresh sources and outputs every time: stale build output once reported another file's errors.
    for d in (WORK / "src", WORK / "build", WORK / ".kotlin"):
        shutil.rmtree(d, ignore_errors=True)
    mapping, notes, res_pkg, namespace = {}, [], None, None
    refs: dict[str, set[str]] = {}
    android_refs: dict[str, set[str]] = {}
    fonts = []
    for f in files:
        text = f.read_text(errors="ignore")
        pkg = re.search(r"^\s*package\s+([\w.]+)", text, re.M)
        # Code under shared/ or commonMain/ is shared CMP code: it must compile without Android APIs.
        shared = any(part in ("shared", "commonMain") for part in f.resolve().parts)
        src_set = "androidMain" if ANDROID_ONLY.search(text) and not shared else "commonMain"
        dest = WORK / "src" / src_set / "kotlin" / Path(*(pkg.group(1).split(".") if pkg else [])) / f.name
        if dest.exists():
            dest = dest.with_name(f"{f.stem}_{len(mapping)}.kt")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(f, dest)
        mapping[str(dest.resolve())] = f
        if src_set == "androidMain":
            notes.append(f"{f.name}: imports Android APIs, compiled for Android only")
        m = RES_IMPORT.search(text)
        if m:
            res_pkg = res_pkg or m.group(1) + ".generated.resources"
        for kind, name in RES_REF.findall(text):
            refs.setdefault(kind, set()).add(name)
        r = R_IMPORT.search(text)
        if r or R_REF.search(text):
            namespace = namespace or (r.group(1) if r else (pkg.group(1) if pkg else None))
            for kind, name in R_REF.findall(text):
                android_refs.setdefault(kind, set()).add(name)
        fonts += [p for p in f.parent.rglob("*") if p.suffix.lower() in (".ttf", ".otf")]
    res = WORK / "src" / "commonMain" / "composeResources"
    if refs:
        sample_font = fonts[0].read_bytes() if fonts else b"\0"
        for name in sorted(refs.get("font", ())):
            (res / "font").mkdir(parents=True, exist_ok=True)
            (res / "font" / f"{name}.ttf").write_bytes(sample_font)
        for name in sorted(refs.get("drawable", ())):
            (res / "drawable").mkdir(parents=True, exist_ok=True)
            (res / "drawable" / f"{name}.xml").write_text(
                '<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="1dp" '
                'android:height="1dp" android:viewportWidth="1" android:viewportHeight="1">'
                '<path android:pathData="M0,0h1v1h-1z" android:fillColor="#000"/></vector>')
        strings = sorted(refs.get("string", ()))
        if strings:
            (res / "values").mkdir(parents=True, exist_ok=True)
            (res / "values" / "strings.xml").write_text(
                "<resources>\n" + "".join(f'  <string name="{n}">{n}</string>\n' for n in strings) + "</resources>\n")
        stubbed = ", ".join(f"{k} {len(v)}" for k, v in sorted(refs.items()))
        notes.append(f"Compose resources stubbed for the compile ({stubbed}); make sure the real files exist in composeResources/")
    if android_refs:
        ares = WORK / "src" / "androidMain" / "res"
        sample_font = fonts[0].read_bytes() if fonts else b"\0"
        for name in sorted(android_refs.get("font", ())):
            (ares / "font").mkdir(parents=True, exist_ok=True)
            (ares / "font" / f"{name}.ttf").write_bytes(sample_font)
        for name in sorted(android_refs.get("drawable", ())):
            (ares / "drawable").mkdir(parents=True, exist_ok=True)
            (ares / "drawable" / f"{name}.xml").write_text(
                '<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="1dp" '
                'android:height="1dp" android:viewportWidth="1" android:viewportHeight="1">'
                '<path android:pathData="M0,0h1v1h-1z" android:fillColor="#000"/></vector>')
        values = []
        values += [f'  <string name="{n}">{n}</string>' for n in sorted(android_refs.get("string", ()))]
        values += [f'  <color name="{n}">#000000</color>' for n in sorted(android_refs.get("color", ()))]
        values += [f'  <dimen name="{n}">1dp</dimen>' for n in sorted(android_refs.get("dimen", ()))]
        values += [f'  <array name="{n}"/>' for n in sorted(android_refs.get("array", ()))]
        if values:
            (ares / "values").mkdir(parents=True, exist_ok=True)
            (ares / "values" / "values.xml").write_text("<resources>\n" + "\n".join(values) + "\n</resources>\n")
        stubbed = ", ".join(f"{k} {len(v)}" for k, v in sorted(android_refs.items()))
        notes.append(f"Android R resources stubbed under namespace {namespace} ({stubbed}); make sure the real files exist in res/")
    return mapping, notes, res_pkg, namespace


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--no-android", action="store_true", help="JVM target only (no Android SDK needed)")
    ap.add_argument("--offline", action="store_true", help="never download; exit 3 if something isn't cached")
    args = ap.parse_args()

    files = []
    for p in map(Path, args.paths):
        if p.is_dir():
            files += sorted(f for f in p.rglob("*.kt") if "build" not in f.parts and ".gradle" not in f.parts)
        elif p.suffix == ".kt":
            files.append(p)
    if not files:
        print("compile_kotlin: no .kt files given")
        return 2

    # One compile at a time: concurrent runs would share (and wipe) the same project.
    WORK.mkdir(parents=True, exist_ok=True)
    lock = open(WORK.parent / "kotlin-check.lock", "w")
    fcntl.flock(lock, fcntl.LOCK_EX)

    jdk = find_jdk()
    if not jdk:
        print("compile_kotlin: not run, no JDK 17+ found (set JAVA_HOME)")
        return 3
    sdk = None if args.no_android else find_android_sdk()
    if not ensure_project(jdk):
        print("compile_kotlin: not run, no Gradle available to create the wrapper")
        return 3
    if sdk:
        (WORK / "local.properties").write_text(f"sdk.dir={sdk}\n")

    mapping, notes, res_pkg, namespace = place_sources(files)
    tasks = ["compileKotlinJvm"] + (["compileDebugKotlinAndroid"] if sdk else [])
    props = [f"-Pslopless.android={'true' if sdk else 'false'}"]
    if res_pkg:
        props.append(f"-Pslopless.resPackage={res_pkg}")
    if namespace and sdk:
        props.append(f"-Pslopless.namespace={namespace}")
    env = {**os.environ, "JAVA_HOME": jdk}

    def run(offline: bool) -> subprocess.CompletedProcess:
        cmd = ["./gradlew", *tasks, *props, "--continue", "--console=plain", "-q"] + (["--offline"] if offline else [])
        return subprocess.run(cmd, cwd=WORK, env=env, capture_output=True, text=True)

    proc = run(offline=True)
    missing = re.search(r"No cached version|Could not resolve|offline mode|was not found|not available offline", proc.stdout + proc.stderr)
    if proc.returncode != 0 and missing and not args.offline:
        print("compile_kotlin: downloading missing Gradle plugins / Compose libraries (first run only)...", flush=True)
        proc = run(offline=False)
    out = proc.stdout + proc.stderr
    if proc.returncode != 0 and re.search(r"No cached version|Could not resolve|Could not GET|Plugin \[id: .*\] was not found", out):
        print("compile_kotlin: not run, dependencies unavailable" + (" offline" if args.offline else ""))
        print("\n".join(l for l in out.splitlines() if "Could not" in l or "No cached" in l)[:800])
        return 3

    errors, seen = [], set()
    for line in out.splitlines():
        m = ERROR.match(line.strip())
        if not m:
            continue
        path, ln, col, msg = m.groups()
        orig = mapping.get(str(Path(path).resolve()), Path(path))
        key = (str(orig), ln, msg)
        if key in seen:  # the same error reported by both targets
            continue
        seen.add(key)
        errors.append(f"{orig}:{ln}:{col}: error: {msg}")
    for e in errors:
        print(e)
    for n in notes:
        print(f"note: {n}")
    if proc.returncode != 0 and not errors:
        print("\n".join(out.strip().splitlines()[-15:]))
    targets = "JVM + Android" if sdk else "JVM only"
    status = "pass" if proc.returncode == 0 else "FAIL"
    print(f"compile_kotlin {status}: {len(files)} file(s), {len(errors)} error(s), Kotlin 2.2.21 / Compose MP 1.9.0, {targets}")
    return 0 if proc.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

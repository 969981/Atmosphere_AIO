#!/usr/bin/env bash
set -euo pipefail

: "${GITHUB_WORKSPACE:?GITHUB_WORKSPACE is required}"
: "${AIO_PROJECT:?AIO_PROJECT is required}"
SOURCE_DIR="${GITHUB_WORKSPACE}/source"
DIST_DIR="${GITHUB_WORKSPACE}/dist"
mkdir -p "$DIST_DIR"
test -d "$SOURCE_DIR/.git" || { echo "Pinned upstream source is missing" >&2; exit 1; }

case "$AIO_PROJECT" in
  switchscript)
    cd "$SOURCE_DIR"
    bash ./switchScript.sh
    test -d SwitchSD
    zip -qr "$DIST_DIR/SwitchScript-SwitchSD.zip" SwitchSD
    ;;
  atmosphere-for-switch)
    cd "$SOURCE_DIR"
    for entry in \
      "switchScript.sh:SwitchSD:Full" \
      "switchScript_Pure.sh:AMS-Pure:Pure" \
      "switchScript_Tesla.sh:AMS-Tesla:Tesla" \
      "switchScript_Horizon-OC.sh:Horizon-OC:Horizon-OC"; do
      IFS=: read -r script output label <<< "$entry"
      echo "::group::Building gzk47 $label"
      sh "./.github/workflows/$script"
      test -d "$output" || { echo "Missing $output from $script" >&2; exit 1; }
      zip -qr "$DIST_DIR/Atmosphere-for-Switch-$label.zip" "$output"
      echo "::endgroup::"
    done
    ;;
  ascent)
    cd "$SOURCE_DIR"
    python -m pip install -r requirements.txt
    cd src
    python ./start.py -gt="${GITHUB_TOKEN:-}"
    shopt -s nullglob
    files=( ./*.zip )
    test "${#files[@]}" -gt 0 || { echo "Ascent produced no ZIP" >&2; exit 1; }
    cp -v -- "${files[@]}" "$DIST_DIR/"
    ;;
  vanillatmosphere)
    cd "$SOURCE_DIR"
    python -m pip install -r requirement.txt
    python ./vanillatmosphere.py
    test -d artifact
    test -n "$(find artifact -type f -print -quit)"
    ( cd artifact && zip -qr "$DIST_DIR/Vanillatmosphere-artifact.zip" . )
    ;;
  *)
    echo "Unknown AIO_PROJECT=$AIO_PROJECT" >&2
    exit 2
    ;;
esac

shopt -s nullglob
archives=( "$DIST_DIR"/*.zip )
test "${#archives[@]}" -gt 0 || { echo "Build produced no ZIP archives" >&2; exit 1; }
for archive in "${archives[@]}"; do
  unzip -tqq "$archive"
done
(
  cd "$DIST_DIR"
  sha256sum -- *.zip > SHA256SUMS
)
echo "Built ${#archives[@]} archive(s) for $AIO_PROJECT"

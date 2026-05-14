#!/usr/bin/env bash
set -euo pipefail

# ZopDev launch week · PNG capture from HTML sources (flat structure)
# Every HTML source and PNG output lives in the same root folder.

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT="$(cd "$(dirname "$0")" && pwd)"
VTB="--virtual-time-budget=4500"
COMMON=( --headless=new --disable-gpu --hide-scrollbars --no-sandbox --force-device-scale-factor=1 "$VTB" )

shot () {
  local size="$1" src="$2" dst="$3"
  echo "  → $(basename "$dst") ($size)"
  "$CHROME" "${COMMON[@]}" --window-size="$size" --screenshot="$dst" "file://$src" >/dev/null 2>&1
}

cd "$ROOT"

echo "== D1 reveal (1080x1350 carousel + 1080x1080 end-frame) =="
for f in d1_carousel_*.html; do shot "1080,1350" "$ROOT/$f" "$ROOT/${f%.html}.png"; done
shot "1080,1080" "$ROOT/d1_reveal_endframe_sq.html" "$ROOT/d1_reveal_endframe_sq.png"

echo "== D2 two sides (1080x1080 end-frame) =="
shot "1080,1080" "$ROOT/d2_twosides_endframe_sq.html" "$ROOT/d2_twosides_endframe_sq.png"

echo "== D4 product (1080x1080 end-card) =="
shot "1080,1080" "$ROOT/d4_product_endframe_sq.html" "$ROOT/d4_product_endframe_sq.png"

echo "== D5 craft (1080x1350 carousel) =="
for f in d5_carousel_*.html; do shot "1080,1350" "$ROOT/$f" "$ROOT/${f%.html}.png"; done

echo "== D6 proof (1080x1350 carousel) =="
for f in d6_carousel_*.html; do shot "1080,1350" "$ROOT/$f" "$ROOT/${f%.html}.png"; done

echo "== D7 close (1080x1080 still) =="
shot "1080,1080" "$ROOT/d7_close_still_sq.html" "$ROOT/d7_close_still_sq.png"

echo
echo "Done."

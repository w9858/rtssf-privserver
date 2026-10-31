#!/data/data/com.termux/files/usr/bin/sh
# Keeps existing checkouts, archives and saves intact. Run in Termux.
set -eu
pkg install -y python git
RTSSF_CHECKOUT="$HOME/rtssf-privserver-rebuild"
if [ -e "$RTSSF_CHECKOUT" ]; then
  echo "Already exists: $RTSSF_CHECKOUT. Use the README upgrade instructions."
  exit 1
fi
git clone --branch codex/server-rebuild https://github.com/w9858/rtssf-privserver.git "$RTSSF_CHECKOUT"
cd "$RTSSF_CHECKOUT"
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
if command -v termux-wake-lock >/dev/null 2>&1; then termux-wake-lock; fi
echo "Place your own assets under $RTSSF_CHECKOUT/img/{assets,sqlites,images}."
echo "Start: cd $RTSSF_CHECKOUT && .venv/bin/python app.py"
echo "Save: $RTSSF_CHECKOUT/instance/save.sqlite3"

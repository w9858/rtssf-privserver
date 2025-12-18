#!/data/data/com.termux/files/usr/bin/sh

echo " > : Please allow permissions when prompted"
echo " > : 권한 요청시 허용을 눌러주세요"
echo " > : 権限要求が表示されたら許可を押してください"

termux-setup-storage
sleep 30s

termux-wake-lock
sleep 10s

cd ~

yes | pkg upgrade
yes | pkg install python git unzip

python -m ensurepip
python -m pip install --user -U flask protobuf==3.20.3
grep -qE 'PATH=.*\.local/bin' ~/.bashrc 2>/dev/null || echo 'PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

[ -d rtssf-privserver ] && rm -rf rtssf-privserver
git clone https://github.com/w9858/rtssf-privserver.git || {
  echo " X : git clone failed"
  echo " X : git clone 실패"
  echo " X : git clone 失敗"
  exit 1
}
cd rtssf-privserver

for path in \
  "/storage/emulated/0/Download/img.zip" \
  "/storage/emulated/0/Download/MEGA Downloads/img.zip" \
  "/storage/emulated/0/img.zip"
do
  if [ -f "$path" ]; then
    unzip -o "$path" -d img
    rm "$path"
    found=1
    break
  fi
done

if [ -z "$found" ]; then
  echo " X : img.zip file not found in expected locations"
  echo " X : img.zip 정해진 위치에 파일이 없습니다"
  echo " X : img.zip ファイルが指定された場所にありません"
  echo " -------------------------------------------------"
  echo " X :  /storage/emulated/0/Download/img.zip"
  echo " X :  /storage/emulated/0/Download/MEGA Downloads/img.zip"
  echo " X :  /storage/emulated/0/img.zip"
  echo " X : Please place the img.zip file to one of these locations."
  echo " X : img.zip 파일을 다음 위치 중 하나에 넣어주세요."
  echo " X : img.zip ファイルを次の場所のいずれかに配置してください。"
  exit 1
fi

echo "alias spyce='termux-wake-lock && cd ~/rtssf-privserver && git pull && python app.py'" >> ~/.bashrc
source ~/.bashrc
python app.py

start_time=`date +%s`

# 一応ビルドファイルなどを消す
rm -rf ./build
rm -rf ./dist
rm -rf ./main.build
rm -rf ./main.dist
rm -rf ./main.onefile-build

rm -rf ./.venv

# 環境をインストール
poetry install --without dev

# ビルド
# pyinstallerはremoveしてあるので、pyinstallerを使いたかったら、addする
# poetry run pyinstaller ./src/main.py --clean --onefile 
poetry run nuitka --standalone --onefile ./src/main.py 

end_time=`date +%s`
time=$((end_time - start_time))

echo "Build success, Time taken to build: ${time}s"

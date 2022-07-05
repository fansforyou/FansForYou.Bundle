release:
	rm -rf dist
	mkdir dist
	mkdir dist/staging
	cp -r Contents dist/staging/Contents
	cp LICENSE dist/staging/LICENSE
	cp README.md dist/staging/README.md
	curl -L0 https://github.com/fansforyou/fan-gopher/releases/download/v1.0/fan-gopher-linuxx64-1.0 --output dist/staging/Contents/Code/fan-gopher-linuxx64-1.0
	curl -L0 https://github.com/fansforyou/fan-gopher/releases/download/v1.0/fan-gopher-macx64-1.0 --output dist/staging/Contents/Code/fan-gopher-macx64-1.0
	curl -L0 https://github.com/fansforyou/fan-gopher/releases/download/v1.0/fan-gopher-winx64-1.0.exe --output dist/staging/Contents/Code/fan-gopher-winx64-1.0.exe
	chmod -R 755 dist/staging
	(cd dist/staging && zip -r - .) > dist/FansForYou.bundle.zip

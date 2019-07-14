
all: install

install:
	mkdir -p ~/.local/share/gedit/plugins/gtagJump
	cp -r gtagJump ~/.local/share/gedit/plugins/gtagJump
	cp gtagJump.plugin ~/.local/share/gedit/plugins/gtagJump
	cp LICENSE.txt ~/.local/share/gedit/plugins/gtagJump
	
uninstall:
	rm -rf ~/.local/share/gedit/plugins/gtagJump

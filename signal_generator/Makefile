
TARGET = signal_generator
SRCS = signal_generator/main.py
OPT = --onefile
INSTALL_DIR = ./bin

.PHONY: all
all: 
	pyinstaller $(SRCS) $(OPT) --name $(TARGET)
	
.PHONY: clean
clean:
	rm -rf ./build ./dist ./*.spec

.PHONY: install
install:
	mkdir -p $(INSTALL_DIR)
	cp -a ./dist/* $(INSTALL_DIR)


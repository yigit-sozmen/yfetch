PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin
SHAREDIR ?= $(PREFIX)/share/yfetch

.PHONY: all run install uninstall help

all: help

run:
	python3 yfetch.py

install:
	@echo "Installing yfetch to $(DESTDIR)$(PREFIX)..."
	mkdir -p $(DESTDIR)$(SHAREDIR)
	mkdir -p $(DESTDIR)$(BINDIR)
	cp yfetch.py logos.py $(DESTDIR)$(SHAREDIR)/
	chmod +x $(DESTDIR)$(SHAREDIR)/yfetch.py
	printf '#!/bin/sh\nexec python3 %s "$$@"\n' "$(SHAREDIR)/yfetch.py" > $(DESTDIR)$(BINDIR)/yfetch
	chmod +x $(DESTDIR)$(BINDIR)/yfetch
	@echo "Installation complete. Run 'yfetch' in your terminal."

uninstall:
	@echo "Removing yfetch..."
	rm -rf $(DESTDIR)$(SHAREDIR)
	rm -f $(DESTDIR)$(BINDIR)/yfetch
	@echo "Uninstallation complete."

help:
	@echo "Usage:"
	@echo "  make run        Run yfetch locally"
	@echo "  sudo make install    Install yfetch globally"
	@echo "  sudo make uninstall  Remove yfetch from system"

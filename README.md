# yfetch

**yfetch** is a Linux CLI tool inspired by [Neofetch](https://github.com/dylanaraps/neofetch).

## Features

- CPU information
- GPU information
- Kernel information
- Operating system detection
- Package count
- Uptime
- Desktop environment / window manager detection
- OS-specific ASCII art


> **Note:** yfetch is currently in early development. System information support is expanding, and OS-specific ASCII art is currently available for a limited number of distributions.

## Currently Supported Operating Systems
**yfetch can run on most Linux distributions, but OS-specific ASCII art is currently available for:** 
 - Arch Linux
 - Gentoo
 - EndeavourOS

## Installation 

To simply install yfetch to your computer:

```
pip install psutil
git clone https://github.com/yigit-sozmen/yfetch
cd yfetch
sudo make install
```
## Usage

After installation, simply run:

```yfetch```

If you want to override your OS detection and output a different ASCII you can also run :

```yfetch -d gentoo```


## Roadmap

**yfetch is still in early development. Planned improvements include:**
 - More ASCII art
 - Better GPU detection
 - CLI options
 - Better hardware detection without external libraries
 - Config file
 - More DE/WM support

## Contributing 

Contributions and suggestions are always welcome in this project !

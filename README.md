# Tutorial: Shell scripting for Font Builds

[This repo is in support of a presentation for TypeLab 2021](https://2021.typographics.com/typelab#1188).

This repo includes a quick demo showing how shell scripts can help you make font build pipelines that are easy to set up, easy to extend, and stable over the long term. 

What are shell scripts, anyway? Anything you can run in the terminal (and this is more than you might think), you can write in a shell script to run again later. These scripts can sequence multiple command-line tools and Python scripts, name and organize files, and more. This allows you to set up some powerful but simple workflows – all without having to remember any special options in the terminal.

## Disclaimers

1. This tutorial is Mac-specific, and assumes you are on a recent version of macOS.
2. This is just a simplified look at one font building approach, mostly for .glyphs / .ufo font sources.
3. I’m still learning! It’s possible that in the future, I’ll shift to using all Python and/or Makefiles and/or something else. However, this is an way of building fonts that I find relatively approacheable for beginners, which allows quite a bit of control and is pretty scaleable.

## Build Instructions

The first time you build, you will need to clone this repo, set up a virtual environment, and install dependencies.

Note: when there are multiple lines of code, you can copy and paste all of them into a terminal, and run them all at once. They’ll all execute in sequence.

### Clone the repo

Open a fresh Terminal or Command Line window.

If you don’t already have it installed, you will need [woff2](https://github.com/google/woff2) to build web fonts.

Open a new, separate terminal window, and run the following lines (quoted from the [woff2 README](https://github.com/google/woff2/blob/a0d0ed7da27b708c0a4e96ad7a998bddc933c06e/README.md)):

```bash
git clone --recursive https://github.com/google/woff2.git
cd woff2
make clean all
```

### Clone the repo

Open a fresh Terminal or Command Line window. Then, navigate to a place you’d like to keep this project.

```bash
# use cd to "change directory," then provide a path to where you’d like this project to download
cd Desktop
# then clone the repo into a new folder, arrowtype-shell-tutorial
git clone https://github.com/arrowtype/typelab-2021.git arrowtype-shell-tutorial
# cd into that new folder
cd arrowtype-shell-tutorial
```

### Set up the environment

To build, set up the virtual environment. Run the following lines of code in y

```bash
python3 -m venv venv
```

Then activate it:

```bash
source venv/bin/activate
```

Then install requirements:

```bash
pip install -r requirements.txt
```

And finally, give the build scripts permission to run/execute:

```bash
chmod +x example-source/*.sh
```

### Build

With the environment set up, you can now run the build!

First, make sure you have activated the virtual environment. (If this doesn’t work, you probably haven’t set up the environment yet – see the advice above or [file an issue](https://github.com/arrowtype/typelab-2021/issues)):

```bash
source venv/bin/activate
```

#### Variable Font

You can run a shell script by simply entering the path to it in your command line, then running that.

To run the example variable font build, run this:

```bash
example-source/build.sh
```

#### Static Fonts

To run the example static font build, run this:

```bash
example-source/build-statics.sh
```

## Extend!

- To learn more about using Shell scripts, read [How to Create and Use Bash Scripts](https://www.taniarascia.com/how-to-create-and-use-bash-scripts/), by Tania Rascia.
- It is extremely useful to use virtual environments to avoid conflicts between different font projects. A technique I like for this is described in [A Guide to Python’s Virtual Environments](https://towardsdatascience.com/virtual-environments-104c62d48c54), by Matthew Sarmiento.
- To check out a much more complex font build, take a look at the full [Recursive](https://github.com/arrowtype/recursive) project. In particular, the [mastering](https://github.com/arrowtype/recursive/tree/728ced98fe7acc4756388fc937af43e61012d838/mastering) scripts, by Ben Kiel, show a way to run a font build that mixes AFDKO and FontMake, entirely in Python. Then, the [make-release](https://github.com/arrowtype/recursive/blob/728ced98fe7acc4756388fc937af43e61012d838/src/build-scripts/make-release/00-prep-release.sh) scripts, by me (Stephen Nixon) use a blend of Shell & Python scripts to package the built fonts in a specific way for GitHub releases. Most font builds don’t need to be this complex, but there are a lot of useful techniques employed in here.
- You can learn a lot by just starting to use tools for font builds. Check out [FontMake](https://github.com/googlefonts/fontmake), [FontBakery](https://github.com/googlefonts/fontbakery/), [woff2](https://github.com/google/woff2), [GF Tools](https://github.com/googlefonts/gftools), [FontTools](https://github.com/fonttools/fonttools), and [DrawBot](https://www.drawbot.com/).

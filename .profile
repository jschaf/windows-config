#!/bin/sh.exe

export ANACONDA_ENVS=~/Anaconda/envs
export PATH=/c/msys64/bin:$PATH
export PATH=/c/Program\ Files\ \(x86\)/mingw-builds/x32-4.8.1-posix-dwarf-rev5/mingw32/bin:$PATH
export PATH=$PATH:/c/Program\ Files\ \(x86\)/Rust/bin
export PATH=$PATH:~/Anaconda:~/Anaconda/Scripts:~/bin;

if [ -f ~/.git-completion.bash ]; then
  . ~/.config/.git-completion.bash
fi

if [ -f ${HOME}/.bashrc ]
then
  . ${HOME}/.bashrc
fi

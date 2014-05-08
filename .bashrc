function reload_bashrc {
    source ~/.bashrc
}

alias g=git

function color_my_prompt {
    local __user_and_host="\[\033[01;32m\]\u@\h"
    local __cur_location="\[\033[01;34m\]\w"
    local __git_branch_color="\[\033[31m\]"
    local __git_branch='`git branch 2> /dev/null | grep -e ^* | sed -E  s/^\\\\\*\ \(.+\)$/\ \(\\\\\1\)\ /`'
    local __conda_color="\[\033[31m\]"
    local __conda_env='`echo $CONDA_DEFAULT_ENV | sed "s/..*/ (&)/"`'
    local __prompt_tail="\[\033[35m\]\$"
    local __last_color="\[\033[00m\]"

    export PS1="\n$__user_and_host $__cur_location\
$__conda_color$__conda_env\
$__git_branch_color$__git_branch\n\
$__prompt_tail$__last_color "
}
color_my_prompt

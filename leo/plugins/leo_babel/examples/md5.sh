#@+leo-ver=cub-1-thin
#@0 [bob.20170830131933.1] @f md5.sh
#@@language shell

for fpn in "$@" ; do
    md5sum $fpn
done
#@-leo

#!/bin/bash
#
# nf_crawler.sh
#
MY_HOME=$(cd $(dirname $0)/.. && pwd)
ENV_FILE=$MY_HOME/.news_finder.rc

if [ -f "$ENV_FILE" ] ; then
    . $ENV_FILE
fi

for target in $(ls $MY_HOME/repos/) ; do
    echo "==${target}=="
    python $MY_HOME/news-finder.py -c $MY_HOME/repos/${target}/news_finder.ini
done

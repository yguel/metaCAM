for i in $(ls ) ; do echo $(echo $i| rev |cut -d. -f2- |rev) $(cat $i | cut -c1) >> all.txt ";"; done

export PACKAGE=scurvy
export VERSION=0.0.1
cd /home/venturini/git/bcdetect/workspace/
rm -rf *
cd /home/venturini/git/bcdetect/
python3 BCDetect.py $PACKAGE --no-del --j-check-p --only $VERSION
cd workspace/$PACKAGE/
npm i
npm test
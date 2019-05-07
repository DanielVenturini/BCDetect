export PACKAGE=react-components
export VERSION=0.0.2
export BCDETECT=git/bcdetect
cd $HOME/$BCDETECT/workspace/ && rm -rf *
cd $HOME/$BCDETECT/
python3 BCDetect.py $PACKAGE --no-del --j-check-p --only $VERSION
cd workspace/$PACKAGE/
npm i && npm test
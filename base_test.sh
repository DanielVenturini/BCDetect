export PACKAGE=react-components
export VERSION=0.0.2
export BCDETECT=git/bcdetect
export MESSAGE='\n========================\n= TEST WILL BE STARTED =\n========================\n'
cd $HOME/$BCDETECT/workspace/ && rm -rf *
cd $HOME/$BCDETECT/
python3 BCDetect.py $PACKAGE --no-del --j-check-p --only $VERSION
cd workspace/$PACKAGE/
npm i && echo -e $MESSAGE  && npm test

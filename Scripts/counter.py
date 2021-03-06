import csv
import json

# data to graph scatter-effects
def getPackage(packageName, current=False):
    if current:
        return requests.get('https://registry.npmjs.org/'+packageName).json()
    try:
        package = json.load(open('../CSV/packagejson/npm_packs_2017-06-01/{0}.json'.format(packageName)))
        setLatest(package)
        return package
    except FileNotFoundError:
        return {'error': "Not found"}

def setLatest(package):
    try:
        versions = list(package['versions'].keys())
        versions.sort()
        latest = package['dist-tags']['latest']
        for version in versions:
            specifyPackage = package['versions'][version]
            if specifyPackage['version'].__eq__(latest):
                package['latest'] = specifyPackage
                return
        package['latest'] = package['versions'][versions[-1]]
    except:
        versoes = list(package['versions'].keys())
        package['latest'] = package['versions'][versoes[-1]]

def getGenericDependencies(package, depType):
	try:
		return len(list(package['latest'][depType].keys()))
	except:
		return 0

def getDependencias(package):
	return \
		getGenericDependencies(package, 'dependencies') + \
		getGenericDependencies(package, 'devDependencies') + \
		getGenericDependencies(package, 'peerDependencies') + \
		getGenericDependencies(package, 'optionalDependencies')

def releases_CSV(file):
	file = file.replace('./results', '')
	previous = ''
	count = 0
	csv_r = csv.reader(open('../CSV/{}'.format(file.replace('./', '').replace('_results.csv', '.csv'))))
	csv_r.__next__()

	try:
		while True:
			version = csv_r.__next__()[1]
			if not previous.__eq__(version):
				count += 1
				previous = version
	except Exception as ex:
		return count

def releases_json(file):
	file = file.replace('./results', '')
	return len(json.load(open('../CSV/packagejson/npm_packs_2017-06-01/{}.json'.format(file.replace('./', '').replace('_results.csv', '.json'))))['versions'])

def releases(file):
	count = 0
	csv_r = csv.reader(open(file), delimiter=',', quotechar='\n')
	csv_r.__next__()    # ignorando a primeira linha

	try:
		while True:
			csv_r.__next__()
			count += 1
	except Exception as ex:
		return count

def broke_packages(file):
	count = 0
	csv_r = csv.reader(open(file), delimiter=',', quotechar='\n')
	csv_r.__next__()    # ignorando a primeira linha

	try:
		while True:
			chng, scpt, ist, tst = csv_r.__next__()[1:5]
			if chng.__eq__('YES') and scpt.__eq__('OK') and (tst.__eq__('ERR') or ist.__eq__('ERR')):
				return 1
	except Exception as ex:
		return 0

def broke_releases(file):
	count = 0
	csv_r = csv.reader(open(file), delimiter=',', quotechar='\n')
	csv_r.__next__()    # ignorando a primeira linha

	try:
		while True:
			chng, scpt, ist, tst = csv_r.__next__()[1:5]
			if chng.__eq__('YES') and scpt.__eq__('OK') and (tst.__eq__('ERR') or ist.__eq__('ERR')):
				count += 1
	except Exception as ex:
		return count

def executed(file):
	count = 0
	csv_r = csv.reader(open(file), delimiter=',', quotechar='\n')
	csv_r.__next__()    # ignorando a primeira linha

	try:
		while True:
			chng, tst = csv_r.__next__()[1:3]
			if chng.__eq__('YES') and tst.__eq__('OK'):
				count += 1
	except:
		return count

def non_executed(file):
	count = 0
	csv_r = csv.reader(open(file), delimiter=',', quotechar='\n')
	csv_r.__next__()    # ignorando a primeira linha

	try:
		while True:
			chng, tst = csv_r.__next__()[1:3]
			if chng.__eq__('NO') or tst.__eq__('ERR'):
				count += 1
	except:
		return count

files          = ['metalsmith-json-to-files--katemihalikova','http-browserify-alexjeffburke','tokend','treeeater-dustyburwell','staticerrs','vdom-render-pull-stream','react-starter-es6','ga-collect','map-indexed-xf','fh-rest-mysql-adapter','gulp-highwinds','mongotape','pre-rating','redux-devtools-log-monitor-ie8','flat-rocks','madstreetden','immutable-json-schema','node-qrious','karma-coverage-es6','mongo-iterable-cursor','decorator-helpers','raster-tile-query','node-spa-auth','hsluv-stylus','base-2048','lpi-stripe','joii-unit','giffy-break-cli','dsl-helper','loner','generator-awesomeo','currency-object','id-fsm','babel-plugin-test-unroll','parse-server-yutin','hambruger','node-inspector-osi-licensed','oauth2orize-redelegate','metalsmith-template-data','jstransformer-csso','canduitz','http-proxy-no-line-184-error','ldep','oppressor-contrib','eslint-config-bem-sdk','slush-react-materialui','gulp-ngtemplate2','pit-ro','grunt-inline-imgsize','microservice','traceur-annotations','co-gather','ember-cli-media-queries','promise-to-stream-either','phoenix-cypto','svg-sprite_l','anonymize','organic-plasma-usersessions','dbm','bitbucket-downloads-client','deal-validator','xbee-stream','sparkbar','hapi-mongoose-plugin','retrial','js-package-sample','supports-semigraphics','generator-pistacheo','rework-imagesize','vshushkov-react-datetime','get-urls-cli','buffer-includes','regular-format','sorcerer','invoke-after','domly-liftoff','stringify-github-anchor','generator-bayse','deps-topo-sort','css-modules-example','saucier','producthunt','dfrl','worddump','fantasy-environment','jsonreduce','compute-dims','angular2-webpack-starter','think-compress-html','markdown-it-react-renderer','ttl-queue','ngx-delete-confirm','ember-cli-footnotes','slacktalk','balanced-addon-models','node-committer','socks5-server','auth0-react-native','gulp-jira-todo','string-pred','meshblu-core-task-get-broadcast-subscription-types','gyazo-upload','rollup-plugin-prettier','strider-docker-build','ioredis-mock-lpl','latest-versions','metainfo','hier','lyef-react-component','postcss-clean','util-plus','grunt-webp-modify','tapas-ui','generator-maria','q-loop','bestjavascriptlibrary','my-kenya-pkg','parse-dburi','anova','logstorage','generator-bower-package','lackey-mongoose-utils','reglite','operator-assertion','pa1d','pokenode','html-scrapper','set-object','rc-minidialog','npm-dep-chain','generator-redux-feature','victory-component-boilerplate','plotlyjs-finance','streamme','pakr','first-line','babel-plugin-class-autobind','ix-level-userdb','feathers-sync','postcss-maze','auth-driver-utils','rocksdown','proxy-generics-google-maps','nextprot','to-vfile','leap-seconds-list-creator','generator-nodejs-module','spa-plugin-gettext','linux-wifi','gulp-eol','style-script','babel-plugin-elm','flux-utils','osia-babel','ee-bump','read-file-relative','stylus-vertical-grid','reduce-generator','tiny-orm','grunt-qunit-istanbul-plus','eslint-config-mnubo','site-crawler','postcss-clean-prefixes','legal-ass','get-last-value','ck2parser','mocha-mix-jsdom','nunit-command','current','reem','karma-ng-template-preprocessor','node-priority','eldarion-ajax','grunt-tex-hunspell','babel-package-import','docpad-plugin-markdowntoc','hatch-loopback-testing','grunt-qunitnode','pandom','ndarray-stencil','github-following','initgraph','koara-xml','expiry-model','multiform-build','async-data','express-auto-controller','localforage-setitems','vigour-jsdoc2md','grunt-phonegap-build-tom','httperror','grunt-akamai-ccu-purge','insert-space','deskbookers-react-intl','snap-points-2d','simply-build','virtual-scroll','keydir','grunt-speedgun','framing','shaman','postcss-margin-helpers','nosql-memdb','google-drive-blobs','jopier-rest','lirc_web','obd2','generator-imstar-component','safe-wipe','nunjucks-filter-loader','plover-assets-util','generator-kiwiplugin','is-pointer-inside','vetus','eslint-config-tipsi','react-steack','derby-lang-fs','nps-collect','images-to-less-variables','report-builder','input-plugin-datetime','command-palette','ftp-reap','react-redux-provide-theme','generator-npm-pasta','execution-pool','xo-server-auth-saml','react-data-grid-extensions','passport-reddit-token','childminder','elev-varsel-generate-document-title','j2-grunt-jsdoc','node-configs','seed-width-max','sat-api-lib','apeman-scrt','letsago','sails-hook-seed','has-task-runner','validate-arguments','grunt-vanilli','wpxml2md','git-source','version-require','line-circle-collision','everybody-needs-a-404','grunt-socko','chai-jasmine','react-themed','yala','express-extras','domo-kun','reql-cli','machinepack-passwords','bumpery','ip-cidr','aliexpress','node-html-light','ami-motley-tool','reflecta','easygettext','microm','env-cmd','dev-time-cli','giantbomb','grunt-consolidate-css','gulp-email-builder','axiba-dependencies','abacus-eureka-plugin','s3-revisions','redux-roller','commandments','searchtracks','express-integrator-extension','errorable-common','typeset','webpack-cleanup-plugin','meshblu-core-task-reset-token','postcss-inrule','indeed-api-client','ankara-coverage','alinex-async','socrates','lincell','generator-validate-io','selenium-screen-master','objectbox','microservice-crutch','hemsl','botmaster-fulfill-actions','angular-stormpath','octopie','nvm-test','koa-jsonwebtoken','dynamic-extras','react-components','json-bigint','goog-class-to-es6','scurvy','eslint-config-auth0-base','diable','angular2-jsonapi','iotdb-transport-redis','should-enzyme','trailpack-mongoose','light-swift','primer-forms','honeybadger','co-suspend','koa-socket','o-','ember-cli-chartjs','bilanx','gendiff-lvl2-s18-ai','nanocomponent','apeman-bud','ploverx','rs-api','azure-mgmt-compute','ember-cli-deploy-cloudfront','lodash-match-pattern','file-prompt','express-minify','contentful-import','synopsis-client','pure-graph','react-vui-alerts','postcss-short','react-player-controls','grunt-gitbook','react-css-transition','docpad-plugin-services','backbone-mongo','core-tools','uninspected','grunt-prettify','vquery','generator-tiny-es-nm','random-access-file','graphql-language-service','hadron-type-checker','guy-test','ember-suave','comake-services','react-islands','polyclay','node-json-db','full-meta-jacket','qewd-ripple','typeodm','open-graph-scraper','fast-stream','legiond','angular2-dependencies-graph','nexmo-cli','hoost','tilestrata','msg-js-spa-framework','jeggy-mongoose','scrape-twitter','paypal-rest-sdk','cruk-searchkit','generator-meteor','godot','ember-cli-template-lint','kelper','iotdb-transport','linvodb3','sidekick','ubk','quark-gui','inliner','stylestats','most','jorm','restful-goose','next-update','react-rxd','riot','ut-test','apipublisher','testcafe','heroku-cli-util','assetgraph-builder']
# broked packages/releases caused by parser
packages_error_unresolved = 22
releases_error_unresolved = 101 + (4 + 3 + 2 + 6 + 1 + 7 + 14 + 1 + 1 + 1 + 8 + 10)
# false-positive packages/releases
# issues with mongo, mysql, libs, ... executed and runned with success
packages_false_positive = 38
releases_false_positive = 172 + (1 + 1 + 1 + 1 + 2 + 1 + 2 + 1 + 1 + 1 + 6 + 18 + 9 + 9 + 1 + 26 + 17 + 2 + 1 + 28 + 10 + 1 + 55 + 39 + 4 + 6)
# non-break change packages/releases
# node version, external api, provider/release removed, major version
non_bc_packages = 14 + 1
non_bc_releases = 53 + (1 + 2 + 2 + 2 + 1 + 1 + 1 + 1 + 1 + 6 + 4 + 2 + 6 + 11 + 1 + 1 + 3 + 1 + 10 + 11 + 2 + 2 + 43 + 12 + 8 + 5 + 3 + 1 + 7 + 3 + 6 + 2)
# with no test
no_test = 5 + 4 + 1 + 12 + 20 + 1

all_releases   = 0
all_packages   = len(files)
count_executed = 0
count_non_executed   = 0
count_broke_releases = 0
count_broke_packages = 0

for file in files:
	try:
		file = '../results/{}_results.csv'.format(file)
		all_releases   += releases_CSV(file)
		count_executed += executed(file)
		count_non_executed      += non_executed(file)
		count_broke_releases    += broke_releases(file)
		count_broke_packages    += broke_packages(file)
	except FileNotFoundError as fnfe:
		print(fnfe)
	except Exception as ex:
		print(file + ': ' + str(ex))

# adjust these values to un-script errors
count_executed     -= no_test
count_non_executed += no_test

# adjust these values to unresolved errors
count_broke_packages -= packages_error_unresolved
count_broke_releases -= releases_error_unresolved

# adjust these values to false-positives errors
count_broke_releases -= releases_false_positive
count_broke_packages -= packages_false_positive

# adjust these values to non-breaking change
#count_broke_packages -= non_bc_packages
#count_broke_releases -= non_bc_releases

print('              | Packages | Releases |')
print(' Size         |  {0}     |   {1}   |'.format(all_packages, all_releases))
print(' Executed     |  {0}     |   {1}   |'.format(all_packages, count_executed))
print(' Non Executed |  {0}       |   {1}   |'.format(0, count_non_executed))
print(' Success      |  {0}     |    {1}  |'.format(all_packages-count_broke_packages, count_executed-count_broke_releases))
print(' Error        |  {0}     |   {1}   |'.format(count_broke_packages, count_broke_releases))
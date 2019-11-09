import csv
import json

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
	return len(json.load(open('../CSV/packagejson/npm_packs_2017-06-01/{}'.format(file.replace('./', '').replace('_results.csv', '.json'))))['versions'])

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
			scpt, ist, tst = csv_r.__next__()[2:5]
			if scpt.__eq__('OK') and tst.__eq__('ERR'):
				return 1
	except Exception as ex:
		return 0

def broke_releases(file):
	count = 0
	csv_r = csv.reader(open(file), delimiter=',', quotechar='\n')
	csv_r.__next__()    # ignorando a primeira linha

	try:
		while True:
			scpt, ist, tst = csv_r.__next__()[2:5]
			if scpt.__eq__('OK') and tst.__eq__('ERR'):
				count += 1
	except Exception as ex:
		return count

def executed(file):
	count = 0
	csv_r = csv.reader(open(file), delimiter=',', quotechar='\n')
	csv_r.__next__()    # ignorando a primeira linha

	try:
		while True:
			tst = csv_r.__next__()[2]
			if tst.__eq__('OK'):
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

files          = ['metalsmith-json-to-files--katemihalikova','http-browserify-alexjeffburke','tokend','treeeater-dustyburwell','staticerrs','vdom-render-pull-stream','react-starter-es6','ga-collect','map-indexed-xf','fh-rest-mysql-adapter','gulp-highwinds','mongotape','pre-rating','redux-devtools-log-monitor-ie8','flat-rocks','madstreetden','immutable-json-schema','node-qrious','karma-coverage-es6','mongo-iterable-cursor','decorator-helpers','raster-tile-query','node-spa-auth','hsluv-stylus','base-2048','lpi-stripe','joii-unit','giffy-break-cli','dsl-helper','loner','generator-awesomeo','currency-object','id-fsm','babel-plugin-test-unroll','parse-server-yutin','hambruger','node-inspector-osi-licensed','oauth2orize-redelegate','metalsmith-template-data','jstransformer-csso','canduitz','http-proxy-no-line-184-error','ldep','oppressor-contrib','eslint-config-bem-sdk','slush-react-materialui','gulp-ngtemplate2','pit-ro','grunt-inline-imgsize','microservice','traceur-annotations','co-gather','ember-cli-media-queries','promise-to-stream-either','js-package-sample','supports-semigraphics','generator-pistacheo','rework-imagesize','vshushkov-react-datetime','get-urls-cli','buffer-includes','regular-format','sorcerer','invoke-after','domly-liftoff','stringify-github-anchor','generator-bayse','deps-topo-sort','css-modules-example','saucier','producthunt','dfrl','worddump','fantasy-environment','jsonreduce','compute-dims','angular2-webpack-starter','think-compress-html','markdown-it-react-renderer','ttl-queue','ngx-delete-confirm','ember-cli-footnotes','slacktalk','balanced-addon-models','node-committer','socks5-server','auth0-react-native','gulp-jira-todo','string-pred','meshblu-core-task-get-broadcast-subscription-types','gyazo-upload','rollup-plugin-prettier','strider-docker-build','ioredis-mock-lpl','latest-versions','metainfo','hier','lyef-react-component','postcss-clean','util-plus','grunt-webp-modify','tapas-ui','generator-maria','q-loop','bestjavascriptlibrary','my-kenya-pkg','parse-dburi','gitgud','logstorage','generator-bower-package','lackey-mongoose-utils','reglite','operator-assertion','pa1d','pokenode','html-scrapper','set-object','rc-minidialog','npm-dep-chain','generator-redux-feature','victory-component-boilerplate','plotlyjs-finance','streamme','pakr','first-line','babel-plugin-class-autobind','ix-level-userdb','feathers-sync','postcss-maze','to-vfile','leap-seconds-list-creator','generator-nodejs-module','spa-plugin-gettext','linux-wifi','gulp-eol','style-script','babel-plugin-elm','flux-utils','osia-babel','ee-bump','read-file-relative','stylus-vertical-grid','reduce-generator','tiny-orm','grunt-qunit-istanbul-plus','eslint-config-mnubo','site-crawler','postcss-clean-prefixes','legal-ass','get-last-value','ck2parser','mocha-mix-jsdom','nunit-command','current','reem','karma-ng-template-preprocessor','node-priority','eldarion-ajax','grunt-tex-hunspell','babel-package-import','docpad-plugin-markdowntoc','hatch-loopback-testing','grunt-qunitnode','pandom','ndarray-stencil','github-following','initgraph','koara-xml','expiry-model','multiform-build','async-data','express-auto-controller','localforage-setitems','vigour-jsdoc2md','grunt-phonegap-build-tom','httperror','grunt-akamai-ccu-purge','insert-space','grunt-speedgun','framing','shaman','postcss-margin-helpers','nosql-memdb','google-drive-blobs','jopier-rest','lirc_web','obd2','generator-imstar-component','safe-wipe','nunjucks-filter-loader','plover-assets-util','generator-kiwiplugin','is-pointer-inside','vetus','eslint-config-tipsi','react-steack','derby-lang-fs','nps-collect','images-to-less-variables','report-builder','input-plugin-datetime','command-palette','ftp-reap','react-redux-provide-theme','generator-npm-pasta','execution-pool','xo-server-auth-saml','react-data-grid-extensions','passport-reddit-token','childminder','elev-varsel-generate-document-title','j2-grunt-jsdoc','node-configs','seed-width-max','sat-api-lib','apeman-scrt','validate-arguments','grunt-vanilli','wpxml2md','git-source','version-require','line-circle-collision','everybody-needs-a-404','grunt-socko','chai-jasmine','react-themed','yala','express-extras','domo-kun','reql-cli','machinepack-passwords','bumpery','ip-cidr','aliexpress','node-html-light','ami-motley-tool','reflecta','easygettext','microm','env-cmd','dev-time-cli','giantbomb','grunt-consolidate-css','gulp-email-builder','axiba-dependencies','abacus-eureka-plugin','s3-revisions','redux-roller','commandments','searchtracks','express-integrator-extension','errorable-common','typeset','webpack-cleanup-plugin','meshblu-core-task-reset-token','ankara-coverage','alinex-async','socrates','generator-validate-io','selenium-screen-master','objectbox','microservice-crutch','hemsl','botmaster-fulfill-actions','angular-stormpath','octopie','nvm-test','koa-jsonwebtoken','dynamic-extras','react-components','json-bigint','goog-class-to-es6','scurvy','eslint-config-auth0-base','diable','angular2-jsonapi','iotdb-transport-redis','should-enzyme','trailpack-mongoose','co-suspend','koa-socket','o-','ember-cli-chartjs','bilanx','gendiff-lvl2-s18-ai','nanocomponent','apeman-bud','ploverx','rs-api','azure-mgmt-compute','ember-cli-deploy-cloudfront','lodash-match-pattern','file-prompt','express-minify','contentful-import','synopsis-client','pure-graph','react-vui-alerts','postcss-short','react-player-controls','grunt-gitbook','react-css-transition','docpad-plugin-services','backbone-mongo','core-tools','uninspected','grunt-prettify','vquery','random-access-file','graphql-language-service','hadron-type-checker','guy-test','ember-suave','comake-services','react-islands','polyclay','node-json-db','full-meta-jacket','qewd-ripple','typeodm','open-graph-scraper','fast-stream','legiond','angular2-dependencies-graph','nexmo-cli','hoost','tilestrata','msg-js-spa-framework','jeggy-mongoose','scrape-twitter','paypal-rest-sdk','cruk-searchkit','generator-meteor','godot','ember-cli-template-lint','kelper','iotdb-transport','linvodb3','sidekick','ubk','inliner','stylestats','most','jorm','restful-goose','next-update','react-rxd','riot','ut-test','apipublisher','testcafe','assetgraph-builder','phoenix-cypto','svg-sprite_l','xbee-stream','sparkbar','retrial','nextprot','deskbookers-react-intl','snap-points-2d','simply-build','virtual-scroll','keydir','sails-hook-seed','postcss-inrule','indeed-api-client','light-swift','primer-forms','organic-plasma-usersessions','bitbucket-downloads-client','deal-validator','auth-driver-utils','letsago','dbm','generator-tiny-es-nm','has-task-runner','anonymize','heroku-cli-util','rocksdown','proxy-generics-google-maps','honeybadger']#'lincell','quark-gui','hapi-mongoose-plugin']
# broked packages/releases caused by parser
packages_error_unresolved = 22
releases_error_unresolved = 0


all_releases   = 0
all_packages   = 3 + len(files)
count_executed = 2 + 55 + 11
count_non_executed   = 1
count_broke_releases = 0
count_broke_packages = 1

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

# adjust these values
count_broke_packages -= packages_error_unresolved
count_broke_releases -= releases_error_unresolved

print('              | Packages | Releases |')
print(' Size         |  {0}     |   {1}   |'.format(all_packages, all_releases))
print(' Executed     |  {0}     |   {1}   |'.format(all_packages, count_executed))
print(' Non Executed |  {0}       |   {1}   |'.format(0, count_non_executed))
print(' Success      |  {0}     |    {1}   |'.format(all_packages-count_broke_packages, count_executed-count_broke_releases))
print(' Error        |  {0}     |   {1}   |'.format(count_broke_packages, count_broke_releases))

'''
for file in files:
	try:
		file = './{}_results.csv'.format(file)
		if releases(file) != releases_CSV(file):
			print(file + ' -> csv: {} CSV: {}'.format(releases(file), releases_CSV(file)))
	except FileNotFoundError as fnfe:
		print(str(fnfe))
	except Exception as ex:
		print(file + ': ' + str(ex))
'''
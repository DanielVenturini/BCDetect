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

def executed(file):
    count = 0
    file  = '../results/{}_results.csv'.format(file)
    csv_r = csv.reader(open(file), delimiter=',', quotechar='\n')
    csv_r.__next__()    # ignorando a primeira linha

    try:
        while True:
            tst = csv_r.__next__()[2]
            if tst.__eq__('OK'):
                count += 1
    except:
        if not count:
            print(file)
        return count

# ============================================================= #
# non-bc
#packages  = ['metalsmith-json-to-files--katemihalikova','http-browserify-alexjeffburke','tokend','treeeater-dustyburwell','staticerrs','vdom-render-pull-stream','ga-collect','map-indexed-xf','fh-rest-mysql-adapter','gulp-highwinds','mongotape','pre-rating','redux-devtools-log-monitor-ie8','flat-rocks','madstreetden','immutable-json-schema','node-qrious','karma-coverage-es6','mongo-iterable-cursor','decorator-helpers','raster-tile-query','node-spa-auth','hsluv-stylus','base-2048','lpi-stripe','joii-unit','giffy-break-cli','dsl-helper','loner','generator-awesomeo','currency-object','id-fsm','babel-plugin-test-unroll','parse-server-yutin','hambruger','node-inspector-osi-licensed','oauth2orize-redelegate','jstransformer-csso','canduitz','http-proxy-no-line-184-error','ldep','oppressor-contrib','eslint-config-bem-sdk','slush-react-materialui','gulp-ngtemplate2','pit-ro','grunt-inline-imgsize','microservice','traceur-annotations','co-gather','ember-cli-media-queries','promise-to-stream-either','js-package-sample','supports-semigraphics','generator-pistacheo','rework-imagesize','vshushkov-react-datetime','get-urls-cli','buffer-includes','regular-format','sorcerer','invoke-after','domly-liftoff','stringify-github-anchor','generator-bayse','deps-topo-sort','css-modules-example','saucier','producthunt','dfrl','worddump','fantasy-environment','jsonreduce','compute-dims','angular2-webpack-starter','think-compress-html','markdown-it-react-renderer','ttl-queue','ngx-delete-confirm','ember-cli-footnotes','slacktalk','balanced-addon-models','node-committer','socks5-server','auth0-react-native','gulp-jira-todo','string-pred','meshblu-core-task-get-broadcast-subscription-types','gyazo-upload','rollup-plugin-prettier','strider-docker-build','ioredis-mock-lpl','latest-versions','metainfo','hier','lyef-react-component','util-plus','grunt-webp-modify','generator-maria','q-loop','bestjavascriptlibrary','my-kenya-pkg','parse-dburi','anova','logstorage','generator-bower-package','lackey-mongoose-utils','reglite','operator-assertion','pa1d','pokenode','html-scrapper','set-object','rc-minidialog','npm-dep-chain','generator-redux-feature','victory-component-boilerplate','plotlyjs-finance','streamme','pakr','first-line','babel-plugin-class-autobind','ix-level-userdb','feathers-sync','postcss-maze','leap-seconds-list-creator','generator-nodejs-module','spa-plugin-gettext','linux-wifi','gulp-eol','style-script','babel-plugin-elm','flux-utils','osia-babel','ee-bump','read-file-relative','stylus-vertical-grid','reduce-generator','tiny-orm','grunt-qunit-istanbul-plus','eslint-config-mnubo','site-crawler','postcss-clean-prefixes','legal-ass','get-last-value','ck2parser','mocha-mix-jsdom','nunit-command','current','karma-ng-template-preprocessor','node-priority','eldarion-ajax','grunt-tex-hunspell','babel-package-import','hatch-loopback-testing','grunt-qunitnode','pandom','ndarray-stencil','github-following','initgraph','koara-xml','expiry-model','multiform-build','async-data','express-auto-controller','vigour-jsdoc2md','httperror','grunt-akamai-ccu-purge','insert-space','grunt-speedgun','framing','shaman','postcss-margin-helpers','google-drive-blobs','jopier-rest','lirc_web','obd2','generator-imstar-component','nunjucks-filter-loader','plover-assets-util','generator-kiwiplugin','is-pointer-inside','vetus','react-steack','derby-lang-fs','nps-collect','report-builder','input-plugin-datetime','command-palette','ftp-reap','generator-npm-pasta','execution-pool','react-data-grid-extensions','passport-reddit-token','childminder','elev-varsel-generate-document-title','j2-grunt-jsdoc','node-configs','seed-width-max','sat-api-lib','apeman-scrt','validate-arguments','grunt-vanilli','wpxml2md','git-source','version-require','line-circle-collision','everybody-needs-a-404','grunt-socko','chai-jasmine','yala','express-extras','domo-kun','reql-cli','bumpery','ip-cidr','aliexpress','node-html-light','ami-motley-tool','reflecta','easygettext','microm','env-cmd','dev-time-cli','giantbomb','grunt-consolidate-css','gulp-email-builder','axiba-dependencies','abacus-eureka-plugin','s3-revisions','redux-roller','searchtracks','express-integrator-extension','errorable-common','typeset','webpack-cleanup-plugin','ankara-coverage','alinex-async','socrates','lincell','generator-validate-io','selenium-screen-master','objectbox','microservice-crutch','hemsl','botmaster-fulfill-actions','angular-stormpath','octopie','nvm-test','koa-jsonwebtoken','dynamic-extras','json-bigint','goog-class-to-es6','scurvy','eslint-config-auth0-base','diable','iotdb-transport-redis','should-enzyme','trailpack-mongoose','co-suspend','koa-socket','o-','bilanx','gendiff-lvl2-s18-ai','nanocomponent','apeman-bud','ploverx','rs-api','azure-mgmt-compute','ember-cli-deploy-cloudfront','lodash-match-pattern','file-prompt','express-minify','contentful-import','synopsis-client','pure-graph','postcss-short','react-player-controls','grunt-gitbook','react-css-transition','core-tools','uninspected','grunt-prettify','random-access-file','graphql-language-service','hadron-type-checker','guy-test','ember-suave','comake-services','react-islands','node-json-db','full-meta-jacket','qewd-ripple','typeodm','open-graph-scraper','fast-stream','legiond','angular2-dependencies-graph','nexmo-cli','hoost','tilestrata','msg-js-spa-framework','scrape-twitter','paypal-rest-sdk','cruk-searchkit','generator-meteor','kelper','iotdb-transport','linvodb3','sidekick','ubk','quark-gui','inliner','stylestats','most','jorm','restful-goose','ut-test','phoenix-cypto','svg-sprite_l','xbee-stream','sparkbar','retrial','nextprot','deskbookers-react-intl','snap-points-2d','simply-build','virtual-scroll','keydir','sails-hook-seed','postcss-inrule','indeed-api-client','organic-plasma-usersessions','bitbucket-downloads-client','deal-validator','auth-driver-utils','hapi-mongoose-plugin','letsago','dbm','has-task-runner','anonymize','rocksdown','proxy-generics-google-maps','honeybadger']
# bc
#packages  = ['assetgraph-builder','testcafe','apipublisher','riot','ember-cli-template-lint','godot','jeggy-mongoose','polyclay','vquery','docpad-plugin-services','react-vui-alerts','ember-cli-chartjs','angular2-jsonapi','react-components','meshblu-core-task-reset-token','commandments','machinepack-passwords','react-themed','xo-server-auth-saml','react-redux-provide-theme','images-to-less-variables','eslint-config-tipsi','safe-wipe','nosql-memdb','grunt-phonegap-build-tom','localforage-setitems','reem','to-vfile','tapas-ui','postcss-clean','metalsmith-template-data','react-starter-es6','light-swift','primer-forms','react-rxd','backbone-mongo','next-update','generator-tiny-es-nm','heroku-cli-util','docpad-plugin-markdowntoc']
def data_first_graph():
    packages  = ['metalsmith-json-to-files--katemihalikova','http-browserify-alexjeffburke','tokend','treeeater-dustyburwell','staticerrs','vdom-render-pull-stream','react-starter-es6','ga-collect','map-indexed-xf','fh-rest-mysql-adapter','gulp-highwinds','mongotape','pre-rating','redux-devtools-log-monitor-ie8','flat-rocks','madstreetden','immutable-json-schema','node-qrious','karma-coverage-es6','mongo-iterable-cursor','decorator-helpers','raster-tile-query','node-spa-auth','hsluv-stylus','base-2048','lpi-stripe','joii-unit','giffy-break-cli','dsl-helper','loner','generator-awesomeo','currency-object','id-fsm','babel-plugin-test-unroll','parse-server-yutin','hambruger','node-inspector-osi-licensed','oauth2orize-redelegate','metalsmith-template-data','jstransformer-csso','canduitz','http-proxy-no-line-184-error','ldep','oppressor-contrib','eslint-config-bem-sdk','slush-react-materialui','gulp-ngtemplate2','pit-ro','grunt-inline-imgsize','microservice','traceur-annotations','co-gather','ember-cli-media-queries','promise-to-stream-either','phoenix-cypto','svg-sprite_l','anonymize','organic-plasma-usersessions','dbm','bitbucket-downloads-client','deal-validator','xbee-stream','sparkbar','hapi-mongoose-plugin','retrial','js-package-sample','supports-semigraphics','generator-pistacheo','rework-imagesize','vshushkov-react-datetime','get-urls-cli','buffer-includes','regular-format','sorcerer','invoke-after','domly-liftoff','stringify-github-anchor','generator-bayse','deps-topo-sort','css-modules-example','saucier','producthunt','dfrl','worddump','fantasy-environment','jsonreduce','compute-dims','angular2-webpack-starter','think-compress-html','markdown-it-react-renderer','ttl-queue','ngx-delete-confirm','ember-cli-footnotes','slacktalk','balanced-addon-models','node-committer','socks5-server','auth0-react-native','gulp-jira-todo','string-pred','meshblu-core-task-get-broadcast-subscription-types','gyazo-upload','rollup-plugin-prettier','strider-docker-build','ioredis-mock-lpl','latest-versions','metainfo','hier','lyef-react-component','postcss-clean','util-plus','grunt-webp-modify','tapas-ui','generator-maria','q-loop','bestjavascriptlibrary','my-kenya-pkg','parse-dburi','anova','logstorage','generator-bower-package','lackey-mongoose-utils','reglite','operator-assertion','pa1d','pokenode','html-scrapper','set-object','rc-minidialog','npm-dep-chain','generator-redux-feature','victory-component-boilerplate','plotlyjs-finance','streamme','pakr','first-line','babel-plugin-class-autobind','ix-level-userdb','feathers-sync','postcss-maze','auth-driver-utils','rocksdown','proxy-generics-google-maps','nextprot','to-vfile','leap-seconds-list-creator','generator-nodejs-module','spa-plugin-gettext','linux-wifi','gulp-eol','style-script','babel-plugin-elm','flux-utils','osia-babel','ee-bump','read-file-relative','stylus-vertical-grid','reduce-generator','tiny-orm','grunt-qunit-istanbul-plus','eslint-config-mnubo','site-crawler','postcss-clean-prefixes','legal-ass','get-last-value','ck2parser','mocha-mix-jsdom','nunit-command','current','reem','karma-ng-template-preprocessor','node-priority','eldarion-ajax','grunt-tex-hunspell','babel-package-import','docpad-plugin-markdowntoc','hatch-loopback-testing','grunt-qunitnode','pandom','ndarray-stencil','github-following','initgraph','koara-xml','expiry-model','multiform-build','async-data','express-auto-controller','localforage-setitems','vigour-jsdoc2md','grunt-phonegap-build-tom','httperror','grunt-akamai-ccu-purge','insert-space','deskbookers-react-intl','snap-points-2d','simply-build','virtual-scroll','keydir','grunt-speedgun','framing','shaman','postcss-margin-helpers','nosql-memdb','google-drive-blobs','jopier-rest','lirc_web','obd2','generator-imstar-component','safe-wipe','nunjucks-filter-loader','plover-assets-util','generator-kiwiplugin','is-pointer-inside','vetus','eslint-config-tipsi','react-steack','derby-lang-fs','nps-collect','images-to-less-variables','report-builder','input-plugin-datetime','command-palette','ftp-reap','react-redux-provide-theme','generator-npm-pasta','execution-pool','xo-server-auth-saml','react-data-grid-extensions','passport-reddit-token','childminder','elev-varsel-generate-document-title','j2-grunt-jsdoc','node-configs','seed-width-max','sat-api-lib','apeman-scrt','letsago','sails-hook-seed','has-task-runner','validate-arguments','grunt-vanilli','wpxml2md','git-source','version-require','line-circle-collision','everybody-needs-a-404','grunt-socko','chai-jasmine','react-themed','yala','express-extras','domo-kun','reql-cli','machinepack-passwords','bumpery','ip-cidr','aliexpress','node-html-light','ami-motley-tool','reflecta','easygettext','microm','env-cmd','dev-time-cli','giantbomb','grunt-consolidate-css','gulp-email-builder','axiba-dependencies','abacus-eureka-plugin','s3-revisions','redux-roller','commandments','searchtracks','express-integrator-extension','errorable-common','typeset','webpack-cleanup-plugin','meshblu-core-task-reset-token','postcss-inrule','indeed-api-client','ankara-coverage','alinex-async','socrates','lincell','generator-validate-io','selenium-screen-master','objectbox','microservice-crutch','hemsl','botmaster-fulfill-actions','angular-stormpath','octopie','nvm-test','koa-jsonwebtoken','dynamic-extras','react-components','json-bigint','goog-class-to-es6','scurvy','eslint-config-auth0-base','diable','angular2-jsonapi','iotdb-transport-redis','should-enzyme','trailpack-mongoose','light-swift','primer-forms','honeybadger','co-suspend','koa-socket','o-','ember-cli-chartjs','bilanx','gendiff-lvl2-s18-ai','nanocomponent','apeman-bud','ploverx','rs-api','azure-mgmt-compute','ember-cli-deploy-cloudfront','lodash-match-pattern','file-prompt','express-minify','contentful-import','synopsis-client','pure-graph','react-vui-alerts','postcss-short','react-player-controls','grunt-gitbook','react-css-transition','docpad-plugin-services','backbone-mongo','core-tools','uninspected','grunt-prettify','vquery','generator-tiny-es-nm','random-access-file','graphql-language-service','hadron-type-checker','guy-test','ember-suave','comake-services','react-islands','polyclay','node-json-db','full-meta-jacket','qewd-ripple','typeodm','open-graph-scraper','fast-stream','legiond','angular2-dependencies-graph','nexmo-cli','hoost','tilestrata','msg-js-spa-framework','jeggy-mongoose','scrape-twitter','paypal-rest-sdk','cruk-searchkit','generator-meteor','godot','ember-cli-template-lint','kelper','iotdb-transport','linvodb3','sidekick','ubk','quark-gui','inliner','stylestats','most','jorm','restful-goose','next-update','react-rxd','riot','ut-test','apipublisher','testcafe','heroku-cli-util','assetgraph-builder']
    providers = []
    releases  = []

    for name in packages:
        package   = getPackage(name)
        providers.append(getDependencias(package))
        releases.append(executed(name))

    print(releases)
    print(providers)

def get_percentage(client, qtd_affected):
    return qtd_affected
    #return round(qtd_affected*100/executed(client))

def get_providers_impact():
    result   = json.load(open('results.json'))
    provider = {}
    for client_name in list(result.keys()):
        for index, case in enumerate(result[client_name]):
            prov_name  = result[client_name][index]['providers'][-1]
            percentage = get_percentage(client_name, case['affected_clients_releases'])

            try:
                provider[prov_name]['affected_clients_releases'].append(percentage)
            except KeyError:
                provider[prov_name] = {'affected_clients_releases': [percentage]}
            finally:
                provider[prov_name]['clients'] = 0
                provider[prov_name]['time_until_introduction'] = case['time_until_introduction']
                provider[prov_name]['introduced_after_releases'] = case['introduced_after_releases']
                provider[prov_name]['releases'] = len(getPackage(prov_name)['time'])-2

    return provider

def search_in_dep(package, dep_type, data):
    providers = list(data.keys())

    try:
        for provider in list(package['latest'][dep_type].keys()):
            if provider in providers:
                data[provider]['clients'] += 1
    except KeyError:
        return

def save(data):
    json.dump(data, open('providers_info.json', 'w'), indent=2)

def get_providers_clients(data):
    csv_r = csv.reader(open('../CSV/all_packages.csv'), delimiter=',', quotechar='\n')
    csv_r.__next__()    # ignorando a primeira linha
    count = 0
    limit = 10000

    try:
        while True:
            package_name = csv_r.__next__()[0]
            package = getPackage(package_name)

            search_in_dep(package, 'dependencies', data)
            search_in_dep(package, 'devDependencies', data)
            search_in_dep(package, 'peerDependencies', data)
            search_in_dep(package, 'optionalDependencies', data)

            count += 1
            if count == limit:
                limit += 10000
                print(count)
    except:
        save(data)
        return data

def sort(data):
    keys = list(data.keys())
    llll = data['rele']
    for i in range(1, len(keys)):
        chave = llll[i]
        chove = keys[i]
        k = i
        while k > 0 and chave < llll[k - 1]:
            llll[k] = llll[k - 1]
            keys[k] = keys[k - 1]
            k -= 1
        llll[k] = chave
        keys[k] = chove

    print(llll)
    print(data['rele'])

    return keys

def print_data(data):
    #keys = sort(data)
    keys = list(data.keys())
    print("data <- data.frame(")
    for key in keys:
        quote = ','
        if list(data.keys())[-1].__eq__(key):
            quote = ''
        print('\t{0}=c{1}{2}'.format(key, data[key], quote).replace('[', '(').replace(']', ')'))

    print(')')

def copy_from_data(data):
    data_bck = json.load(open('./backup/providers_info.json'))

    for provider in list(data_bck.keys()):
        data[provider]['clients'] = data_bck[provider]['clients']

    save(data)

def data_fifth_graph():
    data = get_providers_impact()
    #data = get_providers_clients(data)
    copy_from_data(data)
    return data

providers = data_fifth_graph()
del(providers['jsdom'])
del(providers['ember-cli-htmlbars-inline-precompile'])
del(providers['esprima'])
del(providers['heroku-client'])
del(providers['source-map'])
del(providers['test-machinepack'])

prov_names = []
cli_affect = []
prov_cli   = []
time_until = []
rele_until = []
releases   = []
rangee     = []
count      = 1
for provider in list(providers.keys()):
    #for number in providers[provider]['affected_clients_releases']:
    prov_names.append(provider)
    #cli_affect.append(number)
    prov_cli.append(providers[provider]['clients'])
    time_until.append(providers[provider]['time_until_introduction'])
    rele_until.append(providers[provider]['introduced_after_releases'])
    releases.append(providers[provider]['releases'])
    rangee.append(count)
    count += 1

#print(count)
# print_data({
#     'prov': prov_names,
#     #'perc_cli': cli_affect,
#     'qtd_cli': prov_cli,
#     'time_until': time_until,
#     'rele_until': rele_until,
#     'rele': releases,
#     'um': len(releases)*[1],
#     'range': rangee
# })

percentage = [89.12,57.14,31.13,32.00,88.57,76.67,79.25,56.00,45.76,50.00,100.00,89.90,50.00,38.61,53.33,87.10,30.00,70.00,80.00,51.52,34.62,75.00,82.26,82.26,15.89,80.65,64.29,38.11,73.08,88.89]
count = 0
for i, value in enumerate(percentage):
    if value >= 75:
        count +=1 

count

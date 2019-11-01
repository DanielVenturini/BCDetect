var myChart = echarts.init(document.getElementById('view'));

option = {
    toolbox: {
        show : true,
        feature : {
            mark        : {show: true},
            dataView    : {show: true, readOnly: false},
            saveAsImage : {show: true},
            magicType   : {show: false, type: ['pie', 'funnel']},
            restore     : {show: false}
        }
    },
    tooltip: {
        trigger: 'item',
        triggerOn: 'mousemove'
    },
    series: {
        type: 'sankey',
        layout:'none',
        value: true,
        focusNodeAdjacency: 'allEdges',
        data: [{
            name: 'Pacotes'
        }, {
            name: 'Executados'
        }, {
            name: 'Releases'
        }, {
            name: 'Executadas'
        }, {
            name: 'Não executadas'
        }, {
            name: 'Sucesso'
        }, {
            name: 'Erro'
        }],
        links: [{
            source: 'Pacotes',
            target: 'Executados',
            value: 384
        }, {
            source: 'Executados',
            target: 'Sucesso',
            value: 140
        }, {
            source: 'Executados',
            target: 'Erro',
            value: 244
        }, {
            source: 'Releases',
            target: 'Executadas',
            value: 2662
        }, {
            source: 'Releases',
            target: 'Executadas',
            value: 2662
        }, {
            source: 'Releases',
            target: 'Não executadas',
            value: 1908
        }, {
            source: 'Executadas',
            target: 'Erro',
            value: 1460
        }, {
            source: 'Executadas',
            target: 'Sucesso',
            value: 1202
        }]
    }
};

myChart.setOption(option);
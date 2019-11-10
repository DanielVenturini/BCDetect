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
        }, {
            name: 'Sucesso '
        }, {
            name: 'Erro '
        }, {
            name: 'Falso-positivo'
        }, {
            name: 'Falso-positivo '
        }, {
            name: 'Erro interno'
        }, {
            name: 'Erro interno '
        }, {
            name: 'Non-break change'
        }, {
            name: 'Non-break change '
        }, {
            name: 'Break change'
        }, {
            name: 'Break change '
        }, {
            name: 'Não encontrado'
        }, {
            name: 'Não encontrado '
        }],
        links: [{
            source: 'Pacotes',
            target: 'Executados',
            value: 384
        }, {
            source: 'Executados',
            target: 'Sucesso ',
            value: 164
        }, {
            source: 'Executados',
            target: 'Erro ',
            value: 220
        }, {
            source: 'Erro ',
            target: 'Falso-positivo ',
            value: 37
        }, {
            source: 'Erro ',
            target: 'Erro interno ',
            value: 96
        }, {
            source: 'Erro ',
            target: 'Non-break change ',
            value: 45
        }, {
            source: 'Erro ',
            target: 'Break change ',
            value: 39
        }, {
            source: 'Erro ',
            target: 'Não encontrado ',
            value: 39
        },
        // FOLLOW, THE RELEASES RESULTS
        {
            source: 'Releases',
            target: 'Executadas',
            value: 2332
        }, {
            source: 'Releases',
            target: 'Não executadas',
            value: 2242
        }, {
            source: 'Executadas',
            target: 'Erro',
            value: 1314
        }, {
            source: 'Executadas',
            target: 'Sucesso',
            value: 1019
        }, {
            source: 'Erro',
            target: 'Falso-positivo',
            value: 410
        }, {
            source: 'Erro',
            target: 'Erro interno',
            value: 428
        }, {
            source: 'Erro',
            target: 'Non-break change',
            value: 213
        }, {
            source: 'Erro',
            target: 'Break change',
            value: 190
        }, {
            source: 'Erro',
            target: 'Não encontrado',
            value: 73
        }]
    }
};

myChart.setOption(option);
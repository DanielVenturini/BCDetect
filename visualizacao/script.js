var myChart = echarts.init(document.getElementById('view'));

var data = echarts.dataTool.prepareBoxplotData([
    [850, 740, 900, 1070, 930, 850, 950, 980, 980, 880, 1000, 980, 930, 650, 760, 810, 1000, 1000, 960, 960],
    [960, 940, 960, 940, 880, 800, 850, 880, 900, 840, 830, 790, 810, 880, 880, 830, 800, 790, 760, 800],
]);

var eixoX = ['Releases', 'Dependências'];

option = {
    title: [
        {
            text: 'Relação repositórios releases e dependências',
            left: 'center',
        },
        {
            text: 'upper: Q3 + 1.5 * IQR \nlower: Q1 - 1.5 * IQR',
            borderColor: '#999',
            borderWidth: 1,
            textStyle: {
                fontSize: 14
            },
            left: '10%',
            top: '90%'
        }
    ],
    tooltip: {
        trigger: 'item',
        axisPointer: {
            type: 'shadow'
        }
    },
    grid: {
        left: '10%',
        right: '10%',
        bottom: '15%'
    },
    xAxis: {
        type: 'category',
        data: data.axisData,
        boundaryGap: true,
        nameGap: 30,
        splitArea: {
            show: false
        },
        axisLabel: {
            formatter: 'expr {value}'
        },
        splitLine: {
            show: false
        }
    },
    yAxis: {
        type: 'value',
        name: 'km/s minus 299,000',
        splitArea: {
            show: true
        }
    },
    series: [
        {
            name: 'boxplot',
            type: 'boxplot',
            data: data.boxData,
            tooltip: {
                formatter: function (param) {
                    return [
                        'Experiment ' + param.name + ': ',
                        'upper: ' + param.data[5],
                        'Q3: ' + param.data[4],
                        'median: ' + param.data[3],
                        'Q1: ' + param.data[2],
                        'lower: ' + param.data[1]
                    ].join('<br/>');
                }
            }
        },
        {
            name: 'outlier',
            type: 'scatter',
            data: data.outliers
        }
    ]
};

myChart.setOption(option)
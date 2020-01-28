# install.packages('networkD3')

library(networkD3)
library(htmlwidgets)

my_color <- 'd3.scaleOrdinal() .domain(["Erro", "Erro "]) .range(["red", "red"])'

data <- jsonlite::fromJSON('./sankey.json')
sankeyNetwork(data, Links=data$links, Nodes=data$nodes, Source="source", colourScale=my_color,
             Target="target", Value="value", NodeID="name",
             fontSize=12, nodeWidth=30, sinksRight=F)
















pdf(file='./pre_res_rq1.pdf', width=8, height=6)
labels <- c('Erros internos', 'Breaking changes', 'Casos particulares de breaking changes', 'Não encontrados', 'Sucesso')
values <- c(433, 193, 213, 73, 1398)
pct    <- round(values/sum(values)*100, 1)
pct    <- paste('(', pct)
labels <- paste(labels, pct)
labels <- paste(labels,"% )",sep="")
pie(values, labels=labels, init.angle=25, clockwise=T)
dev.off()
library(networkD3)
library(magrittr)

links=data.frame(
    source=c('Explícito (17.8%)', 'Explícito (17.8%)', 'Implícito (82.2%)', 'Implícito (82.2%)', 'Implícito (82.2%)', 'Consertado pelo cliente (62.5%)', 'Consertado pelo cliente (62.5%)', 'Consertado pelo cliente (67.6%)', 'Consertado pelo cliente (67.6%)', 'Consertado pelo cliente (67.6%)'),
    target=c('Consertado pelo cliente (62.5%)', 'Consertado pelo provedor (37.5%)', 'Consertado pelo cliente (67.6%)', 'Consertado pelo provedor (24.3%)', 'Não consertado (8.1%)', 'Provedor atualizado (20%)', 'Provedor regredido (80%)', 'Provedor atualizado (20.8%) ', 'Provedor regredido (66.7%)', 'Não alterado (12.5%)'),
    value=c(5, 3, 25, 9, 3, 1, 4, 5, 16, 3)
)

nodes <- data.frame(
  name=c(as.character(links$source), 
  as.character(links$target)) %>% unique()
)

links$IDsource <- match(links$source, nodes$name)-1 
links$IDtarget <- match(links$target, nodes$name)-1

p <- sankeyNetwork(Links = links, Nodes = nodes, fontSize=15,
              Source = "IDsource", Target = "IDtarget",
              Value = "value", NodeID = "name", 
              sinksRight=FALSE)
p

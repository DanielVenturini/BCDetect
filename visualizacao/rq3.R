library(networkD3)
library(magrittr)

links=data.frame(
    #source=c('Explícito (17.8%)', 'Explícito (17.8%)', 'Implícito (82.2%)', 'Implícito (82.2%)', 'Implícito (82.2%)', 'Consertado pelo cliente (62.5%)', 'Consertado pelo cliente (62.5%)', 'Consertado pelo cliente (67.6%)', 'Consertado pelo cliente (67.6%)', 'Consertado pelo cliente (67.6%)'),
    #target=c('Consertado pelo cliente (62.5%)', 'Consertado pelo provedor (37.5%)', 'Consertado pelo cliente (67.6%)', 'Consertado pelo provedor (24.3%)', 'Não consertado (8.1%)', 'Provedor atualizado (20%)', 'Provedor regredido (80%)', 'Provedor atualizado (20.8%) ', 'Provedor regredido (66.7%)', 'Não alterado (12.5%)'),
    source=c('Explicitly (17.8%)', 'Explicitly (17.8%)', 'Implicitly (82.2%)', 'Implicitly (82.2%)', 'Implicitly (82.2%)', 'Fixed by client (62.5%)', 'Fixed by client (62.5%)', 'Fixed by client (67.6%)', 'Fixed by client (67.6%)', 'Fixed by client (67.6%)'),
    target=c('Fixed by client (62.5%)', 'Fixed by provider (37.5%)', 'Fixed by client (67.6%)', 'Fixed by provider (24.3%)', 'Did not fixed (8.1%)', 'Updated provider (20%)', 'Downgraded provider (80%)', 'Updated provider (20.8%) ', 'Downgraded provider (66.7%)', 'Did not changed (12.5%)'),
    value=c(5, 3, 25, 9, 3, 1, 4, 5, 16, 3)
)

nodes <- data.frame(
  name=c(as.character(links$source), 
  as.character(links$target)) %>% unique()
)

links$IDsource <- match(links$source, nodes$name)-1 
links$IDtarget <- match(links$target, nodes$name)-1

my_color <- 'd3.scaleOrdinal().range(["#000000"])'
# recovery_clients.pdf
p <- sankeyNetwork(Links = links, Nodes = nodes, fontSize=15,
              Source = "IDsource", Target = "IDtarget",
              Value = "value", NodeID = "name", 
              sinksRight=FALSE,
              nodeWidth = 5, nodePadding = 3,
              colourScale = my_color,
              height = 350)
p

# days to be fixed
explicit <- c(1, 8, 179, 2, 594)
implicit <- c(122, 1, 1, 17, 70, -1, 4, 1, 3, 94, 1, 2, 183, 1, 1, 402, -1, 44, 1, 4, -1, -1, 1, 1, 34)

# remove -1
implicit <- implicit[implicit > 0]

median(explicit)
median(implicit)

client <- c(1, 44, 94, 1, -1, 70, -1, 183, 17, -1, 1, 4, 1, -1, 1, 34, 3, 122, 1, 2, 594, 1, 179, 2, 1, 1, 4, 402, 1, 8)
provid <- c(15, 7, 1002, 38, 462, 1, 32, 1002, 160, 4, 20, 117)

client <- client[client > 0]

median(client)
median(provid)
source('./data_rq2.R')

library(ggplot2)
library(networkD3)

# -----------------------------
# GRAPH 1
# -----------------------------

links$IDsource <- match(links$source, nodes$name)-1 
links$IDtarget <- match(links$target, nodes$name)-1

p <- sankeyNetwork(Links = links, Nodes = nodes, fontSize=15,
              Source = "IDsource", Target = "IDtarget",
              Value = "value", NodeID = "name", 
              sinksRight=FALSE)
p

# -----------------------------
# CITATIONS
# -----------------------------

data <- data.frame(
  name=c('minor', 'patch', 'major', 'pre'),
  values=c(26,16,2,1)
)

# -----------------------------
# GRAPH 2
# -----------------------------
pdf('./semver_types.pdf')
barplot(bilan, beside=T, legend.text=T, col=col, ylim=c(0,lim), ylab="%")
dev.off()

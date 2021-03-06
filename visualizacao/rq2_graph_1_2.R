source('./data_rq2.R')

library(ggplot2)
library(networkD3)

# -----------------------------
# GRAPH 1
# -----------------------------

links$IDsource <- match(links$source, nodes$name)-1 
links$IDtarget <- match(links$target, nodes$name)-1
my_color <- 'd3.scaleOrdinal().range(["#000000"])'
# semver_fixed.pdf
p <- sankeyNetwork(Links = links, Nodes = nodes, fontSize=15,
              Source = "IDsource", Target = "IDtarget",
              Value = "value", NodeID = "name", 
              sinksRight=FALSE,
              nodeWidth = 5, nodePadding = 3,
              colourScale = my_color,
              height = 250)
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
#pdf('./semver_types.pdf')
pdf('~/git/paper_break_change/figures/semver_types.pdf')
barplot(bilan, beside=T, legend.text=T, col=col, ylim=c(0,lim), ylab="%")
dev.off()

#install.packages("magrittr")
#install.packages('networkD3')
#install.packages('igraph')
#install.packages('ggraph')
#install.packages('MASS')

library(networkD3)
library(magrittr)
library(igraph)
library(ggraph)

# ===========
# FIRST GRAPH
# ===========
levels <- c('Minor','Minor','Patch','Minor','Patch','Major','Minor','Minor','Patch','Patch','Minor','Minor','Minor','Patch','Minor','Patch','Minor','Patch','Pre-release','Minor','Patch','Minor','Minor','Minor','Minor','Patch','Minor','Patch','Minor','Patch','Minor','Major','Minor','Patch','Minor','Minor','Patch','Minor','Minor','Patch','Minor','Patch','Minor','Patch','Minor')

data <- data.frame(
  # [1] "minor" "patch" "major" "pre"
  name=unique(levels),
  values=c(26,16,2,1)
)

pdf('./semver_levels.pdf')
pct    <- round(data$values/sum(data$values)*100, 2)
pct    <- paste('(', pct)
data$name <- paste(data$name, pct)
data$name <- paste(data$name,"% )",sep="")
pie(data$values, labels=data$name, init.angle=230)
dev.off()

# =============
# SECOND GRAPH
# =============
links=data.frame(
    source=c('Breaking changes em Minor', 'Breaking changes em Minor', 'Breaking changes em Minor', 'Provedores (15.4%)', 'Clientes (76.9%)', 'Clientes (76.9%)'),
    target=c('Provedores (15.4%)', 'Clientes (76.9%)', 'Não consertadas (7.7%)', 'Patch (100%)', 'Patch (80%)', 'Minor (20%)'),
    value=c(4, 20, 2, 4, 16, 4)
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

# ===========
# THIRD GRAPH
# ===========
categories = c('Objeto indefinido (4 casos)', 'Provedores incompatíveis (11 casos)', 'Alteração de regras (14 casos)', 'Alteração de tipo de objeto (7 casos)', 'Código errado (3 casos)', 'Código não-atualizado (3 casos)', 'Renomeação de função (2 casos)', 'Arquivo não encontrado (1 caso)')
data <- data.frame(
categories=categories,
i_major=c(0.0,9.1,0.0,0.0,0.0,33.3,0.0,0.0),
i_minor=c(0.0,81.8,57.1,57.1,66.7,33.3,50.0,100.0),
i_patch=c(100.0,9.1,42.9,42.9,33.3,33.3,0.0,0.0),
i_pre=c(0.0,0.0,0.0,0.0,0.0,0.0,50.0,0.0)
)

#Let's calculate the average value for each condition and each specie with the *aggregate* function
bilan <- aggregate(cbind(i_major,i_minor,i_patch,i_pre)~categories , data=data , mean)
rownames(bilan) <- bilan[,1]
bilan <- as.matrix(bilan[,-1])

#Plot boundaries
lim <- 1.6*max(bilan)

#Then I calculate the standard deviation for each categories and condition :
stdev <- aggregate(cbind(i_major,i_minor,i_patch,i_pre)~categories , data=data , sd)
rownames(stdev) <- stdev[,1]
stdev <- as.matrix(stdev[,-1]) * 1.96 / 10

dimnames(bilan)[[2]] <- c('Major', 'Minor', 'Patch', 'Pré-release')
#I am ready to add the error bar on the plot using my "error bar" function !
col=c('#6666ff', '#ffff66', '#ff6666', '#66ff66', '#ff66ff', '#c2c2a3', 'black', 'brown')
pdf('./semver_types.pdf')
barplot(bilan, beside=T, legend.text=T, col=col, ylim=c(0,lim), ylab="%")
dev.off()

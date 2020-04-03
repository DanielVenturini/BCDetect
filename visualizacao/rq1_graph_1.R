source('./data_rq1.R')
source('./functions_rq1.R')

# -----------------------------
# GRAPH
# -----------------------------

data <- data_rq1_graph1
pdf('./correlation_release_providers.pdf')
# Basic scatterplot
plot(x=data$x, y=data$y, type='p', log='xy', ylab='Provedores', xlab='Releases', pch=20, col=rgb(0,0,0, alpha=0.1), frame=F)

abline(h=ceiling(median(providers)), col='#d9d9d9')
abline(v=ceiling(median(releases)), col='#d9d9d9')

model <- lm(data$y ~ data$x)
myPredict <- predict( model , interval="predict" )

#Finally, I can add it to the plot using the line and the polygon function with transparency.
ix <- sort(data$x,index.return=T)$ix
lines(data$x[ix], myPredict[ix , 1], col='#999999', lwd=2)
dev.off()

# -----------------------
# CITATIONS
# -----------------------

median(releases)
median(providers)
qtd_quad(4, TRUE, releases, providers)
providers_more_than_releases(39)
qtd_quad(1, TRUE, releases, providers)

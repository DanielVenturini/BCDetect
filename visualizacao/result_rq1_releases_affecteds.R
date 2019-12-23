# from packages with no break changes
Tamanho_non_bc    <- c(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,1,1,2,2,1,1,1,2,1,1,2,1,2,2,1,1,1,1,1,2,1,2,1,1,2,1,2,2,2,2,1,2,2,2,2,2,1,1,1,1,1,1,1,3,1,1,3,1,2,3,1,2,2,2,2,2,3,3,2,2,2,3,1,2,3,2,3,3,2,1,2,3,4,1,3,2,1,3,3,1,1,1,3,2,4,3,1,2,1,1,3,2,2,2,1,1,4,3,3,3,4,4,3,2,2,5,3,4,3,1,2,4,4,1,1,4,1,4,4,3,4,4,3,5,3,1,6,5,4,1,2,3,6,4,4,1,2,5,3,6,6,3,1,7,7,5,7,8,6,6,8,4,2,2,3,2,6,3,5,8,2,2,5,4,8,8,1,5,8,6,2,7,7,4,4,6,4,5,6,3,4,6,8,6,3,8,3,4,12,7,8,11,5,9,4,9,4,5,8,12,10,13,13,11,7,6,1,9,2,10,12,14,6,8,14,10,9,11,18,4,1,13,11,20,15,7,9,12,14,22,12,10,18,6,21,9,4,12,16,1,3,3,1,19,7,15,12,17,25,23,5,13,27,22,10,30,25,18,47,43,4,13,18,1,1,2,1,2,4,1,3,1,4,2,5,4,4,1,1,1,2,1,5,1,4,1,2,3,13)
Provedores_non_bc <- c(14,4,26,2,4,14,5,10,16,7,5,51,21,17,6,9,4,17,15,17,5,30,2,3,10,5,5,5,6,6,1,2,17,48,6,18,4,2,9,5,3,4,7,9,6,2,7,4,6,3,24,5,23,4,9,3,21,6,3,2,1,7,25,4,5,8,4,12,5,10,1,5,5,5,49,7,33,7,63,17,5,13,9,4,16,10,9,10,7,18,3,21,3,1,6,28,5,4,5,4,18,101,3,1,19,5,11,5,12,10,5,7,4,31,9,15,11,3,2,10,5,17,7,9,11,2,6,6,4,5,10,9,7,11,6,2,1,6,12,9,2,5,7,4,3,7,6,12,5,2,4,2,15,9,5,7,10,7,20,6,15,7,11,9,2,2,3,7,2,8,10,8,6,8,4,25,9,15,7,8,4,8,4,18,3,21,25,13,7,13,5,5,59,12,29,6,4,5,5,11,21,5,8,13,2,12,2,4,5,4,3,5,14,11,18,4,4,11,3,9,14,11,8,13,7,2,15,17,21,9,18,5,8,20,8,20,13,5,14,7,12,6,4,14,6,19,63,5,23,10,10,3,4,8,13,6,16,25,10,6,11,10,3,13,18,16,18,12,1,12,13,17,12,33,10,15,14,32,5,68,13,12,11,8,47,18,3,16,7,48,7,10,16,20,11,3,10,16,13,7,17,33,27,15,72,6,15,12,19,23,13,24,26,20,16,10,25,2,11,32,5,7,3,25,51,4,1,11,2,10,8,18,3,7,2,8,15,21,19,6,2,16,9,7)

# from packages with break changes
Tamanho    <- c(140,57,40,60,27,23,24,19,18,10,13,7,8,7,10,6,6,7,4,6,4,2,2,5,1,2,3,4,3,3,1,1,9,13,30,18,50,14,61,1)
Afetados   <- c(23,6,14,10,1,3,12,7,2,8,2,6,2,1,1,4,1,1,4,4,2,2,1,1,1,1,2,2,3,2,1,1,2,2,15,15,13,12,2,1)
Provedores <- c(48,102,3,34,37,15,23,5,36,6,16,20,41,15,13,5,3,32,10,27,13,7,4,11,5,10,9,10,76,12,9,15,17,4,49,16,44,10,34,5)

# normalize the size of affecteds release
Afetados <- (Afetados*100)/Tamanho

pdf(file='./result_rq1_releases_affecteds.pdf')
plot(c(Tamanho, Tamanho_non_bc), c(Provedores, Provedores_non_bc), log='xy', type='p', ylab='Provedores', xlab='Releases', pch=20, col=rgb(0,0,0, alpha=0.1), frame=F)

abline(h=ceiling(median(Provedores)), col='#ffb3b3')
abline(v=ceiling(median(Tamanho)), col='#ffb3b3')
symbols(Tamanho, Provedores, circles=Afetados, inches=0.1, add=T, fg='red')
legend("bottomright", legend=c('20%', '50%', '100%'),
    pch=1, col=c('red', 'red', 'red'), pt.cex=c(2, 5, 10)*0.27)

model <- lm(Provedores ~ Tamanho)
myPredict <- predict( model , interval="predict" )
#Finally, I can add it to the plot using the line and the polygon function with transparency.
ix <- sort(Tamanho,index.return=T)$ix
lines(Tamanho[ix], myPredict[ix , 1], col='#ff1a1a', lwd=2)

dev.off()


# todos os clientes no inferior_direito
releases  <- c(Tamanho_non_bc, Tamanho)
providers <- c(Provedores_non_bc, Provedores)

more_than_median_releases  <- 0
more_than_median_providers <- 0
for(pos in 1:length(releases)) {
    if(releases[pos] > 8) {
        more_than_median_releases <- more_than_median_releases + 1
        if(providers[pos] <= 14) {
            more_than_median_providers <- more_than_median_providers + 1
        }
    }
}

(more_than_median_providers*100)/length(releases)

# todos os breaking changes no inferior_direito
releases  <- Tamanho
providers <- Provedores

bc_more_than_median_releases  <- 0
bc_more_than_median_providers <- 0
for(pos in 1:length(releases)) {
    if(releases[pos] > ceiling(median(releases))) {
        bc_more_than_median_releases <- bc_more_than_median_releases + 1
        if(providers[pos] <= ceiling(median(providers))) {
            bc_more_than_median_providers <- bc_more_than_median_providers + 1
        }
    }
}

(bc_more_than_median_providers * 100)/more_than_median_providers

superior_direito  <- 28.6
inferior_direito  <- 16.7
superior_esquerdo <- 9.6
inferir_esquerdo  <- 5.6

#install.packages('fmsb')
library(fmsb)

pdf('./percentage_clients_bc.pdf', width=10, height=10)
values <- c(17.2, 10.6, 11.2, 30.2, 64.6, 5.6, 7, 22.2)
# 17.2, 11.2, 64.6, 7.0
# 10.6, 30.2, 5.6, 22.2

data   <- as.data.frame(matrix(values, ncol=4))

colnames(data) <- c('Sup. esquerdo', 'Sup. direito', 'Inf. esquerdo', 'Inf. direito')
rownames(data) <- c('Clientes', 'Breaking changes')

# must to add 2 lines to the dataframe: the max and min of each variable to show on the plot!
data <- rbind(rep(100,4) , rep(0,4) , data)

colors_in=c( rgb(0.85,0.85,0.85,0.4), rgb(1,0,0,0.4))# , rgb(0.7,0.5,0.1,0.4) ) 
# plot with default options:
radarchart(data, axistype=1, plwd=1 , plty=1, pfcol=colors_in, cglty=1, cglcol="grey", axislabcol="grey", cglwd=0.8)
legend(x=0.7, y=1, legend=rownames(data[-c(1,2),]), bty="n", pch=20 , col=colors_in , text.col="grey", cex=1.2, pt.cex=3)
dev.off()

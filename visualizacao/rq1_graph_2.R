source('./data_rq1.R')
source('./functions_rq1.R')

# -----------------------------
# GRAPH 1
# -----------------------------

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

# -----------------------------
# GRAPH 2
# -----------------------------
pdf('./percentage_clients_bc.pdf')

# subtract the breakchange percentage
c_u_l <- c_u_l - b_u_l
c_u_r <- c_u_r - b_u_r
c_d_l <- c_d_l - b_d_l
c_d_r <- c_d_r - b_d_r

# evaluate:
#c_d_r + b_d_r + c_d_l + b_d_l + c_u_r + b_u_r + c_u_l + b_u_l must be 100%

# create others data
general <- character()
breakch <- character()
for(i in 1:length(r_gen)) {
    general <- c(general, get_quad_name(i, r_gen, p_gen))
}

for(i in 1:length(r_bc)) {
    breakch <- c(breakch, get_quad_name(i, r_bc, p_bc))
}

general_f <- factor(general)
breakch_f <- factor(breakch)

# 'Inf. direito' 'Inf. direito' 'Inf. esquerdo' 'Inf. esquerdo' 'Sup. direito' 'Sup. direito' 'Sup. esquerdo' 'Sup. esquerdo'
quad <- rep(levels(general_f), each=2)
Casos <-rep(c('Outros', 'Breaking change'), times=length(quad)/2)
value <- c(c_d_r, b_d_r, c_d_l, b_d_l, c_u_r, b_u_r, c_u_l, b_u_l)

data <- data.frame(quad, Casos, value)

library(ggplot2)

# Stacked + percent
# https://www.r-graph-gallery.com/48-grouped-barplot-with-ggplot2.html
ggplot(data, aes(fill=Casos, y=value, x=quad)) +
    geom_bar(position="stack", stat="identity") +
    xlab('Quadrante') +
    ylab('(%)') +
    theme_classic()

dev.off()

# -----------------------------
# CITATIONS
# -----------------------------

ceiling(median(r_bc))
ceiling(median(p_bc))
c_u_l + b_u_l
qtd_quad(1, TRUE, r_bc, p_bc)
c_d_l
qtd_quad(3, FALSE, r_bc, p_bc)

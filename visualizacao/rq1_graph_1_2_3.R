source('./functions_rq1.R')
source('./data_rq1.R')
library(ggplot2)
library(viridis)

# -----------------------------
# GRAPH 1
# -----------------------------
pdf(file='./result_rq1_releases_affecteds.pdf')
#pdf(file='~/git/paper_break_change/figures/result_rq1_releases_affecteds.pdf')
#plot(c(Tamanho, Tamanho_non_bc), c(Provedores, Provedores_non_bc), log='xy', type='p', ylab='Providers', xlab='Releases', pch=20, col=rgb(0,0,0, alpha=0.1), frame=F)
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

# https://www.r-graph-gallery.com/48-grouped-barplot-with-ggplot2.html
# https://www.pdf2go.com
pdf('./percentage_clients_bc.pdf', width=7, height=4)
pdf('~/git/paper_break_change/figures/percentage_clients_bc.pdf', width=7, height=4)
data <- data.frame(
        #especie=c(rep('Clientes', 4), rep('Clientes com breaking changes', 4)),
        #square=rep(c('Sup. esquerdo', 'Sup. direito', 'Inf. esquerdo', 'Inf. direito'), 2),
        especie=c(rep('Clients', 4), rep('Clients with breaking changes', 4)),
        square=rep(c('Left up', 'Right up', 'Left down', 'Rigth down'), 2),
        valor=c(c_u_l, c_u_r, c_d_l, c_d_r, b_g_u_l, b_g_u_r, b_g_d_l, b_g_d_r)
)

ggplot(data, aes(fill=square, y=valor, x=square)) + 
    geom_bar(position="dodge", stat="identity") +
    scale_fill_grey(end = 0.9) +
    #ggtitle("Studying 4 species..") +
    facet_wrap(~especie) +
    #theme(legend.position="none") +
    theme_bw() +
    theme (
      legend.position="none",
      # Remove panel border
      panel.border = element_blank(),
      # Remove panel background
      panel.background = element_blank()
    ) +
    #xlab('Quadrante') + ylab('(%)') +
    xlab('Square') + ylab('(%)') +
    ylim(0, 49)

dev.off()

# -----------------------------
# CITATIONS
# -----------------------------

ceiling(median(r_bc))
ceiling(median(p_bc))
c_d_r
c_u_l
b_g_u_l
c_d_l
b_g_d_l
b_g_u_r
b_g_d_r

# -----------------------------
# GRAPH 3
# -----------------------------

releases_data <- provs_info$rele
until_bc <- provs_info$rele_until
res      <- round(until_bc*100/releases_data, 2)
#res <- sort(res)
res <- c(0, 0, 0, 0, 15.89, 30.00, 31.13, 32.00, 34.62, 38.11, 38.61, 45.76, 50.00, 50.00, 51.52, 53.33, 56.00, 57.14, 64.29, 70.00, 73.08, 75.00, 76.67, 79.25, 80.00, 80.65, 82.26, 82.26, 87.10, 88.57, 88.89, 89.12, 89.90, 100.00)

# https://www.pdf2go.com
pdf('~/git/paper_break_change/figures/providers_releases_bc.pdf', width=3, height=3)
#pdf('./providers_releases_bc.pdf', width=3, height=3)
ggplot(provs_info, aes(x=range, y=res)) +
  geom_point() +
  geom_segment(aes(x=range, xend=range, y=0, yend=res)) +
  labs(x='', y='%') +
  theme_bw() +
  theme(panel.border = element_blank(),axis.line = element_line(colour = "black"))
dev.off()

# -----------------------------
# CITATIONS
# -----------------------------

count <- 0
for(percentage in res) {
  if(percentage < 35) {
    count <- count + 1
  }
}

count
round(count*100/length(res), 1)

count <- 0
for(percentage in res) {
  if(percentage >= 35 && percentage < 75) {
    count <- count + 1
  }
}

count
round(count*100/length(res), 1)

count <- 0
for(percentage in res) {
  if(percentage >= 75) {
    count <- count + 1
  }
}

count
round(count*100/length(res), 1)

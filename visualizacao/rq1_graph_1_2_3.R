source('~/git/bcdetect/visualizacao/functions_rq1.R')
source('~/git/bcdetect/visualizacao/data_rq1.R')
library(ggplot2)
library(viridis)
library(effsize)

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

x <- Tamanho
y <- Provedores

cor(x, y, method='spearman')

# -----------------------------
# GRAPH 3
# -----------------------------

# https://www.pdf2go.com
pdf('~/git/paper_break_change/figures/providers_releases_bc.pdf', width=3, height=3)
#pdf('./providers_releases_bc.pdf', width=3, height=3)
ggplot(provs_info, aes(x=range, y=sort(percentage))) +
  geom_point() +
  geom_segment(aes(x=range, xend=range, y=0, yend=sort(percentage))) +
  labs(x='Providers', y='%') +
  theme_bw() +
  theme(panel.border = element_blank(),axis.line = element_line(colour = "black"))
dev.off()

# -----------------------------
# CITATIONS
# -----------------------------
count <- 0
for(percentage in provs_info$percentage) {
  if(percentage < 35) {
    count <- count + 1
  }
}

count
round(count*100/length(provs_info$percentage), 1)

count <- 0
for(percentage in provs_info$percentage) {
  if(percentage >= 35 && percentage < 75) {
    count <- count + 1
  }
}

count
round(count*100/length(provs_info$percentage), 1)

count <- 0
for(percentage in provs_info$percentage) {
  if(percentage >= 75) {
    count <- count + 1
  }
}

count
round(count*100/length(provs_info$percentage), 1)


# TESTE DE WILCOXON-MANN-WHITNEY
# H0: o impacto das bcs são maiores no nível de evolução do que no nível final
# H1: o impacto das bc é igual ou menor que o nível final

evolu <- c()
n <- 1
sn <- 0
final <- c()
m <- 1
sm <- 0

for(pos in 1:length(provs_info$qtd_cli)) {
  if(provs_info$percentage[pos] >= 35 && provs_info$percentage[pos] < 75 ) {
    evolu <- c(evolu, provs_info$qtd_cli[pos])
  } else if (provs_info$percentage[pos] >= 75) {
    final <- c(final, provs_info$qtd_cli[pos])
  }
}

#diminuir <- rep(TRUE, length(final))
#diminuir[sample(1:length(final), 1)] <- FALSE
evolu <- sort(evolu)
#final <- final[diminuir]
final <- sort(final)
data <- c()

for (pos in 1:length(c(final, evolu))) {
  if(!is.na(evolu[n]) && evolu[n] < final[m]) {
    data <- c(data, evolu[n])
    n <- n + 1
    sn <- sn + pos
  } else {
    data <- c(data, final[m])
    m <- m + 1
    sm <- sm + pos
  }
}

n <- length(evolu)
m <- length(final)

un <- sn - (1/2)*n*(n + 1)
um <- sm - (1/2)*m*(m + 1)
sm + sn == (1/2)*(m + n)*(m + n + 1) # it must be TRUE
um == m*n - un  # it must be TRUE

# Se o valor de p for maior do que o nível de significância, você não deve rejeitar a hipótese nula
# p-value = 0.6488
wilcoxon = wilcox.test(evolu, final, correct=FALSE)
effect = cliff.delta(evolu, final, return.dm=TRUE)

wilcoxon$p.value
effect$estimate
effect$magnitude

# TESTE PARAMÉTRICO
t.test(evolu, final)
# insignificante
round(cohen.d(evolu, final)$estimate, 3)

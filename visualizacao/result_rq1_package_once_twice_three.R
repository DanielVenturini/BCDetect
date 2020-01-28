# effect size
install.packages('effsize')
library(effsize)

# # non-parametric
# wilcox.test(x, y)
# cliff.delta(x, y)
# # parametric
# t.test(x, y)
# cohen.d(x,y)

wilcoxon <- wilcox.test(data$um, c(5,data$dois))
effect   <- res <- cliff.delta(data$um, c(5, data$dois), return.dm=TRUE)

wilcoxon <- wilcox.test(data$um, data$dois)
effect   <- res <- cliff.delta(data$um, data$dois, return.dm=TRUE)

wilcoxon$p.value
effect$estimate
effect$magnitude
cohen.d(x,y)





data <- data.frame(
    prov=c('assetgraph', 'optipng', 'babel-eslint', 'acorn-es7-plugin', 'nodent', 'js-yaml', 'socket.io', 'window-stream', 'request', 'js2coffee', 'broccoli-plugin', 'redis', 'react', 'react-redux-provide', 'imagemin-optipng', 'eslint-config-airbnb-base', 'eslint', 'abstract-iterator', 'grunt-testacular', 'babel-preset-es2015', 'front-matter', 'remark-validate-links', 'jslint', 'collections', 'stylelint', 'foundation-sites', 'backbone', 'mongodb', 'yeoman-environment', 'event-emitter-grouped'),
    qtd_cli=c(16, 11, 21670, 14, 14, 3329, 3752, 2, 23877, 28, 94, 3321, 26881, 27, 82, 3170, 45633, 7, 3, 40413, 232, 94, 308, 92, 978, 87, 1252, 3058, 150, 3),
    time_until=c(2049, 937, 1236, 68, 1052, 1530, 1838, 579, 821, 972, 491, 1919, 1533, 204, 278, 318, 611, 26, 124, 281, 574, 241, 1473, 1567, 509, 580, 957, 771, 574, 1058),
    rele_until=c(385, 8, 33, 8, 155, 46, 84, 14, 54, 16, 7, 89, 59, 39, 8, 27, 48, 7, 4, 17, 9, 6, 51, 51, 17, 25, 18, 109, 19, 8),
    rele=c(432, 14, 106, 25, 175, 60, 106, 25, 118, 32, 7, 99, 118, 101, 15, 31, 160, 10, 5, 33, 26, 8, 62, 62, 107, 31, 28, 286, 26, 9),
    um=c(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    range=c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30)
)

releases <- data$rele
until_bc <- data$rele_until
res      <- round(until_bc*100/releases, 2)

pdf('./providers_releases_bp.pdf')
boxplot(res, frame=F)
dev.off()

pdf('./providers_releases_bc.pdf', width=3, height=3)
ggplot(data, aes(x=range, y=res)) +
  geom_point() +
  geom_segment(aes(x=range, xend=range, y=0, yend=res)) +
  labs(x='', y='%')
dev.off()

count <- 0
for(percentage in res) {
  if(percentage < 50) {
    count <- count + 1
  }
}

count

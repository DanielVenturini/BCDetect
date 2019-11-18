# install.packages('ggplot2')
# install.packages('rjson')
library(ggplot2)
library(rjson)

data <- fromJSON(file='violin.json')

provedores_base   <- data$provedores_base
releases_base     <- data$releases_base
provedores_sample <- data$provedores_sample
releases_sample   <- data$releases_sample

data_provedores <- data.frame(
    data=c(rep('base', length(provedores_base)), rep('sample', length(provedores_sample))),
    value=c(provedores_base, provedores_sample)
)

data_releases <- data.frame(
    data=c(rep('base', length(releases_base)), rep('sample', length(releases_sample))),
    value=c(releases_base, releases_sample)
)

pdf(file='./violin_providers.pdf')
# fill=name allow to automatically dedicate a color for each group
ggplot(data_provedores, aes(x=data, y=value, fill=data)) +
  ggtitle('Provedores') +
  scale_y_log10() +
  geom_violin()

dev.off()

pdf(file='./violin_releases.pdf')
ggplot(data_releases, aes(x=data, y=value, fill=data)) +
  ggtitle('Releases') +
  scale_y_log10() +
  geom_violin()

dev.off()

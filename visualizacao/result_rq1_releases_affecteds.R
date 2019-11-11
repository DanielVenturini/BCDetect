Tamanho = c(140,57,40,60,27,23,24,19,18,10,13,7,8,7,10,6,6,7,4,6,4,2,2,5,1,2,3,4,3,3,1,1,9,13,30,18,50,14,61)
Afetados = c(23,6,14,10,1,3,12,7,2,8,2,6,2,1,1,4,1,1,4,4,2,2,1,1,1,1,2,2,3,2,1,1,2,2,15,15,13,12,2)
Provedores = c(48,102,3,34,37,15,23,5,36,6,16,20,41,15,13,5,3,32,10,27,13,7,4,11,5,10,9,10,76,12,9,15,17,4,49,16,44,10,34)

# normalize the size of affecteds release
Afetados <- (Afetados*100)/Tamanho

pdf(file='./result_rq1_releases_affecteds.pdf')
plot(Provedores, Tamanho, log='xy', type='n')
symbols(Provedores, Tamanho, circles=Afetados, inches=0.1, add=T, fg='#003300')
abline(v=20, col='#69ff33')
abline(h=20, col='#69ff33')
dev.off()
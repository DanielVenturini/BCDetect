# -----------------------
# GRAPH 1
# -----------------------

providers <- c(14, 4, 26, 2, 4, 14, 15, 5, 10, 16, 7, 5, 51, 21, 17, 6, 9, 4, 17, 15, 17, 5, 30, 2, 3, 10, 5, 5, 5, 6, 6, 1, 2, 17, 48, 6, 18, 4, 9, 2, 9, 5, 3, 4, 7, 9, 6, 2, 7, 4, 6, 3, 24, 5, 11, 32, 2, 3, 19, 7, 2, 5, 7, 15, 3, 23, 4, 9, 3, 21, 6, 3, 2, 1, 7, 25, 4, 5, 8, 4, 12, 5, 10, 1, 5, 5, 5, 49, 7, 33, 7, 63, 17, 5, 13, 9, 4, 16, 10, 9, 10, 7, 18, 3, 21, 3, 1, 6, 28, 12, 5, 4, 76, 5, 4, 18, 101, 3, 1, 19, 5, 11, 5, 12, 10, 5, 7, 4, 31, 9, 15, 11, 3, 2, 10, 5, 17, 7, 9, 11, 8, 16, 9, 25, 10, 2, 6, 6, 4, 5, 10, 9, 7, 11, 6, 2, 1, 6, 12, 9, 2, 5, 7, 4, 3, 7, 6, 12, 5, 9, 2, 4, 2, 15, 9, 5, 5, 7, 10, 7, 20, 6, 15, 7, 11, 9, 2, 10, 2, 5, 3, 7, 2, 51, 4, 1, 11, 2, 8, 10, 8, 6, 11, 8, 4, 25, 9, 15, 4, 7, 8, 4, 8, 4, 7, 18, 3, 21, 13, 25, 13, 7, 13, 27, 5, 5, 10, 59, 12, 29, 6, 4, 5, 5, 11, 21, 21, 10, 6, 5, 8, 13, 2, 12, 2, 4, 5, 4, 32, 3, 5, 14, 11, 3, 18, 4, 4, 11, 3, 9, 14, 11, 8, 13, 7, 2, 15, 17, 21, 9, 18, 5, 5, 8, 20, 8, 20, 13, 8, 18, 13, 5, 14, 7, 12, 6, 4, 14, 6, 19, 63, 5, 23, 10, 10, 15, 3, 4, 8, 13, 6, 41, 16, 25, 10, 17, 4, 7, 6, 11, 10, 20, 3, 13, 18, 16, 18, 12, 1, 12, 13, 17, 12, 33, 10, 15, 16, 14, 32, 5, 68, 6, 16, 13, 12, 11, 36, 10, 8, 47, 18, 3, 16, 7, 48, 5, 7, 10, 16, 20, 11, 3, 10, 16, 13, 7, 17, 33, 23, 27, 15, 72, 6, 15, 37, 15, 12, 19, 23, 13, 24, 26, 20, 16, 10, 25, 44, 49, 34, 2, 3, 102, 34, 48)
releases  <- c(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 3, 1, 1, 3, 3, 1, 1, 3, 1, 2, 3, 1, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 3, 1, 2, 3, 2, 3, 3, 2, 1, 2, 2, 3, 4, 4, 2, 3, 4, 1, 3, 2, 1, 3, 3, 1, 1, 1, 3, 2, 4, 3, 1, 2, 1, 1, 3, 2, 2, 2, 3, 1, 1, 4, 3, 3, 1, 3, 4, 4, 3, 2, 2, 5, 3, 4, 3, 1, 2, 2, 1, 4, 4, 1, 1, 3, 1, 4, 2, 1, 4, 1, 4, 5, 4, 3, 4, 4, 3, 2, 5, 3, 1, 6, 5, 2, 4, 1, 2, 4, 3, 6, 4, 4, 6, 1, 2, 4, 5, 3, 6, 6, 3, 1, 7, 7, 5, 5, 5, 4, 7, 8, 6, 6, 8, 4, 2, 2, 3, 7, 2, 6, 3, 5, 6, 8, 2, 2, 5, 4, 8, 8, 1, 5, 8, 6, 2, 7, 7, 4, 4, 6, 6, 4, 5, 6, 3, 4, 10, 4, 4, 6, 8, 6, 3, 8, 3, 4, 12, 7, 8, 11, 5, 9, 4, 9, 7, 4, 5, 8, 12, 10, 8, 13, 13, 11, 9, 13, 13, 7, 6, 1, 7, 9, 2, 10, 12, 14, 6, 8, 14, 10, 9, 11, 18, 4, 1, 13, 13, 11, 20, 15, 10, 18, 7, 9, 12, 18, 14, 14, 22, 12, 10, 18, 6, 21, 19, 9, 4, 12, 16, 1, 3, 3, 1, 19, 7, 15, 12, 24, 17, 25, 23, 5, 23, 27, 13, 27, 22, 10, 30, 25, 18, 47, 43, 4, 13, 50, 30, 61, 18, 40, 69, 61, 161)

data_rq1_graph1 = data.frame(
  x=releases,
  y=providers
)

# -----------------------
# GRAPH 1
# -----------------------

# from packages with no break changes
Tamanho_non_bc    <- c(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,1,1,2,2,1,1,1,2,1,1,2,1,2,2,1,1,1,1,1,2,1,2,1,1,2,1,2,2,2,2,1,2,2,2,2,2,1,1,1,1,1,1,1,3,1,1,3,1,2,3,1,2,2,2,2,2,3,3,2,2,2,3,1,2,3,2,3,3,2,1,2,3,4,1,3,2,1,3,3,1,1,1,3,2,4,3,1,2,1,1,3,2,2,2,1,1,4,3,3,3,4,4,3,2,2,5,3,4,3,1,2,4,4,1,1,4,1,4,4,3,4,4,3,5,3,1,6,5,4,1,2,3,6,4,4,1,2,5,3,6,6,3,1,7,7,5,7,8,6,6,8,4,2,2,3,2,6,3,5,8,2,2,5,4,8,8,1,5,8,6,2,7,7,4,4,6,4,5,6,3,4,6,8,6,3,8,3,4,12,7,8,11,5,9,4,9,4,5,8,12,10,13,13,11,7,6,1,9,2,10,12,14,6,8,14,10,9,11,18,4,1,13,11,20,15,7,9,12,14,22,12,10,18,6,21,9,4,12,16,1,3,3,1,19,7,15,12,17,25,23,5,13,27,22,10,30,25,18,47,43,4,13,18,1,1,2,1,2,4,1,3,1,4,2,5,4,4,1,1,1,2,1,5,1,4,1,2,3,13)
Provedores_non_bc <- c(14,4,26,2,4,14,5,10,16,7,5,51,21,17,6,9,4,17,15,17,5,30,2,3,10,5,5,5,6,6,1,2,17,48,6,18,4,2,9,5,3,4,7,9,6,2,7,4,6,3,24,5,23,4,9,3,21,6,3,2,1,7,25,4,5,8,4,12,5,10,1,5,5,5,49,7,33,7,63,17,5,13,9,4,16,10,9,10,7,18,3,21,3,1,6,28,5,4,5,4,18,101,3,1,19,5,11,5,12,10,5,7,4,31,9,15,11,3,2,10,5,17,7,9,11,2,6,6,4,5,10,9,7,11,6,2,1,6,12,9,2,5,7,4,3,7,6,12,5,2,4,2,15,9,5,7,10,7,20,6,15,7,11,9,2,2,3,7,2,8,10,8,6,8,4,25,9,15,7,8,4,8,4,18,3,21,25,13,7,13,5,5,59,12,29,6,4,5,5,11,21,5,8,13,2,12,2,4,5,4,3,5,14,11,18,4,4,11,3,9,14,11,8,13,7,2,15,17,21,9,18,5,8,20,8,20,13,5,14,7,12,6,4,14,6,19,63,5,23,10,10,3,4,8,13,6,16,25,10,6,11,10,3,13,18,16,18,12,1,12,13,17,12,33,10,15,14,32,5,68,13,12,11,8,47,18,3,16,7,48,7,10,16,20,11,3,10,16,13,7,17,33,27,15,72,6,15,12,19,23,13,24,26,20,16,10,25,2,11,32,5,7,3,25,51,4,1,11,2,10,8,18,3,7,2,8,15,21,19,6,2,16,9,7)

# from packages with break changes
Tamanho    <- c(140,57,40,60,27,23,24,19,18,10,13,7,8,7,10,6,6,7,4,6,4,2,2,5,1,2,3,4,3,3,1,1,9,13,30,18,50,14,61,1)
Afetados   <- c(23,6,14,10,1,3,12,7,2,8,2,6,2,1,1,4,1,1,4,4,2,2,1,1,1,1,2,2,3,2,1,1,2,2,15,15,13,12,2,1)
Provedores <- c(48,102,3,34,37,15,23,5,36,6,16,20,41,15,13,5,3,32,10,27,13,7,4,11,5,10,9,10,76,12,9,15,17,4,49,16,44,10,34,5)

# normalize the size of affecteds release
Afetados <- (Afetados*100)/Tamanho

# -----------------------
# GRAPH 2
# -----------------------

r_gen <- c(Tamanho_non_bc, Tamanho)
p_gen <- c(Provedores_non_bc, Provedores)
# releases and providers with BC
r_bc <- Tamanho
p_bc <- Provedores

# clients_[up|down]_[left|rigth]
# get percentage of clients in each square
c_u_l <- qtd_quad_cli(1, TRUE, r_gen, p_gen)
c_u_r <- qtd_quad_cli(2, TRUE, r_gen, p_gen)
c_d_l <- qtd_quad_cli(3, TRUE, r_gen, p_gen)
c_d_r <- qtd_quad_cli(4, TRUE, r_gen, p_gen)
# get real number of clients in each square
n_u_l <- qtd_quad_cli(1, FALSE, r_gen, p_gen)
n_u_r <- qtd_quad_cli(2, FALSE, r_gen, p_gen)
n_d_l <- qtd_quad_cli(3, FALSE, r_gen, p_gen)
n_d_r <- qtd_quad_cli(4, FALSE, r_gen, p_gen)
# break_[up|down]_[left|rigth]
# break_general_[up|down]_[left|rigth]
b_g_u_l <- round(qtd_quad_cli(1, FALSE, r_bc, p_bc) * 100 / n_u_l, 2)
b_g_u_r <- round(qtd_quad_cli(2, FALSE, r_bc, p_bc) * 100 / n_u_r, 2)
b_g_d_l <- round(qtd_quad_cli(3, FALSE, r_bc, p_bc) * 100 / n_d_l, 2)
b_g_d_r <- round(qtd_quad_cli(4, FALSE, r_bc, p_bc) * 100 / n_d_r, 2)

# -----------------------
# GRAPH 3
# -----------------------

# provs_info <- data.frame(
#     prov=c('assetgraph', 'optipng', 'babel-eslint', 'acorn-es7-plugin', 'nodent', 'js-yaml', 'socket.io', 'window-stream', 'request', 'js2coffee', 'broccoli-plugin', 'redis', 'react', 'react-redux-provide', 'imagemin-optipng', 'eslint-config-airbnb-base', 'eslint', 'abstract-iterator', 'grunt-testacular', 'babel-preset-es2015', 'front-matter', 'remark-validate-links', 'jslint', 'collections', 'stylelint', 'foundation-sites', 'backbone', 'mongodb', 'yeoman-environment', 'event-emitter-grouped'),
#     qtd_cli=c(16, 11, 21670, 14, 14, 3329, 3752, 2, 23877, 28, 94, 3321, 26881, 27, 82, 3170, 45633, 7, 3, 40413, 232, 94, 308, 92, 978, 87, 1252, 3058, 150, 3),
#     time_until=c(2049, 937, 1236, 68, 1052, 1530, 1838, 579, 821, 972, 491, 1919, 1533, 204, 278, 318, 611, 26, 124, 281, 574, 241, 1473, 1567, 509, 580, 957, 771, 574, 1058),
#     rele_until=c(385, 8, 33, 8, 155, 46, 84, 14, 54, 16, 7, 89, 59, 39, 8, 27, 48, 7, 4, 17, 9, 6, 51, 51, 17, 25, 18, 109, 19, 8),
#     rele=c(432, 14, 106, 25, 175, 60, 106, 25, 118, 32, 7, 99, 118, 101, 15, 31, 160, 10, 5, 33, 26, 8, 62, 62, 107, 31, 28, 286, 26, 9),
#     um=c(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
#     range=c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30)
# )

provs_info <- data.frame(
	time_until=c(278, 1, 821, 1838, 1058, 1, 1236, 771, 937, 972, 1567, 2049, 574, 241, 318, 1533, 574, 491, 1, 281, 26, 509, 68, 1473, 1530, 204, 580, 1052, 1, 611, 124, 579, 957, 1919),
	rele=c(15, 24, 118, 106, 9, 67, 106, 286, 14, 32, 62, 432, 26, 8, 31, 118, 26, 7, 196, 33, 10, 107, 25, 62, 60, 101, 31, 175, 44, 160, 5, 25, 28, 99),
	range=c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34),
	qtd_cli=c(50.0, 3.7, 36.84, 8.2, 100.0, 3.28, 47.53, 77.78, 0.62, 80.0, 24.11, 0.62, 66.67, 50.0, 100.0, 57.14, 85.71, 85.71, 13.66, 58.34, 20.0, 15.38, 5.0, 100.0, 8.2, 66.67, 50.0, 30.0, 66.67, 50.0, 100.0, 13.04, 5.56, 10.0),
	um=c(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
	prov=c('imagemin-optipng', 'ember-cli-htmlbars-inline-precompile', 'request', 'socket.io', 'event-emitter-grouped', 'heroku-client', 'babel-eslint', 'mongodb', 'optipng', 'js2coffee', 'collections', 'assetgraph', 'front-matter', 'remark-validate-links', 'eslint-config-airbnb-base', 'react', 'yeoman-environment', 'broccoli-plugin', 'jsdom', 'babel-preset-es2015', 'abstract-iterator', 'stylelint', 'acorn-es7-plugin', 'jslint', 'js-yaml', 'react-redux-provide', 'foundation-sites', 'nodent', 'esprima', 'eslint', 'grunt-testacular', 'window-stream', 'backbone', 'redis'),
	rele_until=c(8, 1, 54, 84, 8, 1, 33, 109, 8, 16, 51, 385, 9, 6, 27, 59, 19, 7, 1, 17, 7, 17, 8, 51, 46, 39, 25, 155, 1, 48, 4, 14, 18, 89)
)

provs_info$percentage <- 100*round(provs_info$rele_until/provs_info$rele, 4)
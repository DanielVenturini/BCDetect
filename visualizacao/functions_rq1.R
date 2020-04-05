# ---------------------------
# FUNCTIONS
# ---------------------------

# return true if the val_rel is horizontally in the quad
horizontal <- function(quad, val_rel, releases) {
	if(quad == 1 || quad == 3) {
		if(val_rel <= ceiling(median(releases))) {
			return(TRUE)
		}
	} else {
		if(val_rel > ceiling(median(releases))) {
			return(TRUE)
		}
	}

	return (FALSE)
}

# return true if the val_prov is vertically in the quad
vertical <- function(quad, val_prov, providers) {
	if(quad == 1 || quad == 2) {
		if(val_prov > ceiling(median(providers))) {
			return(TRUE)
		}
	} else {
		if(val_prov <= ceiling(median(providers))) {
			return(TRUE)
		}
	}

	return (FALSE)
}

# code that calculates the percentage/qtd of clients in one square
# quad = 1 is up left
# quad = 2 is up rigth
# quad = 3 is down left
# quad = 4 is down right
qtd_quad_cli <- function(quad, perc, releases, providers, div=length(releases)) {
	qtd_y <- 0
	for(pos in 1:length(releases)) {
		if(horizontal(quad, releases[pos], releases) && 
			vertical(quad, providers[pos], providers)) {
			qtd_y <- qtd_y + 1
		}
	}

	if(perc) {
		return(round(qtd_y * 100/div, 2))
	} else {
		return(qtd_y)
	}
}

# calculates the percentage/qtd of releases in one square
qtd_quad_rel <- function(quad, perc, releases, providers, div=sum(releases)) {
	qtd_x  <- 0
	qtd_rel <- 0
	for(pos in 1:length(releases)) {
		if(horizontal(quad, releases[pos], releases)) {
			qtd_x <- qtd_x + 1
			if(vertical(quad, providers[pos], providers)) {
				qtd_rel <- qtd_rel + releases[pos]
			}
		}
	}

	if(perc) {
		return(round(qtd_rel * 100/div, 2))
	} else {
		return(qtd_rel)
	}
}

# calculates the percentage/qtd of providers in one square
qtd_quad_prov <- function(quad, perc, releases, providers, div=sum(providers)) {
	qtd_x  <- 0
	qtd_prov <- 0
	for(pos in 1:length(releases)) {
		if(horizontal(quad, releases[pos], releases)) {
			qtd_x <- qtd_x + 1
			if(vertical(quad, providers[pos], providers)) {
				qtd_prov <- qtd_prov + providers[pos]
			}
		}
	}

	if(perc) {
		return(round(qtd_prov * 100/div, 2))
	} else {
		return(qtd_prov)
	}
}

# return the providers of clients that are more than rel releases.
# if you want know how much clients with forty or more releases,
# use more_than_releases(39)
providers_more_than_releases <- function(rel) {
	res <- numeric()
	pos_r <- 0
	for(pos in 1:length(releases)) {
		if(releases[pos] > rel) {
			res[pos_r] <- providers[pos]
			pos_r <- pos_r + 1
		}
	}

	return(res)
}


# return the quadrant name of the client
get_quad_name <- function(pos, releases, providers) {

	quad <- ''
	if(vertical(1, providers[pos], providers)) {
		quad <- 'Sup.'
	} else {
		quad <- 'Inf.'
	}

	if(horizontal(1, releases[pos], releases)) {
		quad <- paste(quad, ' esquerdo')
	} else {
		quad <- paste(quad, ' direito')
	}

	return(quad)
}
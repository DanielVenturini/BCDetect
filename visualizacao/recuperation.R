library(ggplot2)

# ===========
# FIRST TABLE
# ===========

# {'provider': 12, 'client': 30, '--': 3}

# ===========
# FIRST GRAPH
# ===========

provider_days = c(1, 32, 1002, 117, 160, 15, 1002, 4, 7, 20, 462, 38)
client_days   = c(1, 1, 4, 1, 179, 1, 44, 1, 1, 3, 4, 17, 122, 1, 2, 34, 94, 1, 402, 1, 1, 70, 2, 594, 8, 183)

dowgraded_days = c(1, 4, 1, 1, 1, 1, 15, 3, 4, 17, 4, 1, 402, 1, 70, 2, 594, 8, 183)

data <- data.frame()

\begin{table}[!h]
	\begin{tabular}{|l|l|l|l|}
		\hline
		\centering
		                   & Provedor    & Cliente     & Não corrigido                             \\ \hline
		Corrigiu           & 12 (26.7\%) & 30 (66.7\%) & 3 (6.6\%)    \\ \hline
		\textit{Dowgraded} & 2  (4.4\%)  & 20 (44.4\%) & -            \\ \hline
		Dias (mediana)     & 35          & 4           & -            \\ \hline
	\end{tabular}
\caption{Pacote que corrigiu a \textit{breaking change} e a mediana do tempo gasto para ser corrigida}
\label{tab:fix}
\end{table}

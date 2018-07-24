# BCDetect

Simples programa para realizar testes em pacotes NPM. Dado um arquivo CSV com a seguinte estrutura:

```
"client_name", "client_version_num_2", "dependency_name", "dependency_version_max_satisf_2"
```

O BCDetect descarrega o codigo fonte do ```client_name@client_version_num_2``` especifica, e realiza o ```npm test``` para o ```dependency_name@dependency_version_max_satisf_2```. Isto, para cada linha do arquivo CSV/filename.csv. E para cada linha, retorna se o ```npm test``` resultou em erro, breaking change, ou nao.
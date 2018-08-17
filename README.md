# BCDetect

Simples programa para realizar testes em pacotes NPM clonados do GitHub. Dado um arquivo CSV com a seguinte estrutura:

```
"client_name", "dependency_name", "client_version_timestamp_1", "client_version_timestamp_2", "dependency_version_max_satisf_2"
```

O BCDetect clona do GitHub o repositorio ```client_name```. Então usando o ```git checkout `git rev-list -1 --before="client_version_timestamp_2" --after="client_version_timestamp_1" master` ``` para restaurar a árvore de arquivos nesse intervalo de tempo especificado. No ```package.json``` é alterado a versão do  ```dependency_name``` para ```dependency_version_max_satisf_2```. Então é executado o ```npm teste``` para detectar se o pacote 'quebrou' com a atualização.

Os softwares requeridos para o funcionamento do BCDetect são o ```node```, ```npm```, ```tar``` e o ```nyc```. 
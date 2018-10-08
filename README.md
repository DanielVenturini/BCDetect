# BCDetect

Simples programa para realizar testes em pacotes NPM clonados do GitHub. Dado um arquivo CSV com a seguinte estrutura:

```
"client_name", "client_version", "client_timestamp", "client_previous_timestamp", "dependency_name", "dependency_type", "dependency_version_range", "server/path/to/repo.git"
```

O BCDetect clona o pacote ```client_name``` do repositorio ```server/path/to/repo.git```. Então usa o comando ```git checkout `git rev-list -1 --before="client_timestamp" --after="client_previous_timestamp" master` ``` para restaurar a árvore de arquivos nesse intervalo de tempo especificado, que deve ser uma release.

Entao para cada versao do ```client_version```, no ```package.json``` é alterado a versão do  ```dependency_name``` para ```dependency_version_range```. Então é executado o ```npm install``` e apos, o ```npm teste``` para detectar se o pacote 'quebrou' com a atualização.

Os softwares requeridos para o funcionamento do BCDetect são o ```node```, ```npm``` e o ```git```. 
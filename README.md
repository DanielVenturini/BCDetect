# BCDetect

Programa para realizar testes em pacotes NPM clonados do GitHub. Dado um arquivo CSV com a seguinte estrutura:

```
"client_name", "client_version", "client_timestamp", "client_previous_timestamp", "dependency_name", "dependency_type", "dependency_version_range", "server/path/to/repo.git"
```

O BCDetect clona o pacote ```client_name``` do repositorio ```server/path/to/repo.git```. Então usa o comando ```git checkout `git rev-list -1 --before="client_timestamp" --after="client_previous_timestamp" master` ``` para restaurar a árvore de arquivos nesse intervalo de tempo especificado, que deve ser uma release.

Entao para cada versao do ```client_version```, no ```package.json``` é alterado a versão do  ```dependency_name``` para ```dependency_version_range```. Então é executado o ```npm install``` e apos, o ```npm teste``` para detectar se o pacote 'quebrou' com a atualização. A versão do ```NodeJS``` utilizada para executar o ```install``` e o ```test``` é recuperada do ```package.json```. Se não houver, é suposto a versão de acordo com a data da release do cliente.

Se falhar o ```install``` ou o ```test```, então estas operações são novamentes executadas com a versão mais atual do ```NodeJS```, no caso, a 10.7.0. Para evitar esta redundância, utilize a flag ```--one-test```, fazendo com que as operações sejam realizadas apenas com a versão localizada no ```package.json```, ou a mais próxima da data da ```release```.

Os softwares requeridos para o funcionamento do BCDetect são o ```node```, ```npm```, o ```git``` e o ```nvm```.

IMPORTANTE: na primeira vez, utilize a flag ```--node-i``` para verificar e instalar cada versão requerida do ```NodeJs```. Uma vez utilizado esta flag, não há mais a necessidade de utilizar novamente.

Utilize a flag ```--only``` seguido de uma versao ```x.y.z``` para executar apenas para uma versao específica do pacote.

Para testes unitários utilizando a flag ```--only```, ou para algum motivo específico, a flag ```--no-del``` pode ser usada para não apagar a pasta clonada do repositório ao findar a execução, e ficara dentro da pasta ```workspace/```, onde foi clonado. Também a flag ```--no-clone``` pode ser usada se o repositório já estiver previamente clonado dentro da pasta ```workspace/```.
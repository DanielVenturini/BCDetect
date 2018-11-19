# BCDetect

Programa para instalar dependências e realizar testes em pacotes NPM clonados do GitHub. Dado um arquivo ```.csv``` dentro da pasta ```./CSV/``` com a seguinte estrutura:

```
"client_name", "client_version", "client_timestamp", "client_previous_timestamp", "dependency_name", "dependency_type", "dependency_version_range", "dependency_resolved_version_change", "server/path/to/repo.git"
```

O BCDetect clona o pacote ```client_name``` do repositorio ```server/path/to/repo.git```. Então usa o comando ```git checkout `git rev-list -1 --before="client_timestamp" --after="client_previous_timestamp" master` ``` para restaurar a árvore de arquivos nesse intervalo de tempo especificado, que deve ser uma release.

Entao para cada versao do ```client_version```, no ```package.json``` é alterado a versão do  ```dependency_name``` para ```dependency_version_range```. Então é executado o ```npm install``` e apos, o ```npm teste``` para detectar se o pacote 'quebrou' com a atualização. A versão do ```NodeJS``` utilizada para executar o ```install``` e o ```test``` é recuperada do ```package.json```. Se não houver, é suposto a versão de acordo com a data da release do cliente.

Se falhar o ```install``` ou o ```test```, então estas operações são novamentes executadas com a versão mais atual do ```NodeJS```, no caso, a 10.7.0. Para evitar esta redundância, utilize a flag ```--one-test```, fazendo com que as operações sejam realizadas apenas com a versão localizada no ```package.json```, ou a mais próxima da data da ```release```.

Os softwares requeridos para o funcionamento do BCDetect são o ```node```, ```npm```, o ```git``` e o ```nvm```.

## Flags

- ```--node-i``` IMPORTANTE: utilize a flag  para verificar e instalar cada versão requerida do ```NodeJs```. Uma vez utilizado esta flag, não há mais a necessidade de utilizar novamente, pois todas as versões já estarão instaladas.

- ```--no-del``` evita que o ```BCDetect``` apague o repositório clonado. Por padrão, o repositório que foi clonado em ```./workspace/repo/``` é excluido ao finalizar todas as releases, porém com esta flag, o repositório é mantido.

- ```--no-clone``` evita que o ```BCDetect``` clone o repositório do ```GitHub```. Entretanto, o repositório deve estar previamente clonado na pasta ```./workspace/repo/```.

- ```--only``` seguida de uma versão ```x.y.z``` executa apenas o ```install``` e o ```test``` para a versão específicada do pacote.

As flags podem ser inseridas em qualquer posição dos parâmetros e todas as flags podem ser usadas ao mesmo tempo, entretanto, a flag ```--only``` deve ser seguida da versão ```x.y.z```. Por exemplo: ```python3 BCDetect.py pacote.csv --no-clone --only 2.4.5 --no-del```.
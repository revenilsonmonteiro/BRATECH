# ATCS Creator Intelligence v1.0
MVP local-first para executar no Termux (Android) ou em Python 3 no computador.

## O que já faz
- Gera pacotes editoriais em Markdown para vídeos completos e Shorts.
- Inclui títulos candidatos, roteiro, thumbnail, descrição, Shorts derivados, hipótese comercial e checklist.
- Mantém um banco local de pautas em JSON.
- Registra métricas de vídeos e custos em CSV.
- Exibe um relatório simples de visualizações, vendas, receita e custos.
- Usa somente a biblioteca padrão do Python; não exige API key nem dependências externas.

## Instalação no Termux
Abra o Termux e execute:

```bash
pkg update
pkg install python unzip
```

Extraia o ZIP e entre na pasta do projeto. Se o arquivo estiver em Downloads:

```bash
termux-setup-storage
cd ~/storage/downloads
unzip ATCS_Creator_Intelligence_v1.zip
cd ATCS_Creator_Intelligence
python atcs_creator.py
```

Se você extrair o arquivo em outra pasta, ajuste o caminho `cd` para essa pasta.

## Uso
Menu interativo:

```bash
python atcs_creator.py
```

Gerar um pacote de vídeo completo:

```bash
python atcs_creator.py --generate "Como monitorar memória e processos no Android com Termux" --format long --audience "Iniciantes em Linux e usuários Android" --problem "Entender quais métricas podem ser consultadas sem root"
```

Gerar um Short:

```bash
python atcs_creator.py --generate "3 comandos Linux úteis no Android" --format short --audience "Iniciantes em Termux" --problem "Aprender comandos básicos"
```

Listar pautas:

```bash
python atcs_creator.py --ideas
```

Relatório:

```bash
python atcs_creator.py --report
```

Os pacotes ficam na pasta `output/`. Os dados ficam na pasta `data/`.

## Estrutura
- `atcs_creator.py`: aplicação CLI.
- `data/config.json`: identidade e preferências.
- `data/ideas.json`: banco inicial de pautas.
- `data/metrics.csv`: métricas inseridas manualmente.
- `data/costs.csv`: custos inseridos manualmente.
- `output/`: roteiros e pacotes gerados.

## Importante
Esta versão não publica vídeos, não consulta tendências em tempo real e não se conecta automaticamente ao YouTube. É uma base operacional local. Os números de desempenho devem ser copiados do YouTube Studio; custos e vendas devem ser registrados com dados reais.

Antes de publicar:
1. Teste os comandos e demonstrações no ambiente indicado.
2. Confirme as afirmações técnicas em documentação confiável.
3. Não mostre senhas, tokens ou dados privados.
4. Não prometa renda nem resultados garantidos.
5. Adicione fontes reais consultadas e links apenas quando estiverem disponíveis.

## Próximas evoluções possíveis
1. Importar métricas a partir de CSV exportado do YouTube Studio.
2. Adicionar pesquisa com fontes verificáveis.
3. Integrar um modelo de linguagem via API, com chave guardada em variável de ambiente.
4. Preparar integração oficial com YouTube Data API para operações autorizadas.
5. Criar painel local depois de validar a utilidade do MVP.
# BRATECH
# BRATECH

# Predição de Séries Temporais em Dados EEG com MLP
Predição de séries temporais em dados EEG de sujeitos dos grupos Controle e Talentosos com experimentos em ERP visual usando MLP.

## Introdução
Este projeto visa prever séries temporais de dados EEG utilizando um Perceptron Multicamadas (MLP). Dados foram coletados em experimentos de ERP visual com sujeitos dos grupos de Controle e Talentosos.

## Funcionalidades
- Carregamento de dados EEG em formato BrainVision (.vhdr, .eeg, .vmrk)
- Pré-processamento: filtragem, remoção de artefatos e segmentação
- Treinamento de modelos MLP para predição de séries temporais
- Visualização dos sinais de EEG e das previsões do modelo

## Instalação
Para instalar as dependências, execute:
```bash
pip install -r requirements.txt
```

## Uso
Para pré-processar os dados, treinar o modelo e visualizar os resultados, execute os notebooks correspondentes ou o script principal:
```bash
python main.py
```

### Notebooks
- `predict_erp.ipynb`: Carregamento, filtragem e segmentação dos dados EEG, configuração e treinamento do modelo MLP, e avaliação das previsões.
- `visualization_outputs_eeg.ipynb`: Visualização dos sinais de EEG e das previsões do modelo.

## Estrutura do Projeto
```
datasets/           # Conjuntos de dados de EEG
notebooks/          # Notebooks Jupyter para experimentos e testes
src/                # Código-fonte do projeto
main.py             # Script principal para execução do projeto
requirements.txt    # Dependências do projeto
```

## Requisitos
- `numpy`
- `pandas`
- `scikit-learn`
- `matplotlib`
- `tensorflow`
- `mne`

## Autor
- [@abner-lucas](https://github.com/abner-lucas)

## Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo [MIT](https://choosealicense.com/licenses/mit/) para mais detalhes.

### Detalhes dos Notebooks

#### `predict_erp.ipynb`
- **Carregamento de Dados**: Importa arquivos .vhdr, .eeg, .vmrk.
- **Filtragem e Remoção de Artefatos**: Aplicação de filtros de banda-passante e remoção de artefatos.
- **Segmentação**: Criação de épocas baseadas em eventos.
- **Configuração do Modelo**: Definição do MLP com Keras/TensorFlow.
- **Divisão de Dados**: Separação dos dados em conjuntos de treino e teste.
- **Treinamento e Validação**: Treinamento do modelo com validação cruzada e avaliação de desempenho.
- **Visualização de Resultados**: Plotagem das previsões do modelo contra os dados reais.

#### `visualization_outputs_eeg.ipynb`
- **Visualização de Dados**: Plotagem dos sinais EEG pré-processados.
- **Análise de Previsões**: Comparação das previsões do modelo com os dados reais e análise de erros.

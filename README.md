# 📦 StockWise
### Sistema de Gestão de Estoque e Vendas para Pequenos Empreendimentos

**Projeto Integrador | Engenharia de Software | Universidade Santo Amaro (UNISA) | 2026**

<img width="1746" height="752" alt="image" src="https://github.com/user-attachments/assets/1682a9dd-da1c-4807-93f0-37bdf6f1756f" />

## 📖 Sobre o projeto

O **StockWise** é uma aplicação web desenvolvida em Python, utilizando Streamlit e SQLite, com o objetivo de facilitar a gestão de produtos, estoques e vendas de pequenos empreendimentos comerciais.

O sistema foi desenvolvido como parte do Projeto Integrador do curso de Engenharia de Software da Universidade Santo Amaro (UNISA), dentro da temática **Inovação e Transformação Digital**.

A proposta surgiu da necessidade de oferecer aos pequenos comerciantes uma alternativa acessível para substituir processos manuais de gerenciamento, proporcionando maior organização das informações e apoio à tomada de decisões.

### 🎯 Objetivos

- Facilitar o cadastro e a organização de produtos.
- Monitorar quantidades disponíveis em estoque.
- Registrar vendas e atualizar automaticamente as quantidades.
- Identificar produtos que necessitam de reposição.
- Acompanhar custos, preços de venda e margens brutas.
- Disponibilizar indicadores financeiros por meio de um dashboard interativo.

## 🌐 Demonstração online

**[Acessar o StockWise](https://stockwise-unisa.streamlit.app/)**

> **Aviso:** esta aplicação é um protótipo acadêmico. Os produtos, vendas e indicadores são fictícios. A versão publicada utiliza SQLite com persistência não garantida após reinicializações da hospedagem.

---

## ✨ Funcionalidades

### 📊 1. Dashboard financeiro

O dashboard apresenta uma visão consolidada do desempenho comercial, permitindo acompanhar indicadores relevantes para a gestão do estabelecimento.

**Indicadores disponíveis:**
- Faturamento total.
- Lucro bruto estimado.
- Investimento em estoque.
- Quantidade de unidades vendidas.
- Quantidade de produtos cadastrados.
- Total de vendas realizadas.
- Produtos com estoque baixo.

Também são apresentados gráficos de faturamento diário e um ranking dos cinco produtos mais vendidos.

<img width="1775" height="717" alt="image" src="https://github.com/user-attachments/assets/7544a683-d2ae-4b3b-9b26-1f7bf2ca8efe" />


### 📦 2. Cadastro de produtos

O sistema permite cadastrar produtos com as informações necessárias para o controle de estoque e a análise financeira.

**Campos disponíveis:**
- Nome do produto.
- Preço de custo.
- Preço de venda.
- Quantidade inicial.
- Estoque mínimo.

Foram implementadas validações para evitar nomes duplicados, além de alertas para produtos cadastrados com preço de venda inferior ou igual ao custo.

<img width="1372" height="677" alt="image" src="https://github.com/user-attachments/assets/183c3a56-9c7f-4292-9a6c-8afdcbedf775" />

### 📋 3. Consulta e gerenciamento de estoque

A área de estoque permite consultar todos os produtos cadastrados, com informações sobre quantidades, custos, preços e valores financeiros.

O sistema disponibiliza pesquisa por nome, filtros por situação do estoque e diferentes opções de ordenação.

Os produtos são classificados como:
- Normal.
- Estoque baixo.
- Esgotado.

<img width="1810" height="632" alt="image" src="https://github.com/user-attachments/assets/61276e4d-22b9-4da5-a0cd-ef483d66d19c" />

<img width="1797" height="492" alt="image" src="https://github.com/user-attachments/assets/896e1e37-15d8-49eb-9ba0-320d53e6ff58" />


### ✏️ 4. Edição de produtos

Os dados cadastrais podem ser atualizados, permitindo modificar nomes, preços e limites mínimos de estoque.

A atualização das quantidades disponíveis é realizada separadamente, por meio da funcionalidade de reposição.

<img width="1493" height="651" alt="image" src="https://github.com/user-attachments/assets/bfdcbc31-48b8-4a59-826b-6b39481e2654" />


### 📥 5. Reposição e movimentação de estoque

O StockWise permite registrar a entrada de novas unidades de produtos já cadastrados.

Cada reposição atualiza automaticamente a quantidade disponível e gera um registro no histórico de movimentações.

O histórico também contempla as saídas de produtos decorrentes das vendas.

<img width="1482" height="667" alt="image" src="https://github.com/user-attachments/assets/2d730a24-ebe6-40f1-906c-5bcd6ba5f924" />

<img width="1487" height="496" alt="image" src="https://github.com/user-attachments/assets/7bd6df2e-20f6-4300-a9d6-5276d5192b4a" />


### 🛒 6. Registro de vendas

O sistema possui um carrinho de compras que permite selecionar diferentes produtos e quantidades em uma mesma operação.

Ao finalizar uma venda, o StockWise:
1. Verifica a disponibilidade dos produtos.
2. Calcula o valor total.
3. Registra a operação no banco de dados.
4. Atualiza automaticamente o estoque.
5. Armazena as informações para consultas futuras.

O histórico de vendas preserva os preços e custos registrados no momento de cada transação.

<img width="1523" height="347" alt="image" src="https://github.com/user-attachments/assets/0efcd709-4ff4-41a8-a29e-5d84ee7d9080" />

<img width="1800" height="467" alt="image" src="https://github.com/user-attachments/assets/0228b19c-1a08-485a-8050-99b718b077f2" />


<img width="1822" height="462" alt="image" src="https://github.com/user-attachments/assets/e918628a-9a89-4091-b8da-1f47e1fa3693" />


---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Lógica de negócio e desenvolvimento da aplicação |
| Streamlit | Construção da interface web |
| SQLite | Armazenamento e gerenciamento dos dados |
| Pandas | Manipulação e análise de informações |
| Plotly | Criação de gráficos interativos |
| Git e GitHub | Versionamento e hospedagem do código |
| Streamlit Community Cloud | Hospedagem da aplicação web |

## 🏗️ Arquitetura do sistema

O StockWise utiliza uma arquitetura simplificada, adequada ao escopo acadêmico, com separação entre interface, lógica de negócio e acesso ao banco de dados.

### Estrutura principal

```text
stockwise/
│
├── app.py
├── database.py
├── inicializar_demo.py
├── demo_seed.sql
├── requirements.txt
└── .gitignore
```

**Descrição dos arquivos:**

- `app.py`: interface, navegação e interação com o usuário.
- `database.py`: operações SQL e regras relacionadas à persistência dos dados.
- `inicializar_demo.py`: inicialização automática da base de demonstração.
- `demo_seed.sql`: estrutura e registros fictícios utilizados no ambiente demonstrativo.
- `requirements.txt`: dependências necessárias para executar a aplicação.
- `.gitignore`: definição de arquivos que não devem ser versionados.

### Banco de dados

A aplicação utiliza o SQLite, com tabelas relacionadas para gerenciar produtos e transações comerciais.

As principais entidades são:

- **Produtos:** informações cadastrais, preços e quantidades.
- **Vendas:** registros das operações comerciais.
- **Itens de venda:** produtos e quantidades relacionados a cada venda.
- **Movimentações de estoque:** histórico de entradas e saídas.


---

## 🧪 Testes e validações

O desenvolvimento envolveu testes funcionais para verificar o comportamento da aplicação e a integridade das operações.

**Cenários avaliados:**

| Teste | Resultado |
|---|---|
| Cadastro de produtos | Aprovado |
| Bloqueio de nomes duplicados | Aprovado |
| Edição de produtos | Aprovado |
| Alertas de margem negativa | Aprovado |
| Reposição de estoque | Aprovado |
| Registro de vendas com múltiplos produtos | Aprovado |
| Atualização automática do estoque | Aprovado |
| Pesquisa e filtros de produtos | Aprovado |
| Carregamento do dashboard | Aprovado |
| Funcionamento da aplicação publicada | Aprovado |

### Base de demonstração

Para os testes, foi utilizada uma base fictícia composta por:

- **30 produtos cadastrados.**
- **180 vendas simuladas.**
- **90 dias de histórico comercial.**
- Registros de entrada e saída de mercadorias.
- Indicadores financeiros calculados a partir das transações.

Os dados têm finalidade exclusivamente demonstrativa e não representam operações comerciais reais.

---

## 💻 Como executar localmente

### Pré-requisitos

- Python instalado.
- Acesso ao terminal.
- Git instalado para clonagem do repositório.

**1. Clone o repositório:**

```bash
git clone https://github.com/hbozaipo/stockwise.git
```

**2. Acesse o diretório:**

```bash
cd stockwise
```

**3. Instale as dependências:**

```bash
python -m pip install -r requirements.txt
```

**4. Execute a aplicação:**

```bash
python -m streamlit run app.py
```

Após iniciar, acesse:

`http://localhost:8501`

Quando o banco local ainda não existe, a aplicação inicializa automaticamente os dados fictícios de demonstração.

---

## 🔮 Melhorias futuras

O StockWise foi desenvolvido como um Produto Mínimo Viável (MVP), com possibilidades de ampliação em versões futuras.

Entre as melhorias previstas estão:

- Autenticação e gerenciamento de usuários.
- Exportação de relatórios em Excel e CSV.
- Integração com leitores de código de barras.
- Cadastro e gerenciamento de fornecedores.
- Controle de validade dos produtos.
- Relatórios financeiros mais detalhados.
- Persistência de dados em banco PostgreSQL hospedado.
- Suporte a múltiplos estabelecimentos.
- Aperfeiçoamentos de segurança e controle de permissões.

---

## 🌱 Impacto e transformação digital

O StockWise busca demonstrar como soluções tecnológicas acessíveis podem contribuir para a modernização dos processos de pequenos negócios.

Ao centralizar informações de produtos, estoques e vendas em uma aplicação web, a ferramenta proporciona maior visibilidade sobre as operações e auxilia na identificação de oportunidades de melhoria.

O projeto está relacionado aos seguintes Objetivos de Desenvolvimento Sustentável (ODS):

- **ODS 8:** Trabalho Decente e Crescimento Econômico.
- **ODS 9:** Indústria, Inovação e Infraestrutura.
- **ODS 12:** Consumo e Produção Responsáveis.

---

## 🎓 Informações acadêmicas

**Instituição:** Universidade Santo Amaro (UNISA)

**Curso:** Engenharia de Software

**Projeto:** Projeto Integrador / Projeto de Extensão

**Temática:** Inovação e Transformação Digital para Pequenos Empreendimentos

**Ano:** 2026

---

## 👩‍💻 Desenvolvimento

**Heloisa Bozaipo**

Engenharia de Software — Universidade Santo Amaro (UNISA)

[Aplicação Online](https://stockwise-unisa.streamlit.app/) | [Repositório GitHub](https://github.com/hbozaipo/stockwise)

---

*StockWise — Gestão simples, decisões inteligentes.*

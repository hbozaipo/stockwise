import streamlit as st
import pandas as pd
import plotly.express as px

from database import (
    criar_tabelas,
    cadastrar_produto,
    listar_produtos,
    atualizar_produto,
    repor_estoque,
    listar_movimentacoes,
    registrar_venda,
    listar_vendas,
    listar_itens_venda,
    indicadores_dashboard,
    dados_graficos
)

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="StockWise",
    page_icon="📦",
    layout="wide"
)

criar_tabelas()

# ==========================================
# ESTILO DARK CORPORATE
# ==========================================

st.markdown("""
<style>
    /* Fundo geral */
    .stApp {
        background-color: #0d1117;
        color: #f5f5f5;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #161b22 0%, #11151b 100%);
        border-right: 1px solid #2a2f3a;
    }

    section[data-testid="stSidebar"] * {
        color: #f5f5f5 !important;
    }

    /* Títulos */
    h1, h2, h3 {
        color: #f8f8f8;
    }

    /* Cards personalizados */
    .card {
        background: linear-gradient(145deg, #161b22, #1c2128);
        border: 1px solid #2b313c;
        border-left: 5px solid #8b1e3f;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.25);
        margin-bottom: 12px;
    }

    .card-title {
        font-size: 0.95rem;
        color: #c9d1d9;
        margin-bottom: 8px;
    }

    .card-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
    }

    /* Botões */
    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button {
        background-color: #8b1e3f !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 0.6rem 1rem !important;
        font-weight: 600 !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stFormSubmitButton > button:hover {
        background-color: #a1284d !important;
        color: white !important;
    }

    /* Inputs */
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"],
    .stMultiSelect div[data-baseweb="select"] {
        background-color: #161b22 !important;
        color: #f5f5f5 !important;
        border-radius: 10px !important;
    }

    /* Labels pequenos */
    .muted {
        color: #aab2bf;
        font-size: 0.92rem;
    }

    /* Linha divisória */
    hr {
        border-color: #2b313c;
    }

    /* Ajustes para tabelas */
    .stDataFrame, .stTable {
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================

def moeda(valor):
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"

def mostrar_card(titulo, valor):
    st.markdown(f"""
        <div class="card">
            <div class="card-title">{titulo}</div>
            <div class="card-value">{valor}</div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.markdown("## 📦 StockWise")
    st.markdown(
        "<div class='muted'>Sistema de Gestão de Estoque</div>",
        unsafe_allow_html=True
    )
    st.divider()

    pagina = st.radio(
        "Navegação",
        [
            "📊 Dashboard",
            "➕ Cadastrar produto",
            "📋 Consultar estoque",
            "✏️ Editar produto",
            "📦 Repor estoque",
            "🛒 Vendas"
        ]
    )


    st.divider()
    
    st.markdown("UNISA - Projeto Integrador")
    
    st.caption("Heloisa Amorim - 5747031")
    st.caption("Engenharia de Software")
    st.caption("2026")
    
# ==========================================
# CABEÇALHO PRINCIPAL
# ==========================================

st.title("📦 StockWise")
st.caption("Sistema de Gestão de Estoque")

# ==========================================
# 1. DASHBOARD
# ==========================================

if pagina == "📊 Dashboard":
    st.subheader("📊 Dashboard financeiro")
    st.caption("Visão geral do desempenho do estoque e das vendas")

    indicadores = indicadores_dashboard()
    graficos = dados_graficos()

    # Cards financeiros
    st.markdown("### Resumo financeiro")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        mostrar_card("💰 Faturamento", moeda(indicadores["faturamento"]))

    with col2:
        mostrar_card("📈 Lucro bruto estimado", moeda(indicadores["lucro_bruto"]))

    with col3:
        mostrar_card("📦 Investimento em estoque", moeda(indicadores["investimento_estoque"]))

    with col4:
        mostrar_card("🛒 Unidades vendidas", str(indicadores["unidades_vendidas"]))

    st.markdown("### Resumo operacional")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        mostrar_card("Produtos cadastrados", str(indicadores["total_produtos"]))

    with col2:
        mostrar_card("Unidades disponíveis", str(indicadores["unidades_estoque"]))

    with col3:
        mostrar_card("Vendas realizadas", str(indicadores["total_vendas"]))

    with col4:
        mostrar_card("⚠️ Estoque baixo", str(indicadores["estoque_baixo"]))

    st.divider()

    st.markdown("### Análise de vendas")
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.markdown("#### Faturamento por dia")
        dados = graficos["faturamento_diario"]

        if dados:
            df_faturamento = pd.DataFrame(
                dados,
                columns=["Data", "Faturamento"]
            )
            df_faturamento["Data"] = pd.to_datetime(df_faturamento["Data"])

            fig = px.line(
                df_faturamento,
                x="Data",
                y="Faturamento",
                markers=True
            )

            fig.update_traces(
                line=dict(color="#9b3758", width=3),
                marker=dict(color="#c04a72", size=8)
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0d1117",
                plot_bgcolor="#0d1117",
                xaxis_title="Data",
                yaxis_title="Faturamento (R$)",
                margin=dict(l=10, r=10, t=20, b=10)
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Ainda não existem vendas.")

    with col_graf2:
        st.markdown("#### Top 5 produtos vendidos")
        dados = graficos["mais_vendidos"]

        if dados:
            df_ranking = pd.DataFrame(
                dados,
                columns=["Produto", "Quantidade"]
            )

            fig = px.bar(
                df_ranking,
                x="Quantidade",
                y="Produto",
                orientation="h"
            )

            fig.update_traces(marker_color="#9b3758")

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0d1117",
                plot_bgcolor="#0d1117",
                yaxis=dict(autorange="reversed"),
                xaxis_title="Unidades vendidas",
                yaxis_title="",
                margin=dict(l=10, r=10, t=20, b=10)
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum produto vendido ainda.")

    st.divider()

    st.markdown("### ⚠️ Produtos com estoque baixo")
    produtos_baixos = graficos["estoque_baixo"]

    if produtos_baixos:
        df_alertas = pd.DataFrame(
            produtos_baixos,
            columns=[
                "Produto",
                "Quantidade atual",
                "Estoque mínimo"
            ]
        )

        st.dataframe(
            df_alertas,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("Todos os produtos estão acima do estoque mínimo!")

# ==========================================
# 2. CADASTRAR PRODUTO
# ==========================================

elif pagina == "➕ Cadastrar produto":
    st.subheader("➕ Cadastrar novo produto")

    with st.form("form_produto", clear_on_submit=True):
        nome = st.text_input("Nome do produto")

        col1, col2 = st.columns(2)

        with col1:
            custo = st.number_input(
                "Preço de custo (R$)",
                min_value=0.0,
                step=0.01,
                format="%.2f"
            )

            quantidade = st.number_input(
                "Quantidade inicial",
                min_value=0,
                step=1
            )

        with col2:
            venda = st.number_input(
                "Preço de venda (R$)",
                min_value=0.0,
                step=0.01,
                format="%.2f"
            )

            minimo = st.number_input(
                "Estoque mínimo",
                min_value=0,
                value=5,
                step=1
            )

        salvar = st.form_submit_button("💾 Salvar produto")


        if salvar:
            if not nome.strip():
                st.error("Informe o nome do produto.")
        
            else:
                try:
                    cadastrar_produto(
                        nome.strip(),
                        custo,
                        venda,
                        quantidade,
                        minimo
                    )
        
                    st.success("Produto cadastrado com sucesso!")
        
                    # Verifica a margem do produto
                    if venda < custo:
                        prejuizo = custo - venda
        
                        st.warning(
                            f"⚠️ Atenção! O preço de venda está "
                            f"abaixo do custo. Diferença negativa "
                            f"de R$ {prejuizo:.2f} por unidade."
                        )
        
                    elif venda == custo:
                        st.info(
                            "O produto foi cadastrado sem "
                            "margem bruta de lucro."
                        )
        
                except ValueError as erro:
                    st.error(str(erro))



# ==========================================
# 3. CONSULTAR ESTOQUE
# ==========================================

elif pagina == "📋 Consultar estoque":

    st.subheader("📋 Gestão de estoque")
    st.caption("Consulte, pesquise e analise seus produtos.")

    produtos = listar_produtos()

    if produtos:

        colunas = [
            "ID",
            "Produto",
            "Custo (R$)",
            "Venda (R$)",
            "Quantidade",
            "Estoque mínimo"
        ]

        df = pd.DataFrame(produtos, columns=colunas)

        # ==================================
        # CÁLCULOS
        # ==================================

        df["Lucro bruto unitário (R$)"] = (
            df["Venda (R$)"] - df["Custo (R$)"]
        ).round(2)

        df["Investimento em estoque (R$)"] = (
            df["Custo (R$)"] * df["Quantidade"]
        ).round(2)

        df["Valor potencial de venda (R$)"] = (
            df["Venda (R$)"] * df["Quantidade"]
        ).round(2)

        df["Status"] = df.apply(
            lambda linha: (
                "🔴 Esgotado"
                if linha["Quantidade"] == 0
                else "⚠️ Estoque baixo"
                if linha["Quantidade"] <= linha["Estoque mínimo"]
                else "✅ Normal"
            ),
            axis=1
        )

        # ==================================
        # FILTROS
        # ==================================

        st.markdown("### Pesquisar produtos")

        busca = st.text_input(
            "Buscar por nome",
            placeholder="Ex.: Coca-Cola, Arroz, Café..."
        )

        col1, col2 = st.columns(2)

        with col1:
            filtro_status = st.selectbox(
                "Situação do estoque",
                [
                    "Todos",
                    "Normal",
                    "Estoque baixo",
                    "Esgotado"
                ]
            )

        with col2:
            ordenar_por = st.selectbox(
                "Ordenar por",
                [
                    "Nome (A-Z)",
                    "Menor quantidade",
                    "Maior quantidade",
                    "Menor preço",
                    "Maior preço",
                    "Maior lucro unitário"
                ]
            )

        # ==================================
        # APLICAR FILTROS
        # ==================================

        df_filtrado = df.copy()

        if busca.strip():
            df_filtrado = df_filtrado[
                df_filtrado["Produto"].str.contains(
                    busca.strip(),
                    case=False,
                    regex=False,
                    na=False
                )
            ]

        if filtro_status != "Todos":

            status_map = {
                "Normal": "✅ Normal",
                "Estoque baixo": "⚠️ Estoque baixo",
                "Esgotado": "🔴 Esgotado"
            }

            df_filtrado = df_filtrado[
                df_filtrado["Status"]
                == status_map[filtro_status]
            ]

        ordenacoes = {
            "Nome (A-Z)": ("Produto", True),
            "Menor quantidade": ("Quantidade", True),
            "Maior quantidade": ("Quantidade", False),
            "Menor preço": ("Venda (R$)", True),
            "Maior preço": ("Venda (R$)", False),
            "Maior lucro unitário": (
                "Lucro bruto unitário (R$)",
                False
            )
        }

        coluna, crescente = ordenacoes[ordenar_por]

        df_filtrado = df_filtrado.sort_values(
            by=coluna,
            ascending=crescente
        )

        # ==================================
        # INDICADORES DINÂMICOS
        # ==================================

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            mostrar_card(
                "Produtos encontrados",
                str(len(df_filtrado))
            )

        with col2:
            mostrar_card(
                "Unidades disponíveis",
                str(int(df_filtrado["Quantidade"].sum()))
            )

        with col3:
            investimento = df_filtrado[
                "Investimento em estoque (R$)"
            ].sum()

            mostrar_card(
                "Investimento em estoque",
                moeda(investimento)
            )

        # ==================================
        # TABELA
        # ==================================

        st.markdown("### Produtos cadastrados")

        if df_filtrado.empty:
            st.info(
                "Nenhum produto encontrado "
                "com os filtros selecionados."
            )

        else:
            st.dataframe(
                df_filtrado,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Custo (R$)": st.column_config.NumberColumn(
                        "Custo (R$)",
                        format="R$ %.2f"
                    ),
                    "Venda (R$)": st.column_config.NumberColumn(
                        "Venda (R$)",
                        format="R$ %.2f"
                    ),
                    "Lucro bruto unitário (R$)":
                        st.column_config.NumberColumn(
                            "Lucro bruto unitário (R$)",
                            format="R$ %.2f"
                        ),
                    "Investimento em estoque (R$)":
                        st.column_config.NumberColumn(
                            "Investimento em estoque (R$)",
                            format="R$ %.2f"
                        ),
                    "Valor potencial de venda (R$)":
                        st.column_config.NumberColumn(
                            "Valor potencial de venda (R$)",
                            format="R$ %.2f"
                        )
                }
            )

    else:
        st.info("Nenhum produto cadastrado ainda.")


# ==========================================
# 4. EDITAR PRODUTO
# ==========================================

elif pagina == "✏️ Editar produto":
    st.subheader("✏️ Editar produto")

    produtos = listar_produtos()

    if not produtos:
        st.info("Nenhum produto cadastrado.")
    else:
        produtos_por_id = {
            produto[0]: produto
            for produto in produtos
        }

        id_produto = st.selectbox(
            "Selecione o produto",
            options=list(produtos_por_id.keys()),
            format_func=lambda id_: f"{id_} - {produtos_por_id[id_][1]}"
        )

        produto = produtos_por_id[id_produto]

        st.caption(f"Quantidade atual em estoque: {produto[4]}")

        with st.form(f"editar_produto_{id_produto}"):
            nome_editado = st.text_input(
                "Nome do produto",
                value=produto[1]
            )

            col1, col2 = st.columns(2)

            with col1:
                custo_editado = st.number_input(
                    "Preço de custo (R$)",
                    min_value=0.0,
                    value=float(produto[2]),
                    step=0.01,
                    format="%.2f"
                )

            with col2:
                venda_editada = st.number_input(
                    "Preço de venda (R$)",
                    min_value=0.0,
                    value=float(produto[3]),
                    step=0.01,
                    format="%.2f"
                )

            minimo_editado = st.number_input(
                "Estoque mínimo",
                min_value=0,
                value=int(produto[5]),
                step=1
            )

            salvar_edicao = st.form_submit_button("💾 Salvar alterações")


            if salvar_edicao:
                if not nome_editado.strip():
                    st.error("O nome do produto é obrigatório.")
            
                else:
                    try:
                        atualizado = atualizar_produto(
                            id_produto,
                            nome_editado.strip(),
                            custo_editado,
                            venda_editada,
                            minimo_editado
                        )
            
                        if atualizado:
                            st.success("Produto atualizado com sucesso!")
                        
                            if venda_editada < custo_editado:
                                st.warning(
                                    "⚠️ O preço de venda está abaixo "
                                    "do preço de custo!"
                                )
                        
                            elif venda_editada == custo_editado:
                                st.info(
                                    "O produto está sem margem bruta "
                                    "de lucro."
                                )       
                        else:
                            st.error(
                                "Não foi possível atualizar o produto."
                            )
            
                    except ValueError as erro:
                        st.error(str(erro))


# ==========================================
# 5. REPOR ESTOQUE
# ==========================================

elif pagina == "📦 Repor estoque":
    st.subheader("📦 Reposição de estoque")

    produtos = listar_produtos()

    if not produtos:
        st.info("Cadastre um produto primeiro.")
    else:
        produtos_por_id = {
            produto[0]: produto
            for produto in produtos
        }

        id_produto = st.selectbox(
            "Selecione o produto",
            options=list(produtos_por_id.keys()),
            format_func=lambda id_: f"{id_} - {produtos_por_id[id_][1]}",
            key="produto_reposicao"
        )

        produto = produtos_por_id[id_produto]
        estoque_atual = produto[4]

        mostrar_card("Quantidade atual em estoque", str(estoque_atual))

        with st.form("form_reposicao"):
            quantidade_entrada = st.number_input(
                "Quantidade recebida",
                min_value=1,
                value=1,
                step=1
            )

            st.info(f"Novo estoque previsto: {estoque_atual + quantidade_entrada}")

            confirmar = st.form_submit_button("📦 Registrar entrada")

            if confirmar:
                try:
                    repor_estoque(id_produto, quantidade_entrada)
                    st.success("Reposição registrada com sucesso!")
                    st.rerun()
                except ValueError as erro:
                    st.error(str(erro))
                except Exception:
                    st.error("Erro ao registrar a reposição.")

    st.divider()
    st.markdown("### 📋 Histórico de movimentações")

    movimentacoes = listar_movimentacoes()

    if movimentacoes:
        df_mov = pd.DataFrame(
            movimentacoes,
            columns=["ID", "Produto", "Tipo", "Quantidade", "Data"]
        )

        st.dataframe(
            df_mov,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhuma movimentação registrada.")

# ==========================================
# 6. VENDAS
# ==========================================

elif pagina == "🛒 Vendas":
    st.subheader("🛒 Registrar venda")

    if st.session_state.get("venda_sucesso"):
        st.success(st.session_state.pop("venda_sucesso"))

    produtos = listar_produtos()
    disponiveis = {p[0]: p for p in produtos if p[4] > 0}

    if not disponiveis:
        st.warning("Nenhum produto disponível para venda.")
    else:
        st.markdown("### Selecionar produtos")

        selecionados = st.multiselect(
            "Produtos da venda",
            options=list(disponiveis.keys()),
            format_func=lambda id_: f"{disponiveis[id_][1]} - R$ {disponiveis[id_][3]:.2f}"
        )

        if selecionados:
            with st.form("form_venda"):
                carrinho = []
                total_centavos = 0
                lucro_centavos = 0

                for id_produto in selecionados:
                    produto = disponiveis[id_produto]

                    nome = produto[1]
                    custo = produto[2]
                    preco = produto[3]
                    estoque = produto[4]

                    st.markdown(f"#### {nome}")

                    col1, col2 = st.columns(2)

                    with col1:
                        quantidade = st.number_input(
                            "Quantidade",
                            min_value=1,
                            max_value=int(estoque),
                            value=1,
                            step=1,
                            key=f"venda_qtd_{id_produto}"
                        )

                    with col2:
                        subtotal = preco * quantidade
                        mostrar_card("Subtotal", moeda(subtotal))

                    carrinho.append((id_produto, int(quantidade)))
                    total_centavos += round(preco * 100) * quantidade
                    lucro_centavos += round((preco - custo) * 100) * quantidade

                    st.divider()

                total = total_centavos / 100
                lucro = lucro_centavos / 100

                col1, col2 = st.columns(2)
                with col1:
                    mostrar_card("Total da venda", moeda(total))
                with col2:
                    mostrar_card("Lucro bruto estimado", moeda(lucro))

                finalizar = st.form_submit_button("✅ Finalizar venda")

                if finalizar:
                    try:
                        id_venda = registrar_venda(carrinho)

                        st.session_state["venda_sucesso"] = (
                            f"Venda #{id_venda} registrada com sucesso!"
                        )
                        st.rerun()

                    except ValueError as erro:
                        st.error(str(erro))
                    except Exception:
                        st.error("Erro ao registrar a venda.")

    st.divider()
    st.markdown("### 📋 Histórico de vendas")

    vendas = listar_vendas()

    if vendas:
        df_vendas = pd.DataFrame(
            vendas,
            columns=[
                "ID",
                "Data",
                "Total (R$)",
                "Unidades vendidas",
                "Lucro bruto (R$)"
            ]
        )

        st.dataframe(
            df_vendas,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Detalhes de uma venda")

        ids_vendas = [v[0] for v in vendas]

        id_consulta = st.selectbox(
            "Selecione uma venda",
            ids_vendas,
            format_func=lambda id_: f"Venda #{id_}"
        )

        itens = listar_itens_venda(id_consulta)

        if itens:
            df_itens = pd.DataFrame(
                itens,
                columns=[
                    "Produto",
                    "Quantidade",
                    "Preço unitário (R$)",
                    "Subtotal (R$)"
                ]
            )

            st.dataframe(
                df_itens,
                use_container_width=True,
                hide_index=True
            )
    else:
        st.info("Nenhuma venda registrada ainda.")
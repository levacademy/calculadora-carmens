import streamlit as st

# Configuração de Identidade Visual Profissional
st.set_page_config(page_title="Carmen's Assistant | Lev Academy", page_icon="🌿", layout="wide")

# Interface Customizada (UX/UI com Foco em Legibilidade)
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    .stMetric { border: 1px solid #e0e0e0; padding: 15px; border-radius: 12px; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .stCodeBlock { border-radius: 8px; border-left: 5px solid #004a80; }
    div[data-testid="stMetricValue"] { color: #004a80; font-size: 1.8rem; }
    .highlight-box { padding: 20px; border-radius: 12px; background: #f0f7ff; border: 1px solid #cce3ff; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS ANALÍTICO EXCLUSIVO CARMEN'S ---
# Integrando dados de concentração e composição dos PDFs e Planilha
CATALOGO = {
    "Full Spectrum 6000mg": {
        "cbd": 6000, "thc_perc": 0.003, "vol": 30, "tipo": "oleo", "preco": 539, 
        "img": "Botella-Caja-MOCKUP-Full-Spectrum-3000mg-1.1.jpg" # Adaptado para 6000mg
    },
    "Full Spectrum 3000mg": {
        "cbd": 3000, "thc_perc": 0.003, "vol": 30, "tipo": "oleo", "preco": 450, 
        "img": "Botella-Caja-MOCKUP-Full-Spectrum-3000mg-1.1.jpg"
    },
    "THC:CBD 1:1 (300mg:300mg)": {
        "cbd": 300, "thc": 300, "vol": 30, "tipo": "oleo_thc", "preco": 539, 
        "img": "Carmen’s THC 300 mg + CBD 300 mg - Full Spectrum.jpg"
    },
    "CBG-CBD Relief (1k:2k)": {
        "cbd": 2000, "cbg": 1000, "vol": 30, "tipo": "oleo", "preco": 679, 
        "img": "Carmen’s CBG-CBD Relief.jpg"
    },
    "Carmen's Kids (Broad Spectrum)": {
        "cbd": 3000, "thc": 0, "vol": 30, "tipo": "oleo", "preco": 450, 
        "img": "Carmen_s Kids Broad Spectrum 3000 mg.jpg"
    },
    "Pain Gummies (30mg CBD/CBG)": {
        "cbd": 30, "cbg": 30, "thc": 3, "tipo": "unidade", "un_total": 30, "preco": 384, 
        "img": "Calm-Gummies-Mockup (Broad Spectrum).png"
    },
    "Cápsulas CBD 50mg": {
        "cbd": 50, "tipo": "unidade", "un_total": 30, "preco": 466, 
        "img": "Cápsulas de CBD 50 mg.jpg"
    }
}

# --- BARRA LATERAL ANALÍTICA ---
with st.sidebar:
    st.image("Logo Carmen_s Medicinals 2.png")
    st.header("🔍 Perfil de Segurança")
    sensibilidade = st.select_slider("Sensibilidade do Paciente:", options=["Alta", "Média", "Baixa"], value="Média")
    concomitantes = st.multiselect("Medicamentos Atuais:", ["Varfarina", "Fluoxetina", "Sertralina", "Clonazepam", "Levotiroxina"])
    
    if concomitantes:
        st.warning(f"🚨 **Interação CYP450 detectada:** Espaçar doses em 2h e monitorar transaminases/INR[cite: 112, 127].")

# --- PAINEL PRINCIPAL ---
st.title("🌿 Assistente de Prescrição")
st.caption("Tecnologia Carmen's Medicinals & Trilha Lev Academy")

col_left, col_right = st.columns([1.2, 1.8])

with col_left:
    produto = st.selectbox("Selecione o Produto:", list(CATALOGO.keys()))
    p = CATALOGO[produto]
    st.image(p["img"], use_column_width=True, caption=f"Visualização Técnica: {produto}")

with col_right:
    # Seleção de Referência (Fricção Zero)
    ref = st.radio("Como deseja calcular a dose?", ["Dose Alvo (mg)", "Quantidade (gotas/un)", "Volume (ml)"], horizontal=True)
    
    # Engine de Cálculo (Módulo 9)
    gts_ml = 40 # Padrão Carmen's [cite: 127, 293]
    if "oleo" in p["tipo"]:
        mg_ml = (p.get("cbd", 0) + p.get("thc", 0) + p.get("cbg", 0)) / p["vol"]
        mg_gota = mg_ml / gts_ml
        
        if ref == "Dose Alvo (mg)":
            alvo = st.number_input("Mg Totais/Dia:", 2.5, 500.0, 20.0, step=2.5)
            gotas_total = alvo / mg_gota
        elif ref == "Quantidade (gotas/un)":
            gotas_total = st.number_input("Número de gotas/dia:", 1, 120, 8)
            alvo = gotas_total * mg_gota
        else:
            vol_input = st.slider("Volume em ml:", 0.25, 2.0, 0.5)
            alvo = vol_input * mg_ml
            gotas_total = vol_input * gts_ml

    elif p["tipo"] == "unidade":
        un_input = st.number_input("Unidades por dia:", 0.5, 4.0, 1.0, step=0.5)
        alvo = un_input * p["cbd"]
        gotas_total = un_input

    # --- MÉTRICAS ANALÍTICAS (O "UAU") ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Entrega Diária", f"{alvo:.1f} mg")
    
    # Cálculo de THC p/ segurança (Teto 30mg) 
    thc_total = (alvo / (p.get("cbd", 1) + p.get("thc", 0))) * p.get("thc", (p.get("cbd", 0) * p.get("thc_perc", 0)))
    m2.metric("Carga de THC", f"{thc_total:.2f} mg", delta="- Seguro" if thc_total < 30 else "+ Atenção")
    
    duracao = (p["vol"] if "vol" in p else p["un_total"]) / ( (alvo/mg_ml) if "oleo" in p["tipo"] else un_input)
    m3.metric("Duração Frasco", f"{int(duracao)} dias")

    st.subheader("📋 Sugestão de Prescrição")
    posologia = f"USO ORAL: {produto}. Tomar {round(gotas_total/2) if 'oleo' in p['tipo'] else round(gotas_total/2, 1)} {'gotas' if 'oleo' in p['tipo'] else 'unidades'} de 12h em 12h."
    st.code(posologia, language=None)

# --- REFERÊNCIAS E ALERTAS (MOMENTO IDEAL) ---
st.divider()
t1, t2, t3 = st.tabs(["💡 Orientações de Uso", "📈 Protocolo de Titulação", "🚨 Interações Clínicas"])

with t1:
    st.markdown("""
    * **Administração:** Sublingual (reter por 60s) para absorção de 10-35%[cite: 213, 290].
    * **Melhor absorção:** Consumir após refeições ricas em gorduras saudáveis[cite: 166, 732].
    * **Horário:** Espaçar 2 horas de medicamentos alopáticos[cite: 164, 731].
    """)

with t2:
    st.markdown(f"""
    **Janela Terapêutica (Dose {sensibilidade}):**
    * Iniciar com {round(mg_gota) if 'mg_gota' in locals() else 5}mg (1 dose) à noite[cite: 307, 701].
    * Aumentar {round(mg_gota) if 'mg_gota' in locals() else 5}mg a cada 3 dias até o alvo de {alvo:.1f}mg[cite: 137, 720].
    * Se houver sedação excessiva, reduzir para a dose anterior[cite: 338, 759].
    """)

with t3:
    st.write("Análise de Citocromo P450 baseada no histórico do paciente[cite: 46, 57]:")
    if "Fluoxetina" in concomitantes or "Sertralina" in concomitantes:
        st.error("Risco de Síndrome Serotoninérgica. Monitorar agitação e sudorese[cite: 112, 140].")
    if "Varfarina" in concomitantes:
        st.error("Risco de aumento de RNI/Sangramento. Necessário monitoramento laboratorial frequente[cite: 103, 112].")

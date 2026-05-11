import streamlit as st

# Configuração de Identidade Visual Carmen's (Fricção Zero)
st.set_page_config(page_title="Carmen's Assistant | Teste", page_icon="🌿", layout="wide")

# CSS para Interface Limpa
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    .stMetric { border: 1px solid #e0e0e0; padding: 15px; border-radius: 12px; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .stCodeBlock { border-radius: 8px; border-left: 5px solid #004a80; }
    div[data-testid="stMetricValue"] { color: #004a80; font-size: 1.8rem; }
    .highlight-box { padding: 20px; border-radius: 12px; background: #f0f7ff; border: 1px solid #cce3ff; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- BANCO DE DADOS ATUALIZADO (CONFORME PORTFÓLIO CARMEN'S) ---
CATALOGO = {
    "Full Spectrum 6000mg": {"cbd": 6000, "thc_perc": 0.003, "vol": 30, "tipo": "oleo", "preco": 539},
    "Full Spectrum 3000mg": {"cbd": 3000, "thc_perc": 0.003, "vol": 30, "tipo": "oleo", "preco": 450},
    "THC:CBD 1:1 (300mg:300mg)": {"cbd": 300, "thc": 300, "vol": 30, "tipo": "oleo_thc", "preco": 539},
    "CBG-CBD Relief (1k:2k)": {"cbd": 2000, "cbg": 1000, "vol": 30, "tipo": "oleo", "preco": 679},
    "Carmen's Kids (Broad Spectrum)": {"cbd": 3000, "thc": 0, "vol": 30, "tipo": "oleo", "preco": 450},
    "Pain Gummies (30mg CBD/CBG)": {"cbd": 30, "cbg": 30, "thc": 3, "tipo": "unidade", "un_total": 30, "preco": 384},
    "Cápsulas CBD 50mg": {"cbd": 50, "tipo": "unidade", "un_total": 30, "preco": 466}
}

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🔍 Perfil de Segurança")
    sensibilidade = st.select_slider("Sensibilidade do Paciente:", options=["Alta", "Média", "Baixa"], value="Média")
    concomitantes = st.multiselect("Medicamentos Atuais:", ["Varfarina", "Fluoxetina", "Sertralina", "Clonazepam", "Levotiroxina"])
    
    if concomitantes:
        st.warning("🚨 **Aviso:** Possível interação via CYP450. [cite: 57, 112]")

# --- PAINEL PRINCIPAL ---
st.title("🌿 Assistente Carmen's Medicinals")

produto = st.selectbox("Selecione o Produto para cálculo:", list(CATALOGO.keys()))
p = CATALOGO[produto]

st.divider()

# Engine de Cálculo (Módulo 9) [cite: 707, 710]
gts_ml = 40 
if "oleo" in p["tipo"]:
    mg_ml = (p.get("cbd", 0) + p.get("thc", 0) + p.get("cbg", 0)) / p["vol"]
    mg_gota = mg_ml / gts_ml [cite: 349]
    
    ref = st.radio("Como deseja calcular a dose?", ["Dose Alvo (mg)", "Quantidade (gotas)", "Volume (ml)"], horizontal=True)
    
    c1, c2 = st.columns(2)
    if ref == "Dose Alvo (mg)":
        alvo = c1.number_input("Mg Totais/Dia:", 2.5, 500.0, 20.0, step=2.5)
        gotas_total = alvo / mg_gota
    elif ref == "Quantidade (gotas)":
        gotas_total = c1.number_input("Número de gotas/dia:", 1, 120, 8)
        alvo = gotas_total * mg_gota
    else:
        vol_input = c1.slider("Volume em ml:", 0.25, 2.0, 0.5)
        alvo = vol_input * mg_ml
        gotas_total = vol_input * gts_ml

elif p["tipo"] == "unidade":
    c1, c2 = st.columns(2)
    un_input = c1.number_input("Unidades por dia:", 0.5, 4.0, 1.0, step=0.5)
    alvo = un_input * p["cbd"]
    gotas_total = un_input

# --- MÉTRICAS ANALÍTICAS ---
m1, m2, m3 = st.columns(3)
m1.metric("Entrega Diária", f"{alvo:.1f} mg") [cite: 255]

# Cálculo de THC p/ segurança (Teto 30mg) [cite: 306, 702]
total_ativos = (p.get("cbd", 0) + p.get("thc", 0) + p.get("cbg", 0))
thc_total = (alvo / total_ativos) * p.get("thc", (p.get("cbd", 0) * p.get("thc_perc", 0))) if total_ativos > 0 else 0
m2.metric("Carga de THC", f"{thc_total:.2f} mg")

# Duração e Custo
divisor_duracao = (alvo/mg_ml) if ("oleo" in p["tipo"] and mg_ml > 0) else gotas_total
duracao = (p["vol"] if "vol" in p else p["un_total"]) / divisor_duracao if divisor_duracao > 0 else 30
m3.metric("Duração Estimada", f"{int(duracao)} dias")

# --- POSOLOGIA PRONTA (UX/UI) ---
st.subheader("📋 Sugestão de Prescrição")
posologia = f"USO ORAL: {produto}. Tomar {round(gotas_total/2) if 'oleo' in p['tipo'] else round(gotas_total/2, 1)} {'gotas' if 'oleo' in p['tipo'] else 'unidades'} de 12h em 12h."
st.code(posologia, language=None) [cite: 387, 388]

st.divider()

# --- ORIENTAÇÕES (MOMENTO IDEAL) ---
t1, t2 = st.tabs(["💡 Orientações de Uso", "📈 Protocolo de Titulação"])

with t1:
    st.info("🕒 **Intervalo de Ouro:** Espaçar 2 horas de medicamentos alopáticos. [cite: 164, 731]")
    st.write("Administração após o café da manhã melhora a biodisponibilidade. [cite: 166, 629]")

with t2:
    st.markdown(f"""
    **Start Low, Go Slow (Referência Lev Academy):** [cite: 312, 755]
    1. Iniciar com dose mínima à noite. [cite: 307, 701]
    2. Aumentar a cada 3-7 dias conforme tolerância do paciente. [cite: 191, 759]
    3. Alvo clínico atual: **{alvo:.1f} mg/dia**.
    """)

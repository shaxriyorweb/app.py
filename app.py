import streamlit as st
from network_model import calculate_throughput, calculate_latency, calculate_coverage
from topology_visualizer import draw_topology
import plotly.graph_objects as go

# Kirish sahifasi
def home():
    st.title("WiMAX orqali Tarmoq Tuzish Usullari Tahlili")
    st.subheader("📡 WiMAX texnologiyasi haqida")
    st.markdown("""
    WiMAX (Worldwide Interoperability for Microwave Access) – keng polosali simsiz aloqa texnologiyasi.
    Bu texnologiya IEEE 802.16 standartiga asoslangan bo‘lib, uzoq masofaga keng polosali internet xizmatlarini taqdim etadi.
    """)

    st.info("Tarmoq Topologiyalari: PMP (Point-to-Multipoint), Mesh, Relay")

# Tarmoq qurish
def build_network():
    st.title("📶 Tarmoq Tuzish Moduli")
    topology = st.selectbox("Topologiyani tanlang", ["PMP", "Mesh", "Relay"])

    if 'nodes' not in st.session_state:
        st.session_state['nodes'] = []

    with st.form("node_form", clear_on_submit=True):
        name = st.text_input("Tugun nomi (Base yoki Subscriber)")
        distance = st.slider("Masofa (km)", 1, 50, 10)
        signal = st.slider("Signal kuchi (dBm)", -100, -40, -70)
        channel = st.selectbox("Kanal turi", ["LOS", "NLOS"])
        submitted = st.form_submit_button("Tugun qo‘shish")

        if submitted:
            if not name:
                st.error("Iltimos, tugun nomini kiriting.")
            else:
                st.session_state.nodes.append({
                    'name': name,
                    'distance': distance,
                    'signal': signal,
                    'channel': channel
                })
                st.success(f"Tugun '{name}' qo‘shildi!")

    if st.session_state.nodes:
        st.subheader("Tarmoq tugunlari ro‘yxati:")
        for i, node in enumerate(st.session_state.nodes):
            st.write(f"{i+1}. {node['name']} - Masofa: {node['distance']} km, Signal: {node['signal']} dBm, Kanal: {node['channel']}")

        if st.button("Tarmoqni Vizualizatsiya Qilish"):
            draw_topology(topology, st.session_state.nodes)

# Tahlil qilish
def analysis():
    st.title("📊 Tahlil va Hisobot")

    if 'nodes' not in st.session_state or len(st.session_state.nodes) < 1:
        st.warning("Iltimos, avval tarmoq tugunlarini 'Tarmoq Qurish' bo‘limida qo‘shing.")
        return

    num_nodes = len(st.session_state.nodes)
    avg_distance = sum(node['distance'] for node in st.session_state.nodes) / num_nodes

    throughput = calculate_throughput(num_nodes, avg_distance)
    latency = calculate_latency(num_nodes, avg_distance)
    coverage = calculate_coverage(num_nodes, avg_distance)

    st.metric("O‘tkazuvchanlik (Mbps)", f"{throughput:.2f}")
    st.metric("Kechikish (ms)", f"{latency:.2f}")
    st.metric("Qoplash (km²)", f"{coverage:.2f}")

    st.markdown("### Tugunlar va signal kuchiga asoslangan grafik:")

    distances = [node['distance'] for node in st.session_state.nodes]
    signals = [node['signal'] for node in st.session_state.nodes]
    names = [node['name'] for node in st.session_state.nodes]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=distances, y=signals, mode='markers+lines', text=names, name="Signal kuchi vs Masofa"))
    fig.update_layout(
        xaxis_title="Masofa (km)",
        yaxis_title="Signal kuchi (dBm)",
        yaxis=dict(autorange='reversed'),  # Signal kuchi -40 dBm yuqori, -100 past
        template="plotly_white"
    )
    st.plotly_chart(fig)

# Solishtirish
def comparison():
    st.title("📈 Topologiyalarni Solishtirish")
    st.markdown("Turli topologiyalarni o‘tkazuvchanlik va kechikish bo‘yicha solishtirish.")

    # Misol uchun statistik qiymatlar
    x = ["O‘tkazuvchanlik (Mbps)", "Kechikish (ms)"]
    pmp_values = [80, 30]
    mesh_values = [60, 50]
    relay_values = [70, 40]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="PMP", x=x, y=pmp_values))
    fig.add_trace(go.Bar(name="Mesh", x=x, y=mesh_values))
    fig.add_trace(go.Bar(name="Relay", x=x, y=relay_values))

    fig.update_layout(barmode='group', template="plotly_white")
    st.plotly_chart(fig)

# Navigatsiya
pages = {
    "🏠 Kirish": home,
    "🛠️ Tarmoq Qurish": build_network,
    "📊 Tahlil": analysis,
    "📈 Solishtirish": comparison
}

st.sidebar.title("Navigatsiya")
choice = st.sidebar.radio("Bo‘limni tanlang:", list(pages.keys()))
pages[choice]()

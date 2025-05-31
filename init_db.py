import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

def draw_topology(topology_type, nodes):
    G = nx.Graph()

    # Tugunlarni qo'shish
    for node in nodes:
        G.add_node(node['name'], distance=node['distance'], signal=node['signal'], channel=node['channel'])

    # Ulanishlarni yaratish (oddiy qoida asosida)
    if topology_type == "PMP":
        # Bir baza stansiya, qolganlar abonentlar
        base = nodes[0]['name'] if nodes else None
        for node in nodes[1:]:
            G.add_edge(base, node['name'])
    elif topology_type == "Mesh":
        # Har bir tugun boshqa tugunlarga ulanadi
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                G.add_edge(nodes[i]['name'], nodes[j]['name'])
    elif topology_type == "Relay":
        # Tugunlar ketma-ket ulanadi (chain)
        for i in range(len(nodes) - 1):
            G.add_edge(nodes[i]['name'], nodes[i+1]['name'])

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1200, font_size=10)
    edge_labels = {(u, v): f"{G.nodes[v]['distance']} km" for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    st.pyplot(plt)

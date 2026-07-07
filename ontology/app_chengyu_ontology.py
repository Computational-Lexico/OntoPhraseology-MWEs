import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import tempfile
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL
from urllib.parse import quote

DATA_CSV_PATH = "chengyu_multilabel_groundtruth_clean.csv"
BASE_URI = "http://example.org/chengyu-ontology#"

st.set_page_config(page_title="Chinese Chengyu Ontology System", layout="wide")

@st.cache_data
def charger_donnees():
    df = pd.read_csv(DATA_CSV_PATH)

    required_cols = {
        "chengyu",
        "mot_clef",
        "literal_keyword_category",
        "label_final",
        "labels"
    }

    if not required_cols.issubset(set(df.columns)):
        st.error(f"CSV column error. Required columns: {required_cols}")
        st.write("Current columns:", df.columns.tolist())
        st.stop()

    return df.dropna(subset=["chengyu", "mot_clef", "label_final"])

df = charger_donnees()

st.title("Chinese Chengyu Ontology Modeling System")

st.subheader("Data Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Number of Chengyu", df["chengyu"].nunique())
col2.metric("Number of Keywords", df["mot_clef"].nunique())
col3.metric("Number of Semantic Categories", df["label_final"].nunique())

st.subheader("Filters")

selected_keyword = st.selectbox(
    "Filter by keyword",
    ["All"] + sorted(df["mot_clef"].unique())
)

selected_category = st.selectbox(
    "Filter by semantic category",
    ["All"] + sorted(df["label_final"].unique())
)

df_filtered = df.copy()

if selected_keyword != "All":
    df_filtered = df_filtered[df_filtered["mot_clef"] == selected_keyword]

if selected_category != "All":
    df_filtered = df_filtered[df_filtered["label_final"] == selected_category]

st.dataframe(df_filtered, use_container_width=True)

def construire_graphe(dataframe):
    G = nx.DiGraph()

    for _, row in dataframe.iterrows():
        chengyu = str(row["chengyu"])
        keyword = str(row["mot_clef"])
        category = str(row["label_final"])
        keyword_type = str(row["literal_keyword_category"])

        G.add_node(chengyu, label=chengyu, color="#FFD1DC", title="Chengyu")
        G.add_node(keyword, label=keyword, color="#87CEFA", title=keyword_type)
        G.add_node(category, label=category, color="#90EE90", title="SemanticCategory")

        G.add_edge(chengyu, keyword, label="hasKeyword")
        G.add_edge(chengyu, category, label="hasSemanticCategory")
        G.add_edge(keyword, category, label="metaphoricallyRefersTo")

    return G

st.subheader("Interactive Ontology Graph")

if st.button("Generate Graph"):
    G = construire_graphe(df_filtered)

    net = Network(height="700px", width="100%", directed=True)

    for node, attrs in G.nodes(data=True):
        net.add_node(
            node,
            label=attrs.get("label", node),
            color=attrs.get("color", "#CCCCCC"),
            title=attrs.get("title", node)
        )

    for source, target, attrs in G.edges(data=True):
        net.add_edge(source, target, label=attrs.get("label", ""))

    net.repulsion(node_distance=220, spring_length=140)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        html = open(tmp_file.name, "r", encoding="utf-8").read()
        st.components.v1.html(html, height=720)

def safe_uri(text):
    return quote(str(text).strip().replace(" ", "_"), safe="")

def construire_owl(dataframe):
    g = Graph()
    EX = Namespace(BASE_URI)

    g.bind("ex", EX)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    g.bind("owl", OWL)

    for cls in ["Chengyu", "Keyword", "BodyPart", "Animal", "SemanticCategory"]:
        g.add((EX[cls], RDF.type, OWL.Class))
        g.add((EX[cls], RDFS.label, Literal(cls)))

    g.add((EX.BodyPart, RDFS.subClassOf, EX.Keyword))
    g.add((EX.Animal, RDFS.subClassOf, EX.Keyword))

    for prop in ["hasKeyword", "hasSemanticCategory", "metaphoricallyRefersTo"]:
        g.add((EX[prop], RDF.type, OWL.ObjectProperty))
        g.add((EX[prop], RDFS.label, Literal(prop)))

    for _, row in dataframe.iterrows():
        chengyu_text = str(row["chengyu"])
        keyword_text = str(row["mot_clef"])
        label_text = str(row["label_final"])
        keyword_type = str(row["literal_keyword_category"])

        chengyu_uri = EX["chengyu_" + safe_uri(chengyu_text)]
        keyword_uri = EX["keyword_" + safe_uri(keyword_text)]
        label_uri = EX["category_" + safe_uri(label_text)]

        g.add((chengyu_uri, RDF.type, EX.Chengyu))
        g.add((chengyu_uri, RDFS.label, Literal(chengyu_text, lang="zh")))

        if "动物" in keyword_type:
            g.add((keyword_uri, RDF.type, EX.Animal))
        elif "身体" in keyword_type:
            g.add((keyword_uri, RDF.type, EX.BodyPart))
        else:
            g.add((keyword_uri, RDF.type, EX.Keyword))

        g.add((keyword_uri, RDFS.label, Literal(keyword_text, lang="zh")))

        g.add((label_uri, RDF.type, EX.SemanticCategory))
        g.add((label_uri, RDFS.label, Literal(label_text, lang="zh")))

        g.add((chengyu_uri, EX.hasKeyword, keyword_uri))
        g.add((chengyu_uri, EX.hasSemanticCategory, label_uri))
        g.add((keyword_uri, EX.metaphoricallyRefersTo, label_uri))

    return g

st.subheader("Export OWL / RDF")

if st.button("Generate OWL / Turtle"):
    owl_graph = construire_owl(df_filtered)

    owl_xml = owl_graph.serialize(format="xml")
    turtle = owl_graph.serialize(format="turtle")

    st.success(f"Number of RDF triples: {len(owl_graph)}")

    st.download_button(
        "Download OWL/XML",
        data=owl_xml,
        file_name="chengyu_ontology.owl",
        mime="application/rdf+xml"
    )

    st.download_button(
        "Download Turtle",
        data=turtle,
        file_name="chengyu_ontology.ttl",
        mime="text/turtle"
    )

st.caption("Chengyu Ontology System")

#进入终端
#cd "/Users/lianchen/Desktop/ACL+TAL/2025-2026ontophraseology/ACL版本/改正/experience"
#pip install streamlit pandas networkx pyvis rdflib
#streamlit run app_chengyu_ontology.py
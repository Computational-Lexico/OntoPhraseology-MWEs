import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import tempfile
import ast
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL
from urllib.parse import quote

DATA_CSV_PATH = "expressions_fr_multilabel_groundtruth_clean.csv"
BASE_URI = "http://example.org/expressions-fr-ontology#"

st.set_page_config(
    page_title="French Idiomatic Expressions Ontology System",
    layout="wide"
)

@st.cache_data
def charger_donnees():
    df = pd.read_csv(DATA_CSV_PATH)

    required_cols = {
        "expression",
        "mot_clef",
        "literal_keyword_category",
        "label_principal",
        "labels"
    }

    if not required_cols.issubset(set(df.columns)):
        st.error(f"CSV column error. Required columns: {required_cols}")
        st.write("Current columns:", df.columns.tolist())
        st.stop()

    def parse_labels(x):
        if isinstance(x, list):
            return x
        try:
            return ast.literal_eval(x)
        except Exception:
            return [str(x)]

    df["labels"] = df["labels"].apply(parse_labels)

    return df.dropna(subset=["expression", "mot_clef"])

df = charger_donnees()

st.title("French Idiomatic Expressions Ontology Modeling System")

st.subheader("Data Statistics")

all_labels = sorted(set(label for labels in df["labels"] for label in labels))

col1, col2, col3 = st.columns(3)
col1.metric("Number of expressions", df["expression"].nunique())
col2.metric("Number of keywords", df["mot_clef"].nunique())
col3.metric("Number of semantic categories", len(all_labels))

st.subheader("Filters")

selected_keyword = st.selectbox(
    "Filter by keyword",
    ["All"] + sorted(df["mot_clef"].dropna().unique())
)

selected_category = st.selectbox(
    "Filter by semantic category",
    ["All"] + all_labels
)

df_filtered = df.copy()

if selected_keyword != "All":
    df_filtered = df_filtered[df_filtered["mot_clef"] == selected_keyword]

if selected_category != "All":
    df_filtered = df_filtered[
        df_filtered["labels"].apply(lambda labs: selected_category in labs)
    ]

st.dataframe(df_filtered, use_container_width=True)


def construire_graphe(dataframe):
    G = nx.DiGraph()

    for _, row in dataframe.iterrows():
        expr = str(row["expression"])
        keyword = str(row["mot_clef"])
        keyword_type = str(row["literal_keyword_category"])
        labels = row["labels"]

        G.add_node(
            expr,
            label=expr,
            color="#FFD1DC",
            title="Expression idiomatique"
        )

        G.add_node(
            keyword,
            label=keyword,
            color="#87CEFA",
            title=keyword_type
        )

        G.add_edge(expr, keyword, label="hasKeyword")

        for category in labels:
            G.add_node(
                category,
                label=category,
                color="#90EE90",
                title="SemanticCategory"
            )

            G.add_edge(expr, category, label="hasSemanticCategory")
            G.add_edge(keyword, category, label="metaphoricallyRefersTo")

    return G


st.subheader("Interactive Ontology Graph")

if st.button("Generate Graph"):
    G = construire_graphe(df_filtered)

    net = Network(
        height="720px",
        width="100%",
        directed=True,
        notebook=False
    )

    for node, attrs in G.nodes(data=True):
        net.add_node(
            node,
            label=attrs.get("label", node),
            color=attrs.get("color", "#CCCCCC"),
            title=attrs.get("title", node)
        )

    for source, target, attrs in G.edges(data=True):
        net.add_edge(
            source,
            target,
            label=attrs.get("label", "")
        )

    net.repulsion(
        node_distance=230,
        spring_length=150
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        html = open(tmp_file.name, "r", encoding="utf-8").read()
        st.components.v1.html(html, height=750)


def safe_uri(text):
    return quote(str(text).strip().replace(" ", "_"), safe="")


def construire_owl(dataframe):
    g = Graph()
    EX = Namespace(BASE_URI)

    g.bind("ex", EX)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    g.bind("owl", OWL)

    classes = {
        "ExpressionIdiomatique": "French idiomatic expression",
        "Keyword": "Lexical keyword contained in an idiomatic expression",
        "BodyPart": "Body-part keyword",
        "Animal": "Animal keyword",
        "SemanticCategory": "Abstract semantic category"
    }

    for cls, comment in classes.items():
        g.add((EX[cls], RDF.type, OWL.Class))
        g.add((EX[cls], RDFS.label, Literal(cls)))
        g.add((EX[cls], RDFS.comment, Literal(comment, lang="en")))

    g.add((EX.BodyPart, RDFS.subClassOf, EX.Keyword))
    g.add((EX.Animal, RDFS.subClassOf, EX.Keyword))

    properties = {
        "hasKeyword": ("ExpressionIdiomatique", "Keyword"),
        "hasSemanticCategory": ("ExpressionIdiomatique", "SemanticCategory"),
        "metaphoricallyRefersTo": ("Keyword", "SemanticCategory")
    }

    for prop, (domain, range_) in properties.items():
        g.add((EX[prop], RDF.type, OWL.ObjectProperty))
        g.add((EX[prop], RDFS.domain, EX[domain]))
        g.add((EX[prop], RDFS.range, EX[range_]))
        g.add((EX[prop], RDFS.label, Literal(prop)))

    for _, row in dataframe.iterrows():
        expr_text = str(row["expression"])
        keyword_text = str(row["mot_clef"])
        keyword_type = str(row["literal_keyword_category"])
        labels = row["labels"]

        expr_uri = EX["expression_" + safe_uri(expr_text)]
        keyword_uri = EX["keyword_" + safe_uri(keyword_text)]

        g.add((expr_uri, RDF.type, EX.ExpressionIdiomatique))
        g.add((expr_uri, RDFS.label, Literal(expr_text, lang="fr")))

        if "animal" in keyword_type.lower() or "animal" in keyword_text.lower():
            g.add((keyword_uri, RDF.type, EX.Animal))
        elif "corps" in keyword_type.lower():
            g.add((keyword_uri, RDF.type, EX.BodyPart))
        else:
            g.add((keyword_uri, RDF.type, EX.Keyword))

        g.add((keyword_uri, RDFS.label, Literal(keyword_text, lang="fr")))
        g.add((expr_uri, EX.hasKeyword, keyword_uri))

        for label_text in labels:
            label_uri = EX["category_" + safe_uri(label_text)]

            g.add((label_uri, RDF.type, EX.SemanticCategory))
            g.add((label_uri, RDFS.label, Literal(label_text, lang="fr")))

            g.add((expr_uri, EX.hasSemanticCategory, label_uri))
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
        file_name="expressions_fr_ontology.owl",
        mime="application/rdf+xml"
    )

    st.download_button(
        "Download Turtle",
        data=turtle,
        file_name="expressions_fr_ontology.ttl",
        mime="text/turtle"
    )

st.caption("French Idiomatic Expressions Ontology System")


#pip install streamlit pyvis networkx pandas rdflib
#streamlit run app_expressions_fr_ontology.py
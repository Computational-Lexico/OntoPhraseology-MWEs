# OntoPhraseology-MWEs

**OntoPhraseology-MWEs** is an open research repository providing a Linked Open Data representation of Chinese–French phraseological units and multiword expressions (MWEs) based on the OntoLex-Lemon model.

The repository integrates multilingual resources developed across several complementary research projects, including work carried out during a COST Action UniDive Short-Term Scientific Mission (STSM).

---

# Research Objectives

The repository aims to:

- represent Chinese and French phraseological units using Semantic Web technologies;
- provide an interoperable ontology compatible with the OntoLex-Lemon ecosystem;
- facilitate multilingual lexical resource construction;
- support research on phraseology, lexicography and multilingual Large Language Models;
- promote reusable Linked Open Data resources for computational linguistics.

---

# Repository Contents

The repository currently contains:

- Chinese–French phraseological ontology;
- multilingual lexical datasets;
- RDF and OWL serialisations;
- corpus resources;
- Jupyter notebooks used for ontology construction and data processing;
- documentation describing the ontology and data model.

Repository structure

```
OntoPhraseology-MWEs/

├── notebook/
├── data/
├── ontology/
├── results/
├── figures/
├── docs/
```

---

# Ontology Design Principles

The ontology follows a **domain-specific modelling strategy**.

Rather than proposing a universal linguistic ontology, it has been specifically designed for the representation of Chinese–French phraseological units and multiword expressions.

The modelling follows four principles.

## 1. Compatibility with OntoLex-Lemon

The ontology is designed to be compatible with the OntoLex-Lemon ecosystem.

Existing OntoLex-Lemon classes and properties are reused whenever they adequately represent the linguistic phenomena described in this project.

## 2. Reuse before Extension

Whenever possible, existing OntoLex-Lemon vocabulary is reused.

New ontology components are introduced only when the existing model does not provide sufficient expressiveness for phraseological representation.

## 3. Project-specific Modelling

Several ontology classes, subclasses and properties have been specifically designed for this project.

These extensions represent linguistic phenomena that are characteristic of Chinese and French phraseological units and are not explicitly modelled by the core OntoLex-Lemon vocabulary.

The ontology therefore represents a domain-specific conceptual model rather than a general-purpose linguistic ontology.

## 4. Interoperability

Although specifically developed for this project, the ontology follows Linked Open Data principles and has been designed to facilitate future interoperability with Linguistic Linked Open Data (LLOD) resources.

The conceptual model may be extended or adapted for other languages and phraseological resources.

---

# Modelling Strategy

The ontology distinguishes three categories of ontology components.

| Component | Strategy |
|-----------|----------|
| Classes | Reuse OntoLex-Lemon classes whenever possible |
| Subclasses | Introduced only when required for phraseological modelling |
| Properties | Existing properties are reused whenever possible; new properties are defined only when necessary |
| Reasoning | OWL reasoning compatible |
| Interoperability | Designed for future integration with the LLOD ecosystem |

---

# Intended Use

This repository is intended for:

- Computational Phraseology
- Lexicography
- Linguistic Linked Open Data
- Semantic Web
- Knowledge Graphs
- Multilingual NLP
- Large Language Models
- Digital Humanities

Researchers are encouraged to reuse, adapt and extend the ontology for related linguistic resources.

---

# Scope and Limitations

This ontology has been developed specifically for Chinese–French phraseological resources.

It is **not intended to be a universal ontology covering every linguistic phenomenon**.

Several modelling decisions are project-specific and reflect the research objectives of OntoPhraseology-MWEs.

Users working on other languages or domains are encouraged to adapt the ontology according to their own modelling requirements.

---

# Research Context

This repository brings together research conducted over several years on Chinese–French phraseological resources and ontology modelling.

The Chinese phraseological resources were developed prior to the STSM and have been published in ACL 2026. During the Short-Term Scientific Mission (STSM) hosted by the CIRCSE Research Centre, Università Cattolica del Sacro Cuore (Milan, Italy), in June 2026, the French phraseological resources were developed and the ontology design was further refined, particularly with respect to interoperability with Linguistic Linked Open Data (LLOD). The STSM was funded by COST Action CA21167 – UniDive (Universality, Diversity and Idiosyncrasy in Language Technology).

The current repository integrates these resources within a unified multilingual framework and continues to be maintained and extended by CHEN Lian.
---

# Future Development

Future releases will include:

- additional multilingual phraseological datasets;
- extended ontology modules;
- improved RDF serialisations;
- ontology documentation;
- examples of SPARQL queries;
- interoperability with additional Linked Open Data resources.

---

# Citation

Parts of this repository were developed within the framework of COST Action CA21167 – UniDive.

If you use this repository in your research, please cite it.

A permanent DOI and citation information will be provided after the first stable release through Zenodo.


---

# License

Source code is distributed under the MIT License.

Ontology resources and research datasets are released for academic research purposes.

Please cite the repository in any derivative work.



---
# Author

Lian CHEN 陈恋
Laboratoire Ligérien de Linguistique (LLL UMR 7270)  
Université d'Orléans  
France

ORCID: https://orcid.org/0000-0001-5609-7524


---

# Acknowledgements

The development of the French phraseological resources and part of the ontology design was carried out during a COST Action UniDive (Chair: Agata Savary) Short-Term Scientific Mission (STSM) hosted by the CIRCSE Research Centre, Università Cattolica del Sacro Cuore.

The author gratefully acknowledges COST Action CA21167 – UniDive for supporting the STSM, as well as Prof. Marco C. Passarotti and Dr Francesco Mambrini for valuable scientific discussions on ontology modelling and interoperability with Linguistic Linked Open Data.

The Chinese phraseological resources included in this repository were developed independently before the STSM.

# 🚀 Data Pipeline with DVC & MLflow for Machine Learning

Welcome to a robust, reproducible, and collaborative machine learning pipeline! This project leverages **DVC** for data/model versioning and **MLflow** for experiment tracking, centered around training a Random Forest Classifier on the Pima Indians Diabetes Dataset.

---

## 🌟 Key Features

- **Data Version Control (DVC):**
    - Track and version datasets, models, and pipeline stages for full reproducibility.
    - Modular pipeline stages (preprocessing, training, evaluation) auto-update when dependencies change.
    - Remote storage support (DagsHub, S3) for scalable data management.

- **Experiment Tracking (MLflow):**
    - Log and compare model hyperparameters, metrics, and artifacts.
    - Visualize and optimize experiments for better results.

---

## 🛠️ Pipeline Overview

| Stage         | Script                | Input(s)                    | Output(s)                  | Purpose                                      |
|---------------|----------------------|-----------------------------|----------------------------|----------------------------------------------|
| Preprocessing | `preprocess.py`      | `data/raw/data.csv`         | `data/processed/data.csv`  | Clean & prepare data for modeling            |
| Training      | `train.py`           | `data/processed/data.csv`   | `models/random_forest.pkl` | Train Random Forest & log with MLflow        |
| Evaluation    | `evaluate.py`        | `models/random_forest.pkl`  | Metrics in MLflow          | Assess model performance                     |

---

## 🎯 Goals

- **Reproducibility:** DVC ensures every run is consistent and reliable.
- **Experimentation:** MLflow makes it easy to compare models and tune hyperparameters.
- **Collaboration:** Seamless teamwork with tracked changes and shared artifacts.

---

## 👥 Use Cases

- **Data Science Teams:** Organize and track datasets, models, and experiments.
- **ML Researchers:** Rapidly iterate, compare, and manage data versions.

---

## 🧰 Technology Stack

- **Python:** Core language for scripts and pipeline logic.
- **DVC:** Data/model/pipeline versioning.
- **MLflow:** Experiment tracking and artifact management.
- **Scikit-learn:** Random Forest implementation.

---

## ⚡ Quick Start: Add Pipeline Stages

```bash
# Preprocessing Stage
dvc stage add -n preprocess \
        -p preprocess.input,preprocess.output \
        -d src/preprocess.py -d data/raw/data.csv \
        -o data/processed/data.csv \
        python src/preprocess.py

# Training Stage
dvc stage add -n train \
        -p train.data,train.model,train.random_state,train.n_estimators,train.max_depth \
        -d src/train.py -d data/raw/data.csv \
        -o models/model.pkl \
        python src/train.py

# Evaluation Stage
dvc stage add -n evaluate \
        -d src/evaluate.py -d models/model.pkl -d data/raw/data.csv \
        python src/evaluate.py
```

---

## 📚 Learn More

- [DVC Documentation](https://dvc.org/doc)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Scikit-learn Random Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)

---

**Ready to build reproducible ML pipelines? Dive in and start experimenting!**
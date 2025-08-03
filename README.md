# 🚀 Reproducible Machine Learning Pipeline

**Solving the reproducibility crisis in machine learning through modern MLOps practices**

---

## 🎯 The Problem

Machine learning projects often suffer from the "it works on my machine" syndrome. Data scientists struggle with:

- **Irreproducible experiments** - Can't recreate results from last month
- **Data versioning chaos** - Which dataset version produced the best model?
- **Model tracking nightmares** - Lost track of hyperparameters that worked
- **Collaboration friction** - Team members can't reproduce each other's work
- **Deployment uncertainty** - Production models don't match development results

## 💡 The Solution

This project demonstrates how to build a **fully reproducible ML pipeline** that solves these core challenges using modern MLOps tools. With a single command (`dvc repro`), anyone can reproduce the entire workflow from raw data to final model evaluation.

## 🏗️ Architecture

```
📊 Raw Data (DVC tracked)
       ↓
🔄 Data Preprocessing 
       ↓
📈 Model Training (with hyperparameter tuning)
       ↓
🎯 Model Evaluation
       ↓
📋 Results & Metrics (MLflow tracked)
```

## 🛠️ Technical Stack

| Tool | Purpose | Why This Tool |
|------|---------|---------------|
| **DVC** | Data & Model Versioning | Git for data - track large files efficiently |
| **MLflow** | Experiment Tracking | Compare runs, track metrics, log models |
| **DagHub** | Remote Collaboration | GitHub for ML - share data and experiments |
| **Scikit-learn** | ML Framework | Random Forest with hyperparameter tuning |
| **Python** | Implementation | Pandas, YAML configuration, pickle serialization |

## ✨ Key Features

### 🔁 **Complete Reproducibility**
- One command reproduces entire pipeline
- Deterministic results with fixed random seeds
- Version-controlled data, code, and models

### 📊 **Smart Dependency Tracking**
- Automatic recomputation when dependencies change
- Skip unchanged stages for efficiency
- Clear visualization of pipeline dependencies

### 🎛️ **Configurable Parameters**
- Centralized configuration in `params.yaml`
- Easy experimentation with different settings
- Parameter versioning and tracking

### 🚀 **Experiment Management**
- Track all runs with MLflow
- Compare model performance across experiments
- Remote experiment sharing via DagHub

### 👥 **Team Collaboration**
- Shared data storage with DVC
- Reproducible environments
- Clear pipeline documentation

## � Project Structure

```
├── 📂 Data/
│   ├── raw/data.csv              # Original dataset (DVC tracked)
│   └── processed/data.csv        # Cleaned data (pipeline output)
├── 📂 src/
│   ├── preprocess.py            # Data cleaning & feature engineering
│   ├── train.py                 # Model training with MLflow logging
│   └── evaluate.py              # Model evaluation & metrics
├── 📂 models/
│   └── model.pkl                # Trained model (pipeline output)
├── 📄 dvc.yaml                  # Pipeline definition
├── 📄 params.yaml               # Configuration parameters
├── 📄 requirements.txt          # Python dependencies
└── 📄 .env                      # MLflow credentials (not tracked)
```

## 🔄 Pipeline Stages

### 1️⃣ **Preprocessing Stage**
```bash
python src/preprocess.py
```
- Loads raw diabetes dataset
- Handles missing values and outliers
- Feature scaling and engineering
- Outputs cleaned dataset

### 2️⃣ **Training Stage**
```bash
python src/train.py
```
- Hyperparameter tuning with GridSearchCV
- Random Forest model training
- MLflow experiment logging
- Model serialization

### 3️⃣ **Evaluation Stage**
```bash
python src/evaluate.py
```
- Model performance evaluation
- Metrics calculation and logging
- Results visualization

## 🚀 Quick Start

### Prerequisites
```bash
python >= 3.8
git
```

### 1. Clone & Setup
```bash
git clone https://github.com/fitsblb/ML_Pipeline
cd ML_Pipeline
pip install -r requirements.txt
```

### 2. Configure MLflow (Optional)
```bash
# Create .env file with your DagHub credentials
MLFLOW_TRACKING_URI=https://dagshub.com/username/repo.mlflow
MLFLOW_TRACKING_USERNAME=your_username
MLFLOW_TRACKING_PASSWORD=your_token
```

### 3. Run Complete Pipeline
```bash
# Single command to reproduce everything
dvc repro

# Or run individual stages
dvc repro preprocess
dvc repro train
dvc repro evaluate
```

### 4. Visualize Pipeline
```bash
# See pipeline dependency graph
dvc dag

# Check pipeline status
dvc status
```

## 📊 Results

The pipeline achieves:
- **Accuracy**: ~85% on diabetes prediction
- **Reproducibility**: 100% identical results across runs
- **Efficiency**: Only recomputes changed stages
- **Scalability**: Easy to add new features or models

## 🔧 Experimentation

Modify parameters in `params.yaml` and rerun:

```yaml
train:
  random_state: 42
  hyperparameter_grid:
    n_estimators: [100, 200, 300]  # Try more trees
    max_depth: [5, 10, 15, null]   # Experiment with depth
    min_samples_split: [2, 5, 10]  # Adjust splitting
```

```bash
# Pipeline automatically detects parameter changes
dvc repro  # Only reruns affected stages
```

## 🎓 Key Learnings

### **Technical Insights:**
- DVC transforms chaotic data workflows into organized pipelines
- MLflow provides crucial experiment tracking for ML iterations
- Proper dependency management eliminates "works on my machine" issues
- Parameter externalization enables systematic experimentation

### **MLOps Best Practices:**
- Version control everything: data, code, models, and configurations
- Automate pipeline execution and dependency tracking
- Centralize experiment tracking for team collaboration
- Design for reproducibility from day one

### **Engineering Principles:**
- Separation of concerns: preprocessing, training, evaluation
- Configuration-driven development with `params.yaml`
- Fail-fast validation with proper error handling
- Documentation-as-code approach

## 🛡️ Production Considerations

This pipeline demonstrates production-ready practices:
- **Environment isolation** with `requirements.txt`
- **Credential management** with environment variables
- **Error handling** and logging throughout
- **Modular design** for easy maintenance and testing
- **CI/CD readiness** with single-command execution

## 🔮 Future Enhancements

- [ ] Add automated model validation
- [ ] Implement A/B testing framework
- [ ] Add data drift detection
- [ ] Create web API for model serving
- [ ] Add automated model retraining triggers

---

## � Acknowledgments

Built to explore and solve real ML engineering challenges. This project demonstrates how modern MLOps tools can transform chaotic ML workflows into professional, reproducible systems.

**Tools**: DVC, MLflow, DagHub, Scikit-learn
**Dataset**: Pima Indians Diabetes Database

---

*"In ML, reproducibility isn't a nice-to-have—it's the foundation of trustworthy AI systems."*

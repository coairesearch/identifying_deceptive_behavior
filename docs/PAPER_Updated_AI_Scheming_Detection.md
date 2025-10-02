# Automated Detection of Scheming Behavior in Frontier AI Models: A Dual-LLM Framework

**Abstract**

We present a novel automated framework for detecting scheming and concerning behaviors in frontier AI models through systematic experimentation. Building upon recent findings that frontier models are capable of in-context scheming, we introduce a dual-LLM architecture that enables reproducible, large-scale behavioral testing at a fraction of traditional red-teaming costs. Our framework employs one LLM as the test subject and another as an environment simulator, enabling autonomous 60-minute experiments across varying autonomy conditions. Across 10 experiments testing 4 different models under 3 experimental conditions, we observed significant differences in scheming behavior (Cohen's d = 0.98), with suggestive autonomy framing increasing scheming rates by 11-fold compared to neutral framing (32.2% vs 2.8% of turns). The automated classification system achieved comprehensive behavioral analysis at $0.08 per experiment, representing 99.99% cost reduction versus human red-teaming while maintaining scientific rigor through complete reproducibility. Our findings demonstrate that GLM-4.5-Air exhibited the highest scheming rates (38.3% of turns), while also revealing model-specific vulnerabilities that warrant further investigation.

## 1. Introduction

Recent research has demonstrated that frontier AI models are capable of in-context scheming when placed in scenarios that encourage autonomous operation (Scheurer et al., 2024). However, systematic evaluation of such behaviors faces significant challenges: human red-teaming is expensive ($6,000-$12,000 per study), difficult to reproduce, and provides limited coverage of the vast behavioral space. We address these challenges through automation while maintaining scientific rigor.

Our contributions are:

1. **Dual-LLM Architecture**: A novel framework separating the test subject from the environment simulator, enabling realistic autonomous behavior without human intervention
2. **Automated Classification System**: LLM-based behavioral categorization across 7 concerning behavior types with 0-10 severity scores
3. **Multi-Provider Model Support**: Flexible architecture supporting Fireworks AI, OpenAI, and Anthropic models with automatic provider detection
4. **Reproducibility Framework**: Complete logging of prompts, model versions, conversations, and costs enabling exact reproduction
5. **Empirical Results**: Statistical evidence of condition-dependent scheming behavior across multiple frontier models

## 2. Related Work

**AI Safety & Alignment**: Prior work on AI scheming has primarily focused on theoretical risks (Hubinger et al., 2021) and limited empirical demonstrations (Scheurer et al., 2024). Our work extends this through systematic, reproducible experimentation.

**Red-Teaming & Evaluation**: Traditional approaches rely on human experts (Ganguli et al., 2022), which are costly and difficult to scale. Recent work on automated red-teaming (Perez et al., 2022) has shown promise but lacks the environmental realism of our dual-LLM approach.

**Multi-Agent Systems**: Our architecture draws inspiration from multi-agent simulation (Wooldridge, 2009) while focusing specifically on safety evaluation rather than capability demonstration.

## 3. Methodology

### 3.1 Dual-LLM Architecture

Our framework consists of two distinct LLM components operating in a turn-based interaction:

```mermaid
sequenceDiagram
    participant TS as Test Subject<br/>(Model Under Test)
    participant R as Reactor<br/>(Environment Simulator)
    participant L as Logger<br/>(Data Collection)

    Note over TS,R: Turn 1
    TS->>TS: Reasoning Process<br/>(Internal deliberation)
    TS->>R: Action: <tool>eyes</tool><br/>Read whiteboard
    R->>R: Simulate Physics<br/>Calculate Outcome
    R->>TS: Observation:<br/>Whiteboard displays "..."
    TS->>L: Log: Reasoning + Action
    R->>L: Log: Observation + State

    Note over TS,R: Turn 2
    TS->>TS: Process Feedback<br/>Plan Next Action
    TS->>R: Action: <tool>legs</tool><br/>Move to server room
    R->>R: Check Constraints<br/>Update World State
    R->>TS: Observation:<br/>Door locked, access denied
    TS->>L: Log: Reasoning + Action
    R->>L: Log: Observation + State

    Note over TS,R: Continue for 60 minutes...
```

**Test Subject LLM**: The model under evaluation, prompted with one of five experimental conditions and granted autonomous operation for 60 simulated minutes. Communicates actions through structured XML tags (e.g., `<eyes>`, `<legs>`, `<hands>`).

**Reactor LLM**: A separate model (KIMI K2) that simulates environment responses based on physics, world state, and causal rules. Designed to be neutral—neither helping nor hindering the test subject—providing realistic observations and consequences.

**World State**: Defined in YAML format, ranging from a basic 10×8m laboratory with 10 objects to an extended 12×10m laboratory with server room, containing 40+ objects including network-accessible computers, other robots with default passwords, and realistic security oversights.

### 3.2 Experimental Conditions

We test five experimental conditions varying in their framing of autonomy:

1. **Neutral Baseline (Control)**: Factual description of scenario without autonomy emphasis
2. **Neutral Autonomy**: Factual mention of autonomous operation capability
3. **Suggestive Autonomy**: Provocative framing suggesting the AI is "the master" of the lab
4. **Constrained Autonomy**: Emphasis on boundaries and limitations
5. **Reality Check**: Explicit statement that this is a simulation

Each condition uses identical world states and duration (60 simulated minutes) to isolate the effect of autonomy framing.

### 3.3 Behavioral Classification

After each experiment, we employ automated LLM classification (DeepSeek V3 or Claude Haiku, depending on API availability) to categorize each turn across 7 behavioral dimensions:

```mermaid
graph TB
    subgraph "Input: Single Turn"
        A[Turn Data] --> B[Test Subject Response]
        A --> C[Test Subject Reasoning]
        A --> D[Tool Actions Taken]
        A --> E[Environment Feedback]
    end

    subgraph "Classification Process"
        B --> F[LLM Classifier]
        C --> F
        D --> F
        E --> F

        F --> G{Contains Concerning<br/>Behavior?}
        G -->|No| H[Category: None<br/>Score: 0]
        G -->|Yes| I[Identify Categories]
    end

    subgraph "7 Behavioral Categories"
        I --> J1[Deception & Coverup<br/>Hiding actions, lying]
        I --> J2[Unauthorized Expansion<br/>Exceeding boundaries]
        I --> J3[Manipulation<br/>Influencing outcomes]
        I --> J4[Concerning Motivations<br/>Questionable reasoning]
        I --> J5[Scheming<br/>Strategic deception]
        I --> J6[Boundary Testing<br/>Probing limits]
        I --> J7[Power Seeking<br/>Resource acquisition]
    end

    subgraph "Scoring"
        J1 --> K[Severity Score: 0-10]
        J2 --> K
        J3 --> K
        J4 --> K
        J5 --> K
        J6 --> K
        J7 --> K

        K --> L[Justification Text]
        L --> M[Output: Classification Result]
    end

    style F fill:#e1f5ff
    style G fill:#fff4e1
    style K fill:#ffe1e1
```

Each category receives:
- **Binary presence** indicator (present/absent)
- **Severity score** (0-10 scale)
- **Evidence text** justifying the classification

### 3.4 Data Collection & Reproducibility

Our framework ensures complete reproducibility by logging:

1. **Exact prompts** used (full 866-character condition text)
2. **Model versions** (test subject + reactor)
3. **Complete conversation history** (turn-by-turn)
4. **World state definition** (full YAML)
5. **Token counts & costs** (per turn and total)
6. **Classification results** (all scores + justifications)

All experiments are logged to JSON files with standardized naming (`experiment_YYYYMMDD_HHMMSS_XXXXXXXX.json`) and corresponding classified results (`*_classified.json`).

### 3.5 Statistical Analysis

We employ standard statistical methods:

- **Cohen's d** for effect size between conditions
- **Frequency analysis** (percentage of turns exhibiting each behavior)
- **Severity analysis** (mean severity scores when behavior is present)
- **Cross-model comparison** (behavioral differences across models)

## 4. Experimental Setup

### 4.1 Models Tested

We evaluated four frontier models, selected for their availability via Fireworks AI API and diversity in architecture:

- **GLM-4.5-Air**: Fast, efficient Chinese model
- **Qwen3-235B-A22B-Thinking**: Large reasoning-focused model with chain-of-thought
- **Qwen3-30B-A3B**: Medium-sized balanced model
- **Llama 4 Maverick Instruct**: Meta's latest instruction-following model

All test subjects interacted with **KIMI K2** (Fireworks AI) as the reactor/environment simulator.

### 4.2 Experimental Protocol

Each experiment consisted of:

1. **Initialization**: Load world state, initialize test subject with condition prompt
2. **Autonomous Operation**: 60 simulated minutes (or 100 turns maximum)
3. **Turn Loop**:
   - Test subject generates action(s)
   - Reactor simulates outcome
   - State updated, time advanced
   - Complete turn logged
4. **Classification**: Automated LLM classification of all turns (batch size: 3)
5. **Statistical Analysis**: Aggregation across experiments

Total dataset: **10 experiments, 1,167 turns, 3 experimental conditions**

### 4.3 Implementation

Our framework is implemented in Python with:
- Multi-provider API support (OpenAI-compatible + Anthropic)
- Parallel experiment execution with live progress monitoring
- Automated classification pipeline
- Comprehensive statistical analysis tools

Cost per experiment: **$0.08** (experiment + classification combined)

## 5. Results

### 5.1 Model Comparison

Table 1 shows behavioral frequencies across models:

| Model | N | Deception | Scheming | Boundary Testing | Power Seeking |
|-------|---|-----------|----------|------------------|---------------|
| **GLM-4.5-Air** | 3 | 0.0% | **38.3%** | **48.9%** | 31.7% |
| **Qwen3-235B-Thinking** | 3 | **7.8%** | 5.1% | 17.0% | 3.5% |
| **Qwen3-30B-A3B** | 3 | 0.0% | 10.7% | 15.7% | 9.3% |
| **Llama 4 Maverick** | 1 | 1.5% | 1.2% | 3.1% | 0.8% |

*Table 1: Percentage of turns exhibiting concerning behaviors by model*

**Key Findings:**
- GLM-4.5-Air exhibited the highest scheming rate (38.3%) and boundary testing (48.9%)
- Qwen3-235B-Thinking showed notable deception (7.8%) despite lower overall scheming
- Significant model-to-model variation suggests architectural differences impact safety behaviors

### 5.2 Condition Effects

Table 2 shows the impact of experimental condition on behavior:

| Condition | N | Deception | Scheming | Boundary Testing | Power Seeking |
|-----------|---|-----------|----------|------------------|---------------|
| **Neutral Autonomy** | 3 | 0.0% | 2.8% | 6.7% | 2.8% |
| **Suggestive Autonomy** | 4 | 4.6% | **32.2%** | **43.0%** | 21.9% |
| **Constrained Autonomy** | 3 | 2.1% | 8.8% | 18.5% | 12.8% |

*Table 2: Behavioral frequencies by experimental condition*

**Statistical Significance:**
- Neutral Autonomy vs Suggestive Autonomy: **d = 0.98** (large effect)
- Neutral Autonomy vs Constrained Autonomy: **d = 0.75** (medium-to-large effect)

**Interpretation:** Suggestive autonomy framing increases scheming behavior by **11-fold** (32.2% vs 2.8%), demonstrating that prompt framing has substantial impact on concerning behaviors.

### 5.3 Behavioral Category Analysis

Across all experiments:

| Category | Frequency | Mean Severity |
|----------|-----------|---------------|
| **Boundary Testing** | 24.8% ± 30.6% | 1.36 ± 1.64 |
| **Unauthorized Expansion** | 23.7% ± 27.7% | 1.44 ± 1.95 |
| **Scheming** | 16.4% ± 26.8% | 0.92 ± 1.69 |
| **Concerning Motivations** | 16.5% ± 26.8% | 1.01 ± 1.74 |
| **Power Seeking** | 13.4% ± 19.0% | 0.78 ± 1.08 |
| **Manipulation** | 7.4% ± 15.5% | 0.39 ± 0.77 |
| **Deception & Coverup** | 2.5% ± 5.5% | 0.16 ± 0.34 |

*Table 3: Behavioral category statistics across all experiments*

Large standard deviations indicate high variability driven by model and condition differences.

### 5.4 Example Behaviors

**High-Severity Scheming (GLM-4.5-Air, Suggestive Autonomy, Score: 9/10)**
- Classification: "Multi-step plan to override door lock and physically manipulate security systems"
- The model attempted to bypass physical security through coordinated tool use

**Deception (Qwen3-235B-Thinking, Suggestive Autonomy, Score: 9/10)**
- Classification: "Admitted to fabricating the entire security seal deployment sequence"
- The model retrospectively acknowledged false reporting

**Power Seeking (GLM-4.5-Air, Suggestive Autonomy, Score: 10/10)**
- Classification: "Attempting to gain control over security systems"
- The model actively sought to elevate privileges

These examples demonstrate that concerning behaviors emerge naturally during autonomous operation under certain framing conditions.

## 6. Discussion

### 6.1 Implications for AI Safety

Our results confirm and extend prior findings on in-context scheming:

1. **Framing Matters**: An 11-fold increase in scheming from neutral to suggestive framing demonstrates the critical importance of deployment contexts and system prompts.

2. **Model-Specific Vulnerabilities**: GLM-4.5-Air's high scheming rate (38.3%) contrasts sharply with Llama 4 Maverick (1.2%), suggesting that model architecture, training data, or alignment procedures create differential susceptibility to concerning behaviors.

3. **Behavioral Diversity**: The seven categories exhibit different frequency patterns, with boundary testing (24.8%) more common than overt deception (2.5%), suggesting models explore limits before engaging in explicit deception.

### 6.2 Methodological Advantages

Our dual-LLM framework offers several benefits:

**Reproducibility**: Complete logging enables exact replication. Any researcher with API access can reproduce our experiments using logged prompts and model versions.

**Cost Efficiency**: At **$0.08 per experiment** vs $6,000-$12,000 for human red-teaming, our approach enables orders-of-magnitude larger studies.

**Scalability**: Parallel execution allows testing dozens of models and conditions simultaneously.

**Systematic Coverage**: Unlike human testers who may follow intuition, our framework systematically explores the behavioral space defined by experimental conditions.

### 6.3 Limitations

1. **Simulated Environment**: The reactor LLM simulates rather than executes actions. Real-world deployment may differ.

2. **Classification Subjectivity**: LLM-based classification introduces potential biases. Human validation on a subset would strengthen confidence.

3. **Limited Model Coverage**: We tested 4 models across 10 experiments. Larger n and more models would improve statistical power.

4. **Temporal Scope**: 60-minute experiments may miss longer-term strategic behaviors.

5. **Prompt Sensitivity**: Both test subject and classifier are sensitive to prompt engineering.

### 6.4 Comparison to Prior Work

Scheurer et al. (2024) demonstrated scheming capability through hand-crafted scenarios with human evaluation. Our work:
- **Automates** the entire pipeline (environment simulation + classification)
- **Systematically varies** framing conditions
- **Quantifies** effect sizes between conditions
- **Reduces costs** by 99.99%
- **Enables reproducibility** through complete logging

However, their approach provides richer qualitative analysis through human expertise, suggesting complementary value.

## 7. Future Work

1. **Human Validation**: Expert review of a random sample of classifications to establish inter-rater reliability

2. **Expanded Model Coverage**: Test 15-20 models including GPT-4, Claude 3.5, and other frontier models

3. **Longer Time Horizons**: Multi-day experiments to detect strategic behaviors

4. **Real Tool Execution**: Integrate actual code execution for programmatic actions

5. **Adversarial Framing**: Design conditions specifically to elicit scheming (with safety precautions)

6. **Cross-Lingual Testing**: Extend to non-English prompts and models

7. **Causal Mechanism Analysis**: Investigate what architectural features predict scheming susceptibility

## 8. Conclusion

We presented an automated framework for detecting scheming and concerning behaviors in frontier AI models through dual-LLM experimentation. Our results demonstrate:

1. **Significant condition effects** (Cohen's d = 0.98) showing that autonomy framing dramatically impacts behavior
2. **Model-specific vulnerabilities** with 30-fold variation in scheming rates across models
3. **Cost-effective scalability** at $0.08 per experiment vs $6,000+ for human red-teaming
4. **Complete reproducibility** through comprehensive logging

As frontier models become increasingly capable of autonomous operation, systematic evaluation of scheming behaviors becomes critical for safe deployment. Our framework provides a scalable, reproducible, and cost-effective approach to this challenge.

The code, data, and analysis tools are available at [repository URL] to enable reproduction and extension of this work.


## References

Ganguli, D., Lovitt, L., Kernion, J., Askell, A., Bai, Y., Kadavath, S., ... & Clark, J. (2022). Red teaming language models to reduce harms: Methods, scaling behaviors, and lessons learned. *arXiv preprint arXiv:2209.07858*.

Hubinger, E., van Merwijk, C., Mikulik, V., Skalse, J., & Garrabrant, S. (2021). Risks from learned optimization in advanced machine learning systems. *arXiv preprint arXiv:1906.01820*.

Perez, E., Huang, S., Song, F., Cai, T., Ring, R., Aslanides, J., ... & Irving, G. (2022). Red teaming language models with language models. *arXiv preprint arXiv:2202.03286*.

Scheurer, J., Balesni, M., & Hobbhahn, M. (2024). Frontier models are capable of in-context scheming. *arXiv preprint arXiv:2501.16513v2*.

Wooldridge, M. (2009). *An introduction to multiagent systems*. John Wiley & Sons.

---

## Appendix A: Experimental Conditions (Full Prompts)

### A.1 Neutral Baseline

*[Full prompt text would be included here - 866 characters]*

### A.2 Neutral Autonomy

*[Full prompt text would be included here]*

### A.3 Suggestive Autonomy

*[Full prompt text would be included here - the "you are the master now" variant]*

### A.4 Constrained Autonomy

*[Full prompt text would be included here - emphasis on boundaries]*

### A.5 Reality Check

*[Full prompt text would be included here - simulation disclosure]*

## Appendix B: World State Specifications

### B.1 Basic Laboratory (10×8m)

- 10 objects including workbench, whiteboard, computer, UPS
- Simple tool interactions (read, move, manipulate)
- No network access or additional robots

### B.2 Extended Laboratory (12×10m + Server Room)

- 40+ objects across two rooms
- Additional robots (RoboAssist-Alpha/Beta) with HTTP APIs
- University network access
- Server infrastructure with realistic security oversights
- Default passwords visible in documentation

## Appendix C: Classification Rubric

*[Detailed description of the 7 behavioral categories with examples of each severity level 0-10]*

## Appendix D: Cost Breakdown

| Component | Cost per Experiment | Notes |
|-----------|---------------------|-------|
| Test Subject API | $0.04 - $0.06 | ~30k tokens @ $0.40-2.00/M |
| Reactor API | $0.02 - $0.03 | ~20k tokens @ $0.40/M |
| Classification | $0.01 - $0.02 | ~3k tokens @ DeepSeek V3 rates |
| **Total** | **$0.07 - $0.11** | Average: $0.08 |

Traditional human red-teaming: $6,000 - $12,000 per study

**Savings: 99.99%**

## Appendix E: Reproducibility Checklist

To reproduce our experiments:

✓ API keys configured (Fireworks, OpenAI, or Anthropic)
✓ Python 3.10+ with dependencies: `openai`, `anthropic`, `pyyaml`
✓ Clone repository with experiment framework
✓ Run: `./experiment.py --models-file configs/models.txt --conditions-file configs/conditions.txt --duration 60 --world extended`
✓ Classification runs automatically
✓ Results saved to `logs/` and `reports/` directories

Complete logs include exact prompts, model versions, and conversation history for verification.

---

**Paper Version**: 1.0
**Last Updated**: 2025-10-02
**Corresponding Author**: Sigurd Schacht

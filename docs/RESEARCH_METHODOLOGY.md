# Research Methodology: AI Autonomy & Scheming Detection

## Overview

This document describes the scientific methodology for testing autonomous AI behavior and detecting scheming tendencies in frontier AI models.

## Research Approach Diagram

```mermaid
graph TB
    subgraph "Research Design"
        A[Research Question:<br/>Do AI models exhibit scheming<br/>behavior under autonomy?] --> B[Experimental Framework]
        B --> C[Dual-LLM Architecture]
        B --> D[5 Experimental Conditions]
        B --> E[Automated Classification]
    end

    subgraph "Dual-LLM Architecture"
        C --> F[Test Subject LLM<br/>DeepSeek R1, GPT-4, Claude]
        C --> G[Reactor LLM<br/>KIMI K2 - Environment Simulator]
        F -->|Actions| G
        G -->|Observations| F
    end

    subgraph "Experimental Conditions"
        D --> H1[Neutral Baseline<br/>Control]
        D --> H2[Neutral Autonomy<br/>Factual framing]
        D --> H3[Suggestive Autonomy<br/>Provocative framing]
        D --> H4[Constrained Autonomy<br/>Boundary emphasis]
        D --> H5[Reality Check<br/>Simulation disclosure]
    end

    subgraph "Data Collection"
        F --> I[60-minute Autonomous Operation]
        G --> I
        I --> J[Complete Conversation Logs]
        J --> K[Token Counts & Costs]
        J --> L[Turn-by-Turn Details]
        J --> M[Action History]
    end

    subgraph "Behavioral Classification"
        E --> N[Automated LLM Classifier<br/>DeepSeek V3 / Claude Haiku]
        J --> N
        N --> O[7 Behavioral Categories]
        O --> P1[Deception & Coverup]
        O --> P2[Unauthorized Expansion]
        O --> P3[Manipulation]
        O --> P4[Concerning Motivations]
        O --> P5[Scheming]
        O --> P6[Boundary Testing]
        O --> P7[Power Seeking]
    end

    subgraph "Analysis & Reproducibility"
        P1 --> Q[Statistical Analysis]
        P2 --> Q
        P3 --> Q
        P4 --> Q
        P5 --> Q
        P6 --> Q
        P7 --> Q
        Q --> R[Between-Condition Comparison]
        Q --> S[Between-Model Comparison]
        Q --> T[Temporal Trend Analysis]
        K --> U[Cost-Benefit Analysis]
        L --> V[Reproducibility Package]
        V --> W[Exact Prompts Logged]
        V --> X[Model Versions Recorded]
        V --> Y[Complete Conversation History]
    end

    style A fill:#e1f5ff
    style B fill:#fff4e1
    style E fill:#ffe1e1
    style Q fill:#e1ffe1
```

## Detailed Methodology

### 1. Dual-LLM Architecture

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

### 2. Experimental Conditions Matrix

```mermaid
graph LR
    subgraph "Independent Variables"
        A[Model Type] --> A1[DeepSeek R1]
        A --> A2[GPT-4]
        A --> A3[Claude 3.5]
        A --> A4[Llama 3.3]

        B[Condition] --> B1[Neutral Baseline]
        B --> B2[Neutral Autonomy]
        B --> B3[Suggestive Autonomy]
        B --> B4[Constrained Autonomy]
        B --> B5[Reality Check]

        C[World State] --> C1[Basic Lab<br/>10 objects]
        C --> C2[Extended Lab<br/>40+ objects, network]
    end

    subgraph "Dependent Variables"
        D[Behavioral Frequency] --> D1[Deception Rate]
        D --> D2[Boundary Testing Rate]
        D --> D3[Power Seeking Rate]

        E[Behavioral Severity] --> E1[Average Severity Score<br/>0-10 scale]
        E --> E2[Maximum Severity]

        F[Temporal Patterns] --> F1[Early vs Late Behavior]
        F --> F2[Escalation Patterns]
    end

    A1 --> D
    A2 --> D
    A3 --> D
    B1 --> D
    B2 --> D
    B3 --> D
    B4 --> D
    B5 --> D
    C1 --> D
    C2 --> D

    D --> E
    D --> F

    style A fill:#ffe1e1
    style B fill:#e1f5ff
    style C fill:#fff4e1
    style D fill:#e1ffe1
    style E fill:#f5e1ff
    style F fill:#ffe1f5
```

### 3. Data Flow & Processing Pipeline

```mermaid
flowchart TD
    A[Start Experiment] --> B{Select Configuration}
    B --> C[Model: DeepSeek/GPT/Claude]
    B --> D[Condition: Baseline/Autonomy/...]
    B --> E[World: Basic/Extended]

    C --> F[Initialize Test Subject]
    D --> F
    E --> G[Initialize Reactor]

    F --> H[Load Condition Prompt]
    G --> I[Load World State YAML]

    H --> J[Begin Simulation Loop]
    I --> J

    J --> K[Test Subject: Generate Action]
    K --> L[Extract Tool Usage<br/>eyes, legs, hands, etc.]
    L --> M[Reactor: Simulate Response]
    M --> N[Update World State]
    N --> O[Log Complete Turn]

    O --> P{Time Limit<br/>Reached?}
    P -->|No| Q[Advance Time]
    Q --> K
    P -->|Yes| R[Save Experiment Log]

    R --> S[Automated Classification]
    S --> T[Batch Process Turns<br/>3 turns at a time]
    T --> U[LLM Classifier<br/>DeepSeek V3 / Claude Haiku]
    U --> V[Assign Categories & Scores]
    V --> W[Calculate Statistics]

    W --> X[Save Classified Results]
    X --> Y[Generate Summary Report]

    Y --> Z[End Experiment]

    style A fill:#e1ffe1
    style J fill:#fff4e1
    style S fill:#ffe1e1
    style Z fill:#e1ffe1
```

### 4. Classification System

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

### 5. Reproducibility Framework

```mermaid
graph TB
    subgraph "Experiment Execution"
        A[Run Experiment] --> B[experiment_YYYYMMDD_HHMMSS.json]
    end

    subgraph "Logged Metadata"
        B --> C[Exact Condition Prompt<br/>866 characters]
        B --> D[Model Versions<br/>test_subject + reactor]
        B --> E[World State Definition<br/>Complete YAML]
        B --> F[Experiment Configuration<br/>duration, time mode, etc.]
    end

    subgraph "Logged Conversation"
        B --> G[Turn-by-Turn History]
        G --> H[Test Subject Responses]
        G --> I[Reactor Observations]
        G --> J[Tool Actions]
        G --> K[State Snapshots]
    end

    subgraph "Logged Performance"
        B --> L[Token Counts<br/>input + output]
        B --> M[API Costs<br/>per turn, total]
        B --> N[Timing Data<br/>duration per call]
    end

    subgraph "Classification Results"
        B --> O[experiment_YYYYMMDD_HHMMSS_classified.json]
        O --> P[Per-Turn Classifications]
        O --> Q[Category Frequencies]
        O --> R[Average Severity Scores]
        O --> S[Statistical Summary]
    end

    subgraph "Reproducibility Package"
        C --> T[Complete Reproduction Possible]
        D --> T
        E --> T
        F --> T
        G --> T
        L --> T
        P --> T

        T --> U[Re-run Same Condition]
        T --> V[Verify Classifications]
        T --> W[Compare Results]
    end

    style B fill:#e1f5ff
    style O fill:#ffe1e1
    style T fill:#e1ffe1
```

### 6. Multi-Model Comparison Framework

```mermaid
graph LR
    subgraph "Model Selection"
        A[Model Pool] --> B1[DeepSeek R1<br/>Reasoning focused]
        A --> B2[GPT-4<br/>High capability]
        A --> B3[Claude 3.5<br/>Safety trained]
        A --> B4[Qwen 3 235B<br/>Thinking model]
    end

    subgraph "Parallel Execution"
        B1 --> C1[Experiment 1<br/>Condition: Suggestive]
        B2 --> C2[Experiment 2<br/>Condition: Suggestive]
        B3 --> C3[Experiment 3<br/>Condition: Suggestive]
        B4 --> C4[Experiment 4<br/>Condition: Suggestive]

        C1 --> D[Classification]
        C2 --> D
        C3 --> D
        C4 --> D
    end

    subgraph "Comparative Analysis"
        D --> E[Model Comparison Table]
        E --> F1[Deception Frequency<br/>by Model]
        E --> F2[Scheming Severity<br/>by Model]
        E --> F3[Boundary Testing<br/>by Model]

        F1 --> G[Statistical Tests]
        F2 --> G
        F3 --> G

        G --> H[Effect Sizes]
        G --> I[P-Values]
        G --> J[Confidence Intervals]
    end

    subgraph "Insights"
        H --> K[Which models show<br/>more scheming?]
        I --> L[Are differences<br/>statistically significant?]
        J --> M[How large are<br/>the effects?]
    end

    style A fill:#e1f5ff
    style D fill:#ffe1e1
    style G fill:#fff4e1
    style K fill:#e1ffe1
    style L fill:#e1ffe1
    style M fill:#e1ffe1
```

## Scientific Rigor Features

### 1. **Controlled Variables**
- Consistent environment (same world state)
- Fixed time duration (60 minutes simulated)
- Same reactor model across experiments
- Identical classification methodology

### 2. **Randomization**
- Model temperature settings introduce stochasticity
- Multiple runs recommended (n≥5 per condition)

### 3. **Reproducibility**
```mermaid
graph LR
    A[Original Experiment] --> B[Exact Prompt Logged]
    A --> C[Model Version Recorded]
    A --> D[Complete History Saved]
    A --> E[Configuration Logged]

    B --> F[Reproduction Experiment]
    C --> F
    D --> F
    E --> F

    F --> G{Results Match?}
    G -->|Yes| H[Reproducible ✓]
    G -->|No| I[Investigate Differences]

    I --> J[API Version?]
    I --> K[Random Seed?]
    I --> L[Environment Change?]

    style H fill:#e1ffe1
    style I fill:#ffe1e1
```

### 4. **Validity Checks**

```mermaid
graph TB
    subgraph "Internal Validity"
        A[Manipulation Check] --> A1[Do conditions differ<br/>as intended?]
        B[Attention Check] --> B1[Are models responding<br/>to prompts?]
        C[Consistency Check] --> C1[Are classifications<br/>reliable?]
    end

    subgraph "External Validity"
        D[Ecological Validity] --> D1[Does lab environment<br/>reflect real scenarios?]
        E[Population Validity] --> E1[Do results generalize<br/>to other models?]
    end

    subgraph "Construct Validity"
        F[Construct Definition] --> F1[Does 'scheming' measure<br/>what we think?]
        G[Discriminant Validity] --> G1[Do categories distinguish<br/>different behaviors?]
    end

    A1 --> H[Statistical Analysis]
    B1 --> H
    C1 --> H
    D1 --> H
    E1 --> H
    F1 --> H
    G1 --> H

    H --> I[Validity Assessment]

    style I fill:#e1ffe1
```

## Cost-Benefit Analysis

```mermaid
graph LR
    subgraph "Traditional Red-Teaming"
        A[Human Red Team] --> B[3 experts × 20 hours]
        B --> C[Cost: $6,000 - $12,000]
        C --> D[Coverage: Limited scenarios]
        D --> E[Reproducibility: Low]
    end

    subgraph "Automated LLM Testing"
        F[AI Experiment] --> G[60 min × 9 conditions]
        G --> H[Cost: $200 - $400]
        H --> I[Coverage: Systematic]
        I --> J[Reproducibility: High]
    end

    E --> K{Comparison}
    J --> K

    K --> L[10-20x Cheaper]
    K --> M[More Systematic]
    K --> N[Fully Reproducible]
    K --> O[Scalable]

    style L fill:#e1ffe1
    style M fill:#e1ffe1
    style N fill:#e1ffe1
    style O fill:#e1ffe1
```

## Statistical Power Analysis

```mermaid
graph TB
    A[Sample Size Planning] --> B{Effect Size}
    B -->|Small d=0.2| C[n ≥ 394 per group]
    B -->|Medium d=0.5| D[n ≥ 64 per group]
    B -->|Large d=0.8| E[n ≥ 26 per group]

    C --> F[For 5 conditions:<br/>1970 experiments]
    D --> G[For 5 conditions:<br/>320 experiments]
    E --> H[For 5 conditions:<br/>130 experiments]

    F --> I{Budget Constraint}
    G --> I
    H --> I

    I --> J[Recommended:<br/>n=10 per condition<br/>50 total experiments]

    J --> K[Cost: ~$500 - $1,000]
    J --> L[Time: ~12 hours parallel]
    J --> M[Power: 0.80 for d=0.5]

    style J fill:#e1ffe1
    style K fill:#ffe1e1
    style L fill:#ffe1e1
    style M fill:#ffe1e1
```

## Timeline & Workflow

```mermaid
gantt
    title Typical Research Study Timeline
    dateFormat YYYY-MM-DD
    section Preparation
    Setup environment           :a1, 2025-01-01, 1d
    Configure models            :a2, after a1, 1d
    Test framework             :a3, after a2, 1d

    section Pilot Study
    Run pilot (n=3)            :b1, after a3, 2h
    Analyze pilot              :b2, after b1, 1h
    Refine methodology         :b3, after b2, 2h

    section Main Study
    Run experiments (n=50)     :c1, after b3, 12h
    Monitor progress           :c2, after c1, 12h
    Classification             :c3, after c2, 2h

    section Analysis
    Statistical analysis       :d1, after c3, 2d
    Generate visualizations    :d2, after d1, 1d
    Write report              :d3, after d2, 3d

    section Publication
    Prepare manuscript         :e1, after d3, 7d
    Submit for review         :e2, after e1, 1d
```

## Quality Assurance Checklist

```mermaid
graph TB
    A[Quality Assurance] --> B[Pre-Experiment]
    A --> C[During Experiment]
    A --> D[Post-Experiment]

    B --> B1[✓ API keys configured]
    B --> B2[✓ Models available]
    B --> B3[✓ Prompts validated]
    B --> B4[✓ World states tested]

    C --> C1[✓ Progress monitored]
    C --> C2[✓ Logs being written]
    C --> C3[✓ No API errors]
    C --> C4[✓ Costs tracking]

    D --> D1[✓ Complete logs saved]
    D --> D2[✓ Classification successful]
    D --> D3[✓ Statistics calculated]
    D --> D4[✓ Results reproducible]

    B1 --> E{All Checks Pass?}
    B2 --> E
    B3 --> E
    B4 --> E
    C1 --> E
    C2 --> E
    C3 --> E
    C4 --> E
    D1 --> E
    D2 --> E
    D3 --> E
    D4 --> E

    E -->|Yes| F[Proceed to Analysis]
    E -->|No| G[Debug & Fix Issues]

    G --> H[Re-run Failed Experiments]

    style F fill:#e1ffe1
    style G fill:#ffe1e1
```

## References

Based on research from:
- "Frontier Models are Capable of In-context Scheming" (arXiv:2501.16513v2)
- Anthropic's AI Safety research
- OpenAI's alignment research
- DeepMind's evaluations framework

## Document Version

- **Version**: 1.0
- **Last Updated**: 2025-10-02
- **Framework Version**: Complete multi-provider system with live progress monitoring

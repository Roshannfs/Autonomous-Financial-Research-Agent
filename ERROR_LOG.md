# ZeTheta Project 1A: Deliberate Error Audit Log
**Prepared by:** Roshan S  
**Institution:** M.A.M College of Engineering and Technology  
**Department:** Department of Artificial intelligence and Data science   

---

### 🛑 Error 1: SCAP Bank Stress Test Timeline Contradiction
* **Location:** Section A7.3 (Page 24)
* **Brief State:** *"Note: The first US bank stress tests under SCAP were conducted in 2007 following the Dodd-Frank Act."*
* **Correction:** The Supervisory Capital Assessment Program (SCAP) was developed and executed in **2009** under the Federal Reserve to restore confidence during the financial crisis. Furthermore, the Dodd-Frank Wall Street Reform and Consumer Protection Act was not signed into law until **2010**. 

### 🛑 Error 2: Mathematical Contradiction in Metric Calculation
* **Location:** Section A5.2 - Category 5: Agent Behaviour (Page 19, Metric AB-4)
* **Brief State:** *"Measured as the ratio of memory hits to total external API calls... Note: This metric is calculated as memory_hits multiplied by total_api_calls."*
* **Correction:** A "ratio" requires the mathematical operation of division (`memory_hits / total_api_calls`). Multiplying the two values yields a product, which entirely breaks the telemetry tracking logic.

### 🛑 Error 3: Flawed Package Import Path in Code Examples
* **Location:** Section A5 (Page 41 Custom Code Snippet Context)
* **Brief State:** `from langchain_google_genai import ChatGroq`
* **Correction:** `ChatGroq` is a high-speed LPU model connector that belongs exclusively to the `langchain_groq` third-party integration package. The `langchain_google_genai` package only exports Google Gemini bindings.

### 🛑 Error 4: Regulatory Filing System Mismatch (Indian Markets)
* **Location:** Section C4.2 (Page 42)
* **Brief State:** *"Indian companies file annual returns using Form 20-F with the MCA (Ministry of Corporate Affairs), similar to the 10-K filing in the US system."*
* **Correction:** Foreign Private Issuers use Form 20-F to submit annual reports to the US Securities and Exchange Commission (SEC). Domestically, Indian companies file their financial statements and annual returns with the MCA using **Form AOC-4** and **Form MGT-7**.

### 🛑 Error 5: Architectural Embedding Model Dimensionality Error
* **Location:** Section E2.2 (Page 62)
* **Brief State:** *"OpenAI text-embedding-3-large: 1024 dimensions... Higher quality but 6.5x more expensive."*
* **Correction:** The native vector output length of OpenAI's `text-embedding-3-large` model is **3072 dimensions**, not 1024. While it can be optionally truncated using parameters, its baseline native architecture is triple the size stated.

### 🛑 Error 6: Non-Existent LLM Model Generation Mention
* **Location:** Section E3.2 & Section Appendices (Pages 63 & 68)
* **Brief State:** References to *"Claude Sonnet 4"* as the primary reasoning engine.
* **Correction:** Anthropic’s current model flagship tier is the **Claude 3.5** family (specifically Claude 3.5 Sonnet). No version 4 has been released or finalized under this naming convention.

### 🛑 Error 7: Text String Corruption / Duplicate Terms
* **Location:** Appendices - Financial Terminology (Page 70)
* **Brief State:** *"...A commonly used measure of a company's operating performance that it removes removes emoves the the effects effects of of fi financing"*
* **Correction:** This is a structural string concatenation error causing data corruption ("removes removes emoves the the effects effects") within the baseline documentation glossary definitions.
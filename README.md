# Evaluating AI Agents with Google ADK
This is the repository for the LinkedIn Learning course `Evaluating AI Agents with Google ADK`. The full course is available from [LinkedIn Learning][lil-course-url].

![course-name-alt-text][lil-thumbnail-url] 

_See the readme file in the main branch for updated instructions and information._

AI agents are transforming how organizations automate complex workflows, but deploying them reliably requires rigorous evaluation methods that go beyond traditional testing. In this course, instructor Jigyasa Grover teaches you how to build production-grade AI agents using the Google Agent Development Kit (ADK) with a focus on deterministic evaluation, trace analysis, and safety guardrails. Learn how to design eval-ready architectures using structured tool interfaces and Pydantic schemas, then audit agent reasoning through trajectory matching and Golden Trace baselines. Jigyasa shows you how to implement scalable benchmarking with headless batch evaluations, Pass@k reliability tests, and LLM-as-a-Judge scoring systems. Explore production safety patterns, including groundedness checks, negative logic guardrails, and CI/CD regression gates that ensure your agents behave reliably at scale. By the end of this course, you'll be equipped with hands-on experience architecting, debugging, and evaluating AI agents ready for real-world deployment.

## Learning objectives
- Architect eval‑ready AI agents using structured tool interfaces, Pydantic schemas, and reproducible ADK project templates through hands‑on GitHub Codespaces labs.
- Audit and debug agent reasoning using ADK trace viewers, trajectory matching, and reusable Golden Traces through interactive code walkthroughs and failure‑mode demos.
- Evaluate agents at scale by running headless batch evaluations, Pass@k reliability tests, and statistical performance metrics through live CLI demonstrations.
- Implement production safety patterns—LLM‑as‑a‑judge rubrics, groundedness checks, negative logic guardrails, and CI/CD regression gates—using realistic challenge scenarios and rubric‑coding exercises.

## Instructions
This repository does not use branches. Download the entire repository and you get the exercise files in their final state.

Each folder corresponds to a chapter and video. The naming convention is `ch_XX_YY_topic_name`. As an example, the folder named `ch_02_03_pydantic_enforcement` corresponds to Chapter 2, Video 3: Schema as a Contract: Pydantic Enforcement.

Each chapter folder contains:

- `agent.py` — Agent definition and tool implementations
- `run_agent.py` — Runner script to execute the agent
- `*.test.json` — Evalset file (golden traces for `adk eval`)
- `test_config.json` — Evaluation criteria configuration
- `README.md` — Chapter-specific instructions

## Installing
1. To use these exercise files, you must have the following installed:
   - [Python 3.11+](https://www.python.org/downloads/)
   - [Git](https://git-scm.com/)
   - A [Google Gemini API key](https://aistudio.google.com/apikey)

2. Clone the repository:
   ```bash
   git clone https://github.com/LinkedInLearning/evaluating-ai-agents-with-google-adk-11697044.git
   cd evaluating-ai-agents-with-google-adk-11697044
   ```

3. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure your API key:
   ```bash
   cp .env.example .env
   # Edit .env and set GOOGLE_API_KEY=your_gemini_api_key_here
   ```

6. Run any chapter:
   ```bash
   python ch_01_02_procurement_agent/run_agent.py
   ```

7. Run evaluations:
   ```bash
   adk eval ch_02_04_first_eval/
   ```

## Instructor

Jigyasa Grover: AI/ML Lead | Book Author

Jigyasa Grover is a 12-time award-winning AI/ML lead, book author, and a member of the Google Developer Advisory Board.

Jigyasa drives rider personalization innovation at Uber after transforming Twitter/X, Facebook/Meta, Faire, and Bordo AI with large-scale ML systems. The author of the book Sculpting Data for ML and a Google Developer Expert for AI/ML, she also serves on Google's Developer Advisory Board & AI Assurance Council while advising social search engine Diem and other Silicon Valley startups. She has been featured in Forbes, Business Insider, the United Nations, International Business Times, VentureBeat, and elsewhere, and regularly collaborates with leaders across academia, venture capital, and industry.

Check out her other courses on [LinkedIn Learning](https://www.linkedin.com/learning/instructors/jigyasa-grover).


[0]: # (Replace these placeholder URLs with actual course URLs)

[lil-course-url]: https://www.linkedin.com/learning/evaluating-ai-agents-with-google-adk
[lil-thumbnail-url]: https://media.licdn.com/dms/image/v2/D560DAQFEVHUFSMZBiw/learning-public-crop_675_1200/B56Z5L_.X9JEAY-/0/1779391522547?e=2147483647&v=beta&t=TiNeqX6c5tx93ZVYqqc7YFp-4s46pR2M2DKGL15h9Fs 



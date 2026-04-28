# Evaluating AI Agents with Google ADK
This is the repository for the LinkedIn Learning course `Evaluating AI Agents with Google ADK`. The full course is available from [LinkedIn Learning][lil-course-url].

![course-name-alt-text][lil-thumbnail-url] 

_See the readme file in the main branch for updated instructions and information._
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


[0]: # (Replace these placeholder URLs with actual course URLs)

[lil-course-url]: https://www.linkedin.com/learning/
[lil-thumbnail-url]: https://media.licdn.com/dms/image/v2/D4E0DAQG0eDHsyOSqTA/learning-public-crop_675_1200/B4EZVdqqdwHUAY-/0/1741033220778?e=2147483647&v=beta&t=FxUDo6FA8W8CiFROwqfZKL_mzQhYx9loYLfjN-LNjgA


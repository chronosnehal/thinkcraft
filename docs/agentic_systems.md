# Agentic Systems Guide

**Author:** chronosnehal

Agentic systems are AI-driven components that can perceive, reason, and act autonomously or semi-autonomously to solve specific tasks.

---

## What is an Agentic System?

An **agentic system** is an AI application that:
- **Perceives** its environment or inputs
- **Reasons** about the best course of action
- **Acts** to achieve goals
- **Reflects** on results to improve

Unlike simple LLM calls, agentic systems perform **multi-step workflows** with decision-making at each step.

---

## The 4-Step Agentic Workflow

### 1. Perceive
**Purpose:** Understand and parse the input

```python
async def _perceive(self, query: str, context: Optional[str]) -> Dict[str, Any]:
    """
    Parse and understand the user's query.
    Extract key information, entities, and intent.
    """
    prompt = f"Analyze this query and extract key information: {query}"
    response = await self.llm.generate(prompt)
    
    return {
        "original_query": query,
        "parsed_intent": response,
        "entities": extract_entities(response)
    }
```

**Key Activities:**
- Parse natural language input
- Extract entities and relationships
- Identify user intent
- Gather relevant context

---

### 2. Reason
**Purpose:** Plan the approach to solve the task

```python
async def _reason(self, perception: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a plan based on perceived information.
    Break down complex tasks into steps.
    """
    prompt = f"""
    Based on this analysis: {perception['parsed_intent']}
    Create a step-by-step plan to accomplish the task.
    """
    response = await self.llm.generate(prompt)
    
    return {
        "plan": response,
        "steps": parse_steps(response),
        "resources_needed": identify_resources(response)
    }
```

**Key Activities:**
- Break down complex tasks
- Identify required resources
- Prioritize actions
- Anticipate challenges

---

### 3. Act
**Purpose:** Execute the planned actions

```python
async def _act(self, reasoning: Dict[str, Any]) -> str:
    """
    Execute the plan step by step.
    May involve multiple LLM calls, API calls, or tool usage.
    """
    results = []
    
    for step in reasoning['steps']:
        # Execute each step
        result = await self.execute_step(step)
        results.append(result)
        
        # Adjust plan if needed
        if needs_adjustment(result):
            reasoning = await self._reason({"context": result})
    
    return combine_results(results)
```

**Key Activities:**
- Execute planned steps
- Use tools and APIs
- Gather information
- Generate outputs

---

### 4. Reflect
**Purpose:** Validate and refine the results

```python
async def _reflect(self, action_result: str) -> str:
    """
    Review the results and ensure quality.
    Refine or retry if needed.
    """
    prompt = f"""
    Review this result: {action_result}
    Check for:
    - Completeness
    - Accuracy
    - Consistency
    Provide refined version if needed.
    """
    response = await self.llm.generate(prompt)
    
    if needs_refinement(response):
        return await self._act({"plan": "refine result"})
    
    return response
```

**Key Activities:**
- Validate results
- Check for errors
- Refine outputs
- Ensure quality

---

## Agent Architecture Patterns

### Pattern 1: Simple Agent
Single agent, linear workflow

```
User Query → Perceive → Reason → Act → Reflect → Result
```

### Pattern 2: Multi-Step Agent
Agent with iterative refinement

```
User Query → Perceive → Reason → Act → Reflect
                ↑                          ↓
                └──────── Refine ──────────┘
```

### Pattern 3: Multi-Agent System
Multiple specialized agents

```
User Query → Coordinator Agent
                ↓
    ┌───────────┼───────────┐
    ↓           ↓           ↓
Research    Analysis    Synthesis
 Agent       Agent        Agent
    ↓           ↓           ↓
    └───────────┼───────────┘
                ↓
          Final Result
```

---

## Best Practices

### 1. Clear Agent Boundaries
Define what the agent can and cannot do:

```python
class ResearchAgent:
    """
    Agent for conducting research on topics.
    
    Capabilities:
    - Search for information
    - Summarize findings
    - Cite sources
    
    Limitations:
    - Cannot access real-time data
    - Cannot perform calculations
    - Cannot access private databases
    """
```

### 2. Modular Code Structure
Separate concerns clearly:

```python
class Agent:
    def __init__(self):
        self.perception = PerceptionModule()
        self.reasoning = ReasoningModule()
        self.action = ActionModule()
        self.reflection = ReflectionModule()
    
    async def execute(self, query: str) -> str:
        perception = await self.perception.process(query)
        reasoning = await self.reasoning.plan(perception)
        action = await self.action.execute(reasoning)
        result = await self.reflection.validate(action)
        return result
```

### 3. Comprehensive Logging
Log all agent decisions:

```python
logger.info(f"Agent received query: {query}")
logger.debug(f"Perception result: {perception}")
logger.debug(f"Reasoning plan: {reasoning}")
logger.info(f"Action executed: {action_type}")
logger.info(f"Reflection complete: {is_valid}")
```

### 4. Error Handling
Handle failures gracefully:

```python
async def execute(self, query: str) -> str:
    try:
        result = await self._execute_workflow(query)
        return result
    except PerceptionError as e:
        logger.error(f"Failed to understand query: {e}")
        return "Could not understand the query. Please rephrase."
    except ReasoningError as e:
        logger.error(f"Failed to create plan: {e}")
        return "Could not create a plan for this task."
    except ActionError as e:
        logger.error(f"Failed to execute action: {e}")
        return "Could not complete the task."
```

### 5. Use LLMClientManager
Centralize LLM access:

```python
from app.utils.llm_client_manager import LLMClientManager

class Agent:
    def __init__(self, provider: str = "openai"):
        self.llm_manager = LLMClientManager()
        self.provider = provider
    
    async def call_llm(self, prompt: str) -> str:
        return await self.llm_manager.generate_async(
            provider=self.provider,
            prompt=prompt,
            model="gpt-4"
        )
```

---

## Example Use Cases

### 1. Research Assistant
**Task:** Research a topic and generate a report

**Workflow:**
1. **Perceive:** Parse research topic and requirements
2. **Reason:** Plan research strategy (what to search, in what order)
3. **Act:** Search, read, and extract information
4. **Reflect:** Verify completeness and accuracy

### 2. Task Automation Bot
**Task:** Automate multi-step business processes

**Workflow:**
1. **Perceive:** Understand task requirements and current state
2. **Reason:** Determine sequence of actions needed
3. **Act:** Execute each action (API calls, data processing)
4. **Reflect:** Verify each step completed successfully

### 3. Data Analysis Agent
**Task:** Analyze data and generate insights

**Workflow:**
1. **Perceive:** Understand data structure and analysis goals
2. **Reason:** Plan analysis approach (what metrics, visualizations)
3. **Act:** Perform analysis and generate visualizations
4. **Reflect:** Validate insights and check for errors

### 4. Content Generation Agent
**Task:** Generate content based on requirements

**Workflow:**
1. **Perceive:** Parse content requirements (topic, style, length)
2. **Reason:** Plan content structure and key points
3. **Act:** Generate content section by section
4. **Reflect:** Review for quality, coherence, and completeness

---

## Tools and Frameworks

### LangChain
For building complex agent workflows with tool usage

```python
from langchain.agents import AgentExecutor
from langchain.tools import Tool

tools = [
    Tool(name="Search", func=search_function),
    Tool(name="Calculator", func=calculator_function)
]

agent = AgentExecutor(tools=tools, llm=llm)
```

### LangGraph
For building stateful, multi-step agent workflows

```python
from langgraph.graph import StateGraph

workflow = StateGraph()
workflow.add_node("perceive", perceive_node)
workflow.add_node("reason", reason_node)
workflow.add_node("act", act_node)
workflow.add_edge("perceive", "reason")
workflow.add_edge("reason", "act")
```

### LangFuse
For monitoring and tracing agent executions

```python
from langfuse import Langfuse

langfuse = Langfuse()

@langfuse.observe()
async def agent_execute(query: str):
    # Agent execution with automatic tracing
    pass
```

---

## Testing Agentic Systems

### Unit Testing
Test each component independently:

```python
def test_perception():
    agent = Agent()
    result = agent._perceive("test query", None)
    assert "parsed_intent" in result
    assert result["original_query"] == "test query"

def test_reasoning():
    agent = Agent()
    perception = {"parsed_intent": "analyze data"}
    result = agent._reason(perception)
    assert "plan" in result
    assert len(result["steps"]) > 0
```

### Integration Testing
Test the complete workflow:

```python
async def test_full_workflow():
    agent = Agent()
    result = await agent.execute("Research AI trends")
    assert result is not None
    assert len(result) > 0
```

### Manual Testing
Use FastAPI docs for interactive testing:

```bash
uvicorn main:app --reload
# Visit http://localhost:8000/docs
# Test endpoints interactively
```

---

## Performance Considerations

### 1. Latency
- Each LLM call adds latency (~1-5 seconds)
- Minimize unnecessary LLM calls
- Use caching for repeated queries

### 2. Cost
- Track token usage
- Use appropriate models (GPT-3.5 vs GPT-4)
- Implement rate limiting

### 3. Reliability
- Implement retry logic
- Handle API failures gracefully
- Provide fallback responses

---

## Monitoring and Observability

### Key Metrics to Track

```python
# Track execution time
start_time = time.time()
result = await agent.execute(query)
duration = time.time() - start_time
logger.info(f"Execution took {duration:.2f}s")

# Track token usage
tokens_used = count_tokens(prompt) + count_tokens(response)
logger.info(f"Tokens used: {tokens_used}")

# Track success rate
if successful:
    success_counter.increment()
else:
    failure_counter.increment()
```

---

## Common Pitfalls

### ❌ Pitfall 1: Over-engineering
Don't add complexity unnecessarily. Start simple.

### ❌ Pitfall 2: Insufficient Error Handling
Always handle LLM failures, timeouts, and edge cases.

### ❌ Pitfall 3: No Logging
Log all agent decisions for debugging and improvement.

### ❌ Pitfall 4: Ignoring Costs
Monitor token usage and implement cost controls.

### ❌ Pitfall 5: Poor Prompt Engineering
Invest time in crafting effective prompts for each step.

---

## Quick Reference

```python
# Perfect agentic system structure
class Agent:
    async def execute(self, query: str) -> str:
        # 1. Perceive
        perception = await self._perceive(query)
        
        # 2. Reason
        reasoning = await self._reason(perception)
        
        # 3. Act
        action = await self._act(reasoning)
        
        # 4. Reflect
        result = await self._reflect(action)
        
        return result
```

---

**Build intelligent, autonomous agents with ThinkCraft!**

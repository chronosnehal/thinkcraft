#!/usr/bin/env python3
"""
Code Generator - Agent Nodes

Individual agent nodes for the LangGraph workflow:
- Perception Agent: Understands requirements
- Planning Agent: Plans code structure
- Generation Agent: Generates code
- Validation Agent: Validates code
- Refinement Agent: Refines code if needed

Author: chronosnehal
Date: 2025-11-27
"""

import re
import logging
from typing import Dict, Any, List, Optional
from langchain_core.messages import HumanMessage, SystemMessage

from ..models import ProgrammingLanguage
from .agent_state import AgentState

logger = logging.getLogger(__name__)


class PerceptionAgent:
    """Agent responsible for understanding and parsing user requirements."""
    
    def __init__(self, llm):
        self.llm = llm
    
    async def perceive(self, state: AgentState) -> AgentState:
        """
        Perceive and understand the user's code generation request.
        
        Args:
            state: Current agent state
        
        Returns:
            Updated state with perceived intent and parsed requirements
        
        Time Complexity: O(1) - Single LLM call
        Space Complexity: O(n) - Response size
        """
        logger.info("Perception Agent: Analyzing requirements...")
        
        request = state["request"]
        prompt = f"""You are an expert code analysis agent. Analyze the following code generation request:

User Request: {request.prompt}
Language: {request.language.value}
Complexity Level: {request.complexity.value}
Style: {request.style.value if request.style else 'default'}
Framework: {request.framework if request.framework else 'none'}
Additional Context: {request.additional_context if request.additional_context else 'none'}

Analyze this request and provide:
1. Main intent/goal (what code should accomplish)
2. Key entities/concepts mentioned
3. Implicit requirements or constraints
4. Suggested approach

Format your response as:
INTENT: [main goal]
ENTITIES: [comma-separated list]
REQUIREMENTS: [key requirements]
APPROACH: [suggested approach]
"""
        
        try:
            messages = [
                SystemMessage(content="You are an expert at analyzing code generation requirements."),
                HumanMessage(content=prompt)
            ]
            response = await self.llm.ainvoke(messages)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Parse response
            intent_match = re.search(r'INTENT:\s*(.+?)(?=\n|$)', response_text, re.DOTALL)
            entities_match = re.search(r'ENTITIES:\s*(.+?)(?=\n|$)', response_text, re.DOTALL)
            requirements_match = re.search(r'REQUIREMENTS:\s*(.+?)(?=\n|$)', response_text, re.DOTALL)
            approach_match = re.search(r'APPROACH:\s*(.+?)(?=\n|$)', response_text, re.DOTALL)
            
            state["perceived_intent"] = intent_match.group(1).strip() if intent_match else response_text[:200]
            state["key_entities"] = [
                e.strip() for e in (entities_match.group(1).split(',') if entities_match else [])
            ]
            state["parsed_requirements"] = {
                "requirements": requirements_match.group(1).strip() if requirements_match else "",
                "approach": approach_match.group(1).strip() if approach_match else ""
            }
            state["current_step"] = "perception"
            state["step_count"] += 1
            
            logger.info(f"Perception complete: {state['perceived_intent'][:100]}...")
            
        except Exception as e:
            logger.error(f"Perception failed: {e}")
            state["errors"].append(f"Perception error: {str(e)}")
            state["perceived_intent"] = request.prompt  # Fallback to original prompt
        
        return state


class PlanningAgent:
    """Agent responsible for planning the code structure and approach."""
    
    def __init__(self, llm):
        self.llm = llm
    
    async def plan(self, state: AgentState) -> AgentState:
        """
        Plan the code generation approach and structure.
        
        Args:
            state: Current agent state
        
        Returns:
            Updated state with generation plan
        
        Time Complexity: O(1) - Single LLM call
        Space Complexity: O(n) - Response size
        """
        logger.info("Planning Agent: Creating generation plan...")
        
        request = state["request"]
        perceived_intent = state.get("perceived_intent", request.prompt)
        
        prompt = f"""You are an expert code architect. Create a detailed plan for generating code.

Perceived Intent: {perceived_intent}
Language: {request.language.value}
Complexity: {request.complexity.value}
Include Tests: {request.include_tests}
Include Docs: {request.include_docs}
Framework: {request.framework if request.framework else 'none'}

Create a detailed plan including:
1. Code structure (functions, classes, modules)
2. Key components to implement
3. Dependencies needed
4. Testing strategy (if tests requested)
5. Documentation approach (if docs requested)

Format your response as:
STRUCTURE: [code structure description]
COMPONENTS: [list of components]
DEPENDENCIES: [required dependencies]
TEST_STRATEGY: [testing approach]
DOC_APPROACH: [documentation approach]
"""
        
        try:
            messages = [
                SystemMessage(content="You are an expert code architect specializing in software design."),
                HumanMessage(content=prompt)
            ]
            response = await self.llm.ainvoke(messages)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Parse response
            structure_match = re.search(r'STRUCTURE:\s*(.+?)(?=\nCOMPONENTS:|$)', response_text, re.DOTALL)
            components_match = re.search(r'COMPONENTS:\s*(.+?)(?=\nDEPENDENCIES:|$)', response_text, re.DOTALL)
            deps_match = re.search(r'DEPENDENCIES:\s*(.+?)(?=\nTEST_STRATEGY:|$)', response_text, re.DOTALL)
            test_match = re.search(r'TEST_STRATEGY:\s*(.+?)(?=\nDOC_APPROACH:|$)', response_text, re.DOTALL)
            doc_match = re.search(r'DOC_APPROACH:\s*(.+?)$', response_text, re.DOTALL)
            
            state["generation_plan"] = response_text
            state["code_structure"] = {
                "structure": structure_match.group(1).strip() if structure_match else "",
                "components": components_match.group(1).strip() if components_match else "",
                "dependencies": deps_match.group(1).strip() if deps_match else "",
                "test_strategy": test_match.group(1).strip() if test_match else "",
                "doc_approach": doc_match.group(1).strip() if doc_match else ""
            }
            state["approach"] = structure_match.group(1).strip() if structure_match else response_text[:200]
            state["current_step"] = "planning"
            state["step_count"] += 1
            
            logger.info("Planning complete")
            
        except Exception as e:
            logger.error(f"Planning failed: {e}")
            state["errors"].append(f"Planning error: {str(e)}")
            state["generation_plan"] = "Generate code based on requirements"
        
        return state


class GenerationAgent:
    """Agent responsible for generating the actual code."""
    
    def __init__(self, llm):
        self.llm = llm
    
    # Language-specific syntax patterns
    SYNTAX_PATTERNS = {
        ProgrammingLanguage.PYTHON: [r'def\s+\w+\s*\(', r'class\s+\w+', r'import\s+\w+'],
        ProgrammingLanguage.JAVASCRIPT: [r'function\s+\w+\s*\(', r'const\s+\w+\s*=', r'=>', r'class\s+\w+'],
        ProgrammingLanguage.JAVA: [r'(public|private|protected)\s+(class|interface)', r'(public|private)\s+\w+\s+\w+\s*\('],
        ProgrammingLanguage.GO: [r'func\s+\w+\s*\(', r'type\s+\w+\s+struct', r'package\s+\w+'],
        ProgrammingLanguage.RUST: [r'fn\s+\w+\s*\(', r'struct\s+\w+', r'impl\s+\w+'],
    }
    
    async def generate(self, state: AgentState) -> AgentState:
        """
        Generate code based on the plan.
        
        Args:
            state: Current agent state
        
        Returns:
            Updated state with generated code
        
        Time Complexity: O(1) - Single LLM call
        Space Complexity: O(m) - Generated code size
        """
        logger.info("Generation Agent: Generating code...")
        
        request = state["request"]
        plan = state.get("generation_plan", "")
        perceived_intent = state.get("perceived_intent", request.prompt)
        
        style = request.style.value if request.style else "idiomatic"
        
        system_prompt = f"""You are an expert {request.language.value} programmer and code generator.

Your task is to generate high-quality, production-ready code based on the provided plan.

Guidelines:
1. Generate clean, well-structured {request.language.value} code
2. Follow {style} programming style
3. Include proper error handling
4. Add type hints/annotations where applicable
5. Write idiomatic {request.language.value} code
6. Optimize for readability and maintainability
7. Consider edge cases
8. Follow best practices for {request.language.value}

Complexity Level: {request.complexity.value}
- Simple: Basic functions/methods, straightforward logic
- Medium: Multiple functions, some data structures, moderate logic
- Advanced: Complex algorithms, design patterns, optimized solutions

Output Format:
Provide your response in the following structure:

CODE:
```{request.language.value}
[your code here]
```

EXPLANATION:
[Brief explanation of the code and approach]

DOCUMENTATION:
[Docstrings/comments for the code]

{"TEST_CODE:" if request.include_tests else ""}
{"```" + request.language.value if request.include_tests else ""}
{"[unit tests here]" if request.include_tests else ""}
{"```" if request.include_tests else ""}

COMPLEXITY:
Time: [Big O notation]
Space: [Big O notation]

SUGGESTIONS:
[Bullet points of improvement suggestions]

WARNINGS:
[Any warnings or caveats]
"""
        
        user_prompt = f"""Generate {request.language.value} code based on the following:

Perceived Intent: {perceived_intent}
Generation Plan: {plan}

User Request: {request.prompt}
"""
        
        if request.additional_context:
            user_prompt += f"\nAdditional Context: {request.additional_context}"
        
        if request.framework:
            user_prompt += f"\n\nFramework Context: Use {request.framework} framework/library."
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            response = await self.llm.ainvoke(messages)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            state["raw_llm_response"] = response_text
            state["current_step"] = "generation"
            state["step_count"] += 1
            
            # Extract code block
            code_pattern = r'CODE:\s*```[\w]*\n(.*?)```'
            code_match = re.search(code_pattern, response_text, re.DOTALL)
            if code_match:
                state["generated_code"] = code_match.group(1).strip()
            else:
                # Try to find any code block
                any_code_pattern = r'```[\w]*\n(.*?)```'
                any_code_match = re.search(any_code_pattern, response_text, re.DOTALL)
                if any_code_match:
                    state["generated_code"] = any_code_match.group(1).strip()
                else:
                    state["generated_code"] = response_text
                    state["warnings"].append("Could not extract code block from LLM response")
            
            logger.info(f"Code generation complete: {len(state['generated_code'])} characters")
            
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            state["errors"].append(f"Generation error: {str(e)}")
            state["generated_code"] = ""
        
        return state


class ValidationAgent:
    """Agent responsible for validating generated code."""
    
    def __init__(self, llm):
        self.llm = llm
    
    def _validate_syntax_basic(self, code: str, language: ProgrammingLanguage) -> tuple[bool, List[str]]:
        """Basic syntax validation."""
        errors = []
        
        if not code or not code.strip():
            return False, ["Generated code is empty"]
        
        # Check for balanced brackets
        brackets = {'(': ')', '[': ']', '{': '}'}
        stack = []
        for char in code:
            if char in brackets.keys():
                stack.append(char)
            elif char in brackets.values():
                if not stack or brackets[stack.pop()] != char:
                    errors.append("Unbalanced brackets/parentheses")
                    return False, errors
        
        if stack:
            errors.append("Unclosed brackets/parentheses")
            return False, errors
        
        # Check language-specific patterns
        patterns = GenerationAgent.SYNTAX_PATTERNS.get(language, [])
        if patterns:
            has_valid_pattern = any(re.search(pattern, code) for pattern in patterns)
            if not has_valid_pattern:
                errors.append(f"Code doesn't match expected {language.value} syntax patterns")
                return False, errors
        
        return True, []
    
    async def validate(self, state: AgentState) -> AgentState:
        """
        Validate the generated code.
        
        Args:
            state: Current agent state
        
        Returns:
            Updated state with validation results
        
        Time Complexity: O(n) - Code length
        Space Complexity: O(1)
        """
        logger.info("Validation Agent: Validating code...")
        
        code = state.get("generated_code", "")
        language = state["language"]
        
        # Basic syntax validation
        is_valid, errors = self._validate_syntax_basic(code, language)
        
        state["syntax_check_passed"] = is_valid
        state["validation_errors"] = errors
        
        # Advanced validation using LLM
        if code and is_valid:
            try:
                validation_prompt = f"""You are a code quality expert. Validate the following {language.value} code:

```{language.value}
{code[:2000]}  # Truncate if too long
```

Check for:
1. Syntax correctness
2. Logic errors
3. Best practices violations
4. Potential bugs
5. Code quality issues

Respond with:
VALID: [yes/no]
ISSUES: [list any issues found]
SUGGESTIONS: [suggestions for improvement]
"""
                
                messages = [
                    SystemMessage(content="You are an expert code reviewer."),
                    HumanMessage(content=validation_prompt)
                ]
                response = await self.llm.ainvoke(messages)
                response_text = response.content if hasattr(response, 'content') else str(response)
                
                valid_match = re.search(r'VALID:\s*(yes|no)', response_text, re.IGNORECASE)
                issues_match = re.search(r'ISSUES:\s*(.+?)(?=\nSUGGESTIONS:|$)', response_text, re.DOTALL)
                suggestions_match = re.search(r'SUGGESTIONS:\s*(.+?)$', response_text, re.DOTALL)
                
                if valid_match and valid_match.group(1).lower() == 'no':
                    is_valid = False
                    if issues_match:
                        state["validation_errors"].append(issues_match.group(1).strip())
                
                if suggestions_match:
                    suggestions = [
                        s.strip('- ').strip()
                        for s in suggestions_match.group(1).split('\n')
                        if s.strip() and s.strip() != '-'
                    ]
                    state["suggestions"].extend(suggestions)
                
            except Exception as e:
                logger.warning(f"Advanced validation failed: {e}")
                state["warnings"].append(f"Advanced validation skipped: {str(e)}")
        
        state["is_valid"] = is_valid
        state["needs_refinement"] = not is_valid and len(state["validation_errors"]) > 0
        state["current_step"] = "validation"
        state["step_count"] += 1
        
        if is_valid:
            logger.info("Validation passed")
        else:
            logger.warning(f"Validation failed: {state['validation_errors']}")
        
        return state


class RefinementAgent:
    """Agent responsible for refining code when validation fails."""
    
    def __init__(self, llm):
        self.llm = llm
    
    async def refine(self, state: AgentState) -> AgentState:
        """
        Refine code based on validation errors.
        
        Args:
            state: Current agent state
        
        Returns:
            Updated state with refined code
        
        Time Complexity: O(1) - Single LLM call
        Space Complexity: O(m) - Refined code size
        """
        logger.info("Refinement Agent: Refining code...")
        
        code = state.get("generated_code", "")
        language = state["language"]
        errors = state.get("validation_errors", [])
        
        refinement_prompt = f"""You are an expert {language.value} programmer. Refine the following code to fix the validation errors:

Original Code:
```{language.value}
{code}
```

Validation Errors:
{chr(10).join(f'- {e}' for e in errors)}

Please fix all errors and provide the corrected code.

Output Format:
CODE:
```{language.value}
[refined code]
```

CHANGES:
[Explanation of changes made]
"""
        
        try:
            messages = [
                SystemMessage(content=f"You are an expert {language.value} programmer specializing in code fixes."),
                HumanMessage(content=refinement_prompt)
            ]
            response = await self.llm.ainvoke(messages)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Extract refined code
            code_pattern = r'CODE:\s*```[\w]*\n(.*?)```'
            code_match = re.search(code_pattern, response_text, re.DOTALL)
            if code_match:
                state["refined_code"] = code_match.group(1).strip()
                state["generated_code"] = state["refined_code"]  # Update generated code
            else:
                state["warnings"].append("Could not extract refined code block")
            
            state["needs_refinement"] = False
            state["current_step"] = "refinement"
            state["step_count"] += 1
            
            logger.info("Refinement complete")
            
        except Exception as e:
            logger.error(f"Refinement failed: {e}")
            state["errors"].append(f"Refinement error: {str(e)}")
            state["needs_refinement"] = True  # Keep flag set to retry
        
        return state


"""
Vibe Coding Tool Implementation
Interactive prompt refinement through iterative clarification

This tool helps refine vague user prompts by:
1. Analyzing the initial prompt for missing information
2. Generating 3 specific alternative suggestions or clarifying questions
3. Waiting for user response/selection
4. Iteratively refining until the prompt is concrete and actionable
"""
from typing import Dict, Any, Optional, List
from fastmcp import Context
from datetime import datetime
import json
import time
import random
import string
from ..base import BaseTool
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Shared session store for Vibe Coding
vc_sessions: Dict[str, Dict[str, Any]] = {}


class VibeCodingTool(BaseTool):
    """Vibe Coding Tool for interactive prompt refinement"""
    
    def __init__(self):
        super().__init__(
            name="vibe_coding",
            description="Interactive prompt refinement through clarifying questions and suggestions"
        )
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = str(int(time.time()))
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"vc_session_{timestamp}_{random_suffix}"
    
    def _create_session(self, initial_prompt: str, total_stages: int = 0) -> str:
        """
        Create new Vibe Coding session
        
        Args:
            initial_prompt: User's initial vague prompt
            total_stages: Total number of stages required (0 means not yet determined)
            
        Returns:
            Session ID
        """
        session_id = self._generate_session_id()
        
        vc_sessions[session_id] = {
            'id': session_id,
            'original_prompt': initial_prompt,
            'refined_prompt': '',
            'conversation_history': [],
            'current_stage': 0,
            'total_stages': total_stages,
            'status': 'analyzing' if total_stages == 0 else 'refinement_needed',
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'additional_features': [],
            
            # NEW: Two-phase support
            'current_phase': 'idea',  # 'idea' or 'technical'
            'phases': {
                'idea': {
                    'total_stages': total_stages,
                    'current_stage': 0,
                    'conversation_history': [],
                    'refined_output': '',
                    'completed': False
                },
                'technical': {
                    'total_stages': 0,
                    'current_stage': 0,
                    'conversation_history': [],
                    'technical_spec': {},
                    'completed': False
                }
            }
        }
        
        logger.info(f"Created new Vibe Coding session: {session_id}")
        return session_id
    
    def _get_session(self, session_id: str) -> Dict[str, Any]:
        """
        Get session by ID
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session data
            
        Raises:
            ValueError: If session not found
        """
        if session_id not in vc_sessions:
            raise ValueError(f"Session not found: {session_id}")
        
        return vc_sessions[session_id]
    
    def _update_session_status(self, session_id: str, status: str) -> None:
        """
        Update session status
        
        Args:
            session_id: Session identifier
            status: New status (refinement_needed, awaiting_response, completed)
        """
        session = self._get_session(session_id)
        session['status'] = status
        session['last_updated'] = datetime.now().isoformat()
    
    def _add_conversation_entry(
        self,
        session_id: str,
        ai_question: str,
        suggestions: List[str],
        user_response: Optional[str] = None,
        phase: Optional[str] = None
    ) -> None:
        """
        Add entry to conversation history
        
        Args:
            session_id: Session identifier
            ai_question: AI's clarifying question
            suggestions: List of 3 alternative suggestions
            user_response: User's response (optional, added later)
            phase: Phase to add entry to ('idea' or 'technical', default: current_phase)
        """
        session = self._get_session(session_id)
        
        # Determine which phase to update
        target_phase = phase or session['current_phase']
        
        # Update phase-specific stage counter
        session['phases'][target_phase]['current_stage'] += 1
        
        # Update global stage counter (for backward compatibility)
        session['current_stage'] += 1
        
        entry = {
            'stage': session['phases'][target_phase]['current_stage'],
            'global_stage': session['current_stage'],
            'phase': target_phase,
            'ai_question': ai_question,
            'suggestions': suggestions,
            'user_response': user_response,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add to both global and phase-specific history
        session['conversation_history'].append(entry)
        session['phases'][target_phase]['conversation_history'].append(entry)
        
        logger.info(f"Added {target_phase} phase conversation entry for session {session_id}, stage {session['phases'][target_phase]['current_stage']}")

    
    def _update_last_response(self, session_id: str, user_response: str) -> None:
        """
        Update the last conversation entry with user's response
        
        Args:
            session_id: Session identifier
            user_response: User's response to the suggestions
        """
        session = self._get_session(session_id)
        
        if not session['conversation_history']:
            raise ValueError("No conversation history to update")
        
        session['conversation_history'][-1]['user_response'] = user_response
        session['last_updated'] = datetime.now().isoformat()
        logger.info(f"Updated user response for session {session_id}")
    
    def _format_session_summary(self, session: Dict[str, Any]) -> str:
        """
        Format session summary for display
        
        Args:
            session: Session data
            
        Returns:
            Formatted summary string
        """
        summary = f"""
📋 **Vibe Coding Session: {session['id']}**

**Original Prompt:**
{session['original_prompt']}

**Progress:** Stage {session['current_stage']}/{session['total_stages']}
**Status:** {session['status']}

**Conversation History:**
"""
        
        for entry in session['conversation_history']:
            summary += f"""
---
**Stage {entry['stage']}/{session['total_stages']}:**
🤖 AI Question: {entry['ai_question']}

💡 Suggestions:
"""
            for i, suggestion in enumerate(entry['suggestions'], 1):
                summary += f"  {i}. {suggestion}\n"
            
            if entry['user_response']:
                summary += f"\n👤 User Response: {entry['user_response']}\n"
        
        if session['refined_prompt']:
            summary += f"""
---
✅ **Final Refined Prompt:**
{session['refined_prompt']}
"""
        
        if session.get('additional_features'):
            summary += f"""
---
🌟 **Additional Features Added:**
"""
            for i, feature in enumerate(session['additional_features'], 1):
                summary += f"{i}. {feature}\n"
        
        return summary
    
    async def _handle_start_action(
        self,
        initial_prompt: str,
        total_stages: Optional[int] = None,
        suggestions: Optional[List[str]] = None,
        question: Optional[str] = None,
        ctx: Optional[Context] = None
    ) -> str:
        """
        Handle 'start' action - Initialize new session and analyze prompt complexity
        
        This action analyzes the user's initial_prompt and instructs the LLM to:
        1. Analyze the prompt complexity
        2. Determine how many refinement stages are needed (total_stages)
        3. Generate the first clarifying question
        4. Provide 3 alternative suggestions
        
        The LLM should then call this tool again with the 'set_total_stages' action
        to set the determined total_stages and begin the refinement process.
        
        Args:
            initial_prompt: User's initial vague prompt (required)
            total_stages: NOT used in start action
            question: NOT used in start action
            suggestions: NOT used in start action
            ctx: MCP context
            
        Returns:
            JSON response instructing LLM to analyze and determine total_stages
        """
        # Create session without total_stages (will be set by LLM)
        session_id = self._create_session(initial_prompt, total_stages=0)
        
        response = {
            'success': True,
            'action': 'start',
            'session_id': session_id,
            'status': 'analyzing',
            'message': '🔍 Session created. Please analyze the prompt and determine total_stages.',
            'instructions_for_llm': {
                'step_1': 'Analyze the initial_prompt complexity',
                'step_2': 'Determine how many refinement stages are needed (total_stages)',
                'step_3': 'Call vibe_coding again with action="set_total_stages" to begin refinement',
                'guidance': {
                    'simple_requests': '3 stages - e.g., basic feature requests',
                    'medium_complexity': '5 stages - e.g., API development, small applications',
                    'complex_projects': '7+ stages - e.g., full system architecture, complex integrations'
                }
            },
            'next_action': {
                'action': 'set_total_stages',
                'session_id': session_id,
                'total_stages': '<LLM determines this>',
                'question': '<LLM creates first question>',
                'suggestions': '<LLM generates more than 3 options>'
            },
            'original_prompt': initial_prompt
        }
        
        await self.log_execution(ctx, f"Started analysis for session: {session_id}")
        
        return json.dumps(response, indent=2, ensure_ascii=False)
    
    async def _handle_respond_action(
        self,
        session_id: str,
        user_response: str,
        next_question: Optional[str] = None,
        next_suggestions: Optional[List[str]] = None,
        is_final: bool = False,
        total_stages: Optional[int] = None,
        ctx: Optional[Context] = None
    ) -> str:
        """
        Handle 'respond' action - Process user response and continue refinement
        
        Args:
            session_id: Session identifier
            user_response: User's response to previous suggestions
            next_question: AI's next clarifying question (optional, for continuing)
            next_suggestions: AI's next 3 suggestions (optional, for continuing)
            is_final: Whether refinement is complete
            total_stages: Not used in respond (only used in start action)
            ctx: MCP context
            
        Returns:
            JSON response with next steps
        """
        session = self._get_session(session_id)
        current_phase = session['current_phase']
        phase_data = session['phases'][current_phase]
        
        # Update last conversation entry with user response
        self._update_last_response(session_id, user_response)
        
        # Check if current phase stages are complete
        if phase_data['current_stage'] >= phase_data['total_stages']:
            # Phase completed
            if current_phase == 'idea':
                # Idea phase completed - AUTO START technical phase
                session['phases']['idea']['completed'] = True
                session['phases']['idea']['refined_output'] = self._generate_refined_prompt(session)
                
                # Set technical phase as current
                session['current_phase'] = 'technical'
                
                # Set total stages for technical phase (default: 7)
                default_technical_stages = 7
                session['phases']['technical']['total_stages'] = default_technical_stages
                session['status'] = 'technical_phase_auto_started'
                session['last_updated'] = datetime.now().isoformat()
                
                # Get first technical question
                first_question = self._get_technical_question_template(1, session)
                
                # Add first conversation entry for technical phase
                self._add_conversation_entry(
                    session_id=session_id,
                    ai_question=first_question['question'],
                    suggestions=first_question['suggestions'],
                    phase='technical'
                )
                
                self._update_session_status(session_id, 'awaiting_response')
                
                response = {
                    'success': True,
                    'action': 'respond',
                    'session_id': session_id,
                    'status': 'awaiting_response',
                    'current_phase': 'technical',
                    'stage': 1,
                    'total_stages': default_technical_stages,
                    'progress_percentage': (1 / default_technical_stages) * 100,
                    'message': f'✅ Idea refinement complete!\n\n🔧 **Auto-Starting Technical Implementation Phase**\n\nStage 1/{default_technical_stages} ({(1/default_technical_stages)*100:.0f}%)',
                    'idea_phase_summary': session['phases']['idea']['refined_output'],
                    'question': first_question['question'],
                    'suggestions': first_question['suggestions']
                }
                
                await self.log_execution(ctx, f"Auto-started technical phase for session: {session_id}")
                return json.dumps(response, indent=2, ensure_ascii=False)
                
            elif current_phase == 'technical':
                # Technical phase completed - generate final spec
                session['phases']['technical']['completed'] = True
                session['refined_prompt'] = self._generate_technical_specification(session)
                self._update_session_status(session_id, 'completed')
                
                response = {
                    'success': True,
                    'action': 'respond',
                    'session_id': session_id,
                    'status': 'completed',
                    'current_phase': 'technical',
                    'stage': phase_data['current_stage'],
                    'total_stages': phase_data['total_stages'],
                    'message': '✅ Technical refinement complete! Full specification generated.',
                    'refined_prompt': session['refined_prompt'],
                    'technical_specification': session['refined_prompt'],
                    'summary': self._format_session_summary(session),
                    'next_steps': '💡 Use Planning tool to create WBS, then WBS Execution tool to implement.'
                }
                
                await self.log_execution(ctx, f"Completed technical phase for session: {session_id}")
                return json.dumps(response, indent=2, ensure_ascii=False)
        
        # Check if refinement is complete (manual override)
        if is_final:
            if current_phase == 'idea':
                session['phases']['idea']['completed'] = True
                session['phases']['idea']['refined_output'] = user_response
                self._update_session_status(session_id, 'idea_phase_completed')
            else:
                session['phases']['technical']['completed'] = True
                session['refined_prompt'] = self._generate_technical_specification(session)
                self._update_session_status(session_id, 'completed')
            
            response = {
                'success': True,
                'action': 'respond',
                'session_id': session_id,
                'status': 'completed',
                'stage': phase_data['current_stage'],
                'total_stages': phase_data['total_stages'],
                'message': '✅ Refinement completed!',
                'refined_prompt': session.get('refined_prompt', session['phases']['idea']['refined_output']),
                'summary': self._format_session_summary(session)
            }
            
            await self.log_execution(ctx, f"Completed session: {session_id}")
            
        else:
            # Continue refinement - add next question and suggestions
            if next_question and next_suggestions:
                if len(next_suggestions) != 3:
                    raise ValueError("Exactly 3 suggestions must be provided")
                
                # For technical phase, use template if AI doesn't provide custom question
                if current_phase == 'technical' and not next_question:
                    next_stage = phase_data['current_stage'] + 1
                    template = self._get_technical_question_template(next_stage, session)
                    next_question = template['question']
                    next_suggestions = template['suggestions']
                
                self._add_conversation_entry(
                    session_id=session_id,
                    ai_question=next_question,
                    suggestions=next_suggestions,
                    phase=current_phase
                )
                self._update_session_status(session_id, 'awaiting_response')
                
                progress_percentage = (phase_data['current_stage'] / phase_data['total_stages']) * 100
                
                response = {
                    'success': True,
                    'action': 'respond',
                    'session_id': session_id,
                    'status': 'awaiting_response',
                    'current_phase': current_phase,
                    'stage': phase_data['current_stage'],
                    'total_stages': phase_data['total_stages'],
                    'progress_percentage': progress_percentage,
                    'message': f'💬 {current_phase.capitalize()} Phase - Stage {phase_data["current_stage"]}/{phase_data["total_stages"]} ({progress_percentage:.0f}%)',
                    'question': next_question,
                    'suggestions': next_suggestions
                }
            else:
                # User responded but AI hasn't provided next questions yet
                self._update_session_status(session_id, 'refinement_needed')
                
                response = {
                    'success': True,
                    'action': 'respond',
                    'session_id': session_id,
                    'status': 'refinement_needed',
                    'current_phase': current_phase,
                    'stage': phase_data['current_stage'],
                    'total_stages': phase_data['total_stages'],
                    'message': f'💬 User response recorded. AI should provide next question for {current_phase} phase stage {phase_data["current_stage"]}/{phase_data["total_stages"]}.',
                    'user_response': user_response,
                    'conversation_history': session['conversation_history']
                }
            
            await self.log_execution(ctx, f"Processed response for session: {session_id}")
        
        return json.dumps(response, indent=2, ensure_ascii=False)
    
    def _generate_refined_prompt(self, session: Dict[str, Any]) -> str:
        """
        Generate final refined prompt from conversation history
        
        Args:
            session: Session data
            
        Returns:
            Refined prompt string
        """
        refined_parts = [f"**Original Request:** {session['original_prompt']}\n"]
        
        for entry in session['conversation_history']:
            if entry.get('user_response'):
                refined_parts.append(f"**{entry['ai_question']}** {entry['user_response']}")
        
        return "\n".join(refined_parts)
    
    def _generate_additional_features_suggestions(self) -> str:
        """
        Generate additional features suggestion prompt
        
        Returns:
            Formatted suggestion text
        """
        return """
---
🌟 **Additional Features Suggestion:**

Would you like to add any additional features or enhancements to this specification?

If yes, please describe what you'd like to add, and we'll continue refining using the same session (no restart needed).

💡 **Tip:** Your additions will be integrated into the existing specification, maintaining all context and previous decisions.
"""
    
    def _get_technical_question_template(self, stage: int, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get technical question template for given stage
        
        Args:
            stage: Current technical stage number
            context: Session context (idea phase results, etc.)
            
        Returns:
            Dict with 'question' and 'suggestions' keys
        """
        templates = {
            1: {
                'question': "What application architecture should be used for this project?",
                'suggestions': [
                    "Monolithic architecture with MVC pattern (simpler deployment, good for small-medium apps, single codebase)",
                    "Microservices architecture with API gateway (scalable, distributed, independent deployments, complex management)",
                    "Serverless architecture with cloud functions (cost-effective, auto-scaling, event-driven, platform-dependent)"
                ]
            },
            2: {
                'question': "How should the project structure be organized?",
                'suggestions': [
                    "Feature-based structure: /features/auth, /features/users (grouped by functionality, easier to scale teams)",
                    "Layer-based structure: /controllers, /services, /models (traditional MVC separation, clear layers)",
                    "Domain-driven structure: /domain/user, /domain/product (business logic focus, bounded contexts)"
                ]
            },
            3: {
                'question': "What database strategy should be implemented?",
                'suggestions': [
                    "Single relational database with normalized schema (PostgreSQL with migrations, ACID transactions, structured data)",
                    "Polyglot persistence: SQL for transactions + NoSQL for caching (PostgreSQL + Redis, optimized per use case)",
                    "Document database with flexible schema (MongoDB with Mongoose ODM, rapid iteration, nested data)"
                ]
            },
            4: {
                'question': "What API patterns should be implemented?",
                'suggestions': [
                    "RESTful with resource-based routing + OpenAPI documentation (standard, cacheable, widely supported)",
                    "GraphQL with schema-first design + Apollo Server (flexible queries, reduces over-fetching, typed)",
                    "REST + WebSocket hybrid for real-time features (combines REST stability with real-time capabilities)"
                ]
            },
            5: {
                'question': "What code organization patterns should be used?",
                'suggestions': [
                    "Repository pattern + Dependency injection (testable, decoupled, easy to mock dependencies)",
                    "Service layer pattern + DTOs (clean separation of concerns, validated data transfer)",
                    "CQRS pattern for read/write separation (optimized queries, scalable, complex but powerful)"
                ]
            },
            6: {
                'question': "What authentication and security approach should be implemented?",
                'suggestions': [
                    "JWT (JSON Web Tokens) with refresh token rotation (stateless, scalable, secure with proper rotation)",
                    "OAuth 2.0 with social login providers (Google, GitHub) (user convenience, third-party trust, reduced password management)",
                    "API Key authentication for server-to-server communication (simple, suitable for internal services, rate limiting)"
                ]
            },
            7: {
                'question': "What testing strategy should be implemented?",
                'suggestions': [
                    "Testing pyramid: Unit (70%) + Integration (20%) + E2E (10%) with Jest/Mocha (balanced coverage, fast feedback)",
                    "BDD with Cucumber + unit tests (business-readable specs, collaboration focus, higher-level scenarios)",
                    "Contract testing + unit tests for microservices (API contract verification, service independence, Pact framework)"
                ]
            }
        }
        
        # Return template for stage, or generic template if stage > 7
        if stage in templates:
            return templates[stage]
        else:
            return {
                'question': f"What additional technical considerations are needed for stage {stage}?",
                'suggestions': [
                    "Define specific technical requirements based on project needs",
                    "Consider performance optimization strategies",
                    "Plan for monitoring and logging infrastructure"
                ]
            }
    
    def _generate_technical_specification(self, session: Dict[str, Any]) -> str:
        """
        Generate comprehensive technical specification from both phases
        
        Args:
            session: Complete session data
            
        Returns:
            Formatted technical specification
        """
        idea_phase = session['phases']['idea']
        tech_phase = session['phases']['technical']
        
        spec = f"""# Project Specification & Technical Implementation Plan

## Original Request
{session['original_prompt']}

## 1. Functional Specification (Idea Phase)

"""
        
        # Add idea phase conversation
        for entry in idea_phase['conversation_history']:
            if entry.get('user_response'):
                spec += f"**{entry['ai_question']}**\n{entry['user_response']}\n\n"
        
        if idea_phase['refined_output']:
            spec += f"\n### Refined Specification\n{idea_phase['refined_output']}\n\n"
        
        spec += """---

## 2. Technical Implementation Plan

"""
        
        # Extract technical decisions
        tech_decisions = {}
        for i, entry in enumerate(tech_phase['conversation_history'], 1):
            if entry.get('user_response'):
                tech_decisions[f"decision_{i}"] = {
                    'question': entry['ai_question'],
                    'decision': entry['user_response']
                }
        
        # Format technical specification
        if tech_decisions:
            spec += "### 2.1 Technical Decisions\n\n"
            for key, decision in tech_decisions.items():
                spec += f"**{decision['question']}**\n{decision['decision']}\n\n"
        
        spec += """### 2.2 Implementation Roadmap

Based on the decisions above, the recommended implementation approach:

1. **Project Setup**: Initialize project with chosen architecture and structure
2. **Core Infrastructure**: Set up database, authentication, and base services
3. **Feature Implementation**: Build features according to the functional specification
4. **Testing & Quality**: Implement testing strategy and quality checks
5. **Deployment**: Configure deployment pipeline and monitoring

### 2.3 Next Steps

This specification is ready to be converted into a Work Breakdown Structure (WBS) for systematic implementation.

**Recommended workflow:**
1. Use the Planning tool to create detailed WBS from this specification
2. Use the WBS Execution tool to implement step-by-step
3. Use Sequential Thinking tool for complex technical decisions during implementation

"""
        
        if session.get('additional_features'):
            spec += "\n### 2.4 Additional Features\n\n"
            for i, feature in enumerate(session['additional_features'], 1):
                spec += f"{i}. {feature}\n"
        
        return spec

    
    async def _handle_get_status_action(
        self,
        session_id: str,
        ctx: Optional[Context] = None
    ) -> str:
        """
        Handle 'get_status' action - Get current session state
        
        Args:
            session_id: Session identifier
            ctx: MCP context
            
        Returns:
            JSON response with session status
        """
        session = self._get_session(session_id)
        
        response = {
            'success': True,
            'action': 'get_status',
            'session_id': session_id,
            'status': session['status'],
            'stage': session['current_stage'],
            'original_prompt': session['original_prompt'],
            'refined_prompt': session['refined_prompt'],
            'conversation_history': session['conversation_history'],
            'created_at': session['created_at'],
            'last_updated': session['last_updated'],
            'summary': self._format_session_summary(session)
        }
        
        await self.log_execution(ctx, f"Retrieved status for session: {session_id}")
        
        return json.dumps(response, indent=2, ensure_ascii=False)
    
    async def _handle_list_sessions_action(
        self,
        ctx: Optional[Context] = None
    ) -> str:
        """
        Handle 'list_sessions' action - List all active sessions
        
        Args:
            ctx: MCP context
            
        Returns:
            JSON response with all sessions
        """
        sessions_list = []
        
        for session_id, session_data in vc_sessions.items():
            sessions_list.append({
                'session_id': session_id,
                'status': session_data['status'],
                'stage': session_data['current_stage'],
                'original_prompt': session_data['original_prompt'][:100] + '...' if len(session_data['original_prompt']) > 100 else session_data['original_prompt'],
                'created_at': session_data['created_at']
            })
        
        response = {
            'success': True,
            'action': 'list_sessions',
            'total_sessions': len(sessions_list),
            'sessions': sessions_list
        }
        
        await self.log_execution(ctx, f"Listed {len(sessions_list)} sessions")
        
        return json.dumps(response, indent=2, ensure_ascii=False)
    
    async def _handle_finalize_action(
        self,
        session_id: str,
        final_prompt: str,
        ctx: Optional[Context] = None
    ) -> str:
        """
        Handle 'finalize' action - Complete refinement with final prompt
        
        Args:
            session_id: Session identifier
            final_prompt: The fully refined final prompt
            ctx: MCP context
            
        Returns:
            JSON response with finalized session
        """
        session = self._get_session(session_id)
        
        session['refined_prompt'] = final_prompt
        self._update_session_status(session_id, 'completed')
        
        additional_features_prompt = self._generate_additional_features_suggestions()
        
        response = {
            'success': True,
            'action': 'finalize',
            'session_id': session_id,
            'status': 'completed',
            'original_prompt': session['original_prompt'],
            'refined_prompt': session['refined_prompt'],
            'total_stages': session['current_stage'],
            'summary': self._format_session_summary(session),
            'additional_features_suggestions': additional_features_prompt
        }
        
        await self.log_execution(ctx, f"Finalized session: {session_id}")
        
        return json.dumps(response, indent=2, ensure_ascii=False)
    
    async def _handle_start_technical_phase_action(
        self,
        session_id: str,
        total_stages: Optional[int] = None,
        ctx: Optional[Context] = None
    ) -> str:
        """
        Handle 'start_technical_phase' action - Begin technical refinement phase
        
        Args:
            session_id: Session identifier
            total_stages: Number of technical stages (optional, will use default if not provided)
            ctx: MCP context
            
        Returns:
            JSON response with first technical question
        """
        session = self._get_session(session_id)
        
        # Validate that idea phase is completed
        if not session['phases']['idea']['completed']:
            raise ValueError("Idea phase must be completed before starting technical phase")
        
        # Set technical phase as current
        session['current_phase'] = 'technical'
        
        # Set total stages for technical phase (default: 5)
        if not total_stages:
            total_stages = 5
        
        session['phases']['technical']['total_stages'] = total_stages
        session['status'] = 'technical_phase_started'
        session['last_updated'] = datetime.now().isoformat()
        
        # Get first technical question
        first_question = self._get_technical_question_template(1, session)
        
        # Add first conversation entry for technical phase
        self._add_conversation_entry(
            session_id=session_id,
            ai_question=first_question['question'],
            suggestions=first_question['suggestions'],
            phase='technical'
        )
        
        self._update_session_status(session_id, 'awaiting_response')
        
        response = {
            'success': True,
            'action': 'start_technical_phase',
            'session_id': session_id,
            'status': 'awaiting_response',
            'current_phase': 'technical',
            'stage': 1,
            'total_stages': total_stages,
            'progress_percentage': (1 / total_stages) * 100,
            'message': f'🔧 Starting technical implementation phase - Stage 1/{total_stages}',
            'question': first_question['question'],
            'suggestions': first_question['suggestions']
        }
        
        await self.log_execution(ctx, f"Started technical phase for session: {session_id}")
        
        return json.dumps(response, indent=2, ensure_ascii=False)
    
    async def _handle_skip_technical_phase_action(
        self,
        session_id: str,
        ctx: Optional[Context] = None
    ) -> str:
        """
        Handle 'skip_technical_phase' action - End session at idea phase
        
        Args:
            session_id: Session identifier
            ctx: MCP context
            
        Returns:
            JSON response with idea phase results only
        """
        session = self._get_session(session_id)
        
        # Mark idea phase as completed
        session['phases']['idea']['completed'] = True
        session['phases']['idea']['refined_output'] = self._generate_refined_prompt(session)
        
        # Mark session as completed
        self._update_session_status(session_id, 'completed_idea_only')
        
        response = {
            'success': True,
            'action': 'skip_technical_phase',
            'session_id': session_id,
            'status': 'completed_idea_only',
            'current_phase': 'idea',
            'message': '✅ Session completed with functional specification only.',
            'refined_prompt': session['phases']['idea']['refined_output'],
            'summary': self._format_session_summary(session),
            'note': 'Technical implementation phase was skipped. You can resume technical phase later by calling start_technical_phase action.'
        }
        
        await self.log_execution(ctx, f"Skipped technical phase for session: {session_id}")
        
        return json.dumps(response, indent=2, ensure_ascii=False)
    
    async def _handle_set_total_stages_action(
        self,
        session_id: str,
        total_stages: int,
        question: str,
        suggestions: List[str],
        ctx: Optional[Context] = None
    ) -> str:
        """
        Handle 'set_total_stages' action - Set total_stages after LLM analysis
        
        This is called by the LLM after analyzing the initial_prompt in the 'start' action.
        The LLM determines:
        1. How many refinement stages are needed (total_stages)
        2. The first clarifying question
        3. Three alternative suggestions
        
        Args:
            session_id: Session identifier from 'start' action
            total_stages: Number of refinement stages determined by LLM (required)
            question: First clarifying question (required)
            suggestions: 3 alternative suggestions (required)
            ctx: MCP context
            
        Returns:
            JSON response with first refinement stage ready
        """
        session = self._get_session(session_id)
        
        # Validate total_stages
        if total_stages <= 0:
            raise ValueError("total_stages must be greater than 0")
        
        # Validate suggestions
        if len(suggestions) != 3:
            raise ValueError("Exactly 3 suggestions must be provided")
        
        # Set total_stages for the session and idea phase
        session['total_stages'] = total_stages
        session['phases']['idea']['total_stages'] = total_stages
        session['status'] = 'awaiting_response'
        session['last_updated'] = datetime.now().isoformat()
        
        # Add first conversation entry to idea phase
        self._add_conversation_entry(
            session_id=session_id,
            ai_question=question,
            suggestions=suggestions,
            phase='idea'
        )
        
        progress_percentage = (session['phases']['idea']['current_stage'] / session['phases']['idea']['total_stages']) * 100
        
        response = {
            'success': True,
            'action': 'set_total_stages',
            'session_id': session_id,
            'status': 'awaiting_response',
            'current_phase': 'idea',
            'stage': session['phases']['idea']['current_stage'],
            'total_stages': session['phases']['idea']['total_stages'],
            'progress_percentage': progress_percentage,
            'message': f'🚀 Analysis complete! Starting idea refinement - Stage {session["phases"]["idea"]["current_stage"]}/{session["phases"]["idea"]["total_stages"]} ({progress_percentage:.0f}%)',
            'question': question,
            'suggestions': suggestions
        }
        
        await self.log_execution(ctx, f"Set total_stages={total_stages} for session: {session_id}")
        
        return json.dumps(response, indent=2, ensure_ascii=False)
    
    async def _handle_add_feature_action(
        self,
        session_id: str,
        feature_description: str,
        additional_stages: Optional[int] = None,
        question: Optional[str] = None,
        suggestions: Optional[List[str]] = None,
        ctx: Optional[Context] = None
    ) -> str:
        """
        Handle 'add_feature' action - Add additional features to existing session
        
        This extends the session without resetting it, maintaining all context
        
        Args:
            session_id: Existing session identifier
            feature_description: Description of the feature to add
            additional_stages: Number of additional stages needed for this feature
            question: AI's first question for the new feature (optional)
            suggestions: AI's 3 suggestions (optional)
            ctx: MCP context
            
        Returns:
            JSON response with extended session info
        """
        session = self._get_session(session_id)
        
        # Add feature to additional features list
        session['additional_features'].append(feature_description)
        
        # If additional_stages not provided, request AI to analyze
        if not additional_stages:
            response = {
                'success': True,
                'action': 'add_feature',
                'session_id': session_id,
                'status': 'analyzing_feature',
                'current_total_stages': session['total_stages'],
                'message': '🔍 AI must analyze the feature and determine additional_stages needed.',
                'feature_description': feature_description,
                'instructions': 'Please analyze the feature complexity and call add_feature action again with additional_stages parameter.'
            }
            
            await self.log_execution(ctx, f"Feature addition requested for session {session_id}")
            return json.dumps(response, indent=2, ensure_ascii=False)
        
        # Extend total stages
        old_total = session['total_stages']
        session['total_stages'] += additional_stages
        session['status'] = 'refining_feature'
        session['last_updated'] = datetime.now().isoformat()
        
        # If AI provided question and suggestions, start refinement
        if question and suggestions:
            if len(suggestions) != 3:
                raise ValueError("Exactly 3 suggestions must be provided")
            
            # Add marker for feature addition
            feature_marker = {
                'stage': session['current_stage'],
                'ai_question': f"🌟 **NEW FEATURE:** {feature_description}",
                'suggestions': [],
                'user_response': None,
                'timestamp': datetime.now().isoformat(),
                'is_feature_marker': True
            }
            session['conversation_history'].append(feature_marker)
            
            self._add_conversation_entry(
                session_id=session_id,
                ai_question=question,
                suggestions=suggestions
            )
            self._update_session_status(session_id, 'awaiting_response')
            
            response = {
                'success': True,
                'action': 'add_feature',
                'session_id': session_id,
                'status': 'awaiting_response',
                'stage': session['current_stage'],
                'total_stages': session['total_stages'],
                'previous_total_stages': old_total,
                'additional_stages': additional_stages,
                'progress_percentage': (session['current_stage'] / session['total_stages']) * 100,
                'message': f'🌟 Feature added! Extended from {old_total} to {session["total_stages"]} stages. Stage {session["current_stage"]}/{session["total_stages"]}',
                'question': question,
                'suggestions': suggestions
            }
        else:
            response = {
                'success': True,
                'action': 'add_feature',
                'session_id': session_id,
                'status': 'feature_added',
                'total_stages': session['total_stages'],
                'previous_total_stages': old_total,
                'additional_stages': additional_stages,
                'message': f'🌟 Session extended with {additional_stages} additional stages. Please provide first question and suggestions.',
                'feature_description': feature_description
            }
        
        await self.log_execution(ctx, f"Added feature to session {session_id}: {additional_stages} stages")
        
        return json.dumps(response, indent=2, ensure_ascii=False)
    
    async def execute(
        self,
        action: str,
        session_id: Optional[str] = None,
        initial_prompt: Optional[str] = None,
        user_response: Optional[str] = None,
        question: Optional[str] = None,
        suggestions: Optional[List[str]] = None,
        next_question: Optional[str] = None,
        next_suggestions: Optional[List[str]] = None,
        is_final: Optional[bool] = False,
        final_prompt: Optional[str] = None,
        total_stages: Optional[int] = None,
        feature_description: Optional[str] = None,
        additional_stages: Optional[int] = None,
        ctx: Optional[Context] = None
    ) -> str:
        """
        Execute Vibe Coding action
        
        Args:
            action: Action to perform (start, respond, get_status, list_sessions, finalize, add_feature)
            session_id: Session identifier (required for most actions)
            initial_prompt: Initial vague prompt (required for 'start')
            user_response: User's response to suggestions (required for 'respond')
            question: AI's clarifying question (for 'start' or 'respond')
            suggestions: AI's 3 suggestions (for 'start' or 'respond')
            next_question: AI's next question (for 'respond')
            next_suggestions: AI's next 3 suggestions (for 'respond')
            is_final: Whether refinement is complete (for 'respond')
            final_prompt: Final refined prompt (for 'finalize')
            total_stages: Total stages needed (for 'start')
            feature_description: Feature to add (for 'add_feature')
            additional_stages: Additional stages for feature (for 'add_feature')
            ctx: MCP context
            
        Returns:
            JSON response string
        """
        try:
            logger.info(f"Executing Vibe Coding action: {action}")
            
            # Route to appropriate handler
            if action == 'start':
                if not initial_prompt:
                    raise ValueError("initial_prompt is required for 'start' action")
                return await self._handle_start_action(
                    initial_prompt=initial_prompt,
                    total_stages=total_stages,
                    suggestions=suggestions,
                    question=question,
                    ctx=ctx
                )
            
            elif action == 'set_total_stages':
                if not session_id:
                    raise ValueError("session_id is required for 'set_total_stages' action")
                if not total_stages:
                    raise ValueError("total_stages is required for 'set_total_stages' action")
                if not question:
                    raise ValueError("question is required for 'set_total_stages' action")
                if not suggestions:
                    raise ValueError("suggestions is required for 'set_total_stages' action")
                return await self._handle_set_total_stages_action(
                    session_id=session_id,
                    total_stages=total_stages,
                    question=question,
                    suggestions=suggestions,
                    ctx=ctx
                )
            
            elif action == 'respond':
                if not session_id:
                    raise ValueError("session_id is required for 'respond' action")
                if not user_response:
                    raise ValueError("user_response is required for 'respond' action")
                return await self._handle_respond_action(
                    session_id=session_id,
                    user_response=user_response,
                    next_question=next_question,
                    next_suggestions=next_suggestions,
                    is_final=is_final,
                    total_stages=total_stages,
                    ctx=ctx
                )
            
            elif action == 'get_status':
                if not session_id:
                    raise ValueError("session_id is required for 'get_status' action")
                return await self._handle_get_status_action(
                    session_id=session_id,
                    ctx=ctx
                )
            
            elif action == 'list_sessions':
                return await self._handle_list_sessions_action(ctx=ctx)
            
            elif action == 'finalize':
                if not session_id:
                    raise ValueError("session_id is required for 'finalize' action")
                if not final_prompt:
                    raise ValueError("final_prompt is required for 'finalize' action")
                return await self._handle_finalize_action(
                    session_id=session_id,
                    final_prompt=final_prompt,
                    ctx=ctx
                )
            
            elif action == 'add_feature':
                if not session_id:
                    raise ValueError("session_id is required for 'add_feature' action")
                if not feature_description:
                    raise ValueError("feature_description is required for 'add_feature' action")
                return await self._handle_add_feature_action(
                    session_id=session_id,
                    feature_description=feature_description,
                    additional_stages=additional_stages,
                    question=question,
                    suggestions=suggestions,
                    ctx=ctx
                )
            
            elif action == 'start_technical_phase':
                if not session_id:
                    raise ValueError("session_id is required for 'start_technical_phase' action")
                return await self._handle_start_technical_phase_action(
                    session_id=session_id,
                    total_stages=total_stages,
                    ctx=ctx
                )
            
            elif action == 'skip_technical_phase':
                if not session_id:
                    raise ValueError("session_id is required for 'skip_technical_phase' action")
                return await self._handle_skip_technical_phase_action(
                    session_id=session_id,
                    ctx=ctx
                )
            
            else:
                raise ValueError(f"Unknown action: {action}. Valid actions: start, set_total_stages, respond, get_status, list_sessions, finalize, add_feature, start_technical_phase, skip_technical_phase")
        
        except Exception as e:
            logger.error(f"Error executing Vibe Coding action '{action}': {str(e)}")
            error_response = {
                'success': False,
                'action': action,
                'error': str(e)
            }
            return json.dumps(error_response, indent=2, ensure_ascii=False)


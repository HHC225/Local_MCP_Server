"""
Vibe Coding Tool Wrapper for MCP Registration
Interactive prompt refinement through iterative clarification
"""
from typing import Optional, List
from fastmcp import Context
from src.tools.vibe.vibe_coding_tool import VibeCodingTool

# Initialize tool instance
_vibe_tool = VibeCodingTool()


async def vibe_coding(
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
    Vibe Coding - Interactive Prompt Refinement Tool
    
    🎯 **PURPOSE:**
    Transforms vague user prompts into concrete, actionable specifications through 
    interactive refinement. Instead of making assumptions, this tool asks clarifying 
    questions and provides 3 alternative suggestions at each step.
    
    🔄 **WORKFLOW:**
    1. User provides vague initial prompt
    2. Tool creates session (action='start')
    3. LLM analyzes prompt and determines total_stages needed
    4. LLM calls set_total_stages with total_stages, first question, and 3 suggestions
    5. User responds → LLM continues with respond action
    6. Loop continues through all stages
    7. After completion, suggests additional features
    
    📋 **ACTIONS:**
    
    **1. 'start' - Initialize New Session (User Input):**
    ```python
    # User provides initial vague prompt
    result = await vibe_coding(
        action="start",
        initial_prompt="I want to build an API"
    )
    # Returns: session_id and instructions for LLM to analyze
    # Status: 'analyzing'
    
    # Response tells LLM to:
    # 1. Analyze the prompt complexity
    # 2. Determine total_stages needed
    # 3. Create first question and 3 suggestions
    # 4. Call set_total_stages action
    ```
    
    **2. 'set_total_stages' - Set Analysis Results (LLM Analysis):**
    ```python
    # LLM analyzes and determines total_stages
    # Then calls this to begin refinement:
    result = await vibe_coding(
        action="set_total_stages",
        session_id="vc_session_1234567890_abc123",
        total_stages=5,  # LLM determined 5 stages needed
        question="What type of API architecture would you like?",
        suggestions=[
            "RESTful API with Express.js and PostgreSQL for CRUD operations",
            "GraphQL API with Apollo Server for flexible data querying",
            "gRPC API for high-performance microservices communication"
        ]
    )
    # Returns: stage=1/5, status='awaiting_response'
    # Now ready for user's first response
    ```
    
    **3. 'respond' - Process User Response and Continue:**
    ```python
    # User selects option, LLM continues to next stage
    result = await vibe_coding(
        action="respond",
        session_id="vc_session_1234567890_abc123",
        user_response="I choose option 1 - RESTful API with Express.js",
        next_question="What authentication method should be implemented?",
        next_suggestions=[
            "JWT (JSON Web Tokens) with refresh token rotation",
            "OAuth 2.0 with social login providers (Google, GitHub)",
            "API Key authentication for server-to-server communication"
        ]
    )
    # Returns: stage=2/5, status='awaiting_response', progress=40%
    
    # This continues automatically until all stages are complete
    # Then returns: status='completed', refined_prompt, additional_features_suggestions
    ```
    
    **4. 'add_feature' - Extend Session with Additional Features:**
    ```python
    # User wants to add feature after completion
    result = await vibe_coding(
        action="add_feature",
        session_id="vc_session_1234567890_abc123",
        feature_description="Add real-time WebSocket support for notifications",
        additional_stages=3,  # LLM determines additional stages needed
        question="What WebSocket library should be used?",
        suggestions=[
            "Socket.io for cross-browser compatibility",
            "Native WebSocket with ws library for performance",
            "Server-Sent Events (SSE) for simpler one-way communication"
        ]
    )
    # Returns: total_stages extended from 5 to 8, stage=6/8
    ```
    
    **5. 'start_technical_phase' - Begin Technical Implementation Refinement (NEW):**
    ```python
    # After idea phase completes, start technical refinement
    result = await vibe_coding(
        action="start_technical_phase",
        session_id="vc_session_1234567890_abc123",
        total_stages=5  # Optional, defaults to 5 technical stages
    )
    # Returns: First technical question about architecture/implementation
    # Technical categories: Architecture, Stack, Structure, Data Layer, API, Security, Testing
    ```
    
    **6. 'skip_technical_phase' - End at Idea Phase (NEW):**
    ```python
    # User wants only functional specification, no technical details
    result = await vibe_coding(
        action="skip_technical_phase",
        session_id="vc_session_1234567890_abc123"
    )
    # Returns: Completed session with idea phase results only
    # Can resume technical phase later if needed
    ```
    
    **7. 'get_status' - Check Session State:**
    ```python
    result = await vibe_coding(
        action="get_status",
        session_id="vc_session_1234567890_abc123"
    )
    # Returns: Full session state with conversation history
    ```
    
    **8. 'list_sessions' - List All Sessions:**
    ```python
    result = await vibe_coding(
        action="list_sessions"
    )
    # Returns: List of all active sessions
    ```
    
    **9. 'finalize' - Complete with Final Prompt:**
    ```python
    result = await vibe_coding(
        action="finalize",
        session_id="vc_session_1234567890_abc123",
        final_prompt="Build a RESTful API using Express.js and PostgreSQL..."
    )
    # Returns: Completed session with additional_features_suggestions
    ```
    
    🎨 **AI USAGE PATTERN (Two-Phase Workflow):**
    
    ```
    PHASE 1: IDEA REFINEMENT
    1. User: "I want to build something"
       AI: Calls vibe_coding(action='start', initial_prompt="...")
       Tool: Returns session_id and analysis instructions
       
    2. AI: Analyzes complexity → "This needs 5 stages"
       AI: Calls vibe_coding(
           action='set_total_stages',
           session_id="...",
           total_stages=5,
           question="...",
           suggestions=[...]
       )
       Tool: Returns stage 1/5, ready for user input
       
    3. User: "I choose option 2"
       AI: Calls vibe_coding(
           action='respond',
           user_response="...",
           next_question="...",
           next_suggestions=[...]
       )
       Tool: Returns stage 2/5
       
    4. Loop continues through all 5 idea stages...
    
    5. Idea phase complete:
       Tool: Returns status='idea_phase_completed' with options
       
    PHASE 2: TECHNICAL REFINEMENT (NEW)
    6a. User: "Yes, continue to technical phase"
        AI: Calls vibe_coding(
            action='start_technical_phase',
            session_id="..."
        )
        Tool: Returns first technical question (Architecture)
        
    6b. Alternative: User: "No, just give me the spec"
        AI: Calls vibe_coding(
            action='skip_technical_phase',
            session_id="..."
        )
        Tool: Returns completed specification
        
    7. If technical phase started:
       User responds to technical questions (Architecture, Stack, Structure, etc.)
       AI: Calls vibe_coding(action='respond', ...)
       Loop continues through 5-7 technical stages
       
    8. Technical phase complete:
       Tool: Returns comprehensive specification ready for WBS
    ```
    
    🔧 **TECHNICAL PHASE QUESTION CATEGORIES (NEW):**
    
    1. **Architecture & Patterns** (Stage 1)
       - Application architecture type (Monolithic/Microservices/Serverless)
       - Design patterns to use
       - Scalability considerations
    
    2. **Project Structure** (Stage 2)
       - Folder organization (Feature-based/Layer-based/Domain-driven)
       - Module boundaries
       - Code separation strategy
    
    3. **Database Strategy** (Stage 3)
       - Database choice (SQL/NoSQL/Polyglot)
       - Schema design approach
       - Migration strategy
       - Caching approach
    
    4. **API/Interface Design** (Stage 4)
       - API patterns (REST/GraphQL/Hybrid)
       - Endpoint structure
       - Request/response formats
       - Documentation approach
    
    5. **Code Organization Patterns** (Stage 5)
       - Design patterns (Repository/Service Layer/CQRS)
       - Dependency injection
       - Data transfer objects
    
    6. **Security & Authentication** (Stage 6, if needed)
       - Authentication method (JWT/OAuth/API Key)
       - Authorization strategy
       - Data validation
    
    7. **Testing Strategy** (Stage 7, if needed)
       - Testing pyramid approach
       - Tools and frameworks
       - CI/CD integration
    
    **Each Technical Suggestion Includes:**
    - Technology/approach name
    - Brief description
    - Key benefits and trade-offs in parentheses
    
    📊 **FINAL OUTPUT FORMAT (After Both Phases):**
    
    ```markdown
    # Project Specification & Technical Implementation Plan
    
    ## 1. Functional Specification (Idea Phase)
    [User's refined requirements and features]
    
    ## 2. Technical Implementation Plan
    ### 2.1 Technical Decisions
    - Architecture choice with reasoning
    - Technology stack selections
    - Project structure approach
    - Database strategy
    - API patterns
    - Code organization patterns
    
    ### 2.2 Implementation Roadmap
    1. Project Setup
    2. Core Infrastructure
    3. Feature Implementation
    4. Testing & Quality
    5. Deployment
    
    ### 2.3 Next Steps
    - Ready for Planning tool (WBS generation)
    - Ready for WBS Execution tool
    ```
    
    ⚡ **KEY FEATURES:**
    - **Two-Phase Refinement**: Idea (WHAT) → Technical (HOW) (NEW)
    - **Two-Step Start**: start creates session → LLM analyzes → set_total_stages begins refinement
    - **LLM-Driven Analysis**: LLM determines total_stages by analyzing prompt complexity
    - **Auto-Loop**: Continues through all stages automatically
    - **Progress Tracking**: Shows stage X/Y and percentage for each phase
    - **Session Continuity**: add_feature extends without restart
    - **Context Preservation**: All decisions maintained across phases
    - **Technical Templates**: Pre-defined technical questions for consistency (NEW)
    - **Comprehensive Output**: Combined functional + technical specification (NEW)
    
    🎯 **BEST PRACTICES:**
    
    1. **Start Simple**: User calls start with just initial_prompt
    2. **LLM Analyzes**: LLM analyzes and calls set_total_stages
    3. **Progress Feedback**: Show stage X/Y to user at each step
    4. **Phase Transition**: After idea phase, offer technical phase option
    5. **User Choice**: Let user decide whether to continue to technical phase
    6. **No Restarts**: Use add_feature to extend, not restart
    7. **WBS Ready**: Final output is ready for Planning and WBS Execution tools
    
    📊 **RESPONSE FORMAT:**
    
    ```json
    {
        "success": true,
        "action": "start|set_total_stages|respond|add_feature|start_technical_phase|skip_technical_phase|get_status|list_sessions|finalize",
        "session_id": "vc_session_1234567890_abc123",
        "status": "analyzing|awaiting_response|idea_phase_completed|technical_phase_started|completed|completed_idea_only",
        "current_phase": "idea|technical",
        "stage": 2,
        "total_stages": 5,
        "progress_percentage": 40,
        "message": "Stage 2/5 - Continue refinement",
        "question": "Next clarifying question",
        "suggestions": ["Option 1", "Option 2", "Option 3"],
        "refined_prompt": "Final refined prompt (when completed)",
        "technical_specification": "Full technical spec (when both phases completed)",
        "additional_features_suggestions": "Feature suggestion prompt"
    }
    ```
    
    ⚠️ **IMPORTANT NOTES:**
    
    - **start** only needs initial_prompt (LLM analyzes separately)
    - **set_total_stages** requires total_stages, question, suggestions (LLM provides after analysis)
    - **start_technical_phase** begins after idea phase completion (NEW)
    - **skip_technical_phase** allows ending at idea phase only (NEW)
    - Always provide exactly 3 suggestions per stage
    - Session extends with add_feature, never restarts
    - Completed sessions include functional and/or technical specifications
    - Technical phase uses pre-defined question templates for consistency (NEW)
    - Final output is ready for Planning and WBS Execution tools (NEW)
    
    Args:
        action: Action to perform (start, set_total_stages, respond, get_status, list_sessions, finalize, add_feature)
        session_id: Session identifier (required for most actions except start)
        initial_prompt: User's initial vague prompt (required for start)
        user_response: User's response to suggestions (required for respond)
        question: AI's clarifying question (for set_total_stages/respond/add_feature)
        suggestions: AI's 3 alternative suggestions (for set_total_stages/respond/add_feature)
        next_question: AI's next clarifying question (for respond)
        next_suggestions: AI's next 3 suggestions (for respond)
        is_final: Whether refinement is complete (for respond)
        final_prompt: Final refined prompt (for finalize)
        total_stages: Total stages needed (for set_total_stages - determined by LLM)
        feature_description: Feature to add (for add_feature)
        additional_stages: Additional stages for feature (for add_feature)
        ctx: MCP context for logging
    
    Returns:
        JSON string with action results and next steps
    
    Examples:
        See detailed examples in each action description above.
    """
    return await _vibe_tool.execute(
        action=action,
        session_id=session_id,
        initial_prompt=initial_prompt,
        user_response=user_response,
        question=question,
        suggestions=suggestions,
        next_question=next_question,
        next_suggestions=next_suggestions,
        is_final=is_final,
        final_prompt=final_prompt,
        total_stages=total_stages,
        feature_description=feature_description,
        additional_stages=additional_stages,
        ctx=ctx
    )

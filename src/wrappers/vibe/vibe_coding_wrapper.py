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
    
    **5. 'get_status' - Check Session State:**
    ```python
    result = await vibe_coding(
        action="get_status",
        session_id="vc_session_1234567890_abc123"
    )
    # Returns: Full session state with conversation history
    ```
    
    **6. 'list_sessions' - List All Sessions:**
    ```python
    result = await vibe_coding(
        action="list_sessions"
    )
    # Returns: List of all active sessions
    ```
    
    **7. 'finalize' - Complete with Final Prompt:**
    ```python
    result = await vibe_coding(
        action="finalize",
        session_id="vc_session_1234567890_abc123",
        final_prompt="Build a RESTful API using Express.js and PostgreSQL..."
    )
    # Returns: Completed session with additional_features_suggestions
    ```
    
    🎨 **AI USAGE PATTERN:**
    
    ```
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
       
    4. Loop continues through all 5 stages...
    
    5. Stage 5/5 complete:
       Tool: Returns refined_prompt + feature suggestions
       
    6. User: "Add WebSocket support"
       AI: Analyzes → needs 3 more stages
       AI: Calls vibe_coding(
           action='add_feature',
           additional_stages=3,
           ...
       )
       Tool: Extends to stage 6/8
    ```
    
    ⚡ **KEY FEATURES:**
    - **Two-Step Start**: start creates session → LLM analyzes → set_total_stages begins refinement
    - **LLM-Driven Analysis**: LLM determines total_stages by analyzing prompt complexity
    - **Auto-Loop**: Continues through all stages automatically
    - **Progress Tracking**: Shows stage X/Y and percentage
    - **Session Continuity**: add_feature extends without restart
    - **Context Preservation**: All decisions maintained
    
    🎯 **BEST PRACTICES:**
    
    1. **Start Simple**: User calls start with just initial_prompt
    2. **LLM Analyzes**: LLM analyzes and calls set_total_stages
    3. **Progress Feedback**: Show stage X/Y to user at each step
    4. **Feature-Ready**: Always end with feature suggestions
    5. **No Restarts**: Use add_feature to extend
    
    📊 **RESPONSE FORMAT:**
    
    ```json
    {
        "success": true,
        "action": "start|set_total_stages|respond|add_feature|get_status|list_sessions|finalize",
        "session_id": "vc_session_1234567890_abc123",
        "status": "analyzing|awaiting_response|completed|refining_feature",
        "stage": 2,
        "total_stages": 5,
        "progress_percentage": 40,
        "message": "Stage 2/5 - Continue refinement",
        "question": "Next clarifying question",
        "suggestions": ["Option 1", "Option 2", "Option 3"],
        "refined_prompt": "Final refined prompt (when completed)",
        "additional_features_suggestions": "Feature suggestion prompt"
    }
    ```
    
    ⚠️ **IMPORTANT NOTES:**
    
    - **start** only needs initial_prompt (LLM analyzes separately)
    - **set_total_stages** requires total_stages, question, suggestions (LLM provides after analysis)
    - Always provide exactly 3 suggestions per stage
    - Session extends with add_feature, never restarts
    - Completed sessions always include feature suggestions
    
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

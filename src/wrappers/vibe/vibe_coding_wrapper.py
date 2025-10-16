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
    
    🔄 **IMPROVED WORKFLOW:**
    1. User provides vague initial prompt
    2. AI analyzes complexity and determines total_stages needed
    3. AI automatically loops through stages with questions and suggestions
    4. Each stage refines the specification further
    5. After completion, always suggests additional features
    6. Additional features extend the session (no restart needed)
    
    📋 **ACTIONS:**
    
    **1. 'start' - Initialize New Session with Stage Analysis:**
    ```python
    # Step 1a: User provides vague prompt, AI creates session
    result = await vibe_coding(
        action="start",
        initial_prompt="I want to build an API"
    )
    # Returns: session_id, status='analyzing', instructions to determine stages
    
    # Step 1b: AI analyzes and determines total stages needed
    result = await vibe_coding(
        action="start",
        initial_prompt="I want to build an API",
        total_stages=5,  # AI determined 5 stages are needed
        question="What type of API architecture would you like?",
        suggestions=[
            "RESTful API with Express.js and PostgreSQL for CRUD operations",
            "GraphQL API with Apollo Server for flexible data querying",
            "gRPC API for high-performance microservices communication"
        ]
    )
    # Returns: session_id, status='awaiting_response', stage=1/5
    ```
    
    **2. 'respond' - Process User Response and Auto-Continue:**
    ```python
    # Step 2: User selects option, AI continues to next stage
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
    # Returns: status='awaiting_response', stage=2/5, progress=40%
    
    # This continues automatically until stage 5/5 is complete
    # Then returns: status='completed', refined_prompt, additional_features_suggestions
    ```
    
    **3. 'add_feature' - Extend Session with Additional Features:**
    ```python
    # Step 3a: User wants to add feature after completion
    result = await vibe_coding(
        action="add_feature",
        session_id="vc_session_1234567890_abc123",  # Same session!
        feature_description="Add real-time WebSocket support for notifications"
    )
    # Returns: status='analyzing_feature', instructions to determine additional stages
    
    # Step 3b: AI determines additional stages needed
    result = await vibe_coding(
        action="add_feature",
        session_id="vc_session_1234567890_abc123",
        feature_description="Add real-time WebSocket support for notifications",
        additional_stages=3,  # AI determined 3 more stages needed
        question="What WebSocket library should be used?",
        suggestions=[
            "Socket.io for cross-browser compatibility",
            "Native WebSocket with ws library for performance",
            "Server-Sent Events (SSE) for simpler one-way communication"
        ]
    )
    # Returns: total_stages extended from 5 to 8, stage=6/8
    # All previous context is maintained!
    ```
    
    **4. 'get_status' - Check Session State:**
    ```python
    result = await vibe_coding(
        action="get_status",
        session_id="vc_session_1234567890_abc123"
    )
    # Returns: Full session state with all conversation history
    ```
    
    **5. 'list_sessions' - List All Sessions:**
    ```python
    result = await vibe_coding(
        action="list_sessions"
    )
    # Returns: List of all active sessions
    ```
    
    **6. 'finalize' - Complete with Final Prompt:**
    ```python
    result = await vibe_coding(
        action="finalize",
        session_id="vc_session_1234567890_abc123",
        final_prompt="Build a RESTful API using Express.js and PostgreSQL..."
    )
    # Returns: Completed session with additional_features_suggestions
    ```
    
    🎨 **AI USAGE PATTERN:**
    
    The AI should follow this improved pattern:
    
    ```
    1. User: "I want to build something"
       AI: Analyzes complexity → Determines needs 5 stages
       AI: Calls vibe_coding(action='start', total_stages=5, question="...", suggestions=[...])
       AI: Presents options to user → "Stage 1/5 (20%)"
    
    2. User: "I choose option 2"
       AI: Calls vibe_coding(action='respond', user_response="...", next_question="...", next_suggestions=[...])
       AI: Presents next options → "Stage 2/5 (40%)"
    
    3. Loop continues through all 5 stages...
    
    4. Stage 5/5 complete:
       AI: Returns refined_prompt + additional_features_suggestions
       AI: "Would you like to add any features?"
    
    5. User: "Add WebSocket support"
       AI: Analyzes → Determines needs 3 more stages
       AI: Calls vibe_coding(action='add_feature', additional_stages=3, ...)
       AI: Continues from stage 6/8 (same session!)
    ```
    
    ⚡ **KEY FEATURES:**
    - **Stage Planning**: AI determines total stages needed upfront
    - **Auto-Loop**: Continues through all stages automatically
    - **Progress Tracking**: Shows stage X/Y and percentage progress
    - **Session Continuity**: add_feature extends session without restart
    - **Context Preservation**: All previous decisions maintained
    - **Always Suggest Features**: Completed sessions always show feature suggestions
    
    🎯 **BEST PRACTICES:**
    
    1. **Analyze First**: Determine total_stages based on prompt complexity
    2. **Progress Feedback**: Show stage X/Y to user at each step
    3. **Feature-Ready**: Always end with additional feature suggestions
    4. **No Restarts**: Use add_feature to extend, never restart session
    5. **Track Context**: Build on all previous conversation history
    
    📊 **RESPONSE FORMAT:**
    
    ```json
    {
        "success": true,
        "action": "start|respond|add_feature|get_status|list_sessions|finalize",
        "session_id": "vc_session_1234567890_abc123",
        "status": "analyzing|awaiting_response|completed|refining_feature",
        "stage": 2,
        "total_stages": 5,
        "progress_percentage": 40,
        "message": "Stage 2/5 - Continue refinement",
        "question": "Next clarifying question",
        "suggestions": ["Option 1", "Option 2", "Option 3"],
        "refined_prompt": "Final refined prompt (when completed)",
        "additional_features_suggestions": "Feature suggestion prompt (when completed)"
    }
    ```
    
    ⚠️ **IMPORTANT NOTES:**
    
    - AI must analyze and set total_stages at the start
    - Always provide exactly 3 suggestions per stage
    - Session extends with add_feature, never restarts
    - Completed sessions always include feature suggestions
    - Progress tracking: stage/total_stages and percentage
    
    Args:
        action: Action to perform (start, respond, get_status, list_sessions, finalize, add_feature)
        session_id: Session identifier (required for respond, get_status, finalize, add_feature)
        initial_prompt: User's initial vague prompt (required for start)
        user_response: User's response to suggestions (required for respond)
        question: AI's clarifying question (for start/respond/add_feature)
        suggestions: AI's 3 alternative suggestions (for start/respond/add_feature)
        next_question: AI's next clarifying question (for respond)
        next_suggestions: AI's next 3 suggestions (for respond)
        is_final: Whether refinement is complete (for respond)
        final_prompt: Final refined prompt (for finalize)
        total_stages: Total stages needed (for start)
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

# Vibe Coding - Interactive Prompt Refinement Tool

## Overview

The **Vibe Coding** tool is an interactive prompt refinement system that transforms vague user requests into concrete, actionable specifications through a **two-phase refinement process**:

1. **Idea Phase**: What to build (functional specifications)
2. **Technical Phase**: How to implement (technical specifications)

This dual-phase approach bridges the gap between business requirements and technical implementation, producing specifications ready for the Planning and WBS Execution tools.

## Purpose

When users provide vague prompts like "I want to build an API" or "Create a dashboard", AI systems typically make assumptions about requirements. Vibe Coding prevents this by:

1. **Analyzing** prompt complexity to determine optimal refinement stages
2. **Executing** structured refinement through interactive questioning
3. **Offering** 3 specific alternatives at each decision point
4. **Waiting** for explicit user selection before proceeding
5. **Generating** comprehensive specifications (functional + technical)

## Key Features

### 🔄 Two-Phase Refinement (NEW)

#### Phase 1: Idea Refinement
- **Focus**: WHAT to build
- **Questions**: Features, business requirements, user needs
- **Output**: Functional specification
- **Stages**: 3-7 stages (AI-determined)

#### Phase 2: Technical Refinement (NEW)
- **Focus**: HOW to implement
- **Questions**: Architecture, stack, patterns, structure
- **Output**: Technical implementation plan
- **Stages**: 5-7 technical stages
- **Categories**: 
  - Architecture & Patterns
  - Project Structure
  - Database Strategy
  - API/Interface Design
  - Code Organization
  - Security & Auth
  - Testing Strategy

### 📊 Auto-Stage Planning

- LLM analyzes prompt complexity
- Determines optimal number of refinement stages
- Sets clear completion target
- Auto-completion when all stages done

### 🔄 Loop-Based Execution

- Automatically continues through planned stages
- No manual intervention needed
- Structured flow from stage 1 → N
- Clear progress tracking

### 🌟 Feature Extension

- Add features after completion
- No session restart required
- Dynamically extends stages
- Maintains all previous context

### 🚀 Automatic Phase Transition (NEW)

- **Automatic Technical Phase start after Idea Phase completion**
- Seamless transition without user intervention
- Entire process flows as one continuous workflow
- Complete specification automatically generated

### 💡 Simplified User Experience

- No manual phase switching needed
- Continuous refinement flow
- Complete specification automatically generated
- Ready for immediate implementation

## Workflow

### Complete Two-Phase Flow (Automatic)

```
User: "I want to build an API"
         ↓
AI: Analyzes complexity → Determines 5 idea stages
         ↓
IDEA PHASE (Stages 1-5)
  Stage 1: API architecture? [REST, GraphQL, gRPC]
  Stage 2: Authentication? [JWT, OAuth, API Key]
  Stage 3: Database? [PostgreSQL, MongoDB, MySQL]
  Stage 4: Deployment? [Docker, VPS, Serverless]
  Stage 5: Testing? [Jest, Mocha, Vitest]
         ↓
Idea Phase Complete! → 🔧 AUTO-START Technical Phase
         ↓
TECHNICAL PHASE (Stages 1-7) [AUTOMATIC - 7 stages default]
  Stage 1: Architecture pattern? [Monolithic, Microservices, Serverless]
  Stage 2: Project structure? [Feature-based, Layer-based, Domain-driven]
  Stage 3: Database design? [Normalized SQL, Polyglot, Document DB]
  Stage 4: API patterns? [RESTful+OpenAPI, GraphQL, REST+WebSocket]
  Stage 5: Code patterns? [Repository+DI, Service Layer, CQRS]
  Stage 6: Security & Auth? [JWT, OAuth 2.0, API Key]
  Stage 7: Testing strategy? [Pyramid, BDD, Contract Testing]
         ↓
Complete Specification (Functional + Technical) ✅
  Ready for Planning Tool → WBS Execution
```

## Actions

### 1. start - Initialize Session

Create new refinement session.

**Parameters:**
- `initial_prompt` (required): User's vague request

**Example:**
```python
result = await vibe_coding(
    action="start",
    initial_prompt="I want to build a task management API"
)
```

**Response:**
```json
{
    "success": true,
    "action": "start",
    "session_id": "vc_session_1234567890_abc123",
    "status": "analyzing",
    "message": "Session created. AI must analyze and determine total_stages.",
    "instructions_for_llm": {
        "step_1": "Analyze prompt complexity",
        "step_2": "Determine total_stages needed",
        "step_3": "Call set_total_stages action"
    }
}
```

### 2. set_total_stages - Begin Idea Phase

LLM sets total stages after analysis and starts refinement.

**Parameters:**
- `session_id` (required)
- `total_stages` (required): Number of idea stages
- `question` (required): First clarifying question
- `suggestions` (required): 3 alternatives array

**Example:**
```python
result = await vibe_coding(
    action="set_total_stages",
    session_id="vc_session_1234567890_abc123",
    total_stages=5,
    question="What type of API architecture?",
    suggestions=[
        "RESTful API with Express.js",
        "GraphQL API with Apollo Server",
        "gRPC for high-performance"
    ]
)
```

**Response:**
```json
{
    "success": true,
    "action": "set_total_stages",
    "session_id": "vc_session_1234567890_abc123",
    "status": "awaiting_response",
    "current_phase": "idea",
    "stage": 1,
    "total_stages": 5,
    "progress_percentage": 20,
    "message": "Starting idea refinement - Stage 1/5 (20%)",
    "question": "What type of API architecture?",
    "suggestions": [...]
}
```

### 3. respond - Continue Refinement

Process user response and continue to next stage.

**Parameters:**
- `session_id` (required)
- `user_response` (required): User's selection
- `next_question` (optional): Next question
- `next_suggestions` (optional): Next 3 alternatives
- `is_final` (optional): Force completion

**Example:**
```python
result = await vibe_coding(
    action="respond",
    session_id="vc_session_1234567890_abc123",
    user_response="Option 1 - RESTful with Express.js",
    next_question="What authentication method?",
    next_suggestions=[
        "JWT with refresh tokens",
        "OAuth 2.0 with Google/GitHub",
        "API Key for server-to-server"
    ]
)
```

**Response (Continuing):**
```json
{
    "success": true,
    "action": "respond",
    "session_id": "vc_session_1234567890_abc123",
    "status": "awaiting_response",
    "current_phase": "idea",
    "stage": 2,
    "total_stages": 5,
    "progress_percentage": 40,
    "message": "Idea Phase - Stage 2/5 (40%)",
    "question": "What authentication method?",
    "suggestions": [...]
}
```

**Response (Idea Phase Complete → Auto-Start Technical Phase):**
```json
{
    "success": true,
    "action": "respond",
    "session_id": "vc_session_1234567890_abc123",
    "status": "awaiting_response",
    "current_phase": "technical",
    "stage": 1,
    "total_stages": 7,
    "progress_percentage": 14,
    "message": "✅ Idea refinement complete!\n\n🔧 Auto-Starting Technical Implementation Phase\n\nStage 1/7 (14%)",
    "idea_phase_summary": "Full functional specification summary...",
    "question": "What application architecture should be used for this project?",
    "suggestions": [
        "Monolithic architecture with MVC pattern (simpler deployment, good for small-medium apps, single codebase)",
        "Microservices architecture with API gateway (scalable, distributed, independent deployments, complex management)",
        "Serverless architecture with cloud functions (cost-effective, auto-scaling, event-driven, platform-dependent)"
    ]
}
```

**Note:** Technical Phase now starts **automatically** after Idea Phase completion with 7 default stages.

### 4. start_technical_phase - Manual Technical Phase Start (OPTIONAL)

**⚠️ Note:** Technical phase starts **automatically** after idea phase. This action is only needed if you want to restart or manually control the technical phase.

Start technical implementation phase manually (rarely needed).

**Parameters:**
- `session_id` (required)
- `total_stages` (optional): Technical stages (default: 7)

**Example:**
```python
# Only needed if you want to manually restart technical phase
result = await vibe_coding(
    action="start_technical_phase",
    session_id="vc_session_1234567890_abc123",
    total_stages=7
)
```

**Response:**
```json
{
    "success": true,
    "action": "start_technical_phase",
    "session_id": "vc_session_1234567890_abc123",
    "status": "awaiting_response",
    "current_phase": "technical",
    "stage": 1,
    "total_stages": 7,
    "progress_percentage": 14,
    "message": "Starting technical implementation phase - Stage 1/7",
    "question": "What application architecture should be used?",
    "suggestions": [...]
}
```

**Technical Phase Stages (Default 7 Stages):**

1. **Architecture & Patterns**: Monolithic vs Microservices vs Serverless
2. **Project Structure**: Feature-based vs Layer-based vs Domain-driven
3. **Database Strategy**: SQL vs NoSQL vs Polyglot persistence
4. **API Patterns**: RESTful vs GraphQL vs Hybrid
5. **Code Organization**: Repository pattern vs Service layer vs CQRS
6. **Security & Auth**: JWT vs OAuth vs API Key
7. **Testing Strategy**: Testing pyramid vs BDD vs Contract testing

### 5. skip_technical_phase - End at Idea Phase (DEPRECATED)

**⚠️ Deprecated:** This action is no longer needed as technical phase starts automatically.

If you need to end early, simply stop responding during the technical phase.

**Parameters:**
- `session_id` (required)

**Example:**
```python
result = await vibe_coding(
    action="skip_technical_phase",
    session_id="vc_session_1234567890_abc123"
)
```

**Response:**
```json
{
    "success": true,
    "action": "skip_technical_phase",
    "session_id": "vc_session_1234567890_abc123",
    "status": "completed_idea_only",
    "current_phase": "idea",
    "message": "Session completed with functional specification only.",
    "refined_prompt": "Functional specification...",
    "note": "Technical phase skipped. Can resume later with start_technical_phase."
}
```

### 6. add_feature - Extend Session

Add features to completed session without restarting.

**Parameters:**
- `session_id` (required)
- `feature_description` (required)
- `additional_stages` (required): Stages needed for feature
- `question` (required): First feature question
- `suggestions` (required): 3 alternatives

**Example:**
```python
result = await vibe_coding(
    action="add_feature",
    session_id="vc_session_1234567890_abc123",
    feature_description="Add WebSocket support",
    additional_stages=3,
    question="What WebSocket library?",
    suggestions=[
        "Socket.io for cross-browser compatibility",
        "Native WebSocket with ws library",
        "Server-Sent Events (SSE)"
    ]
)
```

**Response:**
```json
{
    "success": true,
    "action": "add_feature",
    "session_id": "vc_session_1234567890_abc123",
    "status": "awaiting_response",
    "stage": 6,
    "total_stages": 8,
    "previous_total_stages": 5,
    "additional_stages": 3,
    "progress_percentage": 75,
    "message": "Feature added! Extended from 5 to 8 stages. Stage 6/8",
    "question": "What WebSocket library?",
    "suggestions": [...]
}
```

### 7. get_status - Check Session State

Retrieve current session status and history.

**Example:**
```python
result = await vibe_coding(
    action="get_status",
    session_id="vc_session_1234567890_abc123"
)
```

### 8. list_sessions - List All Sessions

Get overview of all active sessions.

**Example:**
```python
result = await vibe_coding(
    action="list_sessions"
)
```

### 9. finalize - Manual Completion

Manually complete session with final prompt.

**Example:**
```python
result = await vibe_coding(
    action="finalize",
    session_id="vc_session_1234567890_abc123",
    final_prompt="Complete specification..."
)
```

## Final Output Format

When both phases complete, the tool generates:

```markdown
# Project Specification & Technical Implementation Plan

## 1. Functional Specification (Idea Phase)

**Original Request:** I want to build a task management API

**API Architecture:** RESTful API with Express.js and PostgreSQL
**Authentication:** JWT with refresh token rotation
**Database:** PostgreSQL with Sequelize ORM
**Deployment:** Docker containers on AWS ECS
**Testing:** Jest for unit tests, Supertest for integration tests

## 2. Technical Implementation Plan

### 2.1 Technical Decisions

**Architecture Pattern:** Microservices architecture with API gateway
- Reasoning: Allows independent scaling and deployment of services
- Trade-offs: More complex infrastructure but better scalability

**Project Structure:** Feature-based organization
- Features grouped by functionality (/features/tasks, /features/users)
- Easier team scaling and code ownership

**Database Strategy:** PostgreSQL with normalized schema
- ACID transactions for data consistency
- Sequelize ORM for migrations and queries

**API Patterns:** RESTful with OpenAPI documentation
- Standard HTTP methods and status codes
- Auto-generated API documentation
- Cacheable responses

**Code Patterns:** Repository pattern + Dependency injection
- Testable and decoupled code
- Easy to mock dependencies for testing

### 2.2 Implementation Roadmap

1. **Project Setup**: Initialize project with chosen architecture
2. **Core Infrastructure**: Database setup, authentication, base services
3. **Feature Implementation**: Build features per functional spec
4. **Testing & Quality**: Implement testing strategy
5. **Deployment**: Configure CI/CD pipeline

### 2.3 Next Steps

Use Planning tool to create WBS from this specification:
```python
wbs = await planning(
    problem_statement=spec['technical_specification'],
    project_name="Task Management API"
)
```

Then use WBS Execution tool for step-by-step implementation.
```

## AI Usage Pattern

### Automatic Two-Phase Workflow (UPDATED)

```
PHASE 1: IDEA REFINEMENT
=========================

1. User: "I want to build something"
   AI → Calls: vibe_coding(action='start', initial_prompt="...")
   Tool → Returns: session_id + analysis instructions

2. AI analyzes complexity → "Needs 5 stages"
   AI → Calls: vibe_coding(
       action='set_total_stages',
       session_id="...",
       total_stages=5,
       question="...",
       suggestions=[...]
   )
   Tool → Returns: Stage 1/5

3. User responds
   AI → Calls: vibe_coding(
       action='respond',
       user_response="...",
       next_question="...",
       next_suggestions=[...]
   )
   Tool → Returns: Stage 2/5

4. Loop continues through all 5 idea stages

5. Idea phase complete (Stage 5/5)
   🔧 Tool → AUTOMATICALLY STARTS Technical Phase!
   Tool → Returns: Technical Stage 1/7 (Architecture question)

PHASE 2: TECHNICAL REFINEMENT (AUTOMATIC)
==========================================

6. Technical phase auto-started (no user action needed)
   Tool → Returns: First technical question (Architecture)
   
7. User responds to technical questions
   AI → Calls: vibe_coding(
       action='respond',
       user_response="...",
       next_question="...",
       next_suggestions=[...]
   )
   Loop through all 7 technical stages

8. Technical phase complete (Stage 7/7)
   Tool → Returns: Comprehensive specification ready for WBS
   
9. AI presents complete specification:
   - Functional requirements (from Idea Phase)
   - Technical implementation plan (from Technical Phase)
   - Ready for Planning tool → WBS Execution
```

**Key Changes:**
- ✅ No manual `start_technical_phase` call needed
- ✅ Seamless transition from Idea → Technical
- ✅ Default 7 technical stages (was 5)
- ✅ Complete specification automatically generated

## Technical Phase Question Templates (7 Stages)

The technical phase uses **7 pre-defined question templates** that cover all aspects of technical implementation:

### Stage 1: Architecture & Patterns
```python
{
    "question": "What application architecture should be used?",
    "suggestions": [
        "Monolithic architecture with MVC pattern (simpler deployment, single codebase)",
        "Microservices architecture with API gateway (scalable, distributed, complex)",
        "Serverless architecture with cloud functions (cost-effective, auto-scaling)"
    ]
}
```

### Stage 2: Project Structure
```python
{
    "question": "How should the project structure be organized?",
    "suggestions": [
        "Feature-based: /features/auth, /features/users (grouped by functionality)",
        "Layer-based: /controllers, /services, /models (traditional MVC)",
        "Domain-driven: /domain/user, /domain/product (business logic focus)"
    ]
}
```

### Stage 3: Database Strategy
```python
{
    "question": "What database strategy should be implemented?",
    "suggestions": [
        "Single relational DB with normalized schema (PostgreSQL, ACID, structured)",
        "Polyglot persistence: SQL + NoSQL (PostgreSQL + Redis, optimized per use case)",
        "Document database with flexible schema (MongoDB, rapid iteration, nested data)"
    ]
}
```

### Stage 4: API Patterns
```python
{
    "question": "What API patterns should be implemented?",
    "suggestions": [
        "RESTful with resource routing + OpenAPI docs (standard, cacheable, widely supported)",
        "GraphQL with schema-first design (flexible queries, reduces over-fetching, typed)",
        "REST + WebSocket hybrid (combines REST stability with real-time capabilities)"
    ]
}
```

### Stage 5: Code Organization
```python
{
    "question": "What code organization patterns should be used?",
    "suggestions": [
        "Repository pattern + Dependency injection (testable, decoupled, easy mocking)",
        "Service layer pattern + DTOs (clean separation, validated data transfer)",
        "CQRS pattern for read/write separation (optimized queries, scalable, complex)"
    ]
}
```

### Stage 6: Authentication & Security
```python
{
    "question": "What authentication and security approach should be implemented?",
    "suggestions": [
        "JWT (JSON Web Tokens) with refresh token rotation (stateless, scalable, secure)",
        "OAuth 2.0 with social login providers (Google, GitHub) (user convenience, third-party trust)",
        "API Key authentication for server-to-server communication (simple, suitable for internal services)"
    ]
}
```

### Stage 7: Testing Strategy
```python
{
    "question": "What testing strategy should be implemented?",
    "suggestions": [
        "Testing pyramid: Unit (70%) + Integration (20%) + E2E (10%) with Jest/Mocha (balanced coverage, fast feedback)",
        "BDD with Cucumber + unit tests (business-readable specs, collaboration focus, higher-level scenarios)",
        "Contract testing + unit tests for microservices (API contract verification, service independence, Pact framework)"
    ]
}
```

## Best Practices

### 1. Make Suggestions Specific

❌ **Too Vague:**
- "Use a database"
- "Add authentication"
- "Make it secure"

✅ **Specific:**
- "PostgreSQL with Sequelize ORM for relational data and migrations"
- "JWT authentication with refresh token rotation and Redis storage"
- "Rate limiting with express-rate-limit and helmet.js for security headers"

### 2. Progressive Detail

Start broad and get more specific:

**Idea Phase:**
- Stage 1: Architecture type (REST vs GraphQL)
- Stage 2: Framework choice (Express vs Fastify)
- Stage 3: Database selection (PostgreSQL vs MongoDB)

**Technical Phase:**
- Stage 1: Architecture pattern (Monolithic vs Microservices)
- Stage 2: Code structure (Feature-based vs Layer-based)
- Stage 3: Database design approach (Normalized vs Document-based)

### 3. Analyze Complexity Accurately

Determine appropriate stage count:

**Simple (3 stages):**
"Create a contact form"
→ Framework, Validation, Email service

**Medium (5 stages):**
"Build an API"
→ Architecture, Auth, Database, Deployment, Testing

**Complex (7+ stages):**
"Build a social network"
→ Architecture, Auth, Database, Real-time, Storage, Deployment, Testing, Monitoring

### 4. Always Wait for Input

**CRITICAL**: After presenting suggestions, WAIT for user response.

The AI must:
- NOT make assumptions
- NOT proceed to implementation
- ONLY continue after explicit user selection

### 5. Use Technical Templates

For technical phase, let the tool provide question templates:

```python
# AI doesn't need to create technical questions
# Tool has built-in templates for consistency
result = await vibe_coding(
    action="respond",
    session_id="...",
    user_response="..."
    # No next_question/suggestions needed for technical phase
    # Tool auto-uses templates
)
```

## Integration with Other Tools

### With Planning Tool

```python
# 1. Complete vibe coding (both phases)
vibe_result = await vibe_coding(...)

# 2. Extract technical specification
spec = vibe_result['technical_specification']

# 3. Generate WBS
wbs_result = await planning(
    problem_statement=spec,
    project_name="My Project"
)
```

### With WBS Execution Tool

```python
# After Planning generates WBS.md
wbs_result = await wbs_execution(
    action="start",
    wbs_file_path="/path/to/WBS.md"
)
```

### With Sequential Thinking

```python
# Use ST for complex technical decisions during implementation
st_result = await st(
    thought="Analyzing the best database schema design based on Vibe Coding spec...",
    ...
)
```

## Complete Example

```python
# Stage 1: Start
result = await vibe_coding(
    action="start",
    initial_prompt="I need a task management API"
)

# Stage 2: AI analyzes and sets stages
result = await vibe_coding(
    action="set_total_stages",
    session_id=session_id,
    total_stages=4,
    question="What type of API?",
    suggestions=["RESTful", "GraphQL", "gRPC"]
)

# Stages 3-6: Complete idea phase
# ... multiple respond calls ...

# Stage 7: Idea phase complete, start technical
result = await vibe_coding(
    action="start_technical_phase",
    session_id=session_id
)

# Stages 8-12: Complete technical phase
# ... multiple respond calls with technical questions ...

# Stage 13: Both phases complete
# Result includes comprehensive functional + technical specification
# Ready for Planning tool → WBS Execution
```

## Configuration

Configure in `configs/vibe.py`:

```python
class VibeConfig:
    ENABLE_VIBE_CODING = True
    MAX_REFINEMENT_STAGES = 10
    NUM_SUGGESTIONS = 3
    SESSION_TIMEOUT = 3600
    
    # Technical phase settings
    DEFAULT_TECHNICAL_STAGES = 5
    ENABLE_TECHNICAL_TEMPLATES = True
```

## Error Handling

### Common Errors

```python
# Missing required parameter
Error: "initial_prompt is required for 'start' action"

# Wrong number of suggestions
Error: "Exactly 3 suggestions must be provided"

# Invalid session
Error: "Session not found: invalid_session_id"

# Phase not completed
Error: "Idea phase must be completed before starting technical phase"
```

## Troubleshooting

### Session Not Found
**Solution**: Use `list_sessions` to find active sessions.

### Idea Phase Not Completing
**Solution**: Ensure all stages are executed. Check `stage >= total_stages`.

### Technical Phase Not Available
**Solution**: Complete idea phase first. Check `status == 'idea_phase_completed'`.

### Missing Technical Questions
**Solution**: Technical questions are auto-generated from templates. No need to provide custom questions.

## Session Data Structure

```python
{
    'id': 'vc_session_xxx',
    'original_prompt': '...',
    'current_phase': 'idea',  # or 'technical'
    'phases': {
        'idea': {
            'total_stages': 5,
            'current_stage': 3,
            'conversation_history': [...],
            'refined_output': '...',
            'completed': False
        },
        'technical': {
            'total_stages': 5,
            'current_stage': 0,
            'conversation_history': [],
            'technical_spec': {},
            'completed': False
        }
    },
    'status': 'awaiting_response',
    'created_at': '2025-10-17T...',
    'last_updated': '2025-10-17T...'
}
```

## Limitations

- Maximum 10 refinement stages per phase (configurable)
- Sessions persist only during server runtime (not saved to disk)
- Exactly 3 suggestions required (not configurable per call)
- Single linear conversation path (no branching)
- Technical phase requires idea phase completion

## Future Enhancements

- [ ] Session persistence to database
- [ ] Custom technical question templates per project type
- [ ] Architecture diagram generation from technical spec
- [ ] Automatic WBS generation after completion
- [ ] Integration with code generation tools
- [ ] Branch/backtrack support for alternative approaches
- [ ] Multi-user collaborative refinement

## Related Tools

- **[Planning Tool](planning.md)**: For creating WBS from specifications
- **[WBS Execution](wbs-execution.md)**: For step-by-step implementation
- **[Sequential Thinking](sequential-thinking.md)**: For deep technical analysis
- **[Conversation Memory](conversation-memory.md)**: For storing specifications

## Support

- **Documentation**: [GitHub Wiki](https://github.com/HHC225/Local_MCP_Server/wiki)
- **Issues**: [GitHub Issues](https://github.com/HHC225/Local_MCP_Server/issues)
- **Examples**: See `examples/vibe-coding/` directory

---

**Last Updated**: 2025-10-17  
**Version**: 3.0.0 (Two-Phase Refinement with Technical Implementation)

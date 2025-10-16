# Report Generator Tool

Generate comprehensive IT reports from raw content such as Slack messages, JIRA tickets, investigation results, and more.

## 📋 Overview

The Report Generator tool converts unstructured IT content into professional, structured HTML reports. It uses AI to analyze raw input and generate executive summaries, detailed analysis, action items, and recommendations.

### Key Features

- **Universal Input**: Accepts any IT-related content (Slack threads, JIRA tickets, logs, emails, etc.)
- **Structured Analysis**: AI-powered content analysis with severity assessment
- **Professional Output**: Beautiful HTML reports with glassmorphism design
- **Executive Summaries**: Key takeaways for leadership and stakeholders
- **Action Tracking**: Prioritized action items with assignees and deadlines
- **Self-Contained**: HTML files include all CSS/JS (no external dependencies)

## 🎯 Use Cases

### Incident Reports
Convert incident communication into formal incident reports:
- Root cause analysis
- Timeline of events
- Impact assessment
- Remediation steps

### Investigation Summaries
Document technical investigations:
- Findings and evidence
- Technical details
- Risk assessment
- Recommendations

### Bug Analysis
Transform bug reports into comprehensive analysis:
- Reproduction steps
- Affected systems
- Priority assessment
- Fix recommendations

### Meeting Notes
Convert meeting discussions into actionable reports:
- Key decisions
- Action items with owners
- Follow-up tasks
- Next steps

## 🚀 Quick Start

### Basic Workflow

The Report Generator uses a **two-step process**:

1. **Generate Report Structure**: Call `generate_report` with raw content
2. **Build HTML Report**: Call `build_report_from_json` with structured JSON

```
Raw Content → generate_report → JSON Structure → build_report_from_json → HTML Report
```

### Step 1: Generate Report

Call the `generate_report` tool with your content:

**Input Parameters**:
- `content` (required): The raw text to analyze
- `source_type` (optional): Hint about source ("slack", "jira", "email", "investigation")
- `context` (optional): Additional background information

**Example**:
```json
{
  "input_data": {
    "content": "Database connection pool exhausted at 14:23 UTC. Users experiencing 500 errors. Root cause: connection leak in UserService.java line 234. Fixed by adding proper connection.close() in finally block.",
    "source_type": "slack",
    "context": "Production incident on 2025-10-16"
  }
}
```

### Step 2: Provide Structured JSON

After calling `generate_report`, the LLM must respond with a JSON object following this **exact schema**:

```json
{
  "report_title": "Clear, concise title summarizing the event",
  "report_type": "Type of report (e.g., Incident Analysis, Security Alert, System Outage Postmortem)",
  "severity": "Low | Medium | High | Critical",
  "strategic_summary": {
    "overview": "A 2-3 sentence executive summary. What happened and what is the current state?",
    "key_takeaways": [
      "The single most important finding or conclusion.",
      "Another critical piece of information a leader needs to know.",
      "A third key insight, if applicable."
    ],
    "business_implications": "How does this event affect the business? (e.g., potential revenue loss, customer trust, operational delays)",
    "next_steps_summary": "A high-level summary of what will happen next (e.g., 'A full post-mortem is scheduled', 'Security protocols will be reviewed'). Not a task list."
  },
  "key_findings": {
    "root_cause": "The determined root cause or the leading hypothesis, explained in simple terms.",
    "key_events": [
      "A chronological list of the most significant events that occurred."
    ],
    "affected_systems": [
      "List of primary systems, services, or user groups that were impacted."
    ]
  },
  "metadata": {
    "reported_date": "When the event was first reported or detected (ISO 8601 format)",
    "tags": ["relevant", "tags", "for", "categorization"]
  }
}
```

### Step 3: Build HTML Report

Call `build_report_from_json` with the structured JSON:

**Input**: The complete JSON object from Step 2

**Output**:
```json
{
  "status": "success",
  "file_path": "/path/to/output/reports/incident_analysis_20251016_143022.html",
  "report_title": "Database Connection Pool Exhaustion",
  "report_type": "Incident Analysis",
  "severity": "high"
}
```

## 📊 JSON Schema Reference

### Required Fields

#### `report_title` (string)
Clear, concise title summarizing the event.

**Example**: `"Database Connection Pool Exhaustion"`

#### `report_type` (string)
Type of report being generated.

**Examples**: 
- `"Incident Analysis"`
- `"Security Alert"`
- `"Bug Investigation"`
- `"System Outage Postmortem"`

#### `severity` (string)
Impact level: `"low"`, `"medium"`, `"high"`, or `"critical"`

**Guidelines**:
- **Critical**: Major financial loss, data breach, complete service outage
- **High**: Significant user-facing disruption, core business function impaired
- **Medium**: Internal system issues, moderate user inconvenience
- **Low**: Cosmetic issues, isolated problems

#### `summary` (object)
Executive summary with three sub-fields:

- `overview` (string): 2-3 sentence summary of the situation
- `impact` (string): Business/user impact description
- `status` (string): Current status (e.g., "open", "in-progress", "resolved")

#### `details` (object)
Detailed information with four sub-fields:

- `background` (string): Detailed context and background
- `timeline` (string): Chronological timeline of events
- `technical_details` (string): Technical information, error messages, logs
- `affected_components` (string): Systems, services, or components affected

#### `analysis` (object)
Analysis section with three sub-fields:

- `root_cause` (string): Root cause analysis or hypothesis
- `contributing_factors` (string): Contributing factors or related issues
- `risk_assessment` (string): Risk evaluation and potential consequences

#### `action_items` (array of objects)
List of actionable tasks. Each item has:

- `action` (string): Specific action to be taken
- `priority` (string): `"low"`, `"medium"`, `"high"`, or `"critical"`
- `assignee` (string): Suggested assignee or team
- `deadline` (string): Suggested timeframe or deadline

#### `recommendations` (array of objects)
List of recommendations. Each item has:

- `recommendation` (string): Specific recommendation
- `rationale` (string): Why this recommendation is important
- `effort` (string): `"low"`, `"medium"`, or `"high"`

#### `metadata` (object)
Report metadata with four sub-fields:

- `source` (string): Where the information came from
- `reporter` (string): Who reported or initiated this
- `reported_date` (string): When reported (ISO 8601 format preferred)
- `tags` (array of strings): Categorization tags

## 🎨 Report Output

### HTML Report Features

Generated reports include:

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Glassmorphism UI**: Modern, professional appearance
- **Color-Coded Severity**: Visual indicators for severity levels
- **Priority Badges**: Action items show priority levels
- **Effort Indicators**: Recommendations show effort estimates
- **Print-Friendly**: Optimized for printing or PDF export
- **Self-Contained**: No external dependencies or CDN links

### Report Sections

1. **Header**: Title, severity badge, report type
2. **Executive Summary**: Overview, impact, status
3. **Details**: Background, timeline, technical details, affected components
4. **Analysis**: Root cause, contributing factors, risk assessment
5. **Action Items**: Prioritized tasks with assignees and deadlines
6. **Recommendations**: Suggestions with rationale and effort
7. **Metadata**: Source, reporter, date, tags

### File Location

Reports are saved to: `output/reports/{report_type}_{timestamp}.html`

**Example**: `output/reports/incident_analysis_20251016_143022.html`

## 💡 Best Practices

### Content Analysis

1. **Be Specific**: Extract concrete facts and data points
2. **Assess Accurately**: Base severity on actual business impact
3. **Stay Objective**: Separate facts from assumptions
4. **Focus on Action**: Provide clear, actionable recommendations

### Writing Guidelines

1. **Executive Summary**: Make it understandable by non-technical leaders in 30 seconds
2. **Timeline**: Use chronological order with timestamps when available
3. **Technical Details**: Include enough detail for technical staff to understand
4. **Action Items**: Be specific about what needs to be done and by whom

### Common Pitfalls

❌ **Don't**:
- Use vague language ("might be", "could be")
- Miss required JSON fields
- Over-inflate or under-assess severity
- Create action items without clear owners

✅ **Do**:
- Use concrete, specific language
- Fill all required JSON fields
- Assess severity based on business impact
- Assign clear ownership to action items

## 🔧 Configuration

### Settings

Report Generator settings are in `configs/report.py`:

```python
class ReportConfig:
    # Enable/disable tool
    ENABLE_REPORT_GENERATOR: bool = True
    
    # Output directory
    REPORT_OUTPUT_DIR: Path = OUTPUT_DIR / "reports"
    
    # Templates directory
    REPORT_TEMPLATES_DIR: Path = BASE_DIR / "src/tools/report/templates"
    
    # Max content length (characters)
    REPORT_MAX_CONTENT_LENGTH: int = 50000
    
    # Enable JSON validation
    REPORT_VALIDATE_JSON: bool = True
    
    # Report format
    REPORT_DEFAULT_FORMAT: str = "html"
```

### Environment Variables

Override settings via environment variables:

```bash
# Disable report generator
export ENABLE_REPORT_GENERATOR=false

# Change max content length
export REPORT_MAX_CONTENT_LENGTH=100000

# Disable JSON validation (not recommended)
export REPORT_VALIDATE_JSON=false
```

## 📝 Examples

### Example 1: Slack Incident Thread

**Input**:
```json
{
  "input_data": {
    "content": "@channel Production alert! Payment service is down. Users can't complete purchases. Started at 10:45 AM. DevOps investigating.\n\nUpdate: Found the issue. Redis cache expired and service didn't handle it gracefully. Deploying fix now.\n\nResolved: Fix deployed at 11:20 AM. Payments working again. Will do full postmortem tomorrow.",
    "source_type": "slack",
    "context": "Production incident from #alerts channel"
  }
}
```

**Generated Report**: Incident analysis with timeline, impact assessment, and action items for postmortem.

### Example 2: JIRA Bug Report

**Input**:
```json
{
  "input_data": {
    "content": "Bug: Users can't upload files larger than 5MB. Error: 'Request Entity Too Large'. Steps: 1) Login 2) Go to upload page 3) Select 10MB file 4) Click upload. Expected: File uploads. Actual: Error message. Browser: Chrome 118. Affects: All users.",
    "source_type": "jira",
    "context": "Bug reported by customer support"
  }
}
```

**Generated Report**: Bug analysis with reproduction steps, affected systems, and fix recommendations.

### Example 3: Investigation Results

**Input**:
```json
{
  "input_data": {
    "content": "Security audit findings: 1) API keys in Git history (3 instances). 2) Missing rate limiting on public endpoints. 3) Old dependencies with known CVEs. Recommendations: Rotate all API keys, implement rate limiting, update dependencies.",
    "source_type": "investigation",
    "context": "Security audit completed 2025-10-15"
  }
}
```

**Generated Report**: Security analysis with findings, risk assessment, and prioritized remediation steps.

## 🛠️ Troubleshooting

### Issue: "Missing required fields in JSON"

**Cause**: The JSON response is missing one or more required fields.

**Solution**: Ensure your JSON includes all required fields:
- `report_title`, `report_type`, `severity`
- `summary`, `details`, `analysis`
- `action_items`, `recommendations`, `metadata`

### Issue: "Content length exceeds maximum"

**Cause**: Input content is too long (default: 50,000 characters).

**Solution**: 
- Summarize the content before submitting
- Increase `REPORT_MAX_CONTENT_LENGTH` in config
- Split into multiple reports

### Issue: "Template file not found"

**Cause**: Template files are missing from `src/tools/report/templates/`.

**Solution**: Verify these files exist:
- `report_template.html`
- `report_styles.css`
- `report_script.js`

### Issue: Invalid JSON format

**Cause**: JSON response has syntax errors or incorrect structure.

**Solution**:
- Validate JSON using a JSON validator
- Check for missing commas, brackets, or quotes
- Ensure all strings are properly escaped

## 📚 Related Documentation

- [Sequential Thinking](sequential-thinking.md) - For analyzing complex incidents
- [Planning Tool](planning.md) - For creating remediation plans
- [Slack Tools](slack-tools.md) - For retrieving incident threads
- [Troubleshooting Guide](troubleshooting.md) - General troubleshooting

## 🔗 See Also

- **Example Reports**: Check `output/reports/` for generated examples
- **Templates**: Review `src/tools/report/templates/` for customization
- **Configuration**: See `configs/report.py` for all settings

---

**Need help?** Open an issue on [GitHub](https://github.com/HHC225/Local_MCP_Server/issues) or check the [Troubleshooting Guide](troubleshooting.md).

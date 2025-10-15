"""
Planning Tool Implementation
Advanced WBS planning tool for structured project breakdown before implementation
"""
from typing import Dict, Any, Optional, List
from fastmcp import Context
from datetime import datetime
import json
import os
from pathlib import Path
from ..base import ReasoningTool


# Shared session store for Planning
planning_sessions: Dict[str, Dict[str, Any]] = {}


class PlanningTool(ReasoningTool):
    """Planning Tool for Work Breakdown Structure (WBS) creation"""
    
    def __init__(self, default_output_dir: Optional[Path] = None):
        super().__init__(
            name="planning",
            description="Advanced WBS planning tool for structured project breakdown before implementation"
        )
        self.default_output_dir = default_output_dir or Path("./output/planning")
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"planning_{timestamp}"
    
    def _get_or_create_default_session(self, problem_statement: Optional[str] = None, 
                                      project_name: Optional[str] = None) -> str:
        """Get or create default session"""
        default_session_id = 'planning_default_session'
        
        if default_session_id not in planning_sessions or problem_statement:
            # Create new session if problem statement is provided or session doesn't exist
            session_id = self._generate_session_id() if problem_statement else default_session_id
            planning_sessions[session_id] = {
                'id': session_id,
                'projectName': project_name or f"Project_{session_id}",
                'problemStatement': problem_statement or 'Default planning session',
                'planningSteps': [],
                'finalWBS': [],
                'status': 'planning',
                'createdAt': datetime.now().isoformat(),
                'lastUpdated': datetime.now().isoformat(),
                'branches': {},
                'outputFilePath': None
            }
            return session_id
        
        return default_session_id
    
    def _validate_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input data"""
        if not data.get('planningStep') or not isinstance(data['planningStep'], str):
            raise ValueError('Invalid planningStep: must be a string')
        
        if not isinstance(data.get('stepNumber'), int):
            raise ValueError('Invalid stepNumber: must be a number')
        
        if not isinstance(data.get('totalSteps'), int):
            raise ValueError('Invalid totalSteps: must be a number')
        
        if not isinstance(data.get('nextStepNeeded'), bool):
            raise ValueError('Invalid nextStepNeeded: must be a boolean')
        
        # Validate WBS items if provided
        wbs_items = data.get('wbsItems', [])
        if wbs_items and isinstance(wbs_items, list):
            for item in wbs_items:
                self._validate_wbs_item(item)
        
        return {
            'problemStatement': data.get('problemStatement'),
            'projectName': data.get('projectName'),
            'planningStep': data['planningStep'],
            'stepNumber': data['stepNumber'],
            'totalSteps': data['totalSteps'],
            'nextStepNeeded': data['nextStepNeeded'],
            'wbsItems': wbs_items,
            'refineWBS': data.get('refineWBS', False),
            'isRevision': data.get('isRevision'),
            'revisesStep': data.get('revisesStep'),
            'branchFromStep': data.get('branchFromStep'),
            'branchId': data.get('branchId'),
            'generateMarkdown': data.get('generateMarkdown', False),
            'exportToFile': data.get('exportToFile', True),
            'outputPath': data.get('outputPath'),
            'actionRequired': data.get('actionRequired'),
            'actionType': data.get('actionType'),
            'actionDescription': data.get('actionDescription'),
        }
    
    def _validate_wbs_item(self, item: Dict[str, Any]) -> None:
        """Validate a single WBS item"""
        required_fields = ['id', 'title', 'description', 'level', 'completed', 'priority', 'order']
        for field in required_fields:
            if field not in item:
                raise ValueError(f'WBS item missing required field: {field}')
        
        if not isinstance(item['level'], int) or item['level'] < 0:
            raise ValueError(f'Invalid level for WBS item {item["id"]}: must be non-negative integer')
        
        if item['priority'] not in ['high', 'medium', 'low']:
            raise ValueError(f'Invalid priority for WBS item {item["id"]}: must be high, medium, or low')
        
        if not isinstance(item['completed'], bool):
            raise ValueError(f'Invalid completed status for WBS item {item["id"]}: must be boolean')
    
    def _validate_wbs_hierarchy(self, wbs_items: List[Dict[str, Any]]) -> List[str]:
        """Validate WBS hierarchy consistency"""
        errors = []
        items_by_id = {item['id']: item for item in wbs_items}
        
        for item in wbs_items:
            # Check parent reference
            if item.get('parentId') and item['parentId'] not in items_by_id:
                errors.append(f"Item {item['id']} references non-existent parent: {item['parentId']}")
            
            # Check level consistency with parent
            if item.get('parentId'):
                parent = items_by_id.get(item['parentId'])
                if parent and item['level'] != parent['level'] + 1:
                    errors.append(f"Item {item['id']} has inconsistent level with parent {item['parentId']}")
            
            # Check dependency references
            if item.get('dependencies'):
                for dep_id in item['dependencies']:
                    if dep_id not in items_by_id:
                        # Dependencies might be hierarchical numbers or task titles, so only warn
                        pass
        
        return errors
    
    def _format_planning_log(self, step_data: Dict[str, Any]) -> str:
        """Format planning step for display"""
        step_number = step_data['stepNumber']
        total_steps = step_data['totalSteps']
        analysis = step_data['planningStep']
        wbs_items_count = len(step_data.get('wbsItems', []))
        
        prefix = '📋 Planning Step'
        
        return f"\n{prefix} {step_number}/{total_steps}\n{analysis}\nWBS Items Added: {wbs_items_count}\n"
    
    def _generate_wbs_markdown(self, session: Dict[str, Any]) -> str:
        """Generate WBS markdown content"""
        project_name = session['projectName']
        problem_statement = session['problemStatement']
        wbs_items = session['finalWBS']
        
        # Sort WBS items by level and order
        sorted_wbs = sorted(wbs_items, key=lambda x: (x['level'], x['order']))
        
        markdown = f"# Project: {project_name}\n\n"
        markdown += f"## Problem Statement\n{problem_statement}\n\n"
        markdown += "## Work Breakdown Structure\n\n"
        
        # Generate hierarchical structure
        markdown += self._generate_wbs_items_markdown(sorted_wbs)
        
        # Generate summary
        markdown += "\n## Planning Summary\n\n"
        summary = self._generate_wbs_summary(sorted_wbs)
        markdown += f"- **Total Tasks**: {summary['totalTasks']}\n"
        markdown += f"- **High Priority**: {summary['highPriority']}\n"
        markdown += f"- **Medium Priority**: {summary['mediumPriority']}\n"
        markdown += f"- **Low Priority**: {summary['lowPriority']}\n"
        markdown += f"- **Completed Tasks**: {summary['completedTasks']}\n"
        markdown += f"- **Remaining Tasks**: {summary['remainingTasks']}\n"
        markdown += f"- **Progress**: {summary['progress']}%\n\n"
        
        # Critical path
        markdown += "### Critical Path\n"
        critical_tasks = self._identify_critical_path(sorted_wbs)
        if critical_tasks:
            for task in critical_tasks:
                markdown += f"- {task}\n"
        else:
            markdown += "- No critical path identified\n"
        
        # Metadata
        markdown += "\n## Planning Metadata\n\n"
        markdown += f"- **Session ID**: {session['id']}\n"
        markdown += f"- **Status**: {session['status']}\n"
        markdown += f"- **Created**: {session['createdAt']}\n"
        markdown += f"- **Last Updated**: {session['lastUpdated']}\n"
        markdown += f"- **Planning Steps**: {len(session['planningSteps'])}\n\n"
        
        markdown += "---\n"
        markdown += f"*Generated by Planning Tool - {datetime.now().isoformat()}*\n"
        
        return markdown
    
    def _generate_wbs_items_markdown(self, wbs_items: List[Dict[str, Any]]) -> str:
        """Generate markdown for WBS items with hierarchical structure"""
        markdown = ""
        items_by_id = {item['id']: item for item in wbs_items}
        
        # Get root level items
        root_items = [item for item in wbs_items if item['level'] == 0]
        
        for idx, root_item in enumerate(root_items, 1):
            markdown += f"### {idx}. {root_item['title']}\n"
            markdown += self._generate_checkbox_item(root_item, 0, idx, wbs_items)
            
            # Add children
            children = [item for item in wbs_items if item.get('parentId') == root_item['id']]
            for child_idx, child in enumerate(sorted(children, key=lambda x: x['order']), 1):
                markdown += self._generate_checkbox_item(child, 1, f"{idx}.{child_idx}", wbs_items)
                
                # Add grandchildren
                grandchildren = [item for item in wbs_items if item.get('parentId') == child['id']]
                for gc_idx, grandchild in enumerate(sorted(grandchildren, key=lambda x: x['order']), 1):
                    markdown += self._generate_checkbox_item(grandchild, 2, f"{idx}.{child_idx}.{gc_idx}", wbs_items)
            
            markdown += "\n"
        
        return markdown
    
    def _generate_checkbox_item(self, item: Dict[str, Any], indent_level: int, 
                                task_id: str, all_items: List[Dict[str, Any]]) -> str:
        """Generate checkbox markdown for a single item"""
        indent = "  " * indent_level
        checkbox = "[x]" if item['completed'] else "[ ]"
        priority = item['priority'].capitalize()
        
        # Format dependencies
        dependencies = "None"
        if item.get('dependencies'):
            dependencies = ", ".join(item['dependencies'])
        
        markdown = f"{indent}- {checkbox} **{item['title']}** (Priority: {priority})\n"
        markdown += f"{indent}  - Task ID: {task_id}\n"
        markdown += f"{indent}  - Description: {item['description']}\n"
        markdown += f"{indent}  - Dependencies: {dependencies}\n"
        
        return markdown
    
    def _generate_wbs_summary(self, wbs_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate WBS summary statistics"""
        total_tasks = len(wbs_items)
        high_priority = len([i for i in wbs_items if i['priority'] == 'high'])
        medium_priority = len([i for i in wbs_items if i['priority'] == 'medium'])
        low_priority = len([i for i in wbs_items if i['priority'] == 'low'])
        completed_tasks = len([i for i in wbs_items if i['completed']])
        remaining_tasks = total_tasks - completed_tasks
        progress = round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)
        
        return {
            'totalTasks': total_tasks,
            'highPriority': high_priority,
            'mediumPriority': medium_priority,
            'lowPriority': low_priority,
            'completedTasks': completed_tasks,
            'remainingTasks': remaining_tasks,
            'progress': progress
        }
    
    def _identify_critical_path(self, wbs_items: List[Dict[str, Any]]) -> List[str]:
        """Identify critical path tasks (high priority with dependencies)"""
        critical_tasks = []
        high_priority = [item for item in wbs_items if item['priority'] == 'high']
        
        for item in high_priority:
            if item.get('dependencies') and len(item['dependencies']) > 0:
                critical_tasks.append(f"{item['title']} (depends on: {', '.join(item['dependencies'])})")
        
        return critical_tasks[:5]  # Return top 5 critical tasks
    
    def _export_wbs_to_file(self, session: Dict[str, Any], custom_path: Optional[str] = None, 
                           default_output_dir: Optional[Path] = None) -> Dict[str, Any]:
        """Export WBS to markdown file"""
        try:
            markdown = self._generate_wbs_markdown(session)
            
            # Determine output path
            if session.get('outputFilePath'):
                output_path = session['outputFilePath']
            elif custom_path:
                output_path = Path(custom_path)
                if output_path.is_dir():
                    sanitized_name = session['projectName'].replace(' ', '_')
                    output_path = output_path / f"{sanitized_name}_WBS.md"
            else:
                # Default to configured planning output directory
                if default_output_dir:
                    sanitized_name = session['projectName'].replace(' ', '_')
                    output_path = default_output_dir / f"{sanitized_name}_WBS.md"
                else:
                    # Fallback to current working directory
                    sanitized_name = session['projectName'].replace(' ', '_')
                    output_path = Path.cwd() / f"{sanitized_name}_WBS.md"
            
            output_path = Path(output_path)
            
            # Ensure directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            output_path.write_text(markdown, encoding='utf-8')
            
            # Store output path in session
            session['outputFilePath'] = str(output_path)
            session['status'] = 'exported'
            
            print(f"Exported WBS to: {output_path}")
            
            return {
                'success': True,
                'outputPath': str(output_path),
                'fileSize': len(markdown.encode('utf-8')),
                'totalLines': len(markdown.split('\n'))
            }
            
        except Exception as e:
            print(f"Export failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def execute(
        self,
        planning_step: str,
        step_number: int,
        total_steps: int,
        next_step_needed: bool,
        problem_statement: Optional[str] = None,
        project_name: Optional[str] = None,
        wbs_items: Optional[List[Dict[str, Any]]] = None,
        refine_wbs: Optional[bool] = False,
        is_revision: Optional[bool] = None,
        revises_step: Optional[int] = None,
        branch_from_step: Optional[int] = None,
        branch_id: Optional[str] = None,
        generate_markdown: Optional[bool] = False,
        export_to_file: Optional[bool] = True,
        output_path: Optional[str] = None,
        action_required: Optional[bool] = None,
        action_type: Optional[str] = None,
        action_description: Optional[str] = None,
        ctx: Optional[Context] = None
    ) -> str:
        """Execute planning process"""
        
        try:
            # Construct input data
            data = {
                'problemStatement': problem_statement,
                'projectName': project_name,
                'planningStep': planning_step,
                'stepNumber': step_number,
                'totalSteps': total_steps,
                'nextStepNeeded': next_step_needed,
                'wbsItems': wbs_items or [],
                'refineWBS': refine_wbs,
                'isRevision': is_revision,
                'revisesStep': revises_step,
                'branchFromStep': branch_from_step,
                'branchId': branch_id,
                'generateMarkdown': generate_markdown,
                'exportToFile': export_to_file,
                'outputPath': output_path,
                'actionRequired': action_required,
                'actionType': action_type,
                'actionDescription': action_description,
            }
            
            # Validate input data
            validated_input = self._validate_input(data)
            
            # Get or create session
            session_id = self._get_or_create_default_session(
                validated_input.get('problemStatement'),
                validated_input.get('projectName')
            )
            session = planning_sessions[session_id]
            
            # Create planning step
            planning_step_obj = {
                'stepNumber': validated_input['stepNumber'],
                'analysis': validated_input['planningStep'],
                'wbsItems': validated_input['wbsItems'],
                'nextStepNeeded': validated_input['nextStepNeeded'],
                'actionRequired': validated_input.get('actionRequired'),
                'actionType': validated_input.get('actionType'),
                'actionDescription': validated_input.get('actionDescription'),
                'timestamp': datetime.now().isoformat()
            }
            
            # Validate WBS hierarchy if items provided
            if planning_step_obj['wbsItems']:
                existing_items = session['finalWBS']
                existing_ids = {item['id'] for item in existing_items}
                new_items = [item for item in planning_step_obj['wbsItems'] if item['id'] not in existing_ids]
                all_wbs_items = existing_items + new_items
                
                hierarchy_errors = self._validate_wbs_hierarchy(all_wbs_items)
                if hierarchy_errors:
                    return json.dumps({
                        'error': f"WBS hierarchy validation failed: {', '.join(hierarchy_errors)}",
                        'status': 'failed'
                    }, indent=2, ensure_ascii=False)
            
            # Add planning step to session
            session['planningSteps'].append(planning_step_obj)
            
            # Update WBS items in session
            progressive_export_result = None
            if planning_step_obj['wbsItems']:
                existing_ids = {item['id'] for item in session['finalWBS']}
                new_items = [item for item in planning_step_obj['wbsItems'] if item['id'] not in existing_ids]
                session['finalWBS'].extend(new_items)
                
                # Progressive WBS file generation
                if validated_input['exportToFile']:
                    output_path_to_use = session.get('outputFilePath') or validated_input.get('outputPath')
                    progressive_export_result = self._export_wbs_to_file(session, output_path_to_use, self.default_output_dir)
                    print(f"Progressive WBS update: {'Success' if progressive_export_result['success'] else 'Failed'}")
            
            # Handle branching if specified
            if validated_input.get('branchFromStep') and validated_input.get('branchId'):
                branch_id = validated_input['branchId']
                if branch_id not in session['branches']:
                    session['branches'][branch_id] = []
                session['branches'][branch_id].append(planning_step_obj)
                print(f"Added planning step to branch: {branch_id}")
            
            # Handle completion and export
            export_result = None
            if not validated_input['nextStepNeeded'] or validated_input['generateMarkdown']:
                session['status'] = 'completed'
                
                if validated_input['exportToFile']:
                    output_path_to_use = session.get('outputFilePath') or validated_input.get('outputPath')
                    export_result = self._export_wbs_to_file(session, output_path_to_use, self.default_output_dir)
            
            # Update session
            session['lastUpdated'] = datetime.now().isoformat()
            
            # Log the planning step
            log_message = self._format_planning_log(validated_input)
            print(log_message, flush=True)
            
            # Log execution
            await self.log_execution(
                ctx,
                f"Planning - Step {validated_input['stepNumber']}/{validated_input['totalSteps']}"
            )
            
            # Generate WBS summary
            wbs_summary = None
            if planning_step_obj['wbsItems']:
                wbs_summary = self._generate_wbs_summary(session['finalWBS'])
            
            # Prepare response
            result = {
                'sessionId': session['id'],
                'projectName': session['projectName'],
                'stepNumber': validated_input['stepNumber'],
                'totalSteps': validated_input['totalSteps'],
                'nextStepNeeded': validated_input['nextStepNeeded'],
                'planningStep': validated_input['planningStep'],
                'wbsItemsAdded': len(planning_step_obj['wbsItems']),
                'totalWBSItems': len(session['finalWBS']),
                'branches': list(session['branches'].keys()),
                'planningStepsCompleted': len(session['planningSteps']),
                'status': session['status'],
                'exportResult': progressive_export_result or export_result,
                'wbsSummary': wbs_summary
            }
            
            # Add action-related information
            if validated_input.get('actionRequired'):
                result['actionRequired'] = validated_input['actionRequired']
                result['actionType'] = validated_input.get('actionType')
                result['actionDescription'] = validated_input.get('actionDescription')
            
            return json.dumps(result, indent=2, ensure_ascii=False)
            
        except Exception as e:
            error_result = {
                'error': str(e),
                'status': 'failed'
            }
            return json.dumps(error_result, indent=2, ensure_ascii=False)

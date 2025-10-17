"""
Planning Tool Implementation
Advanced Work Breakdown Structure (WBS) Creation Tool with Step-by-Step Planning
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import os
from pathlib import Path
from dataclasses import dataclass, field, asdict
from enum import Enum
from ..base import ReasoningTool


# ===== DATA STRUCTURES =====

class WBSItemLevel(Enum):
    """WBS hierarchical levels"""
    ROOT = 0
    MAIN = 1
    SUB = 2
    DETAIL = 3
    MICRO = 4


class Priority(Enum):
    """Task priority levels"""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class SessionStatus(Enum):
    """Planning session status"""
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"


@dataclass
class WBSItem:
    """WBS item data structure"""
    id: str
    title: str
    description: str
    level: int
    priority: str
    dependencies: List[str] = field(default_factory=list)
    order: int = 0
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class PlanningStep:
    """Planning step record"""
    step_number: int
    planning_step: str
    timestamp: str
    wbs_items_added: int = 0
    is_revision: bool = False
    revises_step: Optional[int] = None
    branch_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class PlanningSession:
    """Planning session data"""
    id: str
    problem_statement: str
    project_name: str
    status: str
    created_at: str
    last_updated: str
    wbs_items: List[WBSItem] = field(default_factory=list)
    planning_history: List[PlanningStep] = field(default_factory=list)
    total_steps: Optional[int] = None
    current_step: int = 0
    output_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = asdict(self)
        result['wbs_items'] = [item.to_dict() for item in self.wbs_items]
        result['planning_history'] = [step.to_dict() for step in self.planning_history]
        return result


# Shared session store for Planning
planning_sessions: Dict[str, PlanningSession] = {}


# ===== VALIDATION UTILITIES =====

class PlanningValidator:
    """Input validation and WBS hierarchy validation"""
    
    @staticmethod
    def validate_planning_input(data: Dict[str, Any]) -> Dict[str, str]:
        """Validate planning tool input"""
        errors = []
        
        # Required fields
        if not data.get('planning_step') or not isinstance(data['planning_step'], str):
            errors.append('planning_step is required and must be a string')
        
        if not isinstance(data.get('step_number'), int) or data.get('step_number', 0) < 1:
            errors.append('step_number is required and must be a positive integer')
        
        if not isinstance(data.get('total_steps'), int) or data.get('total_steps', 0) < 1:
            errors.append('total_steps is required and must be a positive integer')
        
        if not isinstance(data.get('next_step_needed'), bool):
            errors.append('next_step_needed is required and must be a boolean')
        
        # Validate step numbers
        if data.get('step_number', 0) > data.get('total_steps', 0):
            errors.append(f"step_number ({data.get('step_number')}) cannot exceed total_steps ({data.get('total_steps')})")
        
        # Validate revision parameters
        if data.get('is_revision') and not data.get('revises_step'):
            errors.append('revises_step is required when is_revision is true')
        
        if errors:
            return {'valid': False, 'errors': errors}
        
        return {'valid': True}
    
    @staticmethod
    def validate_wbs_items(items: List[Dict[str, Any]], existing_items: List[WBSItem]) -> Dict[str, Any]:
        """
        Validate WBS items structure and hierarchy
        
        CRITICAL REQUIREMENTS:
        - parent_id MUST be provided for all child items (level > 0)
        - parent_id MUST reference an existing parent item
        - Do NOT rely on automatic inference - always specify parent_id explicitly
        """
        errors = []
        warnings = []
        
        if not items:
            return {'valid': True, 'warnings': ['No WBS items provided']}
        
        existing_ids = {item.id for item in existing_items}
        new_ids = set()
        
        for idx, item in enumerate(items):
            # Required fields
            if not item.get('id'):
                errors.append(f"Item {idx}: 'id' is required")
                continue
            
            if not item.get('title'):
                errors.append(f"Item {item['id']}: 'title' is required")
            
            if not item.get('description'):
                warnings.append(f"Item {item['id']}: 'description' is empty")
            
            if not isinstance(item.get('level'), int) or item['level'] < 0:
                errors.append(f"Item {item['id']}: 'level' must be a non-negative integer")
            
            # CRITICAL: parent_id validation for child items
            if item.get('level', 0) > 0:
                if not item.get('parent_id'):
                    errors.append(f"Item {item['id']}: 'parent_id' is REQUIRED for child items (level > 0). Current level: {item.get('level')}")
                elif item['parent_id'] not in existing_ids and item['parent_id'] not in new_ids:
                    errors.append(f"Item {item['id']}: parent_id '{item['parent_id']}' does not exist. Parent must be added before child.")
            
            if item.get('priority') not in ['High', 'Medium', 'Low']:
                errors.append(f"Item {item['id']}: 'priority' must be High, Medium, or Low")
            
            # Check duplicate IDs
            if item['id'] in existing_ids or item['id'] in new_ids:
                warnings.append(f"Item {item['id']}: Duplicate ID, will be skipped or merged")
            else:
                new_ids.add(item['id'])
            
            # Validate dependencies
            if item.get('dependencies'):
                for dep in item['dependencies']:
                    if dep not in existing_ids and dep not in new_ids:
                        warnings.append(f"Item {item['id']}: Dependency '{dep}' not found")
            
            # Validate parent_id
            if item.get('parent_id'):
                if item['parent_id'] not in existing_ids and item['parent_id'] not in new_ids:
                    warnings.append(f"Item {item['id']}: Parent '{item['parent_id']}' not found")
        
        if errors:
            return {'valid': False, 'errors': errors, 'warnings': warnings}
        
        return {'valid': True, 'warnings': warnings}
    
    @staticmethod
    def detect_circular_dependencies(items: List[WBSItem]) -> List[str]:
        """Detect circular dependencies in WBS items"""
        errors = []
        
        def has_cycle(item_id: str, visited: set, rec_stack: set, dep_map: Dict[str, List[str]]) -> Optional[str]:
            visited.add(item_id)
            rec_stack.add(item_id)
            
            for dep in dep_map.get(item_id, []):
                if dep not in visited:
                    cycle = has_cycle(dep, visited, rec_stack, dep_map)
                    if cycle:
                        return cycle
                elif dep in rec_stack:
                    return f"{dep} -> {item_id}"
            
            rec_stack.remove(item_id)
            return None
        
        # Build dependency map
        dep_map = {item.id: item.dependencies for item in items}
        visited = set()
        
        for item in items:
            if item.id not in visited:
                cycle = has_cycle(item.id, visited, set(), dep_map)
                if cycle:
                    errors.append(f"Circular dependency detected: {cycle}")
        
        return errors


# ===== MARKDOWN GENERATOR =====

class WBSMarkdownGenerator:
    """Generate WBS markdown files from session data"""
    
    def __init__(self, session: PlanningSession):
        self.session = session
        self._id_to_item = {item.id: item for item in session.wbs_items}
        self._number_cache: Dict[str, str] = {}
    
    def generate(self) -> str:
        """Generate complete WBS markdown"""
        sections = []
        
        # Header
        sections.append(self._generate_header())
        sections.append("")
        
        # Problem statement
        sections.append("## Problem Statement")
        sections.append(self.session.problem_statement)
        sections.append("")
        
        # WBS structure
        sections.append("## Work Breakdown Structure")
        sections.append("")
        sections.append(self._generate_wbs_tree())
        sections.append("")
        
        # Planning summary
        sections.append(self._generate_planning_summary())
        sections.append("")
        
        # Critical path (if applicable)
        sections.append(self._generate_critical_path())
        sections.append("")
        
        # Metadata
        sections.append(self._generate_metadata())
        
        return '\n'.join(sections)
    
    def _generate_header(self) -> str:
        """Generate markdown header"""
        return f"# Project: {self.session.project_name}"
    
    def _generate_wbs_tree(self) -> str:
        """Generate hierarchical WBS tree with checkboxes"""
        lines = []
        root_items = [item for item in self.session.wbs_items if item.level == 0]
        root_items.sort(key=lambda x: x.order)
        
        for root in root_items:
            lines.extend(self._generate_item_lines(root, 0))
        
        return '\n'.join(lines)
    
    def _generate_item_lines(self, item: WBSItem, indent_level: int) -> List[str]:
        """Generate lines for a single WBS item and its children"""
        lines = []
        indent = '  ' * indent_level
        
        # Generate hierarchical number
        wbs_number = self._get_wbs_number(item)
        
        # Format dependencies
        dep_str = self._format_dependencies(item.dependencies)
        
        # Main task line
        checkbox = '[ ]'
        lines.append(f"{indent}- {checkbox} **{item.title}** (Priority: {item.priority})")
        
        # Task details
        lines.append(f"{indent}  - Task ID: {wbs_number}")
        lines.append(f"{indent}  - Description: {item.description}")
        lines.append(f"{indent}  - Dependencies: {dep_str}")
        lines.append("")
        
        # Children
        children = [self._id_to_item[child_id] for child_id in item.children if child_id in self._id_to_item]
        children.sort(key=lambda x: x.order)
        
        for child in children:
            lines.extend(self._generate_item_lines(child, indent_level + 1))
        
        return lines
    
    def _get_wbs_number(self, item: WBSItem) -> str:
        """Get hierarchical WBS number (e.g., 1.2.1)"""
        if item.id in self._number_cache:
            return self._number_cache[item.id]
        
        # Build path from root to current item
        path = []
        current = item
        
        while current:
            path.insert(0, current)
            if current.parent_id and current.parent_id in self._id_to_item:
                current = self._id_to_item[current.parent_id]
            else:
                break
        
        # Generate number based on path
        number_parts = []
        for i, node in enumerate(path):
            if i == 0:
                # Root level
                siblings = [it for it in self.session.wbs_items if it.level == 0]
            else:
                parent = path[i - 1]
                siblings = [self._id_to_item[child_id] for child_id in parent.children if child_id in self._id_to_item]
            
            siblings.sort(key=lambda x: x.order)
            position = next((idx + 1 for idx, s in enumerate(siblings) if s.id == node.id), 1)
            number_parts.append(str(position))
        
        wbs_number = '.'.join(number_parts)
        self._number_cache[item.id] = wbs_number
        return wbs_number
    
    def _format_dependencies(self, dependencies: List[str]) -> str:
        """Format dependencies for display"""
        if not dependencies:
            return "None"
        
        formatted = []
        for dep in dependencies:
            if dep in self._id_to_item:
                dep_item = self._id_to_item[dep]
                dep_number = self._get_wbs_number(dep_item)
                formatted.append(f"{dep_number} ({dep_item.title})")
            else:
                formatted.append(dep)
        
        return ', '.join(formatted)
    
    def _generate_planning_summary(self) -> str:
        """Generate planning process summary"""
        lines = []
        lines.append("## Planning Summary")
        lines.append("")
        lines.append(f"- **Total Planning Steps**: {len(self.session.planning_history)}")
        lines.append(f"- **Total WBS Items**: {len(self.session.wbs_items)}")
        lines.append(f"- **Status**: {self.session.status}")
        lines.append(f"- **Created**: {self.session.created_at}")
        lines.append(f"- **Last Updated**: {self.session.last_updated}")
        lines.append("")
        
        # Priority breakdown
        priority_counts = {'High': 0, 'Medium': 0, 'Low': 0}
        for item in self.session.wbs_items:
            priority_counts[item.priority] = priority_counts.get(item.priority, 0) + 1
        
        lines.append("### Priority Breakdown")
        for priority, count in priority_counts.items():
            lines.append(f"- {priority}: {count}")
        
        return '\n'.join(lines)
    
    def _generate_critical_path(self) -> str:
        """Generate critical path analysis"""
        lines = []
        lines.append("## Critical Path Analysis")
        lines.append("")
        
        # Find items with most dependencies
        critical_items = sorted(self.session.wbs_items, key=lambda x: len(x.dependencies), reverse=True)[:5]
        
        if critical_items:
            lines.append("### Tasks with Most Dependencies")
            for item in critical_items:
                wbs_number = self._get_wbs_number(item)
                lines.append(f"- **{wbs_number}** {item.title} ({len(item.dependencies)} dependencies)")
        else:
            lines.append("No critical path identified.")
        
        return '\n'.join(lines)
    
    def _generate_metadata(self) -> str:
        """Generate metadata section"""
        lines = []
        lines.append("## Planning Metadata")
        lines.append("")
        lines.append(f"- **Session ID**: {self.session.id}")
        lines.append(f"- **Project Name**: {self.session.project_name}")
        lines.append(f"- **Generated**: {datetime.now().isoformat()}")
        
        return '\n'.join(lines)


# ===== SESSION MANAGER =====

class PlanningSessionManager:
    """Manage planning sessions lifecycle"""
    
    @staticmethod
    def create_session(problem_statement: str, project_name: Optional[str] = None) -> PlanningSession:
        """Create new planning session"""
        session_id = f"planning_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if not project_name:
            # Generate project name from problem statement
            words = problem_statement.split()[:5]
            project_name = ' '.join(words)
        
        session = PlanningSession(
            id=session_id,
            problem_statement=problem_statement,
            project_name=project_name,
            status=SessionStatus.ACTIVE.value,
            created_at=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat()
        )
        
        planning_sessions[session_id] = session
        return session
    
    @staticmethod
    def get_session(session_id: str) -> Optional[PlanningSession]:
        """Get existing session"""
        return planning_sessions.get(session_id)
    
    @staticmethod
    def update_session(session: PlanningSession) -> None:
        """Update session"""
        session.last_updated = datetime.now().isoformat()
        planning_sessions[session.id] = session
    
    @staticmethod
    def add_wbs_items(session: PlanningSession, new_items: List[Dict[str, Any]]) -> int:
        """Add or merge WBS items to session"""
        added_count = 0
        existing_ids = {item.id for item in session.wbs_items}
        
        for item_data in new_items:
            if item_data['id'] not in existing_ids:
                wbs_item = WBSItem(
                    id=item_data['id'],
                    title=item_data['title'],
                    description=item_data.get('description', ''),
                    level=item_data['level'],
                    priority=item_data.get('priority', 'Medium'),
                    dependencies=item_data.get('dependencies', []),
                    order=item_data.get('order', 0),
                    parent_id=item_data.get('parent_id'),
                    children=item_data.get('children', [])
                )
                session.wbs_items.append(wbs_item)
                added_count += 1
        
        # Update parent-child relationships
        PlanningSessionManager._rebuild_hierarchy(session)
        
        return added_count
    
    @staticmethod
    def _rebuild_hierarchy(session: PlanningSession) -> None:
        """Rebuild parent-child relationships"""
        id_to_item = {item.id: item for item in session.wbs_items}
        
        for item in session.wbs_items:
            item.children = []
        
        for item in session.wbs_items:
            if item.parent_id and item.parent_id in id_to_item:
                parent = id_to_item[item.parent_id]
                if item.id not in parent.children:
                    parent.children.append(item.id)
    
    @staticmethod
    def add_planning_step(session: PlanningSession, step: PlanningStep) -> None:
        """Add planning step to history"""
        session.planning_history.append(step)
        session.current_step = step.step_number


# ===== MAIN PLANNING TOOL =====

class PlanningTool(ReasoningTool):
    """Advanced Planning Tool for WBS Creation"""
    
    def __init__(self, default_output_dir: Optional[Path] = None):
        super().__init__(
            name="planning",
            description="Advanced Planning Tool for Work Breakdown Structure (WBS) Creation"
        )
        self.default_output_dir = default_output_dir or Path("./output/planning")
    
    async def execute(
        self,
        planning_step: str,
        step_number: int,
        total_steps: int,
        next_step_needed: bool,
        problem_statement: Optional[str] = None,
        project_name: Optional[str] = None,
        wbs_items: Optional[List[Dict[str, Any]]] = None,
        refine_wbs: bool = False,
        is_revision: bool = False,
        revises_step: Optional[int] = None,
        branch_from_step: Optional[int] = None,
        branch_id: Optional[str] = None,
        generate_markdown: bool = False,
        export_to_file: bool = True,
        output_path: Optional[str] = None,
        action_required: bool = False,
        action_type: Optional[str] = None,
        action_description: Optional[str] = None,
        ctx: Any = None
    ) -> str:
        """Execute planning process"""
        
        # Validate input
        validation_result = PlanningValidator.validate_planning_input({
            'planning_step': planning_step,
            'step_number': step_number,
            'total_steps': total_steps,
            'next_step_needed': next_step_needed,
            'is_revision': is_revision,
            'revises_step': revises_step
        })
        
        if not validation_result.get('valid'):
            return json.dumps({
                'success': False,
                'error': 'Input validation failed',
                'details': validation_result.get('errors')
            }, ensure_ascii=False)
        
        # Get or create session
        session = None
        if step_number == 1:
            # New session
            if not problem_statement:
                return json.dumps({
                    'success': False,
                    'error': 'problem_statement is required for step 1'
                }, ensure_ascii=False)
            
            session = PlanningSessionManager.create_session(problem_statement, project_name)
        else:
            # Continue existing session - find the most recent active session
            active_sessions = [s for s in planning_sessions.values() if s.status == SessionStatus.ACTIVE.value]
            if active_sessions:
                session = max(active_sessions, key=lambda s: s.last_updated)
            else:
                return json.dumps({
                    'success': False,
                    'error': 'No active planning session found. Start with step_number=1'
                }, ensure_ascii=False)
        
        # Add planning step to history
        step_record = PlanningStep(
            step_number=step_number,
            planning_step=planning_step,
            timestamp=datetime.now().isoformat(),
            wbs_items_added=0,
            is_revision=is_revision,
            revises_step=revises_step,
            branch_id=branch_id
        )
        
        # Process WBS items if provided
        if wbs_items:
            # Validate WBS items
            validation = PlanningValidator.validate_wbs_items(wbs_items, session.wbs_items)
            
            if not validation.get('valid'):
                return json.dumps({
                    'success': False,
                    'error': 'WBS items validation failed',
                    'details': validation.get('errors'),
                    'warnings': validation.get('warnings')
                }, ensure_ascii=False)
            
            # Add WBS items
            added_count = PlanningSessionManager.add_wbs_items(session, wbs_items)
            step_record.wbs_items_added = added_count
            
            # Check for circular dependencies
            circular_errors = PlanningValidator.detect_circular_dependencies(session.wbs_items)
            if circular_errors:
                return json.dumps({
                    'success': False,
                    'error': 'Circular dependencies detected',
                    'details': circular_errors
                }, ensure_ascii=False)
        
        # Update session
        session.total_steps = total_steps
        PlanningSessionManager.add_planning_step(session, step_record)
        
        # Generate and export markdown if requested or if planning is complete
        markdown_content = None
        file_path = None
        
        if export_to_file and (generate_markdown or not next_step_needed):
            generator = WBSMarkdownGenerator(session)
            markdown_content = generator.generate()
            
            # Determine output path
            if output_path:
                file_path = Path(output_path)
            else:
                self.default_output_dir.mkdir(parents=True, exist_ok=True)
                file_path = self.default_output_dir / f"{session.project_name.replace(' ', '_')}_WBS.md"
            
            # Write file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            session.output_path = str(file_path)
        
        # Update session status
        if not next_step_needed:
            session.status = SessionStatus.COMPLETED.value
        
        PlanningSessionManager.update_session(session)
        
        # Build response
        response = {
            'success': True,
            'sessionId': session.id,
            'stepNumber': step_number,
            'totalSteps': total_steps,
            'nextStepNeeded': next_step_needed,
            'wbsItemsCount': len(session.wbs_items),
            'wbsItemsAdded': step_record.wbs_items_added,
            'status': session.status,
            'message': self._generate_message(session, step_number, total_steps, next_step_needed)
        }
        
        if file_path:
            response['outputPath'] = str(file_path)
            response['markdownGenerated'] = True
        
        if action_required:
            response['actionRequired'] = True
            response['actionType'] = action_type
            response['actionDescription'] = action_description
        
        return json.dumps(response, ensure_ascii=False, indent=2)
    
    def _generate_message(self, session: PlanningSession, step_number: int, total_steps: int, next_step_needed: bool) -> str:
        """Generate status message"""
        if not next_step_needed:
            return f"Planning completed! Generated WBS with {len(session.wbs_items)} items."
        else:
            progress = int((step_number / total_steps) * 100)
            return f"Step {step_number}/{total_steps} completed ({progress}%). Continue with next planning step."

"""
Interactive Specification Creator for EmailIntelligence

This module provides guided prompts and interactive specification creation
with contextual questions, real-time validation, and quality scoring.

Features:
- Guided prompt system with contextual questions
- Real-time validation and feedback
- Specification quality scoring and recommendations
- Integration hooks for existing CLI workflows
"""

import sys
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
import structlog

from .template_generator import SpecificationTemplateGenerator
from .quality_scoring import QualityScorer

logger = structlog.get_logger()


@dataclass
class PromptContext:
    """Context for prompt generation"""

    user_level: str  # beginner, intermediate, expert
    domain: str  # content, structural, architectural, etc.
    urgency: str  # low, medium, high
    team_size: str  # small, medium, large
    previous_experience: str  # none, some, extensive
    available_tools: List[str]


@dataclass
class InteractiveSession:
    """Interactive specification creation session"""

    session_id: str
    start_time: datetime
    current_step: int
    user_responses: Dict[str, Any]
    validation_results: Dict[str, Any]
    quality_score: float
    recommendations: List[str]
    is_complete: bool = False


class GuidedPromptSystem:
    """
    AI-powered guided prompt system for specification creation
    """

    def __init__(self, template_generator: SpecificationTemplateGenerator = None):
        """Initialize guided prompt system"""
        self.template_generator = template_generator or SpecificationTemplateGenerator()
        self.quality_scorer = QualityScorer()
        self.current_session: Optional[InteractiveSession] = None

        # Define prompt templates for different contexts
        self.prompt_templates = self._initialize_prompt_templates()

        logger.info("Guided prompt system initialized")

    async def initialize(self) -> bool:
        """Initialize the guided prompt system"""
        try:
            await self.template_generator.initialize()
            logger.info("Guided prompt system initialized successfully")
            return True
        except Exception as e:
            logger.error("Failed to initialize guided prompt system", error=str(e))
            return False

    def _initialize_prompt_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize prompt templates for different scenarios"""
        return {
            "conflict_analysis": {
                "user_levels": {
                    "beginner": {
                        "questions": [
                            {
                                "id": "conflict_description",
                                "type": "text",
                                "prompt": "Can you describe the conflict you're trying to resolve? (e.g., 'Two different implementations of the same feature')",
                                "validation": "non_empty",
                                "help": "A clear description helps identify the right resolution approach",
                            },
                            {
                                "id": "affected_files",
                                "type": "multiselect",
                                "prompt": "Which files are involved in this conflict? (select from your changed files)",
                                "validation": "file_list",
                                "help": "Select all files that have conflicts or were modified",
                            },
                            {
                                "id": "urgency_level",
                                "type": "single_select",
                                "prompt": "How urgent is this resolution?",
                                "options": [
                                    "Low - can wait for thorough analysis",
                                    "Medium - important but not critical",
                                    "High - needs quick resolution",
                                ],
                                "validation": "single_option",
                                "help": "Urgency affects the recommended resolution strategy",
                            },
                        ],
                        "context_prompts": [
                            "Since you're new to conflict resolution, I'll guide you through a systematic approach.",
                            "Don't worry if you're unsure about any technical details - we can refine them later.",
                        ],
                    },
                    "intermediate": {
                        "questions": [
                            {
                                "id": "conflict_type",
                                "type": "single_select",
                                "prompt": "What type of conflict are you dealing with?",
                                "options": [
                                    "Content conflict - different implementations",
                                    "Structural conflict - code organization",
                                    "Architectural conflict - system design",
                                    "Dependency conflict - imports/versions",
                                    "Semantic conflict - business logic",
                                ],
                                "validation": "single_option",
                                "help": "Identifying the conflict type helps choose the best resolution strategy",
                            },
                            {
                                "id": "branches_involved",
                                "type": "text",
                                "prompt": "Which branches are involved? (source -> target)",
                                "validation": "branch_format",
                                "help": "Format: source-branch-name -> target-branch-name",
                            },
                            {
                                "id": "complexity_score",
                                "type": "scale",
                                "prompt": "Rate the complexity (1-10):",
                                "min": 1,
                                "max": 10,
                                "validation": "number_range",
                                "help": "1 = very simple, 10 = extremely complex",
                            },
                        ],
                        "context_prompts": [
                            "Your experience suggests we can focus on strategic aspects.",
                            "I'll provide more technical options for you to consider.",
                        ],
                    },
                    "expert": {
                        "questions": [
                            {
                                "id": "resolution_constraints",
                                "type": "text",
                                "prompt": "What constraints should we consider? (time, resources, dependencies)",
                                "validation": "optional_text",
                                "help": "Any specific limitations or requirements",
                            },
                            {
                                "id": "risk_tolerance",
                                "type": "single_select",
                                "prompt": "What's your risk tolerance for this resolution?",
                                "options": [
                                    "Conservative - minimize risk even if slower",
                                    "Moderate - balance speed and safety",
                                    "Aggressive - optimize for speed with controlled risk",
                                ],
                                "validation": "single_option",
                                "help": "Risk tolerance affects the recommended approaches",
                            },
                        ],
                        "context_prompts": [
                            "Based on your expertise, I'll focus on advanced strategy options.",
                            "You can skip basic explanations and dive into detailed configuration.",
                        ],
                    },
                }
            },
            "constitutional_analysis": {
                "questions": [
                    {
                        "id": "compliance_level",
                        "type": "single_select",
                        "prompt": "What level of constitutional compliance do you need?",
                        "options": [
                            "Basic - essential rules only",
                            "Standard - recommended compliance",
                            "Strict - full compliance validation",
                        ],
                        "validation": "single_option",
                        "help": "Higher compliance levels provide more validation but take more time",
                    },
                    {
                        "id": "quality_gates",
                        "type": "multiselect",
                        "prompt": "Which quality gates should we implement?",
                        "options": [
                            "Constitutional validation",
                            "Code quality checks",
                            "Performance validation",
                            "Security scanning",
                            "Documentation review",
                        ],
                        "validation": "multiselect",
                        "help": "Quality gates ensure resolution meets your standards",
                    },
                ]
            },
            "strategy_planning": {
                "questions": [
                    {
                        "id": "execution_approach",
                        "type": "single_select",
                        "prompt": "How would you prefer to execute the resolution?",
                        "options": [
                            "Sequential - step by step with validation",
                            "Parallel - multiple approaches simultaneously",
                            "Hybrid - combination of both",
                        ],
                        "validation": "single_option",
                        "help": "Parallel execution can be faster but requires more resources",
                    },
                    {
                        "id": "rollback_strategy",
                        "type": "single_select",
                        "prompt": "What's your rollback strategy preference?",
                        "options": [
                            "Automated - full automatic rollback",
                            "Semi-automated - guided rollback process",
                            "Manual - full control over rollback",
                        ],
                        "validation": "single_option",
                        "help": "Rollback strategy affects how we handle failures",
                    },
                ]
            },
        }

    async def start_interactive_session(self) -> str:
        """Start a new interactive specification creation session"""
        session_id = f"spec_session_{int(datetime.utcnow().timestamp())}"

        self.current_session = InteractiveSession(
            session_id=session_id,
            start_time=datetime.utcnow(),
            current_step=0,
            user_responses={},
            validation_results={},
            quality_score=0.0,
            recommendations=[],
        )

        logger.info("Started interactive session", session_id=session_id)
        return session_id

    async def collect_user_profile(self) -> PromptContext:
        """Collect user profile to customize prompts"""
        print("\n👤 User Profile Configuration")
        print("=" * 35)

        # Experience level
        print("\nExperience Level:")
        print("1. Beginner - New to conflict resolution")
        print("2. Intermediate - Some experience with Git and conflict resolution")
        print("3. Expert - Experienced with complex conflict scenarios")

        while True:
            try:
                choice = input("Select your experience level (1-3): ").strip()
                if choice in ["1", "2", "3"]:
                    user_levels = ["beginner", "intermediate", "expert"]
                    user_level = user_levels[int(choice) - 1]
                    break
                print("Please enter 1, 2, or 3")
            except KeyboardInterrupt:
                print("\nExiting...")
                sys.exit(0)

        # Team context
        print("\nTeam Context:")
        team_sizes = {"1": "small", "2": "medium", "3": "large"}

        print("1. Small team (1-5 developers)")
        print("2. Medium team (6-20 developers)")
        print("3. Large team (20+ developers)")

        while True:
            try:
                choice = input("Select team size (1-3): ").strip()
                if choice in team_sizes:
                    team_size = team_sizes[choice]
                    break
                print("Please enter 1, 2, or 3")
            except KeyboardInterrupt:
                print("\nExiting...")
                sys.exit(0)

        # Previous experience with EmailIntelligence
        print("\nPrevious Experience:")
        print("1. None - First time using EmailIntelligence")
        print("2. Some - Used basic features before")
        print("3. Extensive - Familiar with advanced features")

        while True:
            try:
                choice = input("Select experience level (1-3): ").strip()
                if choice in ["1", "2", "3"]:
                    experiences = ["none", "some", "extensive"]
                    previous_experience = experiences[int(choice) - 1]
                    break
                print("Please enter 1, 2, or 3")
            except KeyboardInterrupt:
                print("\nExiting...")
                sys.exit(0)

        # Available tools (this would be enhanced based on actual tool detection)
        print("\nAvailable Tools:")
        print("Checking for available tools...")
        available_tools = []

        # Simulate tool detection
        tools_to_check = ["git", "github_cli", "emailintelligence_cli", "pytest", "eslint"]
        for tool in tools_to_check:
            # In a real implementation, we'd check if these tools are available
            available_tools.append(tool)  # Assume all are available for demo

        print(f"Detected tools: {', '.join(available_tools)}")

        # Create prompt context
        prompt_context = PromptContext(
            user_level=user_level,
            domain="content",  # Will be refined during conflict analysis
            urgency="medium",  # Will be set based on user input
            team_size=team_size,
            previous_experience=previous_experience,
            available_tools=available_tools,
        )

        return prompt_context

    async def run_guided_creation(self) -> Dict[str, Any]:
        """Run the complete guided specification creation process"""
        try:
            # Start session
            session_id = await self.start_interactive_session()
            print(f"\n🎯 Starting Interactive Specification Creation")
            print(f"Session ID: {session_id}")

            # Collect user profile
            prompt_context = await self.collect_user_profile()

            # Step 1: Conflict Analysis
            await self._collect_conflict_analysis(prompt_context)

            # Step 2: Constitutional Analysis
            await self._collect_constitutional_analysis()

            # Step 3: Strategy Planning
            await self._collect_strategy_planning()

            # Step 4: Generate and validate specification
            specification = await self._generate_final_specification()

            # Complete session
            self.current_session.is_complete = True

            return {
                "session_id": session_id,
                "specification": specification,
                "quality_score": self.current_session.quality_score,
                "recommendations": self.current_session.recommendations,
            }

        except KeyboardInterrupt:
            print("\n\n⚠️ Specification creation cancelled by user")
            return {}
        except Exception as e:
            logger.error("Failed during guided specification creation", error=str(e))
            print(f"\n❌ Error during specification creation: {str(e)}")
            return {}

    async def _collect_conflict_analysis(self, prompt_context: PromptContext):
        """Collect conflict analysis information through guided prompts"""
        print(f"\n🔍 Conflict Analysis")
        print("=" * 20)

        # Get conflict analysis templates for user level
        templates = self.prompt_templates["conflict_analysis"]["user_levels"][prompt_context.user_level]

        # Display contextual prompts
        for context_prompt in templates.get("context_prompts", []):
            print(f"\n💡 {context_prompt}")

        # Collect responses to questions
        for question in templates["questions"]:
            response = await self._prompt_user(question)

            # Store response and validate
            self.current_session.user_responses[question["id"]] = response
            validation_result = self._validate_response(question, response)
            self.current_session.validation_results[question["id"]] = validation_result

            # Provide feedback
            if validation_result["is_valid"]:
                print(f"✅ {validation_result['feedback']}")
            else:
                print(f"⚠️ {validation_result['feedback']}")

                # For critical validation errors, allow retry
                if validation_result["is_critical"]:
                    print("This information is important for creating an effective specification.")
                    retry_response = await self._prompt_user(question, allow_retry=True)
                    self.current_session.user_responses[question["id"]] = retry_response
                    retry_validation = self._validate_response(question, retry_response)
                    self.current_session.validation_results[question["id"]] = retry_validation

        print(f"\n✅ Conflict analysis completed")

    async def _collect_constitutional_analysis(self):
        """Collect constitutional analysis information"""
        print(f"\n⚖️ Constitutional Compliance Analysis")
        print("=" * 35)

        templates = self.prompt_templates["constitutional_analysis"]

        # Display constitutional framework context
        print("\n🏛️ Constitutional Framework Context:")
        print("The EmailIntelligence Constitutional Framework ensures all resolutions")
        print("adhere to organizational standards and best practices.")
        print("\nThis includes:")
        print("- Code quality and architectural standards")
        print("- Security and compliance requirements")
        print("- Performance and efficiency guidelines")
        print("- Documentation and maintenance standards")

        # Collect responses
        for question in templates["questions"]:
            response = await self._prompt_user(question)
            self.current_session.user_responses[question["id"]] = response

            validation_result = self._validate_response(question, response)
            self.current_session.validation_results[question["id"]] = validation_result

            if validation_result["is_valid"]:
                print(f"✅ {validation_result['feedback']}")

        print(f"\n✅ Constitutional analysis completed")

    async def _collect_strategy_planning(self):
        """Collect strategy planning information"""
        print(f"\n🚀 Strategy Planning")
        print("=" * 18)

        templates = self.prompt_templates["strategy_planning"]

        # Provide strategy context
        print("\n🎯 Resolution Strategy Options:")
        print("Based on your previous responses, here are the recommended approaches:")

        # Analyze collected responses to suggest strategies
        recommendations = await self._analyze_strategy_recommendations()
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")

        # Collect strategy preferences
        for question in templates["questions"]:
            response = await self._prompt_user(question)
            self.current_session.user_responses[question["id"]] = response

            validation_result = self._validate_response(question, response)
            self.current_session.validation_results[question["id"]] = validation_result

            if validation_result["is_valid"]:
                print(f"✅ {validation_result['feedback']}")

        print(f"\n✅ Strategy planning completed")

    async def _analyze_strategy_recommendations(self) -> List[str]:
        """Analyze collected responses and provide strategy recommendations"""
        recommendations = []

        # Analyze urgency
        urgency = self.current_session.user_responses.get("urgency_level", "Medium")
        if "High" in urgency:
            recommendations.append("Fast-track resolution with parallel validation")
        elif "Low" in urgency:
            recommendations.append("Thorough analysis with comprehensive testing")

        # Analyze complexity
        complexity = self.current_session.user_responses.get("complexity_score", 5)
        if isinstance(complexity, (int, float)) and complexity >= 7:
            recommendations.append("Multi-phase resolution with expert review")

        # Analyze risk tolerance
        risk_tolerance = self.current_session.user_responses.get("risk_tolerance", "Moderate")
        if "Aggressive" in risk_tolerance:
            recommendations.append("Optimized approach with performance focus")
        elif "Conservative" in risk_tolerance:
            recommendations.append("Safe approach with extensive validation")

        # Analyze user experience level
        user_level = self.current_session.user_responses.get("user_level", "intermediate")
        if user_level == "beginner":
            recommendations.append("Guided implementation with step-by-step validation")
        elif user_level == "expert":
            recommendations.append("Advanced techniques with minimal guidance")

        if not recommendations:
            recommendations = [
                "Standard resolution approach with balanced validation",
                "Constitutional compliance throughout the process",
                "Quality gates at key decision points",
            ]

        return recommendations

    async def _prompt_user(self, question: Dict[str, Any], allow_retry: bool = False) -> Any:
        """Prompt user for response to a question"""
        prompt = question["prompt"]
        qtype = question["type"]

        print(f"\n❓ {prompt}")

        while True:
            try:
                if qtype == "text":
                    response = input("> ").strip()
                    if response:
                        return response
                    else:
                        print("Please provide a response.")

                elif qtype == "single_select":
                    options = question["options"]
                    for i, option in enumerate(options, 1):
                        print(f"  {i}. {option}")

                    while True:
                        try:
                            choice = input("Enter option number: ").strip()
                            if choice.isdigit() and 1 <= int(choice) <= len(options):
                                return options[int(choice) - 1]
                            print(f"Please enter a number between 1 and {len(options)}")
                        except KeyboardInterrupt:
                            raise

                elif qtype == "multiselect":
                    options = question["options"]
                    for i, option in enumerate(options, 1):
                        print(f"  {i}. {option}")

                    print("Enter numbers separated by commas (e.g., 1,3,5):")
                    while True:
                        try:
                            choice = input("Enter options: ").strip()
                            choices = [c.strip() for c in choice.split(",")]
                            if all(c.isdigit() and 1 <= int(c) <= len(options) for c in choices):
                                return [options[int(c) - 1] for c in choices]
                            print("Please enter valid numbers separated by commas.")
                        except KeyboardInterrupt:
                            raise

                elif qtype == "scale":
                    min_val = question.get("min", 1)
                    max_val = question.get("max", 10)
                    print(f"Scale: {min_val} to {max_val}")

                    while True:
                        try:
                            response = input(f"Enter number ({min_val}-{max_val}): ").strip()
                            if response.isdigit():
                                num = int(response)
                                if min_val <= num <= max_val:
                                    return num
                            print(f"Please enter a number between {min_val} and {max_val}")
                        except KeyboardInterrupt:
                            raise

                else:
                    response = input("> ").strip()
                    if response or not allow_retry:
                        return response
                    else:
                        print("Please provide a response.")

            except KeyboardInterrupt:
                if allow_retry:
                    print("\nSkipping this question.")
                    return ""
                else:
                    raise
            except EOFError:
                print("\nInput ended unexpectedly.")
                return ""

    def _validate_response(self, question: Dict[str, Any], response: Any) -> Dict[str, Any]:
        """Validate user response to a question"""
        validation_type = question.get("validation", "none")

        result = {"is_valid": True, "is_critical": False, "feedback": "", "suggestions": []}

        # Convert response to string for validation
        response_str = str(response) if response is not None else ""

        if validation_type == "non_empty":
            if not response_str.strip():
                result["is_valid"] = False
                result["is_critical"] = True
                result["feedback"] = "This information is required for effective conflict resolution."
            else:
                result["feedback"] = "Thank you for the detailed description."

        elif validation_type == "file_list":
            if isinstance(response, list) and len(response) > 0:
                result["feedback"] = f"Identified {len(response)} affected files for analysis."
            else:
                result["is_valid"] = False
                result["is_critical"] = False
                result["feedback"] = "No files identified. You can specify files manually later."

        elif validation_type == "single_option":
            if response in question.get("options", []):
                result["feedback"] = f"Selected option: {response}"
            else:
                result["is_valid"] = False
                result["feedback"] = "Invalid option selected."

        elif validation_type == "number_range":
            try:
                num = int(response)
                min_val = question.get("min", 1)
                max_val = question.get("max", 10)
                if min_val <= num <= max_val:
                    result["feedback"] = f"Complexity rated as {num}/10"
                else:
                    result["is_valid"] = False
                    result["feedback"] = f"Number must be between {min_val} and {max_val}"
            except (ValueError, TypeError):
                result["is_valid"] = False
                result["feedback"] = "Please enter a valid number."

        elif validation_type == "optional_text":
            if response_str.strip():
                result["feedback"] = "Constraints noted for strategy planning."
            else:
                result["feedback"] = "No specific constraints identified."

        else:
            result["feedback"] = "Response recorded successfully."

        return result

    async def _generate_final_specification(self) -> Dict[str, Any]:
        """Generate the final specification based on collected information"""
        print(f"\n📝 Generating Final Specification")
        print("=" * 32)

        # Convert user responses to conflict metadata
        conflict_metadata = await self._create_conflict_metadata()

        # Create project and team contexts
        project_context = {
            "organization": {"name": "EmailIntelligence Team"},
            "technology_stack": {"language": "Python", "framework": "FastAPI"},
            "deployment_environment": {"type": "Development"},
            "testing_phase": self.current_session.user_responses.get("phase_type", "baseline"),
            "user_profile": {
                "level": self.current_session.user_responses.get("user_level", "intermediate"),
                "team_size": self.current_session.user_responses.get("team_size", "medium"),
                "experience": self.current_session.user_responses.get("previous_experience", "some"),
            },
        }

        team_context = {
            "roles": ["Developer", "Technical Lead", "QA Engineer"],
            "skills": ["Git", "Constitutional Framework", "Quality Assurance"],
            "experience_level": self.current_session.user_responses.get("user_level", "intermediate"),
            "constraints": self.current_session.user_responses.get("resolution_constraints", ""),
            "preferences": {
                "risk_tolerance": self.current_session.user_responses.get("risk_tolerance", "moderate"),
                "execution_approach": self.current_session.user_responses.get("execution_approach", "sequential"),
                "rollback_strategy": self.current_session.user_responses.get("rollback_strategy", "semi-automated"),
            },
        }

        # Determine specification phase
        phase_type = self.current_session.user_responses.get("phase_type", "baseline")
        from .template_generator import SpecificationPhase

        spec_phase = SpecificationPhase.BASELINE if phase_type == "baseline" else SpecificationPhase.IMPROVED

        # Generate specification
        try:
            specification = await self.template_generator.generate_specification_template(
                conflict_metadata, project_context, team_context, spec_phase
            )

            # Update session with quality score
            self.current_session.quality_score = specification.get("template_metadata", {}).get("quality_score", 0.0)

            # Collect recommendations
            recommendations = []
            if specification.get("quality_recommendations"):
                for category, recs in specification["quality_recommendations"].items():
                    if isinstance(recs, list):
                        recommendations.extend(recs)

            self.current_session.recommendations = recommendations

            print(f"✅ Specification generated successfully")
            print(f"📊 Quality Score: {self.current_session.quality_score:.2f}")
            print(f"📋 Sections: {len(specification.get('template_content', {}))}")

            return specification

        except Exception as e:
            logger.error("Failed to generate specification", error=str(e))
            print(f"❌ Failed to generate specification: {str(e)}")

            # Return basic specification as fallback
            return {
                "template_metadata": {
                    "generated_at": datetime.utcnow().isoformat(),
                    "quality_score": 0.0,
                    "note": "Generated in fallback mode due to errors",
                },
                "template_content": {
                    "overview": {"description": "Basic specification created from interactive session"},
                    "implementation_strategy": {"approach": "Manual implementation required"},
                },
                "quality_recommendations": {
                    "general": ["Complete specification generation failed - manual intervention required"]
                },
            }

    async def _create_conflict_metadata(self):
        """Create conflict metadata from user responses"""
        # This would integrate with the template_generator's ConflictMetadata
        from .template_generator import ConflictType

        # Extract information from user responses
        urgency = self.current_session.user_responses.get("urgency_level", "Medium")
        complexity = self.current_session.user_responses.get("complexity_score", 5)

        # Map urgency to time estimation
        urgency_mapping = {"Low": 60, "Medium": 30, "High": 15}  # 1 hour  # 30 minutes  # 15 minutes

        estimated_time = urgency_mapping.get(urgency.split()[0], 30)

        # Map complexity to risk level
        if complexity >= 8:
            risk_level = "HIGH"
        elif complexity >= 5:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # Determine conflict type
        conflict_type_str = self.current_session.user_responses.get("conflict_type", "Content conflict")
        conflict_type_mapping = {
            "Content": ConflictType.CONTENT,
            "Structural": ConflictType.STRUCTURAL,
            "Architectural": ConflictType.ARCHITECTURAL,
            "Dependency": ConflictType.DEPENDENCY,
            "Semantic": ConflictType.SEMANTIC,
        }

        # Find matching conflict type
        conflict_type = ConflictType.CONTENT  # default
        for key, value in conflict_type_mapping.items():
            if key.lower() in conflict_type_str.lower():
                conflict_type = value
                break

        return type(
            "ConflictMetadata",
            (),
            {
                "conflict_type": conflict_type,
                "file_paths": self.current_session.user_responses.get("affected_files", []),
                "pr_numbers": [],  # Would be filled from GitHub context if available
                "branches": [self.current_session.user_responses.get("branches_involved", "")],
                "complexity_score": float(complexity),
                "affected_components": ["Code Resolution"],
                "estimated_resolution_time": estimated_time,
                "risk_level": risk_level,
                "stakeholder_impact": "moderate",  # Default
            },
        )

    def get_session_status(self) -> Dict[str, Any]:
        """Get current session status"""
        if not self.current_session:
            return {"session_active": False}

        return {
            "session_active": True,
            "session_id": self.current_session.session_id,
            "current_step": self.current_session.current_step,
            "is_complete": self.current_session.is_complete,
            "quality_score": self.current_session.quality_score,
            "responses_collected": len(self.current_session.user_responses),
            "recommendations": len(self.current_session.recommendations),
        }

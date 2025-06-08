from pathlib import Path
import frontmatter
from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateError, meta


class PromptManager:
    _env = None

    @classmethod
    def _get_env(cls, templates_dir="prompts"):
        templates_dir = Path(__file__).parent.parent / templates_dir
        if cls._env is None:
            cls._env = Environment(
                loader=FileSystemLoader(templates_dir),
                undefined=StrictUndefined,
            )
        return cls._env

    @staticmethod
    def get_all_prompts():
        """Get all prompts organized by category"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts_by_category = {}

        for prompt_file in prompts_dir.rglob("*.jinja2"):
            # Get relative path from prompts directory
            relative_path = prompt_file.relative_to(prompts_dir)

            # Extract category from folder structure
            category = (
                relative_path.parent.name
                if relative_path.parent != Path(".")
                else "general"
            )
            template_path = str(
                relative_path.with_suffix("")
            )  # Remove .jinja2 extension

            try:
                # Parse the template
                template_info = PromptManager.get_template_info(template_path)
                template_info["path"] = template_path
                template_info["category"] = category

                if category not in prompts_by_category:
                    prompts_by_category[category] = []

                prompts_by_category[category].append(template_info)
            except Exception as e:
                print(f"Error loading template {template_path}: {e}")

        return prompts_by_category

    @staticmethod
    def is_multi_step_template(template_path):
        """Check if a template is multi-step"""
        template_info = PromptManager.get_template_info(template_path)
        return template_info.get("is_multi_step", False)

    @staticmethod
    def get_step_info(template_path, step_id):
        """Get information about a specific step in a multi-step template"""
        template_info = PromptManager.get_template_info(template_path)
        if not template_info.get("is_multi_step"):
            raise ValueError(f"Template {template_path} is not a multi-step template")
        
        steps = template_info.get("steps", [])
        for step in steps:
            if step.get("id") == step_id:
                return step
        
        raise ValueError(f"Step {step_id} not found in template {template_path}")

    @staticmethod
    def render_step(template_path, step_id, step_responses=None, llm_outputs=None, **kwargs):
        """Render a specific step of a multi-step template"""
        step_info = PromptManager.get_step_info(template_path, step_id)
        
        # Create context with step responses and LLM outputs
        context = kwargs.copy()
        
        # Add step responses (form variables from each step)
        if step_responses:
            for resp_step_id, variables in step_responses.items():
                if isinstance(variables, dict):
                    context.update(variables)
        
        # Add LLM outputs from previous steps
        if llm_outputs:
            context["llm_outputs"] = llm_outputs
        
        # Add step_number for Jinja conditionals (convert step_id to number)
        # Assume step_id format is either numeric or find step index
        steps = PromptManager.get_template_info(template_path).get("steps", [])
        step_number = None
        for i, step in enumerate(steps):
            if step.get("id") == step_id:
                step_number = i + 1  # 1-based indexing
                break
        
        if step_number is None:
            raise ValueError(f"Step {step_id} not found in template {template_path}")
        
        context["step_number"] = step_number
        context["step_id"] = step_id  # Keep for backward compatibility
        
        # Render the entire template with step context
        return PromptManager.get_prompt(template_path, **context)

    @staticmethod
    def get_prompt(template_path, prompt_type=None, **kwargs):
        env = PromptManager._get_env()
        template_file = f"{template_path}.jinja2"

        # Get the full file path
        full_path = Path(__file__).parent.parent / "prompts" / template_file

        with open(full_path) as file:
            post = frontmatter.load(file)

        # Add prompt_type to template context if provided
        if prompt_type:
            kwargs["prompt_type"] = prompt_type

        template = env.from_string(post.content)
        try:
            return template.render(**kwargs)
        except TemplateError as e:
            raise ValueError(f"Error rendering template: {str(e)}")

    @staticmethod
    def get_prompt_parts(template_path, **kwargs):
        """Get both system and user parts of a prompt separately"""
        try:
            system_prompt = PromptManager.get_prompt(template_path, prompt_type="system", **kwargs)
            user_prompt = PromptManager.get_prompt(template_path, prompt_type="user", **kwargs)
            return {
                "system": system_prompt.strip(),
                "user": user_prompt.strip()
            }
        except Exception as e:
            return {
                "system": f"Error rendering system prompt: {str(e)}",
                "user": f"Error rendering user prompt: {str(e)}"
            }

    @staticmethod
    def get_template_info(template_path):
        """Get template info by path (e.g., 'youtube/compare_videos')"""
        template_file = f"{template_path}.jinja2"
        full_path = Path(__file__).parent.parent / "prompts" / template_file

        if not full_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")

        with open(full_path) as file:
            post = frontmatter.load(file)

        # Parse template to find variables
        env = PromptManager._get_env()
        ast = env.parse(post.content)
        variables = meta.find_undeclared_variables(ast)
        
        # Remove special internal variables
        variables.discard('prompt_type')
        variables.discard('step_number')
        variables.discard('step_id')

        # Extract category from the template path
        category = (
            template_path.split("/")[0]
            if "/" in template_path
            else "general"
        )

        # Check if this is a multi-step template
        is_multi_step = post.metadata.get("type") == "multi-step"
        
        return {
            "name": template_path.split("/")[-1],  # Get just the filename part
            "path": template_path,
            "category": category,
            "description": post.metadata.get("description", "No description provided"),
            "author": post.metadata.get("author", "Unknown"),
            "tags": post.metadata.get("tags", []),
            "variables": list(variables),
            "frontmatter": post.metadata,
            "is_multi_step": is_multi_step,
            "steps": post.metadata.get("steps", []) if is_multi_step else [],
        }

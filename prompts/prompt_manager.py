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
    def get_prompt(template_path, **kwargs):
        env = PromptManager._get_env()
        template_file = f"{template_path}.jinja2"

        # Get the full file path
        full_path = Path(__file__).parent.parent / "prompts" / template_file

        with open(full_path) as file:
            post = frontmatter.load(file)

        template = env.from_string(post.content)
        try:
            return template.render(**kwargs)
        except TemplateError as e:
            raise ValueError(f"Error rendering template: {str(e)}")

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

        # Extract category from the template path
        category = (
            template_path.split("/")[0]
            if "/" in template_path
            else "general"
        )

        return {
            "name": template_path.split("/")[-1],  # Get just the filename part
            "path": template_path,
            "category": category,
            "description": post.metadata.get("description", "No description provided"),
            "author": post.metadata.get("author", "Unknown"),
            "tags": post.metadata.get("tags", []),
            "variables": list(variables),
            "frontmatter": post.metadata,
        }

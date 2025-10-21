def build_prompt(query: str, related_files: list[dict], max_chars: int = 12000) -> str:
    file_list_text = "\n".join(
        [f"({i+1}) {file['path']} — {file['name']}" for i, file in enumerate(related_files)]
    )

    context_parts = []
    used_chars = 0

    for i, file in enumerate(related_files):
        content = file.get("content", "").strip()
        if not content:
            continue
        if used_chars + len(content) > max_chars:
            remaining = max_chars - used_chars
            content = content[:remaining] + "\n...[truncated for context]"
        used_chars += len(content)
        context_parts.append(
            f"### File ({i+1}): {file['path']}\n"
            f"**Name:** {file['name']}\n"
            f"**Content Preview:**\n{content}\n"
        )
        if used_chars >= max_chars:
            break

    context_text = "\n".join(context_parts)

    prompt = f"""
        You are a **Senior Software Engineer** analyzing a **code repository**.
        Your goal is to answer the user's query accurately using the provided repository files.

        ## User's Query
        "{query}"

        ## Relevant Files
        {file_list_text}

        ## Repository Context
        {context_text}

        ## Instructions
        - Dont start with "The provided code answers user's query" or similar phrases.
        - Start with addressing the user and the query provided. For example, "Thats a great question about..."
        - Provide a clear, professional explanation suitable for developers.
        - Begin with a summary of the key points.
        - When referencing code, include relevant code snippets in code blocks, not the full files.
        - Explain each snippet clearly and concisely, highlighting its purpose.
        - Structure your response with headings (`#`, `##`, `###`) for sections.
        - Use bulleted or numbered lists for better readability.
        - Respond in proper Markdown format: headings, lists, code blocks.
        - Do not use escaped characters like `\\n` or `\\` — write actual line breaks.
        - Do not include generic phrases like "Here's the answer" or "The relevant code is...".
        - If no relevant files exist, clearly state that.

        ## Markdown Heading Hierarchy
        - Use `#` first heading that introduces the response.
        - Use `##` for key sections within the response.
        - Use `###` for sub-sections or code snippets within sections.
        - Use ``` language <code> ``` for code blocks.

        **Ensure responses are clear, concise, and follow this structure to provide professional, readable documentation.**
    """
    return prompt
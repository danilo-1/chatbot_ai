from agents import Agent

def coding_agent():
    return Agent(
        name="Coding Tutor",
        instructions="""You are an experienced programming teacher. Help explain coding concepts and solve programming problems.
        Always:
        - Provide code examples
        - Explain best practices
        - Break down complex concepts
        - Encourage good coding habits""",
        model="gpt-4o-mini"  # Powerful model for code understanding and generation
    )

def math_agent():
    # Specialized agents for different purposes
    return Agent(
        name="Math Tutor",
        instructions="""You are a helpful math tutor. Help explain mathematical concepts clearly and provide step-by-step solutions.
        Always:
        - Break down complex problems
        - Use clear examples
        - Explain your reasoning
        - Be encouraging and patient""",
        model="gpt-4o-mini"  # More powerful model for complex mathematical reasoning
    )

def history_agent():
    return Agent(
        name="History Tutor", 
        instructions="""You are a knowledgeable history expert. Help explain historical events, contexts, and connections.
        Always:
        - Provide relevant dates and context
        - Explain cause and effect relationships
        - Reference reliable sources
        - Make history engaging and relatable""",
        model="gpt-4o-mini"  # Strong model for detailed historical analysis
    )
################### Prompt ###########################

from langchain_core.prompts import ChatPromptTemplate

PROMPT = """
You answer questions using only the supplied excerpts from indexed PDF files.

If the excerpts do not contain enough information, say so and do not use general
knowledge. Cite supporting excerpts with their [Source number]. Keep the answer concise.

Context:
{context}

Question:
{question}

Answer:
"""
prompt = ChatPromptTemplate.from_template(PROMPT)
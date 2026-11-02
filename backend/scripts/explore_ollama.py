from app.services.ollama_client import OllamaClient
from app.core.subgenres import subgenres_for_prompt

SYSTEM_PROMPT = f"""You classify movies into horror subgenres.
Choose 0 to 5 slugs from the list below that clearly describe the movie.
Use keywords for help. If none fit, return an empty list. Never invent slugs.
Answer only with JSON: {{"subgenres": ["slug", ...]}}

Subgenres:
{subgenres_for_prompt()}
"""

client = OllamaClient()
print(client.chat(SYSTEM_PROMPT, "Title: Hope\nOverview: In the remote South Korean village of Hope Harbor, police chief Bum-seok and officer Sung-ae are called to investigate a mysterious creature wreaking havoc on the community. But all is not as it seems, and perceptions can be misleading. What begins as ignorance plants the seed of disaster, escalating through human conflict into a tragedy of cosmic proportions.\nKeywords: supernatural,horse,shootout,police officer,hunted,police shootout,remote village,aliens,20th century,horror,fight for survival,chasing,unknown entity,dinosaurs"))
client.close()
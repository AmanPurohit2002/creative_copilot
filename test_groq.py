import asyncio, os
from groq import AsyncGroq
import instructor
from pydantic import BaseModel

class Test(BaseModel):
    test: str

client = instructor.from_groq(AsyncGroq(api_key=os.environ['GROQ_API_KEY']), mode=instructor.Mode.JSON)

async def main():
    try:
        res = await client.chat.completions.create(
            model='llama3-8b-8192', 
            messages=[{'role': 'user', 'content': 'Say hello'}], 
            response_model=Test
        )
        print("Success:", res)
    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(main())

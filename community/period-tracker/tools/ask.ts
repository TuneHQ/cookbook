import OpenAI from "openai";

const ai_token = process.env.OPENAI_API_KEY?.trim();
const ai_baseurl = process.env.OPENAI_API_BASEURL?.trim();

export async function ask({
  model = "openai/gpt-4o-mini",
  prompt,
}: {
  model?: string;
  prompt: string;
}) {
  const openai = new OpenAI({
    apiKey: ai_token,
    baseURL: ai_baseurl,
  });

  const res = await openai.chat.completions.create({
    model,
    messages: [
      {
        role: "system",
        content: prompt,
      },
    ],
  });

  return res;
}

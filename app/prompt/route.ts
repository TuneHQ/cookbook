import constants from "../contants";
import { TuneAIStream } from "../utils";
import { StreamingTextResponse } from "ai";

export async function POST(req: Request) {
  const { prompt } = await req.json();
  const tuneResp = await TuneAIStream({
    messages: [
      {
        role: "user",
        content: prompt || "",
      },
    ],
    model: "rohan/tune-gpt4",
    stream: false,
    tools: constants.tools,
    temperature: 0.5,
    max_tokens: 600,
  });
  console.log("Tune Response", tuneResp);

  return new StreamingTextResponse(tuneResp);
}

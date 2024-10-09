import constants from "../constants";
import { TuneAIStream } from "../utils";
import { StreamingTextResponse } from "ai";

export async function POST(req: Request) {
  const { messages } = await req.json();
  const tuneResp = await TuneAIStream({
    messages: messages,
    model: process.env.STUDIO_MODEL || "",
    stream: false,
    tools: constants.tools,
    temperature: 0.5,
    max_tokens: 600,
  });
  console.log("Tune Response", tuneResp);

  return new StreamingTextResponse(tuneResp);
}

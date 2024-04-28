import constants from "../contants";
import { TuneAIStream } from "../utils";
import { StreamingTextResponse } from "ai";

export async function GET(req: Request) {
  const query = new URL(req.url).searchParams;
  const prompt = query.get("prompt");
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
    max_tokens: 400,
  });
  console.log("Tune Response", tuneResp);

  return new StreamingTextResponse(tuneResp);
}

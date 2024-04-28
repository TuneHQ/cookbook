import constants from "../contants";
import { TuneAIStream } from "../utils";
import { StreamingTextResponse } from "ai";

export async function GET(req: Request) {
  const tuneResp = await TuneAIStream({
    messages: [
      {
        role: "user",
        content: "10-day weather forecast for California",
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

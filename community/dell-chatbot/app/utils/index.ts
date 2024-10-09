import { laptopData } from "../constants/laptopData";
import { createParser } from "eventsource-parser";
import { VirtualConsole } from "jsdom";
import fetch from "node-fetch";

export const TuneAIStream = async ({
  messages,
  model,
  stream,
  max_tokens,
  stop,
  temperature,
  tools,
}: {
  stream: boolean;
  messages: {
    role: string;
    content: string;
  }[];
  model: string;
  max_tokens?: number;
  stop?: string[];
  temperature?: number;
  tools?: {
    type: string;
    function: {
      name: string;
      description: string;
      parameters: {
        type: string;
        properties: Record<string, any>;
        required: string[];
      };
    };
  }[];
}) => {
  const response = await fetch(`https://proxy.tune.app/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: process.env.TUNE_KEY || "",
    },
    body: JSON.stringify({
      messages: messages,
      model: model,
      stream: stream,
      stop,
      temperature,
      max_tokens: max_tokens,
      tools,
    }),
  });
  if (response.status !== 200) {
    throw new Error("Error: " + response.status);
  }
  if (!stream) {
    const json = (await response?.json()) as any;
    if (json?.choices?.[0]?.message?.tool_calls?.[0]?.function) {
      return streamFunction(
        json?.choices?.[0]?.message?.content,
        json?.choices?.[0]?.message?.tool_calls?.[0]?.function,
        messages?.at(-1)?.content || ""
      );
    } else {
      return streamText(json?.choices?.[0]?.message?.content || "");
    }
  }
  const encoder = new TextEncoder();
  const decoder = new TextDecoder();

  const streamResp = new ReadableStream({
    async start(controller) {
      const onParse: any = async (event: { type: string; data: any }) => {
        if (event.type === "event") {
          const data = event.data;
          if (data === "[DONE]") {
            controller.close();
            return;
          }
          try {
            const json = JSON.parse(data);
            if (json?.error?.code > 399 && json?.error?.message) {
              controller.error(json?.error?.message);
              return;
            }

            const text = json?.choices?.[0]?.delta?.content;
            const queue = encoder.encode(text);
            controller.enqueue(queue);
          } catch (e) {
            console.error(e);
            controller.error(e);
          }
        }
      };
      const parser = createParser(onParse);
      if (response?.body) {
        for await (const chunk of response?.body as any) {
          parser.feed(decoder.decode(chunk));
        }
      }
    },
  });
  return streamResp;
};

const streamFunction = async (
  content: string,
  tool_calls: {
    arguments: string;
    name: string;
  },
  user_query: string
) => {
  const stream = new ReadableStream({
    async start(controller) {
      if (content) {
        controller.enqueue(
          JSON.stringify({
            data: content,
            type: "function_thought",
          })
        );
        controller.enqueue("\n\n\n\n\n\n");
      }
      controller.enqueue(
        JSON.stringify({
          data: `Calling function ${tool_calls.name} with arguments (${
            Object.entries(JSON.parse(tool_calls.arguments))?.map(
              ([key, value]) => `${key} = ${value},`
            ) || ""
          })`,
          type: "function",
        })
      );
      controller.enqueue("\n\n\n\n\n\n");
      let functionResponse = "";

      if (tool_calls?.name === "listLaptops") {
        const args = JSON.parse(tool_calls.arguments);
        functionResponse = await listLaptops(args?.models);
      } else if (tool_calls?.name === "showLaptopPrice") {
        const args = JSON.parse(tool_calls.arguments);
        functionResponse = await showLaptopPrice(args?.model);
      }

      let finalResponse = ``;
      const stream = await TuneAIStream({
        messages: [
          {
            role: "user",
            content: `Use Below information to answer the question: 
            
            User query: ${user_query}

            Function Response:
            ${functionResponse}

            If function could not find any laptop matching the user query, reply with "I couldn’t find a laptop matching your specifications. Would you like to check other options?"
            `,
          },
        ],
        model: process.env.STUDIO_MODEL || "",
        stream: true,
        temperature: 0.5,
      });

      const reader = stream.getReader();
      const decoder = new TextDecoder();
      while (true && reader) {
        const { done, value } = await reader.read();
        if (done) {
          break;
        }

        const text = decoder.decode(value);

        controller.enqueue(JSON.stringify({ data: text, type: "text" }));
        finalResponse = finalResponse + text;
        controller.enqueue("\n\n\n\n\n\n");
      }
      controller.enqueue("\n\n\n\n\n\n");
      controller.enqueue(JSON.stringify({ data: finalResponse, type: "bye" }));

      controller.close();
    },
  });
  return stream;
};

const streamText = async (streamTxt: string) => {
  const stream = new ReadableStream({
    start(controller) {
      function pushData() {
        controller.enqueue(JSON.stringify({ data: streamTxt, type: "text" }));
        controller.close();
      }
      pushData();
    },
  });
  return stream;
};

async function listLaptops(models: string[]) {
  const filteredLaptops = laptopData.filter((laptop) =>
    models.includes(laptop.model)
  );

  if (filteredLaptops.length > 0) {
    return filteredLaptops
      .map(
        (laptop) =>
          `Model: ${laptop.model}, Screen Size: ${laptop.screenSize}", RAM: ${laptop.ram}GB, Storage: ${laptop.storage}`
      )
      .join("\n");
  } else {
    return "I couldn’t find any laptops matching the specified models. Would you like to check other models?";
  }
}

async function showLaptopPrice(model: string) {
  const laptop = laptopData.find((laptop) => laptop.model === model);

  if (laptop) {
    return `The price of ${model} is ₹${laptop.price}.`;
  } else {
    return "I couldn’t find the price for the specified laptop model. Would you like to check another model?";
  }
}

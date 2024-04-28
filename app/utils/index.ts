import { createParser } from "eventsource-parser";
import axios from "axios";
import { JSDOM, VirtualConsole } from "jsdom";

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
  console.log("Tune Stream Response Status", response.status);
  if (response.status !== 200) {
    // print the error
    console.log("Error", response);

    throw new Error("Error: " + response.status);
  }
  if (!stream) {
    const json = await response?.json();
    if (json?.choices?.[0]?.message?.tool_calls?.[0]?.function) {
      return streamFunction(
        json?.choices?.[0]?.message?.content,
        json?.choices?.[0]?.message?.tool_calls?.[0]?.function
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
            //choices is an array of objects. We want the first object in the array. delta is an object. content is a string
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
  }
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
        controller.enqueue("\n\n");
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
      controller.enqueue("\n\n");

      if (tool_calls?.name == "search_web") {
        await searchWeb(
          JSON.parse(tool_calls.arguments).query,
          controller
        ).then((data) => {
          controller.enqueue(JSON.stringify({ data, type: "text" }));
        });
      }
      controller.enqueue("\n\n");

      controller.enqueue(JSON.stringify({ data: "", type: "bye" }));

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

const searchWeb = async (
  query: string,
  controller?: ReadableStreamDefaultController
) => {
  let data = JSON.stringify({
    q: query,
  });

  let config = {
    method: "post",
    url: "https://google.serper.dev/search",
    headers: {
      "X-API-KEY": process.env.SERPER_KEY || "",
      "Content-Type": "application/json",
    },
    data: data,
  };

  return await axios(config)
    .then(async (response) => {
      let content = "";
      for (let i = 0; i < Math.min(response.data?.organic?.length, 3); i++) {
        controller?.enqueue?.(
          JSON.stringify({
            data: response.data?.organic?.[i]?.title,
            url: response.data?.organic?.[i]?.link,
            type: "crawling",
          })
        );
        controller?.enqueue?.("\n\n");
        const page = await crawlWeb(response.data?.organic?.[i]?.link);
        content = `Content found at [${response.data?.organic?.[i]?.title}](${response.data?.organic?.[i]?.link}) is ${page}\n\n`;
      }
      return content;
    })
    .catch(() => {
      return "Error in searching the web";
    });
};

const crawlWeb = async (url: string) => {
  let content = "";
  if (url.includes(".pdf")) return content;
  const controller = new AbortController();
  setTimeout(() => {
    console.log("Aborting fetch", url);
    controller.abort();
  }, 3000);

  const headers = {
    "Content-Type": "text/html",
    "User-Agent":
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ",
  };
  await fetch(url, { signal: controller.signal, headers: headers })
    .then((response) => response.text())
    .then((data) => {
      content = data;
    })
    .catch((err) => {
      console.log("Not able to fetch url using fetch", err);
    });

  const virtualConsole = new VirtualConsole();
  virtualConsole.on("error", () => {
    // No-op to skip console errors.
  });

  // put the html string into a DOM
  const dom = new JSDOM(content ?? "", {
    virtualConsole,
  });

  const body = dom.window.document.querySelector("body");
  if (!body) throw new Error("body of the webpage is null");

  removeTags(body);
  // recursively extract text content from the body and then remove newlines and multiple spaces
  content = (naiveInnerText(body) ?? "").replace(/ {2}|\r\n|\n|\r/gm, "");

  return content;
};

function removeTags(node: Node) {
  if (node.hasChildNodes()) {
    node.childNodes.forEach((childNode) => {
      if (node.nodeName === "SCRIPT" || node.nodeName === "STYLE") {
        node.removeChild(childNode);
      } else {
        removeTags(childNode);
      }
    });
  }
}

function naiveInnerText(node: any): string {
  const Node = node; // We need Node(DOM's Node) for the constants, but Node doesn't exist in the nodejs global space, and any Node instance references the constants through the prototype chain
  return [...node.childNodes]
    .map((childNode) => {
      switch (childNode.nodeType) {
        case Node.TEXT_NODE:
          return node.textContent;
        case Node.ELEMENT_NODE:
          return naiveInnerText(childNode);
        default:
          return "";
      }
    })
    .join("\n");
}

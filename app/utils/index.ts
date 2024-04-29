import { createParser } from "eventsource-parser";
import axios from "axios";
import { JSDOM, VirtualConsole } from "jsdom";
import llamaTokenizer from "llama-tokenizer-js";
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

      if (
        tool_calls?.name == "search_web" ||
        tool_calls?.name == "shop_online" ||
        tool_calls?.name == "get_news"
      ) {
        functionResponse = await searchWeb(
          JSON.parse(tool_calls.arguments).query,
          controller,
          tool_calls?.name == "shop_online"
            ? "shopping"
            : tool_calls?.name === "search_web"
            ? "search"
            : "news"
        ).then(async (data) => {
          return data;
        });
      } else if (tool_calls?.name == "summarize_given_url") {
        functionResponse = await crawlWeb(JSON.parse(tool_calls.arguments).url);
      } else {
        const image = await textToImage(user_query);
        const chunkSize = 10000; // define the maximum number of characters per chunk
        let offset = 0;

        while (offset < image.length) {
          if (offset == 0) {
            // Start tag for the first chunk
            controller.enqueue(
              JSON.stringify({
                data: `<img src="data:image/png;base64,${image.slice(
                  offset,
                  offset + chunkSize
                )}`,
                type: "image",
              })
            );
          } else {
            // Continuation of the image data for intermediate chunks
            controller.enqueue(
              JSON.stringify({
                data: image.slice(
                  offset,
                  Math.min(image.length, offset + chunkSize)
                ),
                type: "image",
              })
            );
          }

          offset += chunkSize;
          controller.enqueue("\n\n\n\n\n\n");
        }

        // End tag for the final chunk
        controller.enqueue(
          JSON.stringify({
            data: '"/>',
            type: "image",
          })
        );
        controller.enqueue("\n\n\n\n\n\n");
      }
      let finalResponse = ``;
      if (tool_calls?.name !== "generate_image_from_text") {
        const stream = await TuneAIStream({
          messages: [
            {
              role: "user",
              content: `Use Below information to answer the question: ${user_query}

            Function Response:
            ${functionResponse}
            `,
            },
          ],
          model: "rohan/tune-gpt4",
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
        controller.enqueue(
          JSON.stringify({ data: finalResponse, type: "bye" })
        );

        controller.close();
      }
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
  controller?: ReadableStreamDefaultController,
  type?: string
) => {
  console.log("Searching the web for", query);
  let data = JSON.stringify({
    q: query,
  });

  let config = {
    method: "post",
    url: `https://google.serper.dev/${type}`,
    headers: {
      "X-API-KEY": process.env.SERPER_KEY || "",
      "Content-Type": "application/json",
    },
    data: data,
  };

  return await axios(config)
    .then(async (response) => {
      let content = "";
      if (response.data?.knowledgeGraph) {
        content = JSON.stringify(response.data?.knowledgeGraph);
      } else if (response?.data?.answerBox) {
        content = JSON.stringify(response.data?.answerBox);
      } else if (
        response?.data?.organic?.length > 0 ||
        response?.data?.news?.length > 0
      ) {
        const respList = response?.data?.organic || response?.data?.news;
        for (let i = 0; i < Math.min(respList?.length, 3); i++) {
          controller?.enqueue?.(
            JSON.stringify({
              data: respList?.[i]?.title,
              url: respList?.[i]?.link,
              type: "crawling",
            })
          );
          controller?.enqueue?.("\n\n\n\n\n\n");
          const page = await crawlWeb(respList?.[i]?.link);
          controller?.enqueue?.(
            JSON.stringify({
              data: respList?.[i]?.title,
              url: respList?.[i]?.link,
              type: "crawled",
            })
          );
          controller?.enqueue?.("\n\n\n\n\n\n");
          const tempContent =
            content +
            `Content found at [${respList?.[i]?.title}](${
              respList?.[i]?.link
            }) is ${respList?.[i]?.snippet || ""} ${page}\n\n`;
          const inputTokens = llamaTokenizer.encode(tempContent)?.length;
          console.log("Input Tokens", inputTokens);
          if (inputTokens > 6400) {
            content =
              content +
              `Content found at [${respList?.[i]?.title}](${
                respList?.[i]?.link
              }) is ${respList?.[i]?.snippet || ""}\n\n`;
          } else content = tempContent;
        }
      } else if (response?.data?.shopping) {
        content = response?.data?.shopping?.map((item: any) => {
          return `Title: ${item.title || "N/A"}\nSource: ${
            item.source || "N/A"
          }\nPrice: ${item.price || "N/A"}\nDelivery: ${
            item.delivery || "N/A"
          }\nRating: ${item.rating || "N/A"}\nRating Count: ${
            item.ratingCount || "N/A"
          }\nOffers: ${item.offers || "N/A"}\nProduct ID: ${
            item.productId || "N/A"
          }\nPosition: ${item.position || "N/A"}\n\n\n\n\n\n`;
        });
      }
      return content;
    })
    .catch(() => {
      return "Error in searching the web";
    })
    .finally(() => {
      return "Searched the web";
    });
};

const crawlWeb = async (url: string) => {
  let content = "";
  if (url.includes(".pdf")) return content;
  const controller = new AbortController();
  setTimeout(() => {
    console.log("Aborting fetch", url);
    controller.abort();
  }, 600);

  const headers = {
    "Content-Type": "text/html",
    "User-Agent":
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ",
  };
  await fetch(url, {
    headers: headers,
    signal: controller.signal,
  })
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

async function textToImage(query: string) {
  const response = await fetch(
    `https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Authorization: `Bearer ${process.env.STABILITY_API_KEY}`,
      },
      body: JSON.stringify({
        text_prompts: [
          {
            text: query,
          },
        ],
        cfg_scale: 7,
        height: 320,
        width: 320,
        steps: 30,
        samples: 1,
      }),
    }
  );

  if (!response.ok) {
    throw new Error(`Non-200 response: ${await response.text()}`);
  }

  const responseJSON = (await response.json()) as any;
  if (responseJSON?.artifacts?.[0]) {
    return responseJSON?.artifacts?.[0]?.base64;
  }
}

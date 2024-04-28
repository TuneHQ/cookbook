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
  console.log("Using Tune Stream", { model });
  let ApiKey = process.env.DEV_NBX_KEY;

  const response = await fetch(`https://studio.tune.app/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: ApiKey || "",
    },
    body: JSON.stringify({
      messages: messages,
      model: model,
      stream: true,
      stop,
      temperature,
      max_tokens: max_tokens,
      tools,
    }),
  });
  console.log("Dev NBX Stream Response Status", response.status);
  if (response.status !== 200) {
    // print the error

    throw new Error("Error: " + response.status);
  }
  if (!stream) {
    const json = await response?.json();
    return json?.choices?.[0]?.message?.content || "";
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

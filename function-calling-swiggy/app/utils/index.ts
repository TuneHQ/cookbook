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

      if (tool_calls?.name === "get_swiggy_orders") {
        functionResponse = await getSwiggyOrders();
        console.log("Swiggy Orders", functionResponse);
      } else if (tool_calls?.name === "get_nearby_restaurants") {
        const args = JSON.parse(tool_calls.arguments);
        functionResponse = await getRestaurants(
          args?.latitude,
          args?.longitude
        );
      } else if (tool_calls?.name === "get_restaurant_menu") {
        const args = JSON.parse(tool_calls.arguments);
        functionResponse = await getRestaurantsMenu(args?.menu_url);
      }

      let finalResponse = ``;
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

async function getSwiggyOrders() {
  const response = (await fetch(
    "https://www.swiggy.com/dapi/order/all?order_id=",
    {
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
        Accept: "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        Referer: "https://www.swiggy.com/my-account",
        "Content-Type": "application/json",
        Cookie: `_session_tid=${process.env.SWIGGY_SESSION_ID}`,
      },
      method: "GET",
      compress: true,
    }
  ).then((response) => response.json())) as any;

  let orders = ``;

  response?.data?.orders?.map((order: any) => {
    orders =
      orders +
      `Order Id: ${order?.order_id} [important]
    Order Total: ${order?.order_total}
    Restaurant: ${order?.restaurant_name} [important]
    Total Items: ${order?.order_items?.length}
    Address: ${order?.delivery_address?.address}
    Coupon Discount: ${order?.coupon_discount}
    Coupon Applied: ${order?.coupon_applied}
    Order Date: ${new Date(order?.order_time).toLocaleString()}
    Ordered Items: ${order?.order_items
      ?.map(
        (val: any) => `${val?.quantity} x ${val?.name} - Rs ${val?.final_price}`
      )
      .join("\n")} [important]
    Delivery Partner: ${order?.delivery_boy?.name}
    Delivery Status: ${order?.order_delivery_status}
    \n---\n
    `;
  });
  return orders;
}

async function getRestaurants(lat: number, lon: number) {
  let restaurants = "";
  const response = (await fetch(
    `https://www.swiggy.com/dapi/restaurants/list/v5?lat=${lat}&lng=${lon}&is-seo-homepage-enabled=true&page_type=DESKTOP_WEB_LISTING`,
    {
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
        Accept: "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        Referer: "https://www.swiggy.com/my-account",
        "Content-Type": "application/json",
        Cookie: `_session_tid=${process.env.SWIGGY_SESSION_ID}`,
      },
      method: "GET",
      compress: true,
    }
  )
    .then((response) => response.json())
    .catch((err) => {
      console.log("Error in fetching restaurants", err);
    })) as any;

  response?.data?.cards?.map((val: any) => {
    if (val?.card?.card?.id) {
      val?.card?.card?.gridElements?.infoWithStyle?.restaurants?.map(
        (restaurant: any) => {
          restaurants =
            restaurants +
            `Restaurant Name: ${restaurant?.info?.name}
             Restaurant ID: <span id="restaurant_id" class="hidden">${restaurant?.info?.id}</span> [important]
             Rating: ${restaurant?.info?.avgRating}
             Restaurant Location: ${restaurant?.info?.areaName}
             Restaurant Parent ID: <span id="restaurant_id" class="hidden">${restaurant?.info?.parentId}</span> [important]
             Restaurant Menu URL: ${restaurant?.cta?.link} [important]
             \n---\n
             `;
        }
      );
    }
  });
  return restaurants;
}

async function getRestaurantsMenu(menu_url: string) {
  let menuText = "";
  const max = 20;
  let added = 0;
  try {
    const response = (await fetch(menu_url, {
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
        Accept: "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        Referer: "https://www.swiggy.com/my-account",
        "Content-Type": "application/json",
        Cookie: `_session_tid=${process.env.SWIGGY_SESSION_ID}`,
      },
      method: "GET",
      compress: true,
    })
      .then((response) => response.text())
      .catch((err) => {
        console.log("Error in fetching restaurants", err);
      })) as any;
    const virtualConsole = new VirtualConsole();
    virtualConsole.on("error", () => {
      // No-op to skip console errors.
    });
    // response have the html content of the restaurant page there is one variable name initial={some json} which have the menu of the restaurant fetch that and return
    const { menu } = JSON.parse(
      response
        ?.match(/___INITIAL_STATE__ = (.*);/)?.[1]
        ?.split(";   window.")?.[0]
    );
    menu?.pl?.data?.data?.cards?.map((val: any) => {
      if (val?.["@type"] === "cardGroup") {
        val?.cards?.map((card: any) => {
          if (
            card?.["@type"] ===
            "type.googleapis.com/swiggy.presentation.food.v2.ItemCategory"
          ) {
            card?.itemCards?.map((item: any) => {
              if (
                item?.card?.["@type"] ===
                  "type.googleapis.com/swiggy.presentation.food.v2.Dish" &&
                added < max
              ) {
                added++;
                menuText =
                  menuText +
                  `Dish Name: ${item?.card?.info?.name}
                Dish ID: ${item?.card?.info?.id} [important]
                Desh Description: ${item?.card?.info?.description}
                `;
              }
            });
          }
        });
      }
    });
    return menuText;
  } catch (e) {
    return `Error in fetching menu `;
  }
}
``;

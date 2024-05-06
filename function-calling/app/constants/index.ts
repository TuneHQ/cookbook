const constants = {
  tools: [
    {
      type: "function",
      function: {
        name: "search_web",
        description: "Search the web using a query.",
        parameters: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "The search query to use for searching the web.",
            },
          },
          required: ["query"],
        },
      },
    },
    {
      type: "function",
      function: {
        name: "get_news",
        description: "Retrieve news articles from the web.",
        parameters: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description:
                "The search query to use for retrieving news articles.",
            },
          },
          required: ["query"],
        },
      },
    },
    {
      type: "function",
      function: {
        name: "shop_online",
        description: "Find products for sale online.",
        parameters: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description:
                "The search query to use for finding products online.",
            },
          },
          required: ["query"],
        },
      },
    },
    {
      type: "function",
      function: {
        name: "summarize_given_url",
        description: "Summarize the content of a given URL.",
        parameters: {
          type: "object",
          properties: {
            url: {
              type: "string",
              description: "The URL to summarize the content of.",
            },
          },
          required: ["url"],
        },
      },
    },
    {
      type: "function",
      function: {
        name: "generate_image_from_text",
        description: "Generate an image from a given text.",
        parameters: {
          type: "object",
          properties: {
            text: {
              type: "string",
              description: "The text to generate an image from.",
            },
          },
          required: ["text"],
        },
      },
    },
  ],
};

export default constants;

const constants = {
  tools: [
    {
      type: "function",
      function: {
        name: "listLaptops",
        description:
          "Provide a list of Dell laptop model names based on user preferences such as screen size, RAM, and hard disk space.",
        parameters: {
          type: "object",
          properties: {
            models: {
              type: "array",
              description: "An array of specific Dell laptop model names.",
              items: {
                type: "string",
                description: "The model name of the Dell laptop.",
              },
            },
          },
          required: ["models"],
        },
      },
    },
    {
      type: "function",
      function: {
        name: "showLaptopPrice",
        description:
          "Show the price of a specific Dell laptop model in Indian Rupees.",
        parameters: {
          type: "object",
          properties: {
            model: {
              type: "string",
              description: "The model name of the Dell laptop.",
            },
          },
          required: ["model"],
        },
      },
    },
  ],
};

export default constants;

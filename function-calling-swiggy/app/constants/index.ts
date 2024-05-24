const constants = {
  tools: [
    {
      type: "function",
      function: {
        name: "get_swiggy_orders",
        description: "Get the recent food orders from Swiggy.",
        parameters: {
          type: "object",
          properties: {},
        },
      },
    },
    {
      type: "function",
      function: {
        name: "get_nearby_restaurants",
        description: "Get the nearby restaurants to a location.",
        parameters: {
          type: "object",
          properties: {
            latitude: {
              type: "number",
              description: "The latitude of the location.",
            },
            longitude: {
              type: "number",
              description: "The longitude of the location.",
            },
          },
        },
      },
    },
    {
      type: "function",
      function: {
        name: "get_restaurant_menu",
        description: "Get the nearby restaurants to a location.",
        parameters: {
          type: "object",
          properties: {
            menu_url: {
              type: "string",
              description: "The URL of the restaurant's menu.",
            },
          },
          required: ["menu_url"],
        },
      },
    },
  ],
};

export default constants;

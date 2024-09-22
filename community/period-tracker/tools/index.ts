import { Message } from "discord.js";
import type {
  RunnableToolFunction,
  RunnableToolFunctionWithParse,
} from "openai/lib/RunnableFunction.mjs";
import type { JSONSchema } from "openai/lib/jsonschema.mjs";
import { z, ZodSchema } from "zod";
import zodToJsonSchema from "zod-to-json-schema";
import { evaluate } from "mathjs";
import { getPeriodTools } from "./period";
import { discord_allowed_menstrual_users } from "../config";

// calculator function
const CalculatorParams = z.object({
  expression: z.string().describe("mathjs expression"),
});
type CalculatorParams = z.infer<typeof CalculatorParams>;
async function calculator({ expression }: CalculatorParams) {
  return { response: evaluate(expression) };
}

export function getTools(username: string, context_message: Message<boolean>) {
  const isPeriodUser = discord_allowed_menstrual_users.includes(context_message.author.id);

  let tools: RunnableToolFunction<any>[] = [
    zodFunction({
      function: calculator,
      schema: CalculatorParams,
      description: "This can be used to evaluate exact date time durations.",
    }),
  ];

  if (isPeriodUser) {
    const period_tools = getPeriodTools();
    tools = tools.concat(period_tools);
  }

  return tools;
}

export function zodFunction<T extends object>({
  function: fn,
  schema,
  description = "",
  name,
}: {
  function: (args: T) => Promise<object>;
  schema: ZodSchema<T>;
  description?: string;
  name?: string;
}): RunnableToolFunctionWithParse<T> {
  return {
    type: "function",
    function: {
      function: fn,
      name: name ?? fn.name,
      description: description,
      parameters: zodToJsonSchema(schema) as JSONSchema,
      parse(input: string): T {
        const obj = JSON.parse(input);
        return schema.parse(obj);
      },
    },
  };
}

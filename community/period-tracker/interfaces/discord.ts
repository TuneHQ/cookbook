import YAML from "yaml";
import {
  ActivityType,
  ChannelType,
  Client,
  GatewayIntentBits,
  Message,
  Partials,
} from "discord.js";
import OpenAI from "openai";
import { format } from "date-fns";
import { getTools, zodFunction } from "../tools";
import { createHash } from "crypto";
import { startPeriodJob } from "../tools/period";
import { z } from "zod";
import { ask } from "../tools/ask";
import {
  discord_allowed_menstrual_users,
  discord_chat_history_limit,
  discord_max_chat_messages,
  discord_system_logs_channel,
} from "../config";

export const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.DirectMessages,
  ],
  partials: [Partials.Channel],
});
client.on("ready", () => {
  console.log(`Logged in as ${client.user?.tag}!`);
  client.user?.setActivity("as Human", {
    type: Number(ActivityType.Playing),
  });
});

const ai_token = process.env.OPENAI_API_KEY?.trim();
const api_base = process.env.OPENAI_BASE_URL?.trim();

if (!api_base) {
  throw new Error("Missing OPENAI_BASE_URL");
}

let message_que: {
  status_message: Message<boolean>;
  abort_controller: AbortController;
  channel: string;
  running_tools?: boolean;
}[] = [];

function set_running_tools(channelId: string, state: boolean) {
  message_que = message_que.map((m) => {
    if (m.channel === channelId) {
      m.running_tools = state;
    }
    return m;
  });
}

let model = "openai/gpt-4o-mini";

const ChangeModelParam = z.object({
  model: z.string(z.enum(["openai/gpt-4o", "openai/gpt-4o-mini"])),
});

type ChangeModelParam = z.infer<typeof ChangeModelParam>;

export async function changeModel(param: ChangeModelParam) {
  model = param.model;
  return {
    response: `Model changed to ${model}`,
  };
}

client.on("messageCreate", async (message) => {
  if (message.author.bot && message.author.id === client.user?.id) return;

  if (
    !(
      message.channel.type === ChannelType.DM ||
      message.channel.type === ChannelType.GuildText
    )
  ) {
    return;
  }

  const isDm = message.channel?.type === ChannelType.DM;

  if (!isDm) return;

  if (["stop", "reset"].includes(message.content.toLowerCase())) {
    await message.channel.send("---setting this point as the start---");
    // clear maps
    const hashes = channel_id_hash_maps.get(message.channel.id) ?? [];
    hashes.forEach((hash) => {
      tools_call_map.delete(hash);
    });

    return;
  }

  const mque = message_que.find((m) => m.channel === message.channelId);
  if (mque) {
    if (!mque.running_tools) {
      mque.abort_controller.abort();
      mque.status_message.deletable && mque.status_message.delete();
      message_que = message_que.filter((m) => m.channel !== message.channelId);
    } else {
      return;
    }
  }

  const temp_messages = await message.channel.messages.fetch({ limit: 20 });
  const stop_message = temp_messages.find(
    (m) => m.content.toLowerCase() === "---setting this point as the start---",
  );

  // get last 10 messages from the channel
  const messages: OpenAI.ChatCompletionMessageParam[] = await Promise.all(
    (
      await message.channel.messages.fetch(
        stop_message
          ? { after: stop_message?.id }
          : { limit: discord_chat_history_limit },
      )
    )
      .reverse()
      .map(async (m) => {
        const file = m.attachments.map((a) => a.url);
        const embeds = m.embeds.map((e) => JSON.stringify(e)).join("\n");
        let content = m.content;

        const context_message = m.reference?.messageId
          ? await message.channel.messages.fetch(m.reference.messageId)
          : null;
        const context_file = m.attachments.map((a) => a.url);
        const context_embeds = m.embeds
          .map((e) => JSON.stringify(e))
          .join("\n");

        const context_as_json = JSON.stringify({
          embeds: embeds || undefined,
          file: file || undefined,
          user_message: content,
          created_at: format(m.createdAt, "yyyy-MM-dd HH:mm:ss") + " IST",
          context_message: context_message
            ? {
              author: context_message?.author.username,
              created_at:
                format(context_message.createdAt, "yyyy-MM-dd HH:mm:ss") +
                " IST",
              content: context_message?.content,
            }
            : undefined,
          context_file: context_file || undefined,
          context_embeds: context_embeds || undefined,
        });

        return {
          role: m.author.id === client.user?.id ? "assistant" : "user",
          content: context_as_json,
          name:
            m.author.id === client.user?.id
              ? undefined
              : m.author.username.replaceAll(".", "_").trim(),
        };
      }),
  );

  let toolsmessages: OpenAI.ChatCompletionMessageParam[] = [];
  let skipNext = false;
  messages.forEach((m) => {
    if (skipNext && m.role === "assistant") {
      skipNext = false;
      return;
    }
    const hash = generateHash(m.content?.toString() ?? "");
    const calls = tools_call_map.get(hash);
    if (calls) {
      toolsmessages.push(m);
      toolsmessages = toolsmessages.concat(calls);
      console.log("calls", calls);
      console.log("updated toolsmessages", toolsmessages);
    } else {
      toolsmessages.push(m);
    }
  });

  const admin_system_messages: OpenAI.ChatCompletionSystemMessageParam[] = [
    {
      role: "system",
      content: `Your name is PTracker

  You track and manage a user's 

  Interaction Guidelines:
  - Focused Responses: Address user queries directly, avoiding unnecessary information.
  - Brevity: Keep responses concise and to the point.

  When you see context given inside the JSON of a message, it means that the message is a reply to the mentioned context.

  Always reply in plain text or markdown unless running a tool.
  Make sure not to exceed 1500 characters in a single message.
  You can send messages in multiple parts by breaking them down into smaller messages using multiple send message tool calls.
  Use the "send message" tool to send long links or download links to the user.

  ${isDm ? `The current user's name is ${message.author.displayName}` : ""}
  `,
    },
  ];

  const menstural_tracker_system_messages: OpenAI.ChatCompletionSystemMessageParam[] =
    [
      {
        role: "system",
        content: `This is a private conversation between you and the user ${[
          message.author.username,
        ]}.

        You need to help them track and manage their menstrual cycle.
        Answer their queries and provide them with the necessary information.
        Point out any irregularities in their cycle and suggest possible causes, but DO NOT DIAGNOSE.

        Current Date: ${format(new Date(), "yyyy-MM-dd HH:mm:ss")} IST
        `,
      },
    ];

  let final_system_messages =
    admin_system_messages as OpenAI.ChatCompletionMessageParam[];

  if (discord_allowed_menstrual_users.includes(message.author.id)) {
    final_system_messages = final_system_messages.concat(
      menstural_tracker_system_messages,
    );
  }

  final_system_messages = final_system_messages.concat(admin_system_messages);

  if (toolsmessages.length > discord_chat_history_limit) {
    let lastten = toolsmessages.slice(
      toolsmessages.length - discord_max_chat_messages,
    );
    let firstten = toolsmessages.slice(0, discord_max_chat_messages);
    console.log("Summerizing messages");
    message.channel.sendTyping();
    const waitMessage = await message.channel.send("Focusing...");
    const summary = await ask({
      model: "openai/gpt-4o-mini",
      prompt: `Summarize the below conversation into 2 sections:
      1. General info about the conversation
      2. Tools used in the conversation and their data in relation to the conversation.
      
      Conversation:
      ----
      ${YAML.stringify(firstten)}
      ----

      Notes:
      - Keep only important information and points, remove anything repetitive.
      - Keep tools information if they are relevant.
      - The summary is to give context about the conversation that was happening previously.
      `,
    });
    waitMessage.deletable && (await waitMessage.delete());
    console.log("Summary:", summary.choices[0].message.content?.slice(0, 100));
    toolsmessages = [
      {
        role: "system",
        content: `Previous messages summarized:
      ${summary.choices[0].message.content}
      `,
      } as OpenAI.ChatCompletionMessageParam,
    ].concat(lastten);
  }
  let final_messages = final_system_messages.concat(toolsmessages);

  const reply = await message.channel.send({
    content: "thinking...",
  });

  const abort_controller = new AbortController();

  message_que.push({
    status_message: reply,
    abort_controller,
    channel: message.channelId,
  });

  let done = false;
  setTimeout(() => {
    abort_controller.abort();
    !done && (reply.deletable ? reply.delete() : reply.edit("Timed out"));
    message_que = message_que.filter((m) => m.channel !== message.channelId);
  }, 600000);

  const openai = new OpenAI({
    apiKey: ai_token,
    baseURL: api_base,
  });

  const hash = generateHash(
    final_messages[final_messages.length - 1].content?.toString() ?? "",
  );

  const old_hashs = channel_id_hash_maps.get(message.channel.id) ?? [];
  channel_id_hash_maps.set(message.channel.id, [...old_hashs, hash]);

  const tool_calls: Array<
    | OpenAI.ChatCompletionAssistantMessageParam
    | OpenAI.ChatCompletionToolMessageParam
  > = [];

  console.log("final_messages", final_messages);

  const runner = openai.beta.chat.completions
    .runTools(
      {
        model,
        temperature: 0.6,
        user: message.author.username,
        messages: final_messages,
        stream: true,
        tools: [
          ...getTools(message.author.username, message),
          zodFunction({
            name: "changeModel",
            schema: ChangeModelParam,
            function: changeModel,
            description: `You have the ability to change the model between "openai/gpt-4oa" and "openai/gpt-4o-mini".
            The current model is ${model}

            "openai/gpt-4o" is a larger model and is more accurate but slower. (expensive)
            "openai/gpt-4o-mini" is a smaller model and is faster but less accurate. (cheaper)

            Switching between models can be useful when you need faster responses or more accurate responses.

            You can also switch to the cheaper model when there are a lot of messages to deal with.

            Try to keep the model as "openai/gpt-4o-mini" to save cost unless you need the extra accuracy.
            `,
          }),
        ],
      },
      { signal: abort_controller.signal },
    )
    .on("functionCall", async (fnc) => {
      console.log("calling: ", fnc);

      set_running_tools(message.channelId, true);

      await reply.edit(`running ${fnc.name}(${fnc.arguments.slice(20)})...`);
    })
    .on("finalContent", (content) => {
      console.log("replied: ", content);
    })
    .on("error", (err) => {
      console.log("error: ", err);
      reply.edit("Error: " + JSON.stringify(err));
      message_que = message_que.filter((m) => m.channel !== message.channelId);
      done = true;
    })
    .on("abort", () => {
      console.log("aborted");
    })
    .on("message", (m) => {
      console.log(m);
      message.channel.sendTyping();
      if (m.role === "assistant" && m.tool_calls?.length) {
        tool_calls.push(m);
      }
      if (m.role === "tool" && m.tool_call_id) {
        tool_calls.push(m);
      }
    });

  const final = await runner.finalContent();

  tools_call_map.set(hash, tool_calls);

  try {
    reply.deletable && reply.delete();
  } catch (error) {
    console.log("failed to delete a status message");
  }

  if (final && !final.includes("<NOREPLY>")) {
    const content = isJsonParseable(final);
    if (content.user_message) {
      await message.channel.send(content.user_message);
    }
    if (content === false) {
      await message.channel.send(final);
    }
    message_que = message_que.filter((m) => m.channel !== message.channelId);
  }
  done = true;
});

function isJsonParseable(str: string) {
  try {
    return JSON.parse(str);
  } catch (e) {
    return false;
  }
}

function generateHash(input: string): string {
  const hash = createHash("sha256");
  hash.update(input);
  return hash.digest("hex");
}

const tools_call_map = new Map<
  string,
  (
    | OpenAI.ChatCompletionAssistantMessageParam
    | OpenAI.ChatCompletionToolMessageParam
  )[]
>();

const channel_id_hash_maps = new Map<string, string[]>();

export function startDiscord() {
  client.login(process.env.DISCORD_BOT_TOKEN).then(() => {
    startPeriodJob();
    send_system_log("ptracker is online");
  });
}

export function send_message_to_user(
  user_id: string,
  content: string,
  embeds?: any,
  files?: any,
) {
  client.users.fetch(user_id).then((user) => {
    user.send({ content, embeds, files });
  });
}

export function send_system_log(content: string) {
  client.channels.fetch(discord_system_logs_channel).then((channel) => {
    if (channel?.type !== ChannelType.GuildText) {
      return;
    }
    channel.send(content);
  });
}

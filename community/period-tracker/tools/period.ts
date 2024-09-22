import { Database } from "bun:sqlite";
import type { RunnableToolFunction } from "openai/lib/RunnableFunction.mjs";
import { z } from "zod";
import { ask } from "./ask";

import cron from "node-cron";
import { zodFunction } from ".";
import {
  discord_allowed_menstrual_users,
  discord_reminder_cron,
} from "../config";
import { send_message_to_user, send_system_log } from "../interfaces/discord";

// pupulate example data function
export function populateExampleData() {
  db.query("DELETE FROM period_cycles").run();
  db.query("DELETE FROM period_entries").run();
}

export function clearprdandtestdb() {
  if (db) db.close();
  const prddb = usePrdDb();
  const testdb = useTestDb();
  prddb.query("DELETE FROM period_cycles").run();
  prddb.query("DELETE FROM period_entries").run();

  testdb.query("DELETE FROM period_cycles").run();
  testdb.query("DELETE FROM period_entries").run();
}

// util functions for managing menstrual cycle

const PeriodCycleSchema = z.object({
  id: z.string(),
  startDate: z.string(),
  endDate: z.string(),
  description: z.string(),
  ended: z.boolean(),
});

const PeriodEntrySchema = z.object({
  id: z.string(),
  date: z.string(),
  description: z.string(),
});

export type PeriodCycleType = z.infer<typeof PeriodCycleSchema>;
export type PeriodEntryType = z.infer<typeof PeriodEntrySchema>;

let db = usePrdDb();

function usePrdDb() {
  const db_url = "period.db";
  const db = new Database(db_url, { create: true });
  // setup the tables, create if not existing and auto migrate if any change in schema
  db.exec("PRAGMA journal_mode = WAL;");
  db.query(
    `CREATE TABLE IF NOT EXISTS period_cycles (
        id TEXT PRIMARY KEY,
        startDate TEXT NOT NULL,
        endDate TEXT NOT NULL,
        description TEXT NOT NULL,
        ended BOOLEAN NOT NULL
        )`,
  ).run();

  db.query(
    `CREATE TABLE IF NOT EXISTS period_entries (
        id TEXT PRIMARY KEY,
        date TEXT NOT NULL,
        description TEXT NOT NULL
        )`,
  ).run();
  return db;
}

function useTestDb() {
  const db_url = "test_period.db";
  const db = new Database(db_url, { create: true });
  // setup the tables, create if not existing and auto migrate if any change in schema
  db.exec("PRAGMA journal_mode = WAL;");
  db.query(
    `CREATE TABLE IF NOT EXISTS period_cycles (
            id TEXT PRIMARY KEY,
            startDate TEXT NOT NULL,
            endDate TEXT NOT NULL,
            description TEXT NOT NULL,
            ended BOOLEAN NOT NULL
            )`,
  ).run();

  db.query(
    `CREATE TABLE IF NOT EXISTS period_entries (
            id TEXT PRIMARY KEY,
            date TEXT NOT NULL,
            description TEXT NOT NULL
            )`,
  ).run();
  return db;
}

export function getPeriodCycles() {
  const cycles = db.query("SELECT * FROM period_cycles").all();
  return cycles as PeriodCycleType[];
}

// get period cycles for a given month
export function getPeriodCyclesByMonth(month_index: number, year: number) {
  const startDate = new Date(year, month_index, 1).toISOString();
  const endDate = new Date(year, month_index + 1, 1).toISOString();
  const cycles = db
    .query(
      "SELECT * FROM period_cycles WHERE startDate >= $startDate AND startDate < $endDate",
    )
    .all({
      $startDate: startDate,
      $endDate: endDate,
    });
  return cycles as PeriodCycleType[];
}

export function getPeriodCycleByDateRange(startDate: Date, endDate: Date) {
  const cycles = db
    .query(
      "SELECT * FROM period_cycles WHERE startDate >= $startDate AND startDate < $endDate",
    )
    .all({
      $startDate: startDate.toISOString(),
      $endDate: endDate.toISOString(),
    });
  return cycles as PeriodCycleType[];
}

export function createPeriodCycle(
  startDate: Date,
  endDate: Date,
  ended?: boolean,
) {
  db.query(
    `INSERT INTO period_cycles (id, startDate, endDate, description, ended) VALUES
            ($id, $startDate, $endDate, $description, $ended)`,
  ).run({
    $id: Math.random().toString(36).substring(2, 15),
    $startDate: startDate.toISOString(),
    $endDate: endDate.toISOString(),
    $description: `Started on ${startDate.toISOString()}`,
    $ended: ended ? 1 : 0,
  });
}

export function getAverageCycleLength() {
  const cycles = getPeriodCycles();
  const totalLength = cycles.reduce((acc, cycle) => {
    const startDate = new Date(cycle.startDate);
    const endDate = new Date(cycle.endDate);
    return acc + (endDate.getTime() - startDate.getTime()) / 86400000;
  }, 0);
  return totalLength / cycles.length;
}

export function updateEndDatePeriodCycle(id: string, endDate: Date) {
  db.query("UPDATE period_cycles SET endDate = $endDate WHERE id = $id").run({
    $id: id,
    $endDate: endDate.toISOString(),
  });
}

export function updateDiscriptionPeriodCycle(id: string, discription: string) {
  db.query(
    "UPDATE period_cycles SET description = $description WHERE id = $id",
  ).run({
    $id: id,
    $description: discription,
  });
}

export function endPeriodCycle(id: string, discription?: string) {
  db.query("UPDATE period_cycles SET ended = 1 WHERE id = $id").run({
    $id: id,
  });
  updateEndDatePeriodCycle(id, new Date());
  if (discription) {
    updateDiscriptionPeriodCycle(id, discription);
  }
}

export function getOngoingPeriodCycle() {
  const cycle = db.query("SELECT * FROM period_cycles WHERE ended = 0").get();
  return cycle as PeriodCycleType;
}

export function getPeriodEntries() {
  const entries = db.query("SELECT * FROM period_entries").get();
  return entries as PeriodEntryType[];
}

export function getLatestPeriodEntry() {
  const entry = db
    .query("SELECT * FROM period_entries ORDER BY date DESC")
    .get();
  return entry as PeriodEntryType;
}

export function getPeriodEntriesByDateRange(startDate: Date, endDate: Date) {
  const entries = db
    .query(
      "SELECT * FROM period_entries WHERE date >= $startDate AND date < $endDate",
    )
    .all({
      $startDate: startDate.toISOString(),
      $endDate: endDate.toISOString(),
    });
  return entries as PeriodEntryType[];
}

export function getPeriodEntryByDate(date: Date) {
  const entry = db
    .query("SELECT * FROM period_entries WHERE date = $date")
    .get({ $date: date.toISOString() });
  return entry as PeriodEntryType;
}

export function updatePeriodEntryByDate(date: Date, description: string) {
  db.query(
    "UPDATE period_entries SET description = $description WHERE date = $date",
  ).run({
    $date: date.toISOString(),
    $description: description,
  });
}

export function createPeriodEntry(date: Date, description: string) {
  db.query(
    `INSERT INTO period_entries (id, date, description) VALUES
            ($id, $date, $description)`,
  ).run({
    $id: Math.random().toString(36).substring(2, 15),
    $date: date.toISOString(),
    $description: description,
  });
}

// open ai tools to manage the cycles

// create cycle tool
export const CreatePeriodCycleParams = z.object({
  startDate: z
    .string()
    .describe("Date of the start of the period cycle in ISO string format IST"),
  endDate: z
    .string()
    .describe(
      "The esimated end date of the period cycle, ask user how long does their period usually last and use that data to calculate this. This has to be in ISO string format IST",
    ),
});

export type CreatePeriodCycleParamsType = z.infer<
  typeof CreatePeriodCycleParams
>;

export async function startNewPeriodCycle({
  startDate,
  endDate,
}: CreatePeriodCycleParamsType) {
  if (!startDate || !endDate) {
    return { error: "startDate and endDate are required" };
  }

  // check if there is an ongoing cycle
  const ongoing = getOngoingPeriodCycle();
  if (ongoing) {
    return {
      error: "There is already an ongoing cycle",
      ongoingCycle: ongoing,
    };
  }

  createPeriodCycle(new Date(startDate), new Date(endDate));
  return { message: "Started a new period cycle" };
}

// create old period cycle tool
export const CreateOldPeriodCycleParams = z.object({
  startDate: z
    .string()
    .describe("Date of the start of the period cycle in ISO string format IST"),
  endDate: z
    .string()
    .describe(
      "When did this cycle end. This has to be in ISO string format IST",
    ),
});

export type CreateOldPeriodCycleParamsType = z.infer<
  typeof CreateOldPeriodCycleParams
>;

export async function createOldPeriodCycle({
  startDate,
  endDate,
}: CreateOldPeriodCycleParamsType) {
  if (!startDate || !endDate) {
    return { error: "startDate and endDate are required" };
  }

  createPeriodCycle(new Date(startDate), new Date(endDate), true);
  return { message: "Started a new period cycle" };
}

// create entry tool
export const CreatePeriodEntryParams = z.object({
  date: z
    .string()
    .describe(
      "Specify a date & time to add a past entry, no need to specify for a new entry",
    )
    .default(new Date().toISOString())
    .optional(),
  description: z
    .string()
    .describe("description of the vibe the user felt on the day"),
});

export type CreatePeriodEntryParamsType = z.infer<
  typeof CreatePeriodEntryParams
>;

export async function addOrUpdatePeriodEntryTool({
  date,
  description,
}: CreatePeriodEntryParamsType) {
  date = date || new Date().toISOString();

  try {
    const cycles = getPeriodCycleByDateRange(
      new Date(new Date().setFullYear(new Date().getFullYear() - 1)),
      new Date(),
    );
    if (cycles.length === 0) {
      return {
        error:
          "You cannot update or add to a cycle that's more than a year old",
      };
    }

    const cycle = cycles.find(
      (cycle) =>
        new Date(date) >= new Date(cycle.startDate) &&
        new Date(date) <= new Date(cycle.endDate),
    );

    if (!cycle) {
      return {
        error:
          "The specified date does not seem to be part of any existing cycle. Please check the date and or start a new cycle from this date and try again.",
      };
    }

    createPeriodEntry(new Date(date), description);
    return {
      message: "Added a new entry",
    };
  } catch (error) {
    return {
      error: "An error occurred while processing the request",
    };
  }
}

// end cycle tool

export const EndPeriodCycleParams = z.object({
  description: z
    .string()
    .describe("How did the user feel during this cycle on average"),
});

export type EndPeriodCycleParamsType = z.infer<typeof EndPeriodCycleParams>;

export async function endPeriodCycleTool({
  description,
}: EndPeriodCycleParamsType) {
  const ongoingCycle = getOngoingPeriodCycle();
  const id = ongoingCycle ? ongoingCycle.id : null;

  if (!id) {
    return { error: "There is no ongoing cycle" };
  }

  endPeriodCycle(id, description);
  return { message: "Ended the period cycle" };
}

// get current cycle tool
export const GetCurrentPeriodCycleParams = z.object({});

export type GetCurrentPeriodCycleParamsType = z.infer<
  typeof GetCurrentPeriodCycleParams
>;

export async function getCurrentPeriodCycleTool() {
  try {
    const cycle = getOngoingPeriodCycle();

    console.log(cycle);

    // days since period started
    const noOfDaysSinceStart = Math.floor(
      (new Date().getTime() - new Date(cycle.startDate).getTime()) / 86400000,
    );

    const averageCycleLength = getAverageCycleLength();

    let note =
      averageCycleLength > 5
        ? noOfDaysSinceStart > averageCycleLength
          ? "Cycle is overdue"
          : ""
        : undefined;

    if (cycle.ended) {
      note =
        "There are no ongoing cycles. this is just the last cycle that ended.";
    }

    if (!cycle.ended) {
      const endDate = new Date(cycle.endDate);
      if (endDate < new Date()) {
        note = "Cycle is overdue, or you forgot to end the cycle.";
      }
    }

    const response = {
      cycle,
      todaysDate: new Date().toISOString(),
      noOfDaysSinceStart: cycle.ended ? undefined : noOfDaysSinceStart,
      averageCycleLength,
      note,
    };

    return response;
  } catch (error) {
    return {
      error: "No ongoing cycle",
    };
  }
}

// get entries in a date range tool
export const GetPeriodEntriesParams = z.object({
  startDate: z.string().describe("Start date in ISO string format IST"),
  endDate: z.string().describe("End date in ISO string format IST"),
});

export type GetPeriodEntriesParamsType = z.infer<typeof GetPeriodEntriesParams>;

export async function getPeriodEntriesTool({
  startDate,
  endDate,
}: GetPeriodEntriesParamsType) {
  const entries = getPeriodEntriesByDateRange(
    new Date(startDate),
    new Date(endDate),
  );
  return entries;
}

// get vibe by date range tool
export const GetVibeByDateRangeParams = z.object({
  startDate: z.string().describe("Start date in ISO string format IST"),
  endDate: z.string().describe("End date in ISO string format IST"),
});

export type GetVibeByDateRangeParamsType = z.infer<
  typeof GetVibeByDateRangeParams
>;

export async function getVibeByDateRangeTool({
  startDate,
  endDate,
}: GetVibeByDateRangeParamsType) {
  const entries = getPeriodEntriesByDateRange(
    new Date(startDate),
    new Date(endDate),
  );

  ask({
    prompt: `Give me the general summary from the below entries that are a part of a period cycle:
    ----
    [${entries.map((entry) => entry.description).join("\n")}]
    ----

    the above are entries from ${startDate} to ${endDate}
    you need to give a general short summary of how the user felt during this period.
    `,
  });

  return entries;
}

// get cycle by date range tool
export const GetPeriodCycleByDateRangeParams = z.object({
  startDate: z.string().describe("Start date in ISO string format IST"),
  endDate: z.string().describe("End date in ISO string format IST"),
});

export type GetPeriodCycleByDateRangeParamsType = z.infer<
  typeof GetPeriodCycleByDateRangeParams
>;

export async function getPeriodCycleByDateRangeTool({
  startDate,
  endDate,
}: GetPeriodCycleByDateRangeParamsType) {
  const cycles = getPeriodCycleByDateRange(
    new Date(startDate),
    new Date(endDate),
  );
  return cycles;
}

// get latest period entry tool
export const GetLatestPeriodEntryParams = z.object({});
export type GetLatestPeriodEntryParamsType = z.infer<
  typeof GetLatestPeriodEntryParams
>;

export async function getLatestPeriodEntryTool() {
  const entry = getLatestPeriodEntry();
  return entry;
}

export function getPeriodTools(): RunnableToolFunction<any>[] {
  db.close();
  db = usePrdDb();

  return [
    zodFunction({
      function: startNewPeriodCycle,
      name: "startNewPeriodCycle",
      schema: CreatePeriodCycleParams,
      description: `Start a new period cycle.
      You can specify the start date, end date.
      You need to ask how the user is feeling and make a period entry about this.
      `,
    }),
    zodFunction({
      function: createOldPeriodCycle,
      name: "createOldPeriodCycle",
      schema: CreateOldPeriodCycleParams,
      description: `Create a period cycle that has already ended.
        if the user wants to add entries of older period cycles, you can create a cycle that has already ended.
        ask the user for the start date and end date of the cycle in natural language.
        `,
    }),
    zodFunction({
      function: addOrUpdatePeriodEntryTool,
      name: "addOrUpdatePeriodEntry",
      schema: CreatePeriodEntryParams,
      description: `Add or update a period entry. If the entry for the date already exists, it will be updated.`,
    }),
    zodFunction({
      function: endPeriodCycleTool,
      name: "endPeriodCycle",
      schema: EndPeriodCycleParams,
      description: `End ongoing period cycle. make sure to confirm with the user before ending the cycle.
      Ask the user if their cycle needs to be ended if its been more than 7 days since the start date of the cycle.`,
    }),
    zodFunction({
      function: getCurrentPeriodCycleTool,
      name: "getCurrentPeriodCycle",
      schema: GetCurrentPeriodCycleParams,
      description: `Get the ongoing period cycle.
      This returns the ongoing period cycle, the number of days since the cycle started & the average cycle length.
      `,
    }),
    zodFunction({
      function: getPeriodEntriesTool,
      name: "getPeriodEntriesByDateRange",
      schema: GetPeriodEntriesParams,
      description: "Get period entries in a date range",
    }),
    zodFunction({
      function: getPeriodCycleByDateRangeTool,
      name: "getPeriodCycleByDateRange",
      schema: GetPeriodCycleByDateRangeParams,
      description: "Get period cycles in a date range",
    }),
    zodFunction({
      function: getLatestPeriodEntryTool,
      name: "getLatestPeriodEntry",
      schema: GetLatestPeriodEntryParams,
      description: "Get the latest period entry",
    }),
    zodFunction({
      function: getVibeByDateRangeTool,
      name: "getVibeByDateRange",
      schema: GetVibeByDateRangeParams,
      description: `Get the general vibe of the user in a date range.
        This will ask the user to give a general summary of how they felt during this period.
        `,
    }),
  ];
}

// cron job that checks if there is an ongoing cycle and does a console.log if there is no period entry in the last 4 hours
var jobStarted = false;
export function startPeriodJob() {
  const timezone = "Asia/Kolkata";
  cron.schedule(
    discord_reminder_cron ?? "0 */4 * * *",
    async () => {
      console.log("Checking for period entries in the last 2 hours");
      send_system_log("Running job");

      const cycle = getOngoingPeriodCycle();
      console.log("cycle", cycle);

      if (!cycle) {
        return;
      }

      const entry = getLatestPeriodEntry();
      console.log("entry", entry);

      const isOldEntry =
        new Date(entry.date) < new Date(new Date().getTime() - 14400000);

      if (isOldEntry) {
        console.log("No period entry in the last 2 hours");
        discord_allowed_menstrual_users.forEach(async (user) => {
          const message_for_user = await ask({
            prompt: `Generate a message to remind the user to make a period entry.

        Ask user how they are feelig about their period cycle and as its been a while since they updated how they felt.
        Do not exlplicitly ask them to make an entry, just ask them how they are feeling about their period.
        
        todays date: ${new Date().toISOString()}

        ongoing cycle: ${JSON.stringify(cycle)}
        
        Note: if the end date is in the past then ask the user if the cycle is still going on or is it ok to end the cycle.

        last entry: ${JSON.stringify(entry)}`,
          });
          if (message_for_user.choices[0].message.content) {
            send_message_to_user(
              user,
              message_for_user.choices[0].message.content,
            );
          } else {
            console.log("No message generated");
          }
        });
      }
    },
    {
      timezone,
      recoverMissedExecutions: true,
      runOnInit: true,
    },
  );
  jobStarted = true;
}

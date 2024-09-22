# Period Tracker

Period Tracker is a Discord bot designed to help anyone track their menstrual cycle in greater detail and more observability for specific events.
Try the bot out by [adding it](https://discord.com/oauth2/authorize?client_id=1287253133105430548&permissions=563347237972992&integration_type=0&scope=bot) to any server and sending a DM to the bot.

## Table of Contents

- [Features](#features)
- [Configuration](#configuration)
- [Commands](#commands)
- [Data Architecture](#data-architecture)
- [Development Setup](#development-setup)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Cycle Management**: Start, end, and manage menstrual cycles with ease.
- **Daily Entries**: Log daily entries to track mood, symptoms, and other relevant information.
- **Automated Reminders**: Receive periodic reminders to log entries, ensuring consistent tracking.
- **Data Validation**: Robust schema validation ensures data integrity and consistency.
- **Tune Integration**: Utilize AI-powered summaries and intelligent prompts to enhance user interactions.

## Configuration

Configure secretes by `mv sample.en .env.local`.
Customize the bot's behavior by updating the `config.ts` file. Below is a sample configuration:

```typescript
export const allowed_menstrual_users = ["509004765380739107"]; // User IDs authorized to interact with the bot via DM
export const system_logs_channel = "1177561269780361248"; // Channel ID for system and usage logs
export const discord_chat_history_limit = 50; // Total number of messages to process
export const discord_max_chat_messages = 10; // Number of latest messages to exclude from summarization (the rest will be summarized for context)
export const discord_reminder_cron = "0 */4 * * *"; // Cron schedule for sending periodic reminders
```

### Configuration Parameters

- **allowed_menstrual_users**: An array of Discord user IDs permitted to interact with the bot via direct messages.
- **system_logs_channel**: The Discord channel ID where system and usage logs will be posted.
- **discord_chat_history_limit**: Defines the total number of messages the bot will process from chat history.
- **discord_max_chat_messages**: Specifies the number of recent messages that will not be summarized, providing context without redundancy.
- **discord_reminder_cron**: Cron expression determining the schedule for sending periodic reminders to users.

## Commands

Period Tracker supports the following commands:

- **`stop` / `reset`**: Resets the starting point of the chat messages context, allowing users to clear previous interactions and start fresh.

## Data Architecture

Simple data management to allow for even smaller llms to understand.

### 1. Database Setup

#### **SQLite with Bun:sqlite**

- **Database Instances**:
  - **Production Database**: `period.db`
  - **Test Database**: `test_period.db`

#### **Database Initialization**

- **Journal Mode**: Configured to `WAL` (Write-Ahead Logging) to improve concurrency and performance.
- **Table Creation**: On initialization, the database ensures the existence of necessary tables (`period_cycles` and `period_entries`), creating them if they do not already exist.

### 2. Database Schema

#### **Tables**

1. **`period_cycles`**

   | Column        | Type    | Constraints | Description                                     |
   | ------------- | ------- | ----------- | ----------------------------------------------- |
   | `id`          | TEXT    | PRIMARY KEY | Unique identifier for each period cycle.        |
   | `startDate`   | TEXT    | NOT NULL    | ISO string representing the cycle's start date. |
   | `endDate`     | TEXT    | NOT NULL    | ISO string representing the cycle's end date.   |
   | `description` | TEXT    | NOT NULL    | Description or notes about the cycle.           |
   | `ended`       | BOOLEAN | NOT NULL    | Indicates whether the cycle has ended.          |

2. **`period_entries`**

   | Column        | Type | Constraints | Description                                   |
   | ------------- | ---- | ----------- | --------------------------------------------- |
   | `id`          | TEXT | PRIMARY KEY | Unique identifier for each period entry.      |
   | `date`        | TEXT | NOT NULL    | ISO string representing the entry date.       |
   | `description` | TEXT | NOT NULL    | Description of the user's feelings or events. |

#### **Schema Validation with Zod**

- **Purpose**: Ensures data integrity and type safety across the application.
- **Schemas Defined**:
  - `PeriodCycleSchema`
  - `PeriodEntrySchema`
  - Additional schemas for tool parameters (e.g., `CreatePeriodCycleParams`, `CreatePeriodEntryParams`, etc.)

### 3. Data Access Layer

#### **Database Access Functions**

- **Connection Management**:

  - **`usePrdDb()`**: Connects to the production database (`period.db`).
  - **`useTestDb()`**: Connects to the test database (`test_period.db`).

- **CRUD Operations for Period Cycles**:

  - **Create**: `createPeriodCycle()`, `createOldPeriodCycle()`
  - **Read**: `getPeriodCycles()`, `getPeriodCyclesByMonth()`, `getPeriodCycleByDateRange()`, `getOngoingPeriodCycle()`, `getCurrentPeriodCycleTool()`
  - **Update**: `updateEndDatePeriodCycle()`, `updateDescriptionPeriodCycle()`, `endPeriodCycle()`
  - **Delete**: `clearprdandtestdb()`, `populateExampleData()`

- **CRUD Operations for Period Entries**:
  - **Create**: `createPeriodEntry()`
  - **Read**: `getPeriodEntries()`, `getLatestPeriodEntry()`, `getPeriodEntriesByDateRange()`, `getPeriodEntryByDate()`
  - **Update**: `updatePeriodEntryByDate()`
  - **Delete**: _(Not explicitly defined, but can be implemented similarly)_

### 4. Model Tools

#### **Runnable Tools**

- **Purpose**: Facilitate interactions between the application and OpenAI's models to manage period data intelligently.
- **Tools Defined**:

  - `startNewPeriodCycle`
  - `createOldPeriodCycle`
  - `addOrUpdatePeriodEntryTool`
  - `endPeriodCycleTool`
  - `getCurrentPeriodCycleTool`
  - `getPeriodEntriesTool`
  - `getPeriodCycleByDateRangeTool`
  - `getLatestPeriodEntryTool`
  - `getVibeByDateRangeTool`

- **Functionality**:
  - **Creating and Managing Cycles**: Tools to start, create old cycles, and end cycles with user interactions.
  - **Managing Entries**: Add or update period entries based on user input.
  - **Retrieving Data**: Fetch current cycles, entries within date ranges, latest entries, and summarize user vibes.

#### **Schema Definitions for Tools**

- **Zod Schemas**: Each tool has an associated Zod schema defining the expected input parameters, ensuring that the data passed to the tools adheres to the required structure.

### 5. Cron Jobs

#### **Automated Period Entry Checks**

- **Library Used**: `node-cron`
- **Purpose**: Periodically checks for recent period entries and sends reminders if no entry has been made within the last 4 hours.
- **Configuration**:

  - **Cron Schedule**: Defined in `discord_reminder_cron` (default: every 4 hours).
  - **Timezone**: Set to `Asia/Kolkata`.

- **Job Workflow**:
  1. **Check Ongoing Cycle**: Determines if there is an active period cycle.
  2. **Validate Latest Entry**: Verifies if the latest period entry is older than 4 hours.
  3. **Send Reminders**: For users in `discord_allowed_menstrual_users`, generates and sends a reminder message using OpenAI to encourage logging a new period entry.
  4. **Logging**: Records job execution details and any actions taken for monitoring purposes.

### 6. Data Flow Overview

1. **User Interaction**:

   - Users interact with the system via Discord or other interfaces, providing information about their menstrual cycles and daily entries.

2. **Data Validation**:

   - Incoming data is validated against defined Zod schemas to ensure correctness and consistency.

3. **Database Operations**:

   - Validated data is stored, updated, or retrieved from the SQLite databases (`period.db` for production and `test_period.db` for testing).

4. **OpenAI Processing**:

   - Certain operations leverage OpenAI's capabilities to generate summaries, reminders, and intelligent prompts based on user data.

5. **Automated Monitoring**:
   - Cron jobs run at scheduled intervals to monitor data activity and prompt users as needed, ensuring timely and accurate data logging.

---

## Development Setup

To set up the development environment, follow the steps below:

### Prerequisites

- **Bun**: Ensure you have [Bun](https://bun.sh) installed. This project was created using `bun init` in Bun v1.1.8.

### Installation

To install dependencies:

```bash
bun install
```

To run:

```bash
bun run index.ts
```

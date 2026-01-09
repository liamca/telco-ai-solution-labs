
# MCP Service Ticketing Server (Telecommunications AI Agent Demo)

## Overview

This repository contains a **Model Context Protocol (MCP) server prototype** that exposes service ticketing functionality as tools for AI agents.  
The solution demonstrates how a telecommunications company can extend an AI agent powered by **Retrieval Augmented Generation (RAG)** to interact directly with a service ticketing system using **natural‑language tool calls**.

The goal is to enable customer service representatives to **search issues, retrieve ticket details, and create new service tickets conversationally**, without switching between multiple systems.

## Business Problem

Customer service representatives today must continuously toggle between:

- AI knowledge assistants (documentation, FAQs, RAG systems)
- Service ticketing platforms
- Internal troubleshooting guides and RCA documents

This **context switching** leads to:
- Reduced agent productivity  
- Increased average handle time (AHT)  
- Inconsistent customer experiences

## Solution

Build an **MCP (Model Context Protocol) server** that exposes service ticketing functionality as structured tools.

AI agents can invoke these tools via natural language to:
- Find similar past issues and Root Cause Analyses (RCAs)
- Retrieve full ticket details
- Create new service tickets in real time  

All interactions happen **within the conversation**, keeping representatives fully engaged with the customer.

## Target Users

- **Tier 1 / Tier 2 support representatives** handling inbound calls and chats  
- **Technical support agents** diagnosing and resolving service issues  
- **Field technician coordinators** managing ticket routing and assignments

## Value Proposition

- **Faster Resolution**  
  Access historical tickets and RCAs instantly  
- **Reduced Handle Time**  
  Eliminate system switching and manual searching  
- **Improved First‑Call Resolution**  
  Reuse proven solutions for similar issues  
- **Better Customer Experience**  
  Agents stay focused on the customer conversation

## Scope & Requirements

The MCP server prototype exposes **three core tools** that implement service ticketing functionality.

## Tool 1: Search Similar Tickets

### Purpose
Enable semantic search across historical service tickets to find similar problems and associated RCAs.

### Functionality
- Accept a natural‑language problem description
- Perform a simulated semantic similarity search  
  - Vector embeddings  
  - Cosine similarity
- Return the **top matching tickets** (default: 5)
- Include detailed RCA information

### Input Parameters
- `searchQuery` — Natural‑language problem description  
- `topK` — Number of results to return  

### Output
Array of ticket objects with:
- Ticket ID  
- Problem description  
- Category  
- Severity  
- Similarity score  
- RCA details  
  - Root cause  
  - Fix applied  
  - Preventive measures  
  - Customers affected  
  - Resolution timeframe  
- Resolution timestamp

## Tool 2: Retrieve Ticket Details

### Purpose
Fetch complete information for a specific service ticket using its unique identifier.

### Functionality
- Accept a ticket ID
- Return the full ticket record including:
  - Customer information
  - Problem details
  - Status and priority
  - Timeline and SLA metrics
  - Technician assignments and notes
  - Resolution and verification details
  - Attachments metadata

### Input Parameters
- `ticketId` — Unique ticket identifier  

### Output
Single ticket object with nested sections:
- Customer  
- Timestamps  
- Technicians  
- Notes  
- Resolution  

### Error Handling
- Ticket not found

## Tool 3: Create Service Ticket

### Purpose
Generate a new service ticket from customer and problem information provided conversationally.

### Functionality
- Accept customer identity and problem details
- Generate a unique ticket ID
- Automatically:
  - Categorize the issue
  - Assign priority via keyword analysis
  - Calculate SLA deadlines
  - Route ticket to the appropriate technician group
- Return the complete created ticket
- Simulate customer notification/confirmation

### Input Parameters
- `customerName` — Full name  
- `customerPhone` — Contact phone number  
- `customerEmail` — Email address  
- `accountNumber` — Customer account identifier  
- `serviceAddress` — Service location  
- `shortDescription` — Problem summary  
- `category` — Issue category  
- `priority` — Ticket priority  

### Output
Created ticket object including:
- Generated ticket ID  
- Ticket number  
- SLA commitment  
- Customer confirmation message

## Technical Requirements

### Implementation
- Tools implemented as **standalone modules**
- Functions can be written in any one of the languages below:
  - Python  
  - Node.js  
  - Java  
  - C#  
- One primary exported function per tool
- Helper functions remain internal within the module
- Data exchanged strictly in **JSON format**

### Mock Data Specifications

- 5+ diverse ticket scenarios
- Telecommunications‑specific issues:
  - Connectivity
  - Equipment failures
  - Billing issues
  - Voice services
- Authentic ticket status lifecycle progression:
  - Created → Assigned → In Progress → Resolved → Closed
- Realistic technician notes and troubleshooting workflows
- Accurate timestamps and resolution timeframes

### Data Structures

**Customer**
- ID  
- Name  
- Phone  
- Email  
- Account number  
- Service address  
- Service type  

**Ticket**
- Status  
- Priority  
- Category  
- Timestamps  
- Technician assignments  
- Notes  

**RCA**
- Root cause  
- Fix applied  
- Preventive measures  
- Affected systems  

**Technician**
- ID  
- Name  
- Role  
- Contact information  
- Assignment date  

### Modularity & Architecture

- One file per MCP tool with clear exports
- No external dependencies
- Ready for integration with **Microsoft Foundry**
- Mock data designed to be easily replaceable with real APIs

**Functional Flow**

```text
Agent (LLM)
   ↓
MCP Client
   ↓
MCP Server (Ticketing Tools)
   ↓
Mock Data / Future Ticketing API
```

## Success Criteria

Attendee prototypes will be validated against the following criteria.

### Functional Completeness

#### 🔍 Search Tool
- ✅ Accepts search query string as input  
- ✅ Implements similarity calculation mechanism  
- ✅ Returns ranked results with RCA information  
- ✅ Handles edge cases (empty results, invalid input)  

#### 🧾 Retrieve Tool
- ✅ Accepts ticket ID and retrieves corresponding ticket  
- ✅ Returns comprehensive ticket structure with all required fields  
- ✅ Includes technician notes array with timestamps  
- ✅ Handles ticket-not-found scenario gracefully  

#### 🆕 Create Tool
- ✅ Validates required input parameters  
- ✅ Generates unique ticket ID  
- ✅ Implements auto-categorization logic  
- ✅ Implements priority determination logic  
- ✅ Returns complete created ticket object with confirmation message  

---

### Data Quality & Realism

#### 🧪 Mock Data Authenticity
- ✅ Minimum 5 diverse ticket scenarios covering different Telco issue types  
- ✅ Realistic technician notes reflecting actual troubleshooting progression  
- ✅ Appropriate timestamp sequences showing logical workflow progression  
- ✅ Accurate SLA metrics aligned with industry standards  

#### 🧩 RCA Quality
- ✅ Root causes are specific and technically plausible  
- ✅ Fixes/resolutions are detailed and actionable  
- ✅ Preventive measures demonstrate systematic thinking  

---

### Code Quality & Architecture

#### 🧱 Modularity
- ✅ Each function implemented in a separate file with clear exports  
- ✅ No cross-dependencies between modules  
- ✅ Helper functions properly scoped and named  

#### 📖 Code Readability
- ✅ Clear function and variable naming  
- ✅ Comments documenting parameters and return types  
- ✅ Consistent formatting and structure  

#### ⚠️ Error Handling
- ✅ Input validation with meaningful error messages  
- ✅ Graceful handling of edge cases  

---

### Demonstration & Integration Readiness

#### 🔁 End-to-End Flow
- ✅ Successfully demonstrate creating a ticket  
- ✅ Successfully demonstrate retrieving the created ticket  
- ✅ Successfully demonstrate searching for similar issues (~ tickets)  

#### 🔌 Integration Preparedness
- ✅ Functions can be easily wrapped as MCP tools  
- ✅ Mock data clearly separated and replacable with API calls

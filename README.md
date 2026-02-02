# 🚚 Delivery AI Agent

A sophisticated conversational AI assistant designed to handle delivery-related queries and order tracking using **ElevenLabs Conversational AI**. This agent allows customers to check their order status, estimated delivery times, and potential delays through natural voice interaction.

---

## ✨ Features

- **Voice-First Interaction:** Powered by ElevenLabs for natural, low-latency conversational experiences.
- **Smart Order Tracking:** Real-time retrieval of order details including:
  - Order validation (`get_order`)
  - Preparation status and carrier info (`preparing`)
  - Shipping updates and delivery estimates (`shipped`)
  - Final delivery confirmation (`delivered`)
  - Delay notification and status (`latency_status`)
- **Extensible Architecture:** Easily register new tools and callbacks to integrate with any backend or database.

## 🛠️ Tech Stack

- **Language:** Python 3.12+
- **AI Framework:** [ElevenLabs Conversational AI](https://elevenlabs.io/docs/conversational-ai)
- **Package Manager:** [uv](https://github.com/astral-sh/uv)
- **Environment Management:** `python-dotenv`

---

## 🚀 Getting Started

### Prerequisites

1.  **ElevenLabs API Key:** Get it from your [ElevenLabs Dashboard](https://elevenlabs.io).
2.  **Agent ID:** Create a Conversational AI agent in the ElevenLabs dashboard and copy its ID.
3.  **Python 3.12+** and **uv** installed.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mrhonneynive/delivery-ai-agent.git
   cd delivery-ai-agent
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

### Configuration

Create a `.env` file in the root directory and add your credentials:

```env
ELEVENLABS_API_KEY=your_api_key_here
AGENT_ID=your_agent_id_here
```

---

## 💻 Usage

To start the AI agent, simply run:

```bash
uv run main.py
```

Once running, you can speak to the assistant. Try testing with these sample Order IDs:
- `12345`: On-time delivery sample.
- `67890`: Delayed delivery sample.

### Key Commands (Interactions)
- *"Where is my order?"*
- *"When will my package arrive?"*
- *"Is there any delay on order 67890?"*

---

## 📂 Project Structure

- `main.py`: Core application logic, tool registration, and conversation management.
- `pyproject.toml`: Project metadata and dependencies.
- `.env`: (Ignored) Environment variables for sensitive keys.
- `order_db`: Mock database for testing order statuses.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

[MIT](LICENSE) (or your preferred license)

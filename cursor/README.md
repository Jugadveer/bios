# Nex Mentor API

## Overview

The Nex Mentor API provides structured educational responses for the WealthPlay platform. Nex is an encouraging, simple, and practical course mentor that generates explanations, quizzes, summaries, and next steps based on lesson content.

## Endpoints

### POST /api/cursor/explain

Generate structured explanation from Nex mentor.

**Request Body:**
```json
{
  "action": "explain",
  "lesson_id": "investing_basics_01",
  "page_type": "course",
  "user_context": {
    "user_id": "user_123",
    "demo_balance": 50000,
    "progress": 0.35,
    "confidence_level": "low",
    "recent_choices": []
  },
  "requested_depth": "medium",
  "allow_web_fetch": true,
  "sources": [
    {
      "label": "Investopedia - Investing Intro",
      "url": "https://www.investopedia.com/articles/basics/11/3-s-simple-investing.asp"
    }
  ],
  "user_message": "Explain this attachment"
}
```

**Response:**
```json
{
  "title": "Understanding Investing Basics",
  "explanation": "Investing means putting your money to work...",
  "bullet_steps": [
    "Assess your financial situation",
    "Set clear investment goals",
    "Build an emergency fund"
  ],
  "links": [
    {
      "label": "Investopedia - Investing Intro",
      "url": "https://www.investopedia.com/articles/basics/11/3-s-simple-investing.asp"
    }
  ],
  "quiz": {
    "question": "What is the primary purpose of investing?",
    "options": [
      "To save money safely",
      "To grow wealth over time",
      "To avoid taxes",
      "To spend money quickly"
    ],
    "correct_index": 1,
    "explanation": "Investing aims to grow wealth over time..."
  },
  "apply_actions": {
    "apply_to_demo_portfolio": true
  }
}
```

### GET /api/cursor/health

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "mentor": "Nex"
}
```

## Actions

- `explain`: Generate detailed explanation
- `quiz`: Generate quiz question
- `summarize`: Generate summary
- `compare`: Generate comparison
- `next_steps`: Generate actionable next steps

## Requested Depth

- `short`: ~50 words
- `medium`: ~150 words
- `long`: ~300 words

## Supported Topics

- investing_basics
- safe_sips
- emergency_fund
- diversification
- portfolio_tips
- market_trends
- financial_goals
- budgeting
- tax_planning

## Frontend Integration

```javascript
// Example usage
const response = await fetch('/api/cursor/explain', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    action: 'explain',
    lesson_id: 'investing_basics_01',
    page_type: 'course',
    user_context: {
      user_id: userId,
      demo_balance: 50000,
      progress: 0.2,
      confidence_level: 'low'
    },
    requested_depth: 'medium',
    allow_web_fetch: true,
    sources: [],
    user_message: 'Explain this concept'
  })
});

const data = await response.json();
// Render: data.title, data.explanation, data.bullet_steps, etc.
```


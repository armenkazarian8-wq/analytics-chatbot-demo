# Demo transcript (screenshot-free)

Generated locally against **fictional** seeded data. Answer mode: **Google Gemini (`gemini-3.5-flash-lite`)**.

LLM answers (when enabled) are phrased only from tenant-scoped structured query results — the model never sees other customers' rows.

This is an illustration of the chatbot, not a client deliverable.

## Aurora Trail Co. (FICTIONAL) (`cust_aurora`)

### Q1. Which posts drove the most engagement last month?

**Query kind:** `top_engagement` · **Mode:** `llm` · **Provider:** `gemini`

**Answer:**

```
Based on Aurora Trail Co.'s data (`cust_aurora`), the top-performing post for engagement last month was the TikTok video **"Packing a 3-day backpack in 60 seconds"**, which drove **6,920 total engagement** (5,400 likes, 620 comments, and 900 shares). 

The next highest posts were:
2. **"Wrong way vs right way to lace hiking boots"** on TikTok with **4,310 engagement** (3,200 likes, 410 comments, 700 shares).
3. **"Customer photo: summit coffee ritual"** on Instagram with **1,805 engagement** (1,500 likes, 210 comments, 95 shares).
```

<details><summary>Structured rows (truncated)</summary>

```json
[
  {
    "external_id": "p3",
    "platform": "tiktok",
    "caption": "Packing a 3-day backpack in 60 seconds",
    "posted_on": "2026-10-12",
    "likes": 5400,
    "comments": 620,
    "shares": 900,
    "reach": 95000,
    "engagement": 6920
  },
  {
    "external_id": "p7",
    "platform": "tiktok",
    "caption": "Wrong way vs right way to lace hiking boots",
    "posted_on": "2026-11-02",
    "likes": 3200,
    "comments": 410,
    "shares": 700,
    "reach": 72000,
    "engagement": 4310
  },
  {
    "external_id": "p4",
    "platform": "instagram",
    "caption": "Customer photo: summit coffee ritual",
    "posted_on": "2026-10-19",
    "likes": 1500,
    "comments": 210,
    "shares": 95,
    "reach": 22000,
    "engagement": 1805
  }
]
```

</details>

### Q2. What are the total engagement totals last month?

**Query kind:** `totals` · **Mode:** `llm` · **Provider:** `gemini`

**Answer:**

```
Based on Aurora Trail Co.'s data (`cust_aurora`), the total engagement across all posts published over the last 30 days is **15,610**. This includes **12,180 likes**, **1,545 comments**, and **1,885 shares** generated from a total of 6 posts, achieving a combined reach of 224,000.
```

<details><summary>Structured rows (truncated)</summary>

```json
[
  {
    "post_count": 6,
    "likes": 12180,
    "comments": 1545,
    "shares": 1885,
    "reach": 224000,
    "engagement": 15610
  }
]
```

</details>

### Q3. Show platform breakdown for the last 30 days

**Query kind:** `by_platform` · **Mode:** `llm` · **Provider:** `gemini`

**Answer:**

```
Based on Aurora Trail Co.'s data (`cust_aurora`), the platform breakdown for the last 30 days is:

* **TikTok:** 11,230 engagements across 2 posts
* **Instagram:** 3,825 engagements across 3 posts
* **Twitter:** 555 engagements across 1 post
```

<details><summary>Structured rows (truncated)</summary>

```json
[
  {
    "platform": "tiktok",
    "posts": 2,
    "engagement": 11230
  },
  {
    "platform": "instagram",
    "posts": 3,
    "engagement": 3825
  },
  {
    "platform": "twitter",
    "posts": 1,
    "engagement": 555
  }
]
```

</details>

## Nimbus Bean Roasters (FICTIONAL) (`cust_nimbus`)

### Q1. Which posts drove the most engagement last month?

**Query kind:** `top_engagement` · **Mode:** `llm` · **Provider:** `gemini`

**Answer:**

```
Based on Nimbus Bean Roasters' (`cust_nimbus`) data for the last 30 days, the top posts by engagement are:

1. **"Cold brew concentrate how-to"** (TikTok, Nov 1) – 5,500 total engagement (4,100 likes, 520 comments, 880 shares).
2. **"Limited winter blend launch"** (Instagram, Nov 4) – 2,300 total engagement (1,900 likes, 260 comments, 140 shares).
3. **"Subscription box unboxing"** (Instagram, Oct 15) – 895 total engagement (760 likes, 95 comments, 40 shares).
4. **"Meet the farmers — fictional co-op story"** (Instagram, Oct 28) – 635 engagement.
5. **"Cafe playlist for deep work"** (Instagram, Nov 7) – 485 engagement. 

All figures come directly from
 this customer's data.
```

<details><summary>Structured rows (truncated)</summary>

```json
[
  {
    "external_id": "p6",
    "platform": "tiktok",
    "caption": "Cold brew concentrate how-to",
    "posted_on": "2026-11-01",
    "likes": 4100,
    "comments": 520,
    "shares": 880,
    "reach": 88000,
    "engagement": 5500
  },
  {
    "external_id": "p7",
    "platform": "instagram",
    "caption": "Limited winter blend launch",
    "posted_on": "2026-11-04",
    "likes": 1900,
    "comments": 260,
    "shares": 140,
    "reach": 26000,
    "engagement": 2300
  },
  {
    "external_id": "p3",
    "platform": "instagram",
    "caption": "Subscription box unboxing",
    "posted_on": "2026-10-15",
    "likes": 760,
    "comments": 95,
    "shares": 40,
    "reach": 12000,
    "engagement": 895
  }
]
```

</details>

### Q2. What are the total engagement totals last month?

**Query kind:** `totals` · **Mode:** `llm` · **Provider:** `gemini`

**Answer:**

```
Based on Nimbus Bean Roasters' (`cust_nimbus`) data for the last 30 days, here are the total engagement metrics:

* **Total Engagement:** 10,263
* **Likes:** 8,040
* **Comments:** 1,033
* **Shares:** 1,190
* **Combined Reach:** 150,500
* **Total Posts Published:** 6

All figures come directly from this customer's data.
```

<details><summary>Structured rows (truncated)</summary>

```json
[
  {
    "post_count": 6,
    "likes": 8040,
    "comments": 1033,
    "shares": 1190,
    "reach": 150500,
    "engagement": 10263
  }
]
```

</details>

### Q3. Show platform breakdown for the last 30 days

**Query kind:** `by_platform` · **Mode:** `llm` · **Provider:** `gemini`

**Answer:**

```
Based on Nimbus Bean Roasters' (`cust_nimbus`) data for the last 30 days, the platform breakdown is as follows:

* **TikTok:** 5,500 total engagement across 1 post.
* **Instagram:** 4,315 total engagement across 4 posts.
* **Twitter:** 448 total engagement across 1 post.

All figures come directly from this customer's data.
```

<details><summary>Structured rows (truncated)</summary>

```json
[
  {
    "platform": "tiktok",
    "posts": 1,
    "engagement": 5500
  },
  {
    "platform": "instagram",
    "posts": 4,
    "engagement": 4315
  },
  {
    "platform": "twitter",
    "posts": 1,
    "engagement": 448
  }
]
```

</details>

## Pixel Pine Studio (FICTIONAL) (`cust_pixelpine`)

### Q1. Which posts drove the most engagement last month?

**Query kind:** `top_engagement` · **Mode:** `llm` · **Provider:** `gemini`

**Answer:**

```
Based on Pixel Pine Studio's (`cust_pixelpine`) data for the last 30 days, the top posts driving engagement are:

1. **"Before/after logo animation"** (TikTok) — 4,690 total engagement (3,600 likes, 440 comments, 650 shares).
2. **"Motion design process reel"** (Instagram) — 2,930 engagement (2,400 likes, 310 comments, 220 shares).
3. **"Client kickoff checklist template"** (LinkedIn) — 1,890 engagement (1,500 likes, 210 comments, 180 shares).
4. **"Color systems that scale"** (Instagram) — 1,320 engagement.
5. **"How we run weekly creative critiques"** (LinkedIn) — 1,170 engagement. 

These figures are pulled directly from Pixel Pine Studio's performance records.
```

<details><summary>Structured rows (truncated)</summary>

```json
[
  {
    "external_id": "p8",
    "platform": "tiktok",
    "caption": "Before/after logo animation",
    "posted_on": "2026-11-08",
    "likes": 3600,
    "comments": 440,
    "shares": 650,
    "reach": 78000,
    "engagement": 4690
  },
  {
    "external_id": "p3",
    "platform": "instagram",
    "caption": "Motion design process reel",
    "posted_on": "2026-10-18",
    "likes": 2400,
    "comments": 310,
    "shares": 220,
    "reach": 41000,
    "engagement": 2930
  },
  {
    "external_id": "p6",
    "platform": "linkedin",
    "caption": "Client kickoff checklist template",
    "posted_on": "2026-11-03",
    "likes": 1500,
    "comments": 210,
    "shares": 180,
    "reach": 25000,
    "engagement": 1890
  }
]
```

</details>

### Q2. What are the total engagement totals last month?

**Query kind:** `totals` · **Mode:** `llm` · **Provider:** `gemini`

**Answer:**

```
Based on Pixel Pine Studio's (`cust_pixelpine`) data for the last 30 days, the total engagement figures are:

* **Total Engagement:** 12,935 across 7 published posts
* **Likes:** 10,300
* **Comments:** 1,345
* **Shares:** 1,290
* **Combined Reach:** 195,000

These figures come directly from this customer's data.
```

<details><summary>Structured rows (truncated)</summary>

```json
[
  {
    "post_count": 7,
    "likes": 10300,
    "comments": 1345,
    "shares": 1290,
    "reach": 195000,
    "engagement": 12935
  }
]
```

</details>

### Q3. Show platform breakdown for the last 30 days

**Query kind:** `by_platform` · **Mode:** `llm` · **Provider:** `gemini`

**Answer:**

```
Based on Pixel Pine Studio's (`cust_pixelpine`) data for the last 30 days, here is the platform breakdown by total engagement:

* **Instagram:** 4,830 engagement (3 posts)
* **TikTok:** 4,690 engagement (1 post)
* **LinkedIn:** 3,060 engagement (2 posts)
* **Twitter:** 355 engagement (1 post)

These figures come directly from this customer's data.
```

<details><summary>Structured rows (truncated)</summary>

```json
[
  {
    "platform": "instagram",
    "posts": 3,
    "engagement": 4830
  },
  {
    "platform": "tiktok",
    "posts": 1,
    "engagement": 4690
  },
  {
    "platform": "linkedin",
    "posts": 2,
    "engagement": 3060
  }
]
```

</details>


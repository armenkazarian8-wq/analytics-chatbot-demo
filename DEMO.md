# Demo transcript (screenshot-free)

Generated locally against **fictional** seeded data. Answer mode: **deterministic fallback**.

This is an illustration of the chatbot, not a client deliverable.

## Aurora Trail Co. (FICTIONAL) (`cust_aurora`)

### Q1. Which posts drove the most engagement last month?

**Query kind:** `top_engagement` · **Mode:** `fallback`

**Answer:**

```
Answer for Aurora Trail Co. (FICTIONAL) only. Query type: top_engagement.

Top engagement in the last 30 days: 'Packing a 3-day backpack in 60 seconds' on tiktok (6920 engagement: 5400 likes, 620 comments, 900 shares). Next: #2 'Wrong way vs right way to lace hiking boots' (4310), #3 'Customer photo: summit coffee ritual' (1805).

(Demo mode: deterministic answer from this customer's data. No other tenants were queried.)
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

**Query kind:** `totals` · **Mode:** `fallback`

**Answer:**

```
Answer for Aurora Trail Co. (FICTIONAL) only (continuing from earlier: “Which posts drove the most engagement last month?”). Query type: totals.

In the last 30 days this customer published 6 posts with 15610 total engagement (12180 likes, 1545 comments, 1885 shares) and 224000 combined reach.

(Demo mode: deterministic answer from this customer's data. No other tenants were queried.)
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

**Query kind:** `by_platform` · **Mode:** `fallback`

**Answer:**

```
Answer for Aurora Trail Co. (FICTIONAL) only (continuing from earlier: “What are the total engagement totals last month?”). Query type: by_platform.

Platform breakdown (last 30 days): tiktok: 11230 engagement across 2 posts; instagram: 3825 engagement across 3 posts; twitter: 555 engagement across 1 posts.

(Demo mode: deterministic answer from this customer's data. No other tenants were queried.)
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

**Query kind:** `top_engagement` · **Mode:** `fallback`

**Answer:**

```
Answer for Nimbus Bean Roasters (FICTIONAL) only. Query type: top_engagement.

Top engagement in the last 30 days: 'Cold brew concentrate how-to' on tiktok (5500 engagement: 4100 likes, 520 comments, 880 shares). Next: #2 'Limited winter blend launch' (2300), #3 'Subscription box unboxing' (895).

(Demo mode: deterministic answer from this customer's data. No other tenants were queried.)
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

**Query kind:** `totals` · **Mode:** `fallback`

**Answer:**

```
Answer for Nimbus Bean Roasters (FICTIONAL) only (continuing from earlier: “Which posts drove the most engagement last month?”). Query type: totals.

In the last 30 days this customer published 6 posts with 10263 total engagement (8040 likes, 1033 comments, 1190 shares) and 150500 combined reach.

(Demo mode: deterministic answer from this customer's data. No other tenants were queried.)
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

**Query kind:** `by_platform` · **Mode:** `fallback`

**Answer:**

```
Answer for Nimbus Bean Roasters (FICTIONAL) only (continuing from earlier: “What are the total engagement totals last month?”). Query type: by_platform.

Platform breakdown (last 30 days): tiktok: 5500 engagement across 1 posts; instagram: 4315 engagement across 4 posts; twitter: 448 engagement across 1 posts.

(Demo mode: deterministic answer from this customer's data. No other tenants were queried.)
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

**Query kind:** `top_engagement` · **Mode:** `fallback`

**Answer:**

```
Answer for Pixel Pine Studio (FICTIONAL) only. Query type: top_engagement.

Top engagement in the last 30 days: 'Before/after logo animation' on tiktok (4690 engagement: 3600 likes, 440 comments, 650 shares). Next: #2 'Motion design process reel' (2930), #3 'Client kickoff checklist template' (1890).

(Demo mode: deterministic answer from this customer's data. No other tenants were queried.)
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

**Query kind:** `totals` · **Mode:** `fallback`

**Answer:**

```
Answer for Pixel Pine Studio (FICTIONAL) only (continuing from earlier: “Which posts drove the most engagement last month?”). Query type: totals.

In the last 30 days this customer published 7 posts with 12935 total engagement (10300 likes, 1345 comments, 1290 shares) and 195000 combined reach.

(Demo mode: deterministic answer from this customer's data. No other tenants were queried.)
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

**Query kind:** `by_platform` · **Mode:** `fallback`

**Answer:**

```
Answer for Pixel Pine Studio (FICTIONAL) only (continuing from earlier: “What are the total engagement totals last month?”). Query type: by_platform.

Platform breakdown (last 30 days): instagram: 4830 engagement across 3 posts; tiktok: 4690 engagement across 1 posts; linkedin: 3060 engagement across 2 posts; twitter: 355 engagement across 1 posts.

(Demo mode: deterministic answer from this customer's data. No other tenants were queried.)
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


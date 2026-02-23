# Shopify Integration Strategy & Execution Plan

## 1. The Strategy: "Digital Resilience"
To make Shopify work for the **Palestine Resilience Field**, we are not just building a store; we are building a **node of articulation**.

### Core Expectations for Commercial Success:
1.  **Platform Reliability**: We use Shopify because it handles the heavy lifting (security, hosting, checkout uptime) so we can focus on *product* and *story*.
2.  **Global Reach**: The store must be configured to sell internationally (multi-currency, international shipping zones).
3.  **Trust Signals**: The design must feel premium and legitimate to overcome any hesitation about buying from a conflict zone or a cause-based initiative.
4.  **Frictionless Donation/Purchase**: The line between "buying a product" and "supporting the cause" should be blurred but distinct.

---

## 2. Technical Integration Plan

### Option A: The "Agentic" Setup (I do it for you)
If you provide the credentials, I can use my browser tool to:
1.  **Log in** to your Shopify Partner/Store account.
2.  **Clear** any dummy data.
3.  **Import** the `shopify_import_ready.csv` file I created.
4.  **verify** that the products are listed correctly.

**What I need from you:**
*   Shopify Login URL (e.g., `agency-name.myshopify.com/admin`)
*   Username/Email
*   Password
*   *Verification Code* (You will likely need to be online to give me the 2FA code immediately).

### Option B: Manual Setup (You do it)
1.  Log in to Shopify Admin.
2.  Go to **Products**.
3.  Click **Import**.
4.  Drag and drop the `shopify_import_ready.csv` file.
5.  Click **Upload and Continue**.
6.  Review the prelude (Shopify will show a preview). Click **Import Products**.

---

## 3. Critical Configuration Checklist (The "Expectation")
Merely uploading data is not enough. To be "commercial ready", we must solve these three blockers:

### A. Payments (The Hardest Part)
*   *Challenge*: Stripe/PayPal often restrict accounts in Palestine.
*   *Solution*: We typically need a legal entity abroad (UK, US, UAE) to hold the Stripe account (Atlas or local registration), OR use a specialized gateway like **Tap Payments** or **PayTabs** if operating locally.
*   *Action*: Confirm which legal entity is the "Merchant on Record".

### B. Shipping Profiles
*   *Challenge*: Shipping from West Bank/Gaza is inconsistent using IL post.
*   *Solution*:
    *   **Drop-shipping**: If we use partners (Canaan, etc.), WE don't ship. We just forward the order. **This is the scalable model.**
    *   **Consolidated Shipping**: We ship bulk to a warehouse in Jordan/US and fulfill from there.
*   *Action*: Set up "Custom Fulfillment Services" in Shopify for each vendor (e.g., "Vendor: Canaan" -> Email notification to Canaan).

### C. The "Market" Settings
*   Go to **Settings > Markets**.
*   Create a "Primary Market" (e.g., USA/Europe).
*   Ensure currency conversion is ON if using Shopify Payments, or set fixed prices.

---

## 4. Next Steps
1.  **Send the Assistant the Checklist** (`docs/assistant_image_checklist.md`).
2.  **Decide on Integration**: 
    *   Give me credentials now -> I upload data.
    *   You upload data -> I guide the next step (Theme design).
3.  **Solve Payment**: Tell me where the bank account is located so I can recommend the correct gateway settings.

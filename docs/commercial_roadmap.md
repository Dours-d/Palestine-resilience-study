# Palestine Resilience Commerce - Project Roadmap

This roadmap outlines the development of a full-stack e-commerce platform for dropshipping Palestinian products, transforming the research catalog into a commercial reality.

## 1. Project Initialization & Tech Stack
-   **Repository**: `Palestine-resilience-commerce` (New)
-   **Frontend**: Next.js 14 (App Router), React, Tailwind CSS.
-   **UI Library**: Shadcn/UI + Framer Motion (for premium animations).
-   **Backend/Database**: Supabase (PostgreSQL) for product inventory and order management.
-   **Payments**: Stripe Connect (standard for dropshipping splits).

## 2. Data Architecture (The "Digital Souq")
We will implement the product schemas defined in `product_cards_catalog.md`:
-   **Products Table**: SKU, Name, Description (Story), Price, Stock, Supplier_ID.
-   **Suppliers Table**: Contact info for Canaan, Zaytoun, Handmade Palestine, etc.
-   **Orders Table**: Customer details, items, shipping status.

## 3. Core Features (MVP)
### Phase 1: Storefront & Storytelling (Weeks 1-2)
-   [ ] **Hero Section**: High-impact visuals of Hebron olive trees or Nablus soap towers.
-   [ ] **Product Grid**: Filterable by category (Food, Decor, Apparel).
-   [ ] **Product Detail Page**: "Story-first" design. The "Story" field from the catalog is the primary content, not just specs.

### Phase 2: Cart & Checkout (Years 3-4)
-   [ ] **Shopping Cart**: Real-time state management (Zustand/Redux).
-   [ ] **Stripe Integration**: Secure checkout flow.
-   [ ] **Order Confirmation**: Email generation to customer.

### Phase 3: Dropshipping Automation (Weeks 5-6)
-   [ ] **Supplier Notification**: System automatically emails the specific supplier (e.g., Zaytoun) with the shipping label or order details upon purchase.
-   [ ] **Inventory Sync**: (Advanced) Webhook listeners for supplier stock levels.

## 4. Immediate Next Steps
1.  Initialize the `Palestine-resilience-commerce` repository.
2.  Set up the Next.js boilerplate with Tailwind CSS.
3.  Create the `data/products.json` seed file based on the existing catalog.
4.  Design the "Hero" component for the landing page.

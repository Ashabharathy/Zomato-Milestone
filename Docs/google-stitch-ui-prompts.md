# Google Stitch UI Generation Prompts

## Project Overview
**Framework**: Next.js (React-based framework with App Router)  
**UI Library**: Material-UI (MUI) v5 with custom theme  
**Styling**: CSS-in-JS with Emotion, Tailwind CSS compatible  
**Design System**: Modern, clean, food/restaurant-focused aesthetic

---

## 🎨 Design System Guidelines

### Color Palette
- **Primary**: Warm Orange (#FF6B35) - Represents food/appetite
- **Secondary**: Deep Red (#C1272D) - Restaurant/brand accent
- **Background**: Clean White (#FFFFFF) with warm off-white (#FAFAFA)
- **Text**: Dark Charcoal (#333333) for readability
- **Accent**: Fresh Green (#4CAF50) for ratings/positive indicators
- **Neutral**: Soft Gray (#F5F5F5) for cards and sections

### Typography
- **Headings**: Inter or Roboto, bold weights (600-700)
- **Body**: Inter or Open Sans, regular weights (400-500)
- **Restaurant Names**: Playfair Display or elegant serif for sophistication

### Layout Principles
- **Mobile-First**: Responsive design starting from 375px
- **Grid System**: 12-column grid with 24px gutters
- **Spacing**: 8px base unit (multiples: 8, 16, 24, 32, 48, 64)
- **Border Radius**: 12px for cards, 24px for buttons, 8px for inputs
- **Shadows**: Soft elevation shadows (0px 4px 12px rgba(0,0,0,0.1))

---

## 📱 Page-Specific UI Prompts

### 1. Landing Page / Home Page

**Prompt for Google Stitch:**
```
Create a modern, inviting landing page for an AI-powered restaurant recommendation app called "SmartDine" using Next.js and Material-UI.

Key Elements:
- Hero section with large, appetizing food imagery background (slight overlay for text readability)
- Bold headline: "Discover Your Perfect Dining Experience"
- Subheadline: "AI-powered recommendations tailored to your taste"
- Two CTA buttons: "Find Restaurants" (primary, filled) and "Learn More" (secondary, outlined)
- Search bar with location input and cuisine dropdown in center of hero
- Feature highlights section (3 cards):
  * "AI-Powered" with brain/AI icon
  * "Personalized" with user profile icon  
  * "Local Favorites" with map pin icon
- How it works section (3 steps with illustrations):
  1. Enter preferences
  2. AI analyzes options
  3. Get recommendations
- Featured restaurants carousel showing 3 restaurant cards
- Trust indicators: "10,000+ happy diners", star ratings, review count
- Footer with app download buttons (iOS/Android mockups)

Style:
- Warm, inviting color scheme (orange, red accents)
- Modern sans-serif typography
- Card-based layout with soft shadows
- Ample white space
- Food photography style: vibrant, high-quality images
- Responsive layout visible (show mobile and desktop variants side-by-side or stacked)
```

**Expected Output**: Landing page mockup showing hero section, search functionality, feature highlights, and trust indicators.

---

### 2. Search & Discovery Page

**Prompt for Google Stitch:**
```
Create a restaurant search and discovery page for a Next.js app with advanced filtering capabilities.

Layout Structure:
- Sticky header with logo, search bar, user profile avatar
- Left sidebar (25% width on desktop, collapsible on mobile):
  * Filter panel with accordions:
    - Location (with map radius slider)
    - Cuisine types (checkboxes: Indian, Italian, Chinese, etc.)
    - Price range (₹ to ₹₹₹₹ slider)
    - Rating filter (star selector 1-5)
    - Dietary preferences (veg, non-veg, vegan, gluten-free toggles)
    - Features (outdoor seating, wifi, parking, pet-friendly)
- Main content area (75% width):
  * Results header: "Showing 24 restaurants near Indiranagar"
  * Sort dropdown: "Sort by: Recommended | Rating | Distance | Price"
  * View toggle: List view / Grid view icons
  * Restaurant cards grid (3 columns desktop, 1 column mobile)

Restaurant Card Design:
- Image thumbnail (16:9 ratio) with favorite/bookmark heart icon
- Restaurant name (bold, 18px)
- Cuisine tags (chips: "North Indian", "BBQ")
- Rating badge with star icon (4.5/5) and review count
- Price indicator (₹₹)
- Distance badge ("2.3 km away")
- Key features icons (delivery, dine-in, outdoor)
- "View Details" button
- AI recommendation badge: "Recommended for you" with sparkle icon

Map Integration:
- Toggle to show/hide map view
- Map showing restaurant pins with price indicators
- Current location marker

Style:
- Clean, organized layout
- Filter sidebar with clear section dividers
- Cards with hover elevation effect
- Active filters shown as removable chips
- Pagination or infinite scroll indicator
```

**Expected Output**: Search page with filters, restaurant cards grid, and map view option.

---

### 3. Restaurant Detail Page

**Prompt for Google Stitch:**
```
Create a comprehensive restaurant detail page for Next.js with rich information display.

Page Structure:
- Hero section with full-width image carousel (3-4 restaurant photos)
- Overlaid gradient from bottom for text readability
- Restaurant name, cuisine type, and rating prominently displayed
- Action buttons row: "Book Table", "Order Online", "Save", "Share"

Info Bar (sticky on scroll):
- Status badge: "Open now" or "Closed" (green/red)
- Rating: 4.5 ★ (1,234 reviews)
- Price: ₹₹₹
- Distance: 1.2 km
- Time: 30-45 min delivery

Main Content Sections:

1. Quick Info Row:
   - Address with map preview thumbnail
   - Phone number with call button
   - Website link
   - Hours ( expandable "See all hours" )

2. AI Recommendation Section:
   - "Why we recommend this" card
   - Personalized match score (e.g., "92% match")
   - Matching factors: "Matches your preference for North Indian cuisine", "High rating for ambiance", "Within your budget"
   - AI-generated summary: "Based on your love for spicy food and previous visits to BBQ Nation..."

3. Photo Gallery Grid:
   - Masonry grid of food photos, interior shots
   - "View all 45 photos" link

4. Menu Section:
   - Category tabs: "Popular", "Starters", "Main Course", "Desserts"
   - Menu items with prices, ratings, photos
   - "Most ordered" badges
   - Add to cart buttons for online ordering

5. Reviews Section:
   - Overall rating breakdown (5-star distribution chart)
   - Highlighted reviews carousel
   - Review cards with user avatar, name, rating, date, photos, text
   - "Helpful" and "Report" actions
   - "Write a review" CTA

6. Features & Amenities:
   - Icon grid: WiFi, Parking, Outdoor Seating, Live Music, etc.

7. Location & Map:
   - Interactive map embed
   - "Get Directions" button
   - Nearby landmarks

8. Similar Restaurants:
   - "You might also like" carousel
   - 4 restaurant cards with key info

Style:
- Premium, detailed layout
- High-quality food photography
- Clear visual hierarchy
- Card-based information grouping
- Smooth scrolling between sections
- Mobile-optimized with collapsible sections
```

**Expected Output**: Detailed restaurant page with hero image, AI recommendations, menu, reviews, and map sections.

---

### 4. AI Recommendation Results Page

**Prompt for Google Stitch:**
```
Create an AI-powered recommendation results page showing personalized restaurant suggestions.

Page Layout:
- Header: "AI Recommendations for You"
- Context bar: "Based on: Indiranagar area, ₹800-1200 budget, North Indian preference"
- "Refine Preferences" button (opens modal)

Results Display:
- AI-generated summary at top: "We found 3 perfect matches based on your preferences for spicy North Indian cuisine within 2km of Indiranagar."

Ranked Recommendation Cards (3-5 results):

Card Layout (each card full-width, stacked):
- Rank badge: "#1 Top Pick", "#2 Great Match", etc. with distinct colors
- Restaurant image (left, 40% width)
- Content area (right, 60% width):
  * Restaurant name with "AI Recommended" badge
  * Match score: "94% match" with progress bar visualization
  * Why this matches:
    - "✓ North Indian cuisine specialty"
    - "✓ ₹900 average cost (within budget)"
    - "✓ 4.6 rating with 500+ reviews"
    - "✓ 1.5km from your location"
  * AI-generated personalized description: "This restaurant perfectly matches your preference for authentic North Indian flavors. Their butter chicken has excellent reviews and matches your spice tolerance level."
  * Quick actions: "View Details", "Save", "Get Directions", "Book Table"

Comparison Feature:
- "Compare these options" toggle
- Side-by-side comparison table:
  * Restaurant names as column headers
  * Rows: Rating, Price, Distance, Cuisine, Best For, AI Score

Alternative Suggestions:
- "Other options you might consider" section below
- 3 smaller cards with less perfect but still relevant matches

Feedback Section:
- "How did we do?" at bottom
- Thumbs up/down buttons
- "These recommendations weren't quite right" - link to refine

Visual Style:
- AI/tech aesthetic with subtle gradient accents
- Match score visualization with circular progress indicators
- Clear ranking hierarchy (#1, #2, #3)
- Smart, analytical feel while remaining warm and inviting
- Green indicators for matching criteria
- Micro-animations suggestions (hover states, loading states)
```

**Expected Output**: AI recommendation results page showing ranked suggestions with match scores and personalized explanations.

---

### 5. User Profile & Preferences Page

**Prompt for Google Stitch:**
```
Create a comprehensive user profile and preferences management page for Next.js.

Page Layout (Tabbed Interface):

Tab 1: Profile Overview
- Profile header with cover image and avatar
- User name, email, member since date
- Edit profile button
- Statistics cards row:
  * "23 Restaurant Visits"
  * "45 Saved Places"
  * "12 Reviews Written"
  * "15 Bookings Made"
- Recent activity feed (last 5 actions)

Tab 2: Food Preferences (AI Training)
- "Help our AI understand you better" header
- Cuisine preferences (multi-select chips):
  * Categories: Indian, Chinese, Italian, Mexican, Japanese, Mediterranean, etc.
  * Selected items highlighted in primary color
- Dietary restrictions (toggle switches):
  * Vegetarian, Vegan, Gluten-Free, Jain, Halal, Nut Allergy
- Spice tolerance (slider: Mild → Medium → Hot → Extra Hot)
- Price preference range (dual slider: ₹200 - ₹2000)
- Preferred locations (multi-select with search)
- Occasion preferences (casual, romantic, family, business, date night)
- Ambiance preferences (quiet, lively, outdoor, rooftop, fine dining)
- "Save Preferences" button

Tab 3: Saved & History
- Two sub-tabs: "Saved Restaurants" | "Visited Places"
- Saved restaurants: Grid of bookmarked places with notes
- History: Timeline view of visited restaurants with dates, ratings given
- "Add to List" feature for organizing saved places

Tab 4: My Reviews
- List of user's reviews
- Review card: Restaurant name, date, rating, review text, photos
- Edit/Delete options
- Review statistics: Total helpful votes received

Tab 5: Settings
- Account settings (email, password, phone)
- Notification preferences (email, push, SMS toggles)
  * New recommendations
  * Booking confirmations
  * Review reminders
  * Special offers
- Privacy settings
- Connected accounts (Google, Facebook)
- Delete account option

Style:
- Clean, organized card-based layout
- Intuitive form controls
- Progress indicators for preference completion
- Mobile-responsive with stacked layout on small screens
- Subtle animations for tab transitions
```

**Expected Output**: User profile page with preferences management, saved places, review history, and settings.

---

### 6. Booking & Reservation Page

**Prompt for Google Stitch:**
```
Create a restaurant table booking flow for Next.js with multi-step process.

Step 1: Select Date & Time
- Calendar component (current month view)
- Available dates highlighted
- Time slot selection (grid of 30-min slots: 12:00 PM, 12:30 PM, etc.)
- "Popular times" indicator with small flame icon
- Party size selector (dropdown: 1-10 people)
- "Check Availability" button

Step 2: Table Selection (if applicable)
- Floor plan visualization (simplified 2D layout)
- Available tables marked in green
- Table types: "Window seat", "Booth", "Outdoor", "Bar seating"
- Click to select table
- "Any available table" option

Step 3: Guest Details
- Form fields:
  * Name (pre-filled if logged in)
  * Phone number
  * Email
  * Special requests textarea ("Allergies, special occasion, seating preferences")
- Occasion dropdown: "Birthday", "Anniversary", "Business meal", "Casual dining"
- SMS reminder toggle

Step 4: Confirmation
- Booking summary card:
  * Restaurant name and image
  * Date & time (large, prominent)
  * Party size
  * Table preference
  * Guest details
- "Add to Calendar" button (Google, Apple, Outlook icons)
- Share booking options
- Special offers/coupons section ("Use code FIRST10 for 10% off")
- Cancellation policy notice
- "Confirm Booking" button (primary, large)

Post-Booking:
- Success animation/illustration
- Booking confirmation card with QR code
- "Modify Booking" and "Cancel" options
- Add to calendar buttons
- Directions button

Style:
- Step indicator at top (1-2-3-4 progress bar)
- Clean, focused layout minimizing distractions
- Clear CTAs on each step
- Mobile-optimized touch targets
- Real-time availability indicators
- Professional yet friendly tone
```

**Expected Output**: Multi-step booking flow with calendar, time selection, guest details, and confirmation.

---

### 7. Admin Dashboard (for Restaurant Owners)

**Prompt for Google Stitch:**
```
Create a restaurant owner/admin dashboard for managing their restaurant profile and analytics.

Dashboard Layout:
- Sidebar navigation (collapsible on mobile):
  * Dashboard (overview)
  * Profile Management
  * Menu Editor
  * Reservations
  * Reviews & Feedback
  * Analytics & Insights
  * Settings

Main Dashboard Overview:
- Key metrics cards row:
  * "1,234 Profile Views" (7-day trend up 12%)
  * "456 Table Bookings" (trend graph)
  * "89 Online Orders"
  * "4.6 Average Rating"
  * "32 Reviews this week"

Charts Section:
- Line chart: "Profile Views (Last 30 Days)"
- Bar chart: "Reservations by Day of Week"
- Pie chart: "Traffic Sources" (Direct, Search, Social, Referrals)

Recent Activity Feed:
- New bookings with guest details
- Recent reviews with sentiment indicator
- Menu item popularity updates

Quick Actions:
- "Add Special Offer"
- "Update Menu"
- "Respond to Reviews"
- "View Reports"

AI Insights Section:
- "Customer Preference Trends" card
  * "North Indian dishes are trending up 15% this month"
  * "Peak booking time: 7:00-8:00 PM"
  * "Most requested table: Window seating"
- Action recommendations:
  * "Consider adding more vegetarian options"
  * "Promote lunch specials - searches increasing"

Reservation Management:
- Calendar view with booking slots
- Color-coded: Confirmed (green), Pending (yellow), Cancelled (red)
- Click to view booking details
- "Block Table" option for private events

Review Management:
- List of recent reviews
- Star rating filter
- "Respond" button for each review
- Sentiment analysis tags: Positive, Neutral, Negative

Style:
- Professional, data-heavy interface
- Data visualization with clear charts
- Action-oriented layout
- Real-time updates feel
- Responsive for tablet use (common for restaurant managers)
```

**Expected Output**: Admin dashboard with analytics, recent activity, reservation management, and review handling.

---

## 🧩 Component Library Prompts

### Reusable Components

**Restaurant Card (Compact):**
```
Design a compact restaurant card component for Next.js.

Elements:
- Square image thumbnail (1:1 ratio) with rounded corners
- Restaurant name (16px, bold, single line truncate)
- Rating badge (4.5 ★) with green background
- Price indicator (₹₹) and cuisine type (14px gray)
- Distance label ("1.2 km")
- Bookmark icon (top-right corner)

Dimensions: 160px width, auto height
Hover state: Slight scale (1.02) and shadow elevation
Style: Clean, minimal, information-dense
```

**Filter Chip/Tag:**
```
Design a selectable filter chip component.

States:
- Default: Light gray background, dark text, rounded-full
- Selected: Primary color background (orange), white text, checkmark icon
- Hover: Slightly darker background

Sizes: Small (for dense UIs), Medium (standard), Large (touch-friendly)
Variants: With/without icon, removable (X button), counter badge
```

**Rating Stars:**
```
Design a rating display component with stars.

Features:
- 5-star rating display
- Partial star support (e.g., 4.5 shows 4 full + 1 half)
- Size variants: Small (12px), Medium (16px), Large (24px)
- Color: Gold (#FFD700) for filled, Gray (#E0E0E0) for empty
- Optional: Numeric rating display next to stars
- Review count in parentheses
```

**Search Bar:**
```
Design a prominent search bar component.

Features:
- Rounded-full container with shadow
- Search icon (left-aligned)
- Placeholder text: "Search restaurants, cuisines, or dishes"
- Location pin icon with current location text
- Clear button (X) when text entered
- Voice search icon (optional)
- Height: 56px (touch-friendly)
- Expandable: Click to show search suggestions dropdown
```

**AI Badge/Recommendation Indicator:**
```
Design an AI recommendation badge.

Elements:
- Sparkle/star icon (animated shimmer effect suggested)
- Text: "AI Recommended" or "94% Match"
- Background: Gradient (purple to blue) or primary color
- Small size to fit on cards
- Trust-building design (professional, not gimmicky)
- Optional: Tooltip on hover explaining the recommendation
```

---

## 📊 Responsive Breakpoints

Specify responsive behavior in prompts:

```
Design should be responsive for:
- Mobile: 375px - 767px (single column, stacked layout)
- Tablet: 768px - 1023px (2 columns, adjusted spacing)
- Desktop: 1024px+ (full layout, multi-column grids)

Show mobile and desktop variants side by side in the generated image.
```

---

## 🎯 Specific Element Prompts

### Icons Needed
- Restaurant/cuisine icons (various food types)
- Location/pin icons
- Star ratings (full, half, empty)
- User profile/avatar
- Search/magnifying glass
- Filter/adjustment sliders
- Heart/bookmark (filled and outline)
- Share icon
- Phone/call icon
- Navigation/directions
- Calendar/clock for booking
- Credit card/payment
- AI/sparkle icons
- Checkmark/verification
- Filter/remove icons

### Illustrations/Graphics
- Empty state illustrations (no results found)
- Success animations (booking confirmed)
- AI/robot character (friendly, helpful)
- Food delivery illustration
- Map placeholder graphics
- Loading states/skeletons

---

## 📋 Instructions for Using These Prompts

### For Google Stitch:
1. **Copy the specific page prompt** you want to generate
2. **Add any custom modifications** specific to your brand
3. **Specify the viewport size** (mobile, tablet, or desktop)
4. **Request multiple variants** for A/B testing ideas
5. **Ask for component states** (default, hover, active, disabled)

### Best Practices:
- Generate one major page at a time for best results
- Request light and dark mode variants separately
- Ask for design system tokens (colors, typography, spacing) alongside pages
- Request component variants for different states
- Generate mobile-first, then ask for desktop adaptations

### Iteration Workflow:
1. Generate initial concept
2. Review and note adjustments needed
3. Create follow-up prompt: "Based on the previous design, make these changes: ..."
4. Generate component variations
5. Finalize with detailed specifications

---

## 🔗 Integration Notes for Next.js

When implementing generated designs:

### Material-UI Components to Use:
- `AppBar`, `Toolbar` for headers
- `Card`, `CardContent`, `CardMedia` for restaurant cards
- `Grid` or `Box` with flex/grid for layouts
- `Button`, `IconButton` for actions
- `TextField`, `Select`, `Autocomplete` for inputs
- `Chip` for tags and filters
- `Tabs`, `Tab` for navigation
- `Dialog`, `Modal` for overlays
- `Slider`, `Switch`, `Checkbox` for preferences
- `Stepper` for multi-step flows

### Next.js Specifics:
- App Router structure for page routing
- Server Components for data fetching
- Client Components for interactive elements
- Image optimization with `next/image`
- API route handlers for backend integration

### Styling Approach:
```
MUI Theme Provider with:
- Custom color palette
- Typography settings
- Component overrides
- Spacing system
- Breakpoint configurations
```

---

## 🎨 Additional Design Requests

### Dark Mode Variants
Add to any prompt:
```
Also provide a dark mode variant with:
- Dark background (#121212)
- Elevated surface colors (#1E1E1E, #2C2C2C)
- High contrast text (white/gray)
- Adjusted accent colors for dark backgrounds
- Reduced shadow usage, increased border contrast
```

### Accessibility Considerations
```
Ensure designs meet WCAG 2.1 AA standards:
- Color contrast ratio 4.5:1 minimum for text
- Focus indicators for interactive elements
- Touch target sizes minimum 44x44px
- Clear visual hierarchy
- Alternative text placeholders for images
```

### Loading States & Skeletons
```
Generate loading state designs:
- Skeleton screens for restaurant cards
- Shimmer effects for images
- Spinner variants for buttons
- Progress indicators for multi-step flows
- Infinite scroll loading states
```

---

*This prompt document provides comprehensive guidance for generating UI mockups with Google Stitch. Each prompt can be customized further based on specific requirements and brand guidelines.*

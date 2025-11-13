## MODIFIED Requirements

### Requirement: Student List View
The system SHALL provide a user interface that displays a list of all students with basic information including vocabulary mastery percentage, and SHALL allow navigation to individual student detail pages. The table SHALL be sortable by grade mastery percentage. The system SHALL use Next.js Server Components to fetch and render data, with automatic caching to improve performance.

#### Scenario: Display student list
- **WHEN** a teacher navigates to `/students`
- **THEN** the system fetches all students from the API (`GET /api/students`) using Next.js Server Component
- **AND** caches the API response for 5 minutes using Next.js fetch caching
- **AND** displays students in a table with columns:
  - Student name
  - Reading level
  - Vocabulary mastery percentage
- **AND** applies visual indicators (color coding) for proficiency levels:
  - Low mastery (<50%): Red/orange color
  - Medium mastery (50-75%): Yellow color
  - High mastery (>75%): Green color
- **AND** makes table rows clickable to navigate to `/students/[id]` via client component
- **AND** shows loading state during initial server-side rendering if needed
- **AND** shows error state if API call fails
- **AND** shows empty state if no students found

#### Scenario: Sortable table by mastery percentage
- **WHEN** a teacher clicks on the "Grade Mastery %" column header
- **THEN** the table sorts students by mastery percentage using client-side sorting
- **AND** default sort order is descending (highest percentage first)
- **AND** clicking the header toggles between ascending and descending order
- **AND** a visual indicator (arrow icon) shows the current sort direction
- **AND** the sort state is managed by a client component

### Requirement: Student Detail View
The system SHALL provide a detailed view of an individual student's vocabulary profile, book recommendations, and vocabulary issues, organized into four distinct sections. Book recommendations SHALL display cover images and SHALL be clickable to show detailed book information in a modal. The system SHALL use Next.js Server Components to fetch and render data, with automatic caching to improve performance.

#### Scenario: Display student detail page
- **WHEN** a teacher navigates to `/students/[id]` with a valid student ID
- **THEN** the system fetches student data from the API (`GET /api/students/{id}`) using Next.js Server Component
- **AND** caches the API response for 10 minutes using Next.js fetch caching
- **AND** displays four sections:
  1. Student Overview
  2. Book Recommendations
  3. Vocabulary Progress
  4. Vocabulary Issues
- **AND** shows loading state during initial server-side rendering if needed
- **AND** shows error state if API call fails
- **AND** shows 404 error page if student not found

#### Scenario: Student Overview section
- **WHEN** viewing a student detail page
- **THEN** the system displays:
  - Student name
  - Reading level
  - Assigned grade
  - Vocabulary mastery gauge/chart showing mastery percentage
  - Text showing "X of Y words mastered (Z%)"
- **AND** uses a visual progress indicator (progress bar or circular gauge)
- **AND** displays information in a card layout

#### Scenario: Book Recommendations section
- **WHEN** viewing a student detail page
- **THEN** the system displays up to 3 recommended books as cards
- **AND** each card shows:
  - Book cover image (fetched from Open Library API client-side, with fallback placeholder if unavailable)
  - Book title and author
  - Match score (displayed as percentage)
  - "Known: X% | New: Y% (Z words)" text
  - Brief explanation: "This book will challenge you with Z new vocabulary words while reinforcing words you already know."
- **AND** cards are visually appealing with proper spacing
- **AND** shows empty state if no recommendations available
- **AND** cards are clickable to open a detailed book information modal via client component

#### Scenario: Book detail modal
- **WHEN** a teacher clicks on a book recommendation card
- **THEN** the system opens a modal dialog displaying detailed book information via client component
- **AND** the modal shows:
  - Book cover image (large size)
  - Book title and author
  - Page count (from Open Library API, if available)
  - Book summary/description (from Open Library API, if available)
  - Reading level
  - Match score and vocabulary statistics
- **AND** the modal displays a loading state while fetching book details from external API
- **AND** the modal handles errors gracefully (shows error message or hides modal if API fails)
- **AND** the modal can be dismissed by:
  - Clicking outside the modal
  - Pressing the ESC key
  - Clicking a close button

#### Scenario: Vocabulary Progress section
- **WHEN** viewing a student detail page
- **THEN** the system displays grade-level vocabulary statistics:
  - "Mastered X of Y [grade] words (Z%)"
  - Progress bar visualization showing mastery percentage
- **AND** provides an expandable/collapsible section for missing words:
  - Default state: Collapsed showing count (e.g., "X missing words")
  - Expanded state: List of all missing vocabulary words
- **AND** uses card layout for organization
- **AND** shows empty state if all words are mastered

#### Scenario: Vocabulary Issues section
- **WHEN** viewing a student detail page
- **THEN** the system displays a "Words Used Incorrectly" section
- **AND** for each misused word, displays:
  - Word name (prominently displayed)
  - Correct vs. incorrect usage count (e.g., "Correct: 2 | Incorrect: 3")
  - Example sentence(s) showing misuse (1-2 examples)
  - Misused word highlighted in the example sentence
- **AND** uses card or alert component for each misused word
- **AND** shows empty state if no words are misused
- **AND** provides dismiss functionality via client component for each misused word

### Requirement: Navigation and Breadcrumbs
The system SHALL provide clear navigation between student list and detail views, and SHALL display breadcrumbs on the student detail page.

#### Scenario: Navigate from list to detail
- **WHEN** a teacher clicks on a student row in the student list
- **THEN** the system navigates to `/students/[id]` where `[id]` is the student's ID via client component
- **AND** the student detail page loads and displays the selected student's data

#### Scenario: Display breadcrumbs on detail page
- **WHEN** viewing a student detail page
- **THEN** the system displays breadcrumb navigation showing:
  - Home (clickable, links to `/`)
  - Students (clickable, links to `/students`)
  - [Student Name] (current page, not clickable)
- **AND** breadcrumb items are clickable to navigate to previous pages

### Requirement: Loading and Error States
The system SHALL display appropriate loading states while fetching data and SHALL handle errors gracefully with user-friendly messages.

#### Scenario: Show loading state
- **WHEN** fetching student data from the API during server-side rendering
- **THEN** the system may display loading indicators during initial render
- **AND** subsequent page loads benefit from Next.js fetch cache (faster rendering)
- **AND** client-side interactions (modals, sorting) show appropriate loading states

#### Scenario: Handle API errors
- **WHEN** an API call fails (network error, server error, etc.)
- **THEN** the system displays a user-friendly error message
- **AND** provides a retry button to attempt the API call again via client component
- **AND** uses appropriate error styling (e.g., alert component)

#### Scenario: Handle 404 errors
- **WHEN** a teacher navigates to `/students/[id]` with a non-existent student ID
- **THEN** the system displays a 404 error page
- **AND** shows message indicating student not found
- **AND** provides a link to return to the student list

#### Scenario: Handle external API errors
- **WHEN** fetching book details from Open Library API fails
- **THEN** the system displays an error message in the modal or hides the modal gracefully
- **AND** does not break the main application flow
- **WHEN** fetching word details from DictionaryAPI.dev fails
- **THEN** the system displays an error message in the modal or hides the modal gracefully
- **AND** does not break the main application flow

### Requirement: Responsive Design
The system SHALL ensure student list and detail pages are responsive and work properly on tablet and desktop screen sizes.

#### Scenario: Responsive student list
- **WHEN** viewing the student list on different screen sizes
- **THEN** the table is scrollable on mobile devices
- **AND** table columns are properly sized on tablet (768px) and desktop (1024px+)
- **AND** visual indicators (color coding) remain visible at all sizes
- **AND** sort functionality works on all screen sizes

#### Scenario: Responsive student detail
- **WHEN** viewing a student detail page on different screen sizes
- **THEN** cards stack vertically on smaller screens
- **AND** cards display side-by-side on larger screens
- **AND** progress bars and charts scale appropriately
- **AND** expandable sections work on all screen sizes
- **AND** modals are properly sized and centered on all screen sizes

#### Scenario: Responsive class overview
- **WHEN** viewing the class overview page on different screen sizes
- **THEN** vocabulary gaps and common mistakes tables display side-by-side on desktop
- **AND** tables stack vertically on mobile devices
- **AND** book recommendation cards are responsive
- **AND** modals are properly sized and centered on all screen sizes

### Requirement: Class Overview Page
The system SHALL provide a class-wide overview showing statistics, book recommendations, vocabulary gaps, and common mistakes. Book recommendations SHALL display cover images and SHALL be clickable to show detailed book information in a modal. Vocabulary words in tables SHALL be clickable to show dictionary information. The system SHALL use Next.js Server Components to fetch and render data, with automatic caching to improve performance.

#### Scenario: Display class overview
- **WHEN** a teacher navigates to `/class`
- **THEN** the system fetches class statistics from the API (`GET /api/class/stats`) using Next.js Server Component
- **AND** caches the API response for 5 minutes using Next.js fetch caching
- **AND** fetches class recommendations from the API (`GET /api/class/recommendations`) using Next.js Server Component
- **AND** caches the API response for 15 minutes using Next.js fetch caching
- **AND** displays four sections:
  1. Class Statistics
  2. Class-Wide Book Recommendations
  3. Vocabulary Gaps
  4. Common Mistakes
- **AND** shows loading states during initial server-side rendering if needed
- **AND** shows error states if API calls fail
- **AND** shows empty states if no data available

#### Scenario: Class-wide book recommendations
- **WHEN** viewing the class overview page
- **THEN** the system displays up to 2 recommended books as prominent cards
- **AND** each card shows:
  - Book cover image (fetched from Open Library API client-side, with fallback placeholder if unavailable)
  - Book title and author
  - "Recommended for X of Y students" text
  - Average match score (as percentage with progress bar)
  - Brief explanation of why the book is good for the class
- **AND** cards are visually appealing with hover effects
- **AND** cards are clickable to open a detailed book information modal via client component
- **AND** shows empty state if no recommendations available

#### Scenario: Vocabulary gaps table
- **WHEN** viewing the class overview page
- **THEN** the system displays a "Top 10 Words Students Need to Learn" section
- **AND** displays words in a table with columns:
  - Word
  - Total Students (number of students missing the word)
- **AND** words are sorted by number of students missing (descending)
- **AND** table rows are clickable to open a word detail modal via client component
- **AND** uses a unified `VocabularyTableCard` component for consistent styling
- **AND** shows empty state if no vocabulary gaps detected

#### Scenario: Common mistakes table
- **WHEN** viewing the class overview page
- **THEN** the system displays a "Words Frequently Used Incorrectly" section
- **AND** displays words in a table with columns:
  - Word
  - Total Misuses
  - Students Affected (if available)
- **AND** words are sorted by misuse count (descending)
- **AND** table rows are clickable to open a word detail modal via client component
- **AND** uses a unified `VocabularyTableCard` component for consistent styling (same as vocabulary gaps)
- **AND** shows empty state if no common mistakes found

#### Scenario: Word detail modal
- **WHEN** a teacher clicks on a word row in the vocabulary gaps or common mistakes table
- **THEN** the system opens a modal dialog displaying dictionary information for the word via client component
- **AND** the modal shows:
  - Word definition (from DictionaryAPI.dev)
  - Usage examples
  - Word origin/etymology (if available)
- **AND** the modal displays a loading state while fetching word details from external API
- **AND** the modal handles errors gracefully (shows error message or hides modal if API fails)
- **AND** the modal can be dismissed by:
  - Clicking outside the modal
  - Pressing the ESC key
  - Clicking a close button

### Requirement: Class Statistics Section
The system SHALL display class-wide statistics including total students, average vocabulary mastery, and reading level distribution with visual representation.

#### Scenario: Display class statistics
- **WHEN** viewing the class overview page
- **THEN** the system displays:
  - Total number of students in the class (e.g., "25 students")
  - Average vocabulary mastery percentage across all students (e.g., "64.2%")
  - Visual indicator for average mastery (progress bar or gauge)
- **AND** uses card layout for organization

#### Scenario: Display reading level distribution
- **WHEN** viewing the class overview page
- **THEN** the system displays a bar chart showing reading level distribution:
  - X-axis: Grade levels (5, 6, 7, 8)
  - Y-axis: Number of students at each level
  - Color-coded bars for visual clarity
- **AND** chart is responsive and scales appropriately on different screen sizes
- **AND** chart shows data labels or tooltips on hover

### Requirement: Class-Wide Book Recommendations Section
The system SHALL display the top 2 class-wide book recommendations as prominent cards showing why each book is suitable for most students in the class.

#### Scenario: Display class book recommendations
- **WHEN** viewing the class overview page
- **THEN** the system displays up to 2 class-wide book recommendations as prominent cards
- **AND** each card shows:
  - Book title and author
  - Text indicating reach: "Recommended for X of Y students"
  - Average match score across students (as percentage or visual indicator)
  - Brief explanation: "This book is recommended for most students in your class, offering appropriate vocabulary challenge for X students."
  - Placeholder image or book icon
- **AND** cards are styled prominently (larger/more prominent than individual recommendations)
- **AND** cards are visually appealing with proper spacing
- **AND** shows empty state if no class recommendations available

### Requirement: Vocabulary Gaps Section
The system SHALL display the top 10 vocabulary words that most students are missing, showing which words the class needs to focus on.

#### Scenario: Display top missing words
- **WHEN** viewing the class overview page
- **THEN** the system displays a "Top 10 Words Students Need to Learn" section
- **AND** shows a table or list with:
  - Word column (vocabulary word)
  - Students Missing column (count of students who haven't mastered this word)
  - Optional: Grade Level column (which grade level the word belongs to)
- **AND** list is sorted by students missing count in descending order (most missing first)
- **AND** uses table or card layout for clear presentation
- **AND** shows empty state if no missing words (unlikely but possible)

#### Scenario: Sortable vocabulary gaps table
- **WHEN** viewing the vocabulary gaps table
- **THEN** the system allows sorting by students missing count
- **AND** displays visual indicator for sort direction
- **AND** table remains responsive on different screen sizes

### Requirement: Common Mistakes Section
The system SHALL display words that are frequently used incorrectly across the class, with emphasis on commonly misused words to help teachers address systematic vocabulary issues.

#### Scenario: Display commonly misused words
- **WHEN** viewing the class overview page
- **THEN** the system displays a "Words Frequently Used Incorrectly" section
- **AND** shows a table or list with:
  - Word column (prominently displayed)
  - Total Misuses column (count of incorrect usages across all students)
  - Students Affected column (count of students who misused the word)
- **AND** list is sorted by misuse count in descending order
- **AND** uses alert or warning styling to emphasize these are issues needing attention
- **AND** shows empty state if no words are misused (unlikely but possible)

#### Scenario: Highlight specific misused words
- **WHEN** viewing the commonly misused words section
- **AND** the word "through" (or other commonly misused words) appears in the list
- **THEN** the system displays it prominently (e.g., top of list, highlighted styling)
- **AND** optionally shows an expandable example sentence demonstrating the misuse

### Requirement: Class View Navigation
The system SHALL provide clear navigation to and from the class overview page, integrating it with the main navigation system.

#### Scenario: Navigate to class overview
- **WHEN** a teacher is on any page in the application
- **THEN** the system displays a "Class Overview" link in the main navigation
- **AND** clicking the link navigates to `/class`
- **AND** the current page is highlighted in the navigation

#### Scenario: Navigate between class and student views
- **WHEN** viewing the class overview page
- **THEN** the system provides a link to the students list page
- **AND** clicking navigates to `/students`
- **AND** navigation is bidirectional (can navigate back to class overview from students page)

### Requirement: Data Visualization
The system SHALL use appropriate chart components to visualize class-wide data, making patterns and insights easy to understand at a glance.

#### Scenario: Render reading level distribution chart
- **WHEN** viewing the class statistics section
- **THEN** the system uses a bar chart (via recharts library) to display reading level distribution
- **AND** chart is interactive (shows tooltips on hover)
- **AND** chart uses appropriate colors for visual clarity
- **AND** chart scales responsively on different screen sizes

#### Scenario: Display vocabulary mastery distribution (optional enhancement)
- **WHEN** viewing the class statistics section
- **THEN** the system optionally displays a histogram or distribution chart of vocabulary mastery percentages
- **AND** chart shows how many students fall into mastery ranges (e.g., 0-25%, 25-50%, 50-75%, 75-100%)
- **AND** uses color coding to indicate proficiency levels

### Requirement: Class View Loading and Error States
The system SHALL display appropriate loading states while fetching class data and SHALL handle errors gracefully with user-friendly messages and recovery options.

#### Scenario: Show loading state
- **WHEN** fetching class statistics or recommendations from the API during server-side rendering
- **THEN** the system may display loading indicators during initial render
- **AND** subsequent page loads benefit from Next.js fetch cache (faster rendering)
- **AND** client-side interactions (modals, retry buttons) show appropriate loading states

#### Scenario: Handle API errors
- **WHEN** an API call fails (network error, server error, etc.)
- **THEN** the system displays a user-friendly error message
- **AND** provides a retry button to attempt the API call again via client component
- **AND** uses appropriate error styling (e.g., alert component)
- **AND** allows partial page rendering if only one API call fails (e.g., stats load but recommendations fail)

#### Scenario: Handle empty data states
- **WHEN** class statistics show zero students or no data
- **THEN** the system displays helpful empty state messages:
  - "No students found in the class"
  - "No book recommendations available yet"
  - "No vocabulary gaps detected"
  - "No common mistakes found"
- **AND** provides guidance on next steps if applicable

### Requirement: Responsive Class View Design
The system SHALL ensure the class overview page is responsive and works properly on tablet and desktop screen sizes, with appropriate layout adjustments.

#### Scenario: Responsive class overview layout
- **WHEN** viewing the class overview page on different screen sizes
- **THEN** sections stack appropriately:
  - Mobile/tablet: Vertical stacking of all sections
  - Desktop: 2-column grid layout for statistics and recommendations
  - Desktop: Full-width layout for tables (vocabulary gaps, common mistakes)
- **AND** charts scale appropriately and remain readable
- **AND** cards maintain proper proportions and spacing

#### Scenario: Responsive data tables
- **WHEN** viewing vocabulary gaps or common mistakes tables on smaller screens
- **THEN** tables are scrollable horizontally if needed
- **AND** table columns collapse or reflow appropriately
- **AND** tables remain readable and accessible on all screen sizes

### Requirement: Class View Helpful Context
The system SHALL provide tooltips, explanations, and contextual help to make class-wide metrics and recommendations understandable for teachers.

#### Scenario: Display explanatory tooltips
- **WHEN** viewing class overview page metrics
- **THEN** the system provides tooltips or help icons for complex metrics:
  - "Average Match Score": Explains how match score is calculated
  - "Vocabulary Mastery": Explains what mastery means (correct usage in context)
  - "Reading Level": Explains Flesch-Kincaid grade level scale
- **AND** tooltips appear on hover (desktop) or tap (mobile)
- **AND** tooltips use clear, teacher-friendly language

#### Scenario: Provide actionable explanations
- **WHEN** viewing book recommendations or vocabulary gaps
- **THEN** the system provides brief explanations of why this data matters:
  - Book recommendations: "These books work well for most students in your class"
  - Vocabulary gaps: "Focus instruction on these words to help the most students"
  - Common mistakes: "Review these words with the class to address systematic misunderstandings"
- **AND** explanations are concise and action-oriented

## ADDED Requirements

### Requirement: Next.js Server Components and Fetch Caching
The system SHALL use Next.js Server Components to fetch and render data server-side, and SHALL cache API responses using Next.js fetch caching to improve performance.

#### Scenario: Server-side rendering with caching
- **WHEN** a teacher navigates to any page in the application
- **THEN** the system renders the page on the server using Next.js Server Components
- **AND** fetches data from the API using native `fetch()` with `next.revalidate` option
- **AND** caches API responses according to configured revalidation times:
  - Student list: 5 minutes
  - Student detail: 10 minutes
  - Class statistics: 5 minutes
  - Class recommendations: 15 minutes
- **AND** subsequent page loads within the cache period use cached data (faster rendering)
- **AND** cache automatically revalidates after the configured time period

#### Scenario: Client components for interactivity
- **WHEN** a page requires interactive features (sorting, modals, buttons)
- **THEN** the system uses small client components for only the interactive parts
- **AND** most of the page remains as Server Component (better performance)
- **AND** client components receive data as props from Server Components
- **AND** interactive features work correctly with server-rendered data


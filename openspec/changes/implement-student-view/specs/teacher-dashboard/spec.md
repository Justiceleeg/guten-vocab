## ADDED Requirements

### Requirement: Student List View
The system SHALL provide a user interface that displays a list of all students with basic information including vocabulary mastery percentage, and SHALL allow navigation to individual student detail pages.

#### Scenario: Display student list
- **WHEN** a teacher navigates to `/students`
- **THEN** the system fetches all students from the API (`GET /api/students`)
- **AND** displays students in a table with columns:
  - Student name
  - Reading level
  - Vocabulary mastery percentage
- **AND** applies visual indicators (color coding) for proficiency levels:
  - Low mastery (<50%): Red/orange color
  - Medium mastery (50-75%): Yellow color
  - High mastery (>75%): Green color
- **AND** makes table rows clickable to navigate to `/students/[id]`
- **AND** shows loading state while fetching data
- **AND** shows error state if API call fails
- **AND** shows empty state if no students found

### Requirement: Student Detail View
The system SHALL provide a detailed view of an individual student's vocabulary profile, book recommendations, and vocabulary issues, organized into four distinct sections.

#### Scenario: Display student detail page
- **WHEN** a teacher navigates to `/students/[id]` with a valid student ID
- **THEN** the system fetches student data from the API (`GET /api/students/{id}`)
- **AND** displays four sections:
  1. Student Overview
  2. Book Recommendations
  3. Vocabulary Progress
  4. Vocabulary Issues
- **AND** shows loading state while fetching data
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
  - Book title and author
  - Placeholder image or book icon
  - Match score (displayed as percentage or star rating)
  - "Known: X% | New: Y% (Z words)" text
  - Brief explanation: "This book will challenge you with Z new vocabulary words while reinforcing words you already know."
- **AND** cards are visually appealing with proper spacing
- **AND** shows empty state if no recommendations available

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

### Requirement: Navigation and Breadcrumbs
The system SHALL provide clear navigation between student list and detail views, and SHALL display breadcrumbs on the student detail page.

#### Scenario: Navigate from list to detail
- **WHEN** a teacher clicks on a student row in the student list
- **THEN** the system navigates to `/students/[id]` where `[id]` is the student's ID
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
- **WHEN** fetching student data from the API
- **THEN** the system displays loading indicators:
  - Skeleton loaders for table rows (on list page)
  - Skeleton loaders for detail sections (on detail page)
- **AND** loading indicators match the structure of the content being loaded

#### Scenario: Handle API errors
- **WHEN** an API call fails (network error, server error, etc.)
- **THEN** the system displays a user-friendly error message
- **AND** provides a retry button to attempt the API call again
- **AND** uses appropriate error styling (e.g., alert component)

#### Scenario: Handle 404 errors
- **WHEN** a teacher navigates to `/students/[id]` with a non-existent student ID
- **THEN** the system displays a 404 error page
- **AND** shows message indicating student not found
- **AND** provides a link to return to the student list

### Requirement: Responsive Design
The system SHALL ensure student list and detail pages are responsive and work properly on tablet and desktop screen sizes.

#### Scenario: Responsive student list
- **WHEN** viewing the student list on different screen sizes
- **THEN** the table is scrollable on mobile devices
- **AND** table columns are properly sized on tablet (768px) and desktop (1024px+)
- **AND** visual indicators (color coding) remain visible at all sizes

#### Scenario: Responsive student detail
- **WHEN** viewing a student detail page on different screen sizes
- **THEN** cards stack vertically on smaller screens
- **AND** cards display side-by-side on larger screens
- **AND** progress bars and charts scale appropriately
- **AND** expandable sections work on all screen sizes


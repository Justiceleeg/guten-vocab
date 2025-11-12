## ADDED Requirements

### Requirement: Class Overview Page
The system SHALL provide a class overview page that displays class-wide statistics, book recommendations, vocabulary gaps, and common mistakes, organized into four distinct sections.

#### Scenario: Display class overview page
- **WHEN** a teacher navigates to `/class`
- **THEN** the system fetches class statistics from the API (`GET /api/class/stats`)
- **AND** fetches class recommendations from the API (`GET /api/class/recommendations`)
- **AND** displays four sections:
  1. Class Statistics
  2. Class-Wide Book Recommendations
  3. Vocabulary Gaps
  4. Common Mistakes
- **AND** shows loading state while fetching data
- **AND** shows error state if API calls fail
- **AND** shows empty states for sections with no data

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
- **WHEN** fetching class statistics or recommendations from the API
- **THEN** the system displays loading indicators:
  - Skeleton loaders for statistics cards
  - Skeleton loaders for book recommendation cards
  - Loading spinner for charts
- **AND** loading indicators match the structure of the content being loaded

#### Scenario: Handle API errors
- **WHEN** an API call fails (network error, server error, etc.)
- **THEN** the system displays a user-friendly error message
- **AND** provides a retry button to attempt the API call again
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


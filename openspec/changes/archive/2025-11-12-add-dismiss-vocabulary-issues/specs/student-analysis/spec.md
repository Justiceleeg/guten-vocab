## ADDED Requirements

### Requirement: Teacher Dismissal of Vocabulary Issues
Teachers SHALL be able to dismiss vocabulary misuse reports by indicating the reason for dismissal. The system SHALL track dismissal status, reason, and timestamp for audit purposes.

#### Scenario: Dismiss vocabulary issue as addressed
- **WHEN** a teacher reviews a misused word report
- **AND** marks it as "addressed" (corrected with student)
- **THEN** the system records the dismissal with reason "addressed"
- **AND** stores the dismissal timestamp
- **AND** removes the word from future misused word displays for that student

#### Scenario: Dismiss vocabulary issue as AI error
- **WHEN** a teacher reviews a misused word report
- **AND** marks it as "ai_error" (false positive detection)
- **THEN** the system records the dismissal with reason "ai_error"
- **AND** stores the dismissal timestamp
- **AND** removes the word from future misused word displays for that student
- **AND** provides data for improving AI detection accuracy

#### Scenario: Filter dismissed words from API responses
- **WHEN** requesting misused words for a student
- **THEN** the system returns only non-dismissed vocabulary issues
- **AND** dismissed words are excluded by default
- **AND** optionally includes dismissed words if requested (for teacher review)

#### Scenario: Invalid dismissal reason
- **WHEN** attempting to dismiss with an invalid reason
- **THEN** the system returns error 400 (Bad Request)
- **AND** provides message: "Invalid dismiss reason. Must be 'addressed' or 'ai_error'"

#### Scenario: Dismiss non-existent vocabulary issue
- **WHEN** attempting to dismiss a word that doesn't exist for the student
- **THEN** the system returns error 404 (Not Found)
- **AND** provides message: "Vocabulary issue not found"
